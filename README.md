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
- The project aimed to only classified by the region with no regards to the period. Sculptures from two historic civilizations will be classified as the same class if the present-day region is the same place.

## Dataset

### Dataset sources

The following are list of collection we have gathered images of sculptures. 
- Online collection
  - Tsz shan monastery buddhist art museum, Hong Kong
  - The Metropolitan Museum of Art, New York
  - Staatliche Museen zu Berlin, Germany
  - Norton Simon Museum, Pasadena, California
  - Rietberg Museum, Zurich, Switzerland
  - Tibet Museum, Gruyères, Switzerland
  - Barakat Gallery, London
  - Asian Art Museum, San Francisco
  - National Museum of Asian Arts, Washington, D.C.
  - Nara National Museum, Nara, Japan
 
- Online Database
  - Online database ColBase by National Institutes for Cultural Heritage, Japan

### Access Dataset

### Notes on Artifacts Origin

It is noteworthy that though all collection are open-source, some of the artifacts are in the museums or private collections which had controversy over the legitimacy of artifact's origin. Some artifacts maybe under the request for repatriation to its home country due to the history of them being looted or illegally sold. Some museums and collections have refused repatriation or have histories of refusing repatriation. By using the data from their online collection, we do not support the refusal of repatriation for artifacts with illegitimate origin by any means. 

## Data Audit

### Summary of Data

### Class balance / key distributions as relevant

### Bias/ Failure modes

#### Bias

- Majority of dataset are artifacts in collection of museums in the United States or Europe which may favor a certain style more. For example, there will be more gold, decorated, undamaged sculptures than plain wooden ones. We can seek more balance in styles via sourcing from collection in Asia but there are also difference in image quality which can cause another bias as well.
- As we have noted in the previous section, some of the artifacts have ambiguity on its origin. As many of them have been sold through several hands, some are illegally, there existed cases where the museum or collection can not be certain of the origin

#### Failure Modes

- The model can classified not based on the art styles but on the materials, which is not the main goal for this project
  - Example: During the 13th Century, in area of present-day Thailand and Cambodia, it is common for Buddhist sculpture to be made of sandstone. The model might classified these correctly but with the wrong reason. Then, if we input the sandstone sculpture from China, the model could classified its origin as Thailand. 
- Influences of Culture
  - Example: Sculpture found in Thailand that are from around 3rd Century could be heavily influence by India or imported from India before they developed into their own art style. Influences of art styles can make misclassification happened.


## Evaluation plan

- Metrics appropriate to the task
- Train/validation/test (or CV) plan

## Initial direction

- What neural approach you expect to try at Check-in 2
- Any early non-neural probe is welcome but not required yet
