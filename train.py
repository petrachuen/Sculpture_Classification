"""
Fine-tune ImageNet-pretrained ResNet50 on a CSV-labeled image dataset.

Example:
  python train.py --csv data/labels.csv --img_dir data/images \
      --filename_col filename --label_col label [--group_col object_id]

Outputs (in --out_dir): splits.csv, history.csv, best.pt, metrics.json,
classification_report.txt, confusion_matrix.png, misclassified.csv
"""
import argparse, json, os, random
import numpy as np
import pandas as pd
import torch, torch.nn as nn
from PIL import Image
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from torchvision import models, transforms as T
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.metrics import (accuracy_score, f1_score, classification_report,
                             confusion_matrix)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

p = argparse.ArgumentParser()
p.add_argument("--csv", required=True)
p.add_argument("--img_dir", required=True)
p.add_argument("--filename_col", default="filename")
p.add_argument("--label_col", default="label")
p.add_argument("--group_col", default=None, help="object ID, to keep all views of an object in one split")
p.add_argument("--out_dir", default="outputs")
p.add_argument("--seed", type=int, default=42)
p.add_argument("--img_size", type=int, default=224)
p.add_argument("--batch_size", type=int, default=32)
p.add_argument("--epochs_head", type=int, default=5)
p.add_argument("--epochs_ft", type=int, default=20)
p.add_argument("--lr_head", type=float, default=1e-3)
p.add_argument("--lr_backbone", type=float, default=1e-4)
p.add_argument("--weight_decay", type=float, default=1e-2)
p.add_argument("--label_smoothing", type=float, default=0.1)
p.add_argument("--patience", type=int, default=6)
p.add_argument("--class_weights", action="store_true", help="use inverse-frequency class weights in the loss")
p.add_argument("--num_workers", type=int, default=2)
args = p.parse_args()

os.makedirs(args.out_dir, exist_ok=True)
random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)
torch.cuda.manual_seed_all(args.seed)
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

# ---------------------------------------------------------------- data
df = pd.read_csv(args.csv)
df = df[[c for c in [args.filename_col, args.label_col, args.group_col] if c]].copy()
df = df.dropna()
df = df[df[args.filename_col].apply(lambda f: os.path.exists(os.path.join(args.img_dir, str(f))))]
classes = sorted(df[args.label_col].unique())
cls2idx = {c: i for i, c in enumerate(classes)}
df["y"] = df[args.label_col].map(cls2idx)
print(f"{len(df)} images, {len(classes)} classes")
print(df[args.label_col].value_counts().to_string())

"""# 70/15/15 stratified split (group-aware if group_col is given)
if args.group_col:
    groups = df[args.group_col].values
    sgkf = StratifiedGroupKFold(n_splits=7, shuffle=True, random_state=args.seed)
    rest_idx, test_idx = next(sgkf.split(df, df["y"], groups))
    rest = df.iloc[rest_idx]
    sgkf2 = StratifiedGroupKFold(n_splits=6, shuffle=True, random_state=args.seed)
    tr_i, va_i = next(sgkf2.split(rest, rest["y"], rest[args.group_col].values))
    train_df, val_df, test_df = rest.iloc[tr_i], rest.iloc[va_i], df.iloc[test_idx]
else:
    rest, test_df = train_test_split(df, test_size=0.15, stratify=df["y"], random_state=args.seed)
    train_df, val_df = train_test_split(rest, test_size=0.15 / 0.85, stratify=rest["y"], random_state=args.seed)

pd.concat([train_df.assign(split="train"), val_df.assign(split="val"),
           test_df.assign(split="test")]).to_csv(f"{args.out_dir}/splits.csv", index=False)
print(f"train={len(train_df)} val={len(val_df)} test={len(test_df)}")

mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
S = args.img_size
train_tf = T.Compose([
    T.RandomResizedCrop(S, scale=(0.6, 1.0)),
    T.RandomHorizontalFlip(),
    T.RandomRotation(10),
    T.ColorJitter(0.2, 0.2, 0.2),
    T.ToTensor(), T.Normalize(mean, std)])
eval_tf = T.Compose([T.Resize(int(S * 256 / 224)), T.CenterCrop(S),
                     T.ToTensor(), T.Normalize(mean, std)])


class ImgDS(Dataset):
    def __init__(self, d, tf):
        self.files = d[args.filename_col].astype(str).tolist()
        self.y = d["y"].tolist()
        self.tf = tf
    def __len__(self): return len(self.files)
    def __getitem__(self, i):
        img = Image.open(os.path.join(args.img_dir, self.files[i])).convert("RGB")
        return self.tf(img), self.y[i]


def loader(d, tf, shuffle):
    return DataLoader(ImgDS(d, tf), batch_size=args.batch_size, shuffle=shuffle,
                      num_workers=args.num_workers, pin_memory=(device == "cuda"))

train_dl, val_dl, test_dl = loader(train_df, train_tf, True), loader(val_df, eval_tf, False), loader(test_df, eval_tf, False)

# ---------------------------------------------------------------- model
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
model.fc = nn.Sequential(nn.Dropout(0.3), nn.Linear(model.fc.in_features, len(classes)))
model = model.to(device)

weight = None
if args.class_weights:
    counts = np.bincount(train_df["y"], minlength=len(classes)).astype(float)
    weight = torch.tensor(counts.sum() / (len(classes) * np.maximum(counts, 1)), dtype=torch.float32).to(device)
criterion = nn.CrossEntropyLoss(weight=weight, label_smoothing=args.label_smoothing)
scaler = torch.amp.GradScaler("cuda", enabled=(device == "cuda"))


def run_epoch(dl, opt=None, sched=None):
    train = opt is not None
    model.train(train)
    losses, preds, ys = [], [], []
    with torch.set_grad_enabled(train):
        for x, y in dl:
            x, y = x.to(device), y.to(device)
            with torch.autocast(device_type=device, enabled=(device == "cuda")):
                out = model(x); loss = criterion(out, y)
            if train:
                opt.zero_grad(set_to_none=True)
                scaler.scale(loss).backward()
                scaler.step(opt); scaler.update()
                if sched: sched.step()
            losses.append(loss.item() * len(y))
            preds += out.argmax(1).cpu().tolist(); ys += y.cpu().tolist()
    n = len(ys)
    return sum(losses) / n, accuracy_score(ys, preds), f1_score(ys, preds, average="macro"), ys, preds


history, best_f1, bad = [], -1, 0


def fit(n_epochs, opt, sched, stage):
    global best_f1, bad
    for ep in range(n_epochs):
        tl, ta, tf1, _, _ = run_epoch(train_dl, opt, sched)
        vl, va, vf1, _, _ = run_epoch(val_dl)
        history.append(dict(stage=stage, epoch=len(history) + 1, train_loss=tl, train_acc=ta,
                            val_loss=vl, val_acc=va, val_macro_f1=vf1))
        print(f"[{stage}] ep{len(history):02d} train_loss={tl:.3f} acc={ta:.3f} | "
              f"val_loss={vl:.3f} acc={va:.3f} macroF1={vf1:.3f}")
        if vf1 > best_f1:
            best_f1, bad = vf1, 0
            torch.save({"model": model.state_dict(), "classes": classes}, f"{args.out_dir}/best.pt")
        else:
            bad += 1
            if stage == "finetune" and bad >= args.patience:
                print("Early stopping."); return


# Stage A: linear probe (backbone frozen)
for n, prm in model.named_parameters():
    prm.requires_grad = n.startswith("fc.")
opt = torch.optim.AdamW(model.fc.parameters(), lr=args.lr_head, weight_decay=args.weight_decay)
fit(args.epochs_head, opt, None, "head")

# Stage B: full fine-tune, lower LR for backbone, cosine schedule with warmup
for prm in model.parameters():
    prm.requires_grad = True
backbone_params = [prm for n, prm in model.named_parameters() if not n.startswith("fc.")]
opt = torch.optim.AdamW([
    {"params": backbone_params, "lr": args.lr_backbone},
    {"params": model.fc.parameters(), "lr": args.lr_head * 0.3}], weight_decay=args.weight_decay)
total = args.epochs_ft * len(train_dl)
warm = len(train_dl)  # 1 epoch warmup
sched = torch.optim.lr_scheduler.SequentialLR(opt, [
    torch.optim.lr_scheduler.LinearLR(opt, start_factor=0.1, total_iters=warm),
    torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(total - warm, 1))], milestones=[warm])
bad = 0
fit(args.epochs_ft, opt, sched, "finetune")
pd.DataFrame(history).to_csv(f"{args.out_dir}/history.csv", index=False)

# ---------------------------------------------------------------- test (once)
model.load_state_dict(torch.load(f"{args.out_dir}/best.pt", map_location=device)["model"])
tl, ta, tf1, ys, preds = run_epoch(test_dl)
metrics = dict(test_loss=tl, test_accuracy=ta, test_macro_f1=tf1, best_val_macro_f1=best_f1,
               n_train=len(train_df), n_val=len(val_df), n_test=len(test_df), seed=args.seed,
               hyperparameters=vars(args))
json.dump(metrics, open(f"{args.out_dir}/metrics.json", "w"), indent=2)
print(f"\nTEST accuracy={ta:.3f} macroF1={tf1:.3f}")

labels = list(range(len(classes)))
rep = classification_report(ys, preds, labels=labels, target_names=[str(c) for c in classes], zero_division=0)
open(f"{args.out_dir}/classification_report.txt", "w").write(rep); print(rep)

cm = confusion_matrix(ys, preds, labels=labels)
fig, ax = plt.subplots(figsize=(max(6, len(classes) * 0.6), max(5, len(classes) * 0.5)))
ax.imshow(cm, cmap="Blues"); ax.set_xticks(labels); ax.set_yticks(labels)
ax.set_xticklabels(classes, rotation=90); ax.set_yticklabels(classes)
for i in labels:
    for j in labels:
        ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=7)
ax.set_xlabel("Predicted"); ax.set_ylabel("True"); plt.tight_layout()
plt.savefig(f"{args.out_dir}/confusion_matrix.png", dpi=150)

h = pd.DataFrame(history)
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs[0].plot(h.train_loss, label="train"); axs[0].plot(h.val_loss, label="val"); axs[0].set_title("Loss"); axs[0].legend()
axs[1].plot(h.train_acc, label="train"); axs[1].plot(h.val_acc, label="val"); axs[1].set_title("Accuracy"); axs[1].legend()
plt.tight_layout(); plt.savefig(f"{args.out_dir}/training_curves.png", dpi=150)

wrong = test_df.assign(pred=[classes[i] for i in preds])
wrong = wrong[wrong["y"].values != np.array(preds)]
wrong.to_csv(f"{args.out_dir}/misclassified.csv", index=False)
print(f"Saved outputs to {args.out_dir}/")
"""