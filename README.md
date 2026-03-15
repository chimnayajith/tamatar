# Tamatar 🍅

Tamatar is a system for **detecting tomato leaf diseases using machine
learning**.

The project combines a **Progressive Web App (PWA)** frontend, a
**backend API**, and a **machine learning model** trained on tomato leaf
images.

Users will be able to capture or upload a photo of a tomato leaf and
receive a prediction about the disease affecting the plant.

------------------------------------------------------------------------

## System Architecture

The system is composed of three main components:

User\
↓\
PWA Frontend\
↓\
Backend API (Django)\
↓\
ML Model (Tomato Disease Classifier)

------------------------------------------------------------------------

## Components

### Frontend -- Progressive Web App

Located in:

tamatar-frontend/

The frontend provides the user interface where users can:

-   upload tomato leaf images
-   capture images using a mobile device
-   view disease predictions
-   receive feedback or recommendations

The frontend is designed as a **Progressive Web App (PWA)** so it can
work well on mobile devices and be installable like a native app.

------------------------------------------------------------------------

### Backend -- Django API

The backend acts as the bridge between the frontend and the machine
learning model.

Responsibilities include:

-   receiving image uploads
-   running inference using the trained model
-   returning predictions to the frontend
-   handling API requests

Example endpoint:

POST /predict

This endpoint accepts an image and returns the predicted disease.

------------------------------------------------------------------------

### Machine Learning Pipeline

Located in:

tamatar-ml/

This module contains the full pipeline used to train the tomato disease
classifier.

The training process includes:

1.  Image preprocessing
2.  Data augmentation
3.  CNN training (ResNet18 / MobileNet / ShuffleNet)
4.  Feature extraction
5.  Feature selection
6.  Classical machine learning classifiers

Detailed documentation for this module is available in:

tamatar-ml/README.md

------------------------------------------------------------------------

## Repository Structure
```
tamatar/ 
├── tamatar-frontend/
└── tamatar-ml/ 
```
------------------------------------------------------------------------
