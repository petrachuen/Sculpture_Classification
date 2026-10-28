import os
import mimetypes
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm  # pip install tqdm

# ---------------------------------------------------------------
df = pd.read_csv("sculpturesData.csv")

# ---------------------------------------------------------------
# 2. Settings
# ---------------------------------------------------------------
URL_COLUMN = "Image"
SAVE_DIR = os.path.join(os.getcwd(), "images")  # "images" folder in the current directory
MAX_WORKERS = 8
TIMEOUT = 15

os.makedirs(SAVE_DIR, exist_ok=True)

# Session with automatic retries and a browser-like User-Agent
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries, pool_maxsize=MAX_WORKERS))
session.mount("https://", HTTPAdapter(max_retries=retries, pool_maxsize=MAX_WORKERS))
session.headers.update({"User-Agent": "Mozilla/5.0"})


def get_extension(url, content_type):
    """Pick a file extension from the URL, falling back to the Content-Type header."""
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext in {".png", ".jpeg"}:
        return ext
    guessed = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
    return guessed or ".jpg"


def download_image(idx, url):
    """Download one image. Returns (index, saved_path or None, error or None)."""
    if not isinstance(url, str) or not url.strip():
        return idx, None, "empty URL"

    url = url.strip()
    try:
        # Skip if already downloaded (lets you re-run safely)
        for existing in os.listdir(SAVE_DIR):
            if existing.startswith(f"{idx}."):
                return idx, os.path.join(SAVE_DIR, existing), None

        r = session.get(url, timeout=TIMEOUT, stream=True)
        r.raise_for_status()

        ext = get_extension(url, r.headers.get("Content-Type"))
        path = os.path.join(SAVE_DIR, f"{idx}{ext}")
        print(path)

        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return idx, path, None

    except Exception as e:
        return idx, None, str(e)


# ---------------------------------------------------------------
# 3. Download in parallel
# ---------------------------------------------------------------
paths = {}
errors = {}

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = []
    for i in range(len(df)):
        futures.append(executor.submit(download_image, df.iat[i, 0], df.iat[i, 4]))
        #print(df.iat[i, 0], df.iat[i, 1]) 

    #futures = [executor.submit(download_image, idx, url) for idx, url in df[URL_COLUMN].items()]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
        idx, path, err = future.result()
        if err:
            errors[idx] = err
        else:
            paths[idx] = path

# Save the local file path back into the dataframe
df["local_path"] = df.index.map(paths.get)

print(f"\nDone. Saved: {len(paths)} | Failed: {len(errors)}")
if errors:
    failed = df.loc[list(errors.keys()), [URL_COLUMN]].copy()
    failed["error"] = failed.index.map(errors.get)
    failed.to_csv("failed_downloads.csv")
    print("Failed URLs written to failed_downloads.csv")