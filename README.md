# DSAN 6000 Project: Sculpture Classification
### Fine-tuning a model to classified Buddhism sculpture by its origin
#### Author: Petra Chuenarrom

## About the Project

(why this project and stuff)

### Defining Success

#### Task of the project

A multi-class image classification. The model will fine-tuning a pre-trained model on a dataset so it could take a photo of a Buddhist sculpture and predict origin by the art styles. 

**The success criteria are as follow**
- 75% success rate in classified the test set into the correct group.
  - This target might get adjusted after baseline test to be more realistic if needed. However, we aimed for the success rate to be more than 50%
- 50% success rate for each classification group individually.
  - There are some rare classes of Buddhism sculpture, such as sculpture from older civilization where we have less amount of artifacts. These classification of image into this class can be extremely misclassified but still not contribute a lot to the overall unsuccessful rate of entire dataset. So, we also set success expectation onto individual groups.
- There are patterns in errors
  - For classification that are unsuccessful, we should be able to see why. The reason should be in recognizable pattern that could furthermore fine-tuning the model in the future if more data is available, or be explainable with more knowledge about the artifacts. 

### Scope of the Project

- Data used for training and testing will only be from the online collection of museums and research centers. The classification will only covered Buddhism in South Asia, East Asia, and Southeast Asia due to the inadequate amount of data from other regions. 

## Dataset

### Dataset sources

### Access Dataset

## Data Audit

### Summary of Data

### Class balance / key distributions as relevant

### Bias/ Failure modes





## Evaluation plan

- Metrics appropriate to the task
- Train/validation/test (or CV) plan

## Initial direction

- What neural approach you expect to try at Check-in 2
- Any early non-neural probe is welcome but not required yet
