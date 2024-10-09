# Facial Recognition Classification

## User Interaction and System Functionality

Users can upload video clips or images from their device or utilize the webcam feed. The system will detect faces within the provided video/webcam stream and predict the individual's approximate age, gender, and emotion.

### Applications

The system offers two key applications:

1. **Restaurant Customer Satisfaction Assessment:** Integration within the restaurant's checkout counter camera allows for real-time customer satisfaction assessment. Traditional survey methods can elicit biased responses, while this system provides unobtrusive insights. 
2. **Data-Driven Insights and Expansion:** Prediction data is stored within a Data Warehouse, enriching the database and enabling analysis of customer preferences. This information helps restaurants gain a deeper understanding of their clientele.

### Prediction Technique

The system utilizes Convolutional Neural Networks (CNNs) for prediction. Images in the training set undergo convolution operations to extract salient features. These features are then passed through fully connected layers to generate the final predictions. 

## Datasets

### Emotion Recognition: FER-2013

The FER-2013 dataset is used for emotion recognition. It can be accessed here: [https://www.kaggle.com/datasets/deadskull7/fer2013](https://www.kaggle.com/datasets/deadskull7/fer2013)

### Age and Gender Prediction: UTKFace

The UTKFace dataset is used to predict age and gender. It is available here: [https://www.kaggle.com/datasets/jangedoo/utkface-new](https://www.kaggle.com/datasets/jangedoo/utkface-new)

## Model Structure

The project uses three separate models:

* **Age Prediction:**  Stored at `IS_project_source_code/source_code/modelsage.h5`
* **Emotion Prediction:** Stored at `IS_project_source_code/source_code/emotion.h5`
* **Gender Prediction:**  Stored at `IS_project_source_code/source_code/gender.h5` 


## Back-end Prediction Processing

- **Model Training:** Keras is used to build and predict on each frame from the video or webcam. 
- **Prediction:** Video or data from the webcam is read frame by frame. Each frame is passed through the face detection model. If a face is detected, its location is identified. Subsequently, the detected face is passed through three models: gender, age, and emotion. Finally, OpenCV is used to display the results on the frame and render them to the GUI.

## Project Limitations

The accuracy on real-world data is not yet optimal, despite good results on the test dataset. Therefore, training the model with real-world data is necessary. Ideally, the data should be collected from the camera used for video capture. 

## Training and evaluation

All Training and evaluation stepp showed in forlder `IS_project_source_code/training_notebooks` which 2 IPYNB are `Emotion.ipynb` and `Gender_Age.ipynb`.

## Software demotration

All source code in `IS_project_source_code/source_code`. Please go there read `README.md` to run demo app.
