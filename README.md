> This project is a follow up this project -> https://github.com/atul-harsh33108/Movie-Review-Sentiment-Analysis-



![Screenshot (1564)](https://github.com/user-attachments/assets/d7968dbf-0973-4b3b-abf0-c9a4af87411e)
![Screenshot (1565)](https://github.com/user-attachments/assets/e59f838b-72da-4e1c-bf98-9df83e09c4bd)

# Movie Sentiment Analysis App

## Overview
This repository contains a Streamlit web application for sentiment analysis of movie reviews, integrated with a Jenkins CI/CD pipeline and Docker containerization. The app uses Logistic Regression, Naive Bayes, and LSTM models to predict review sentiment with 91.92% accuracy.

## Features
- Input movie reviews and select from three models.
- View predictions and history.
- Automated deployment via Jenkins pipeline.
- Containerized with Docker (port 8501, volume logging).

## Setup
1. Clone the repo: `git clone https://github.com/atul-harsh33108/movie-sentiment-app.git`
2. Install Docker Desktop and Jenkins.
3. Run Jenkins: `java -jar jenkins.war`
4. Configure pipeline in Jenkins and build.
5. Access app at `http://localhost:8501/`.

## Technologies
- Python, Scikit-learn, TensorFlow, Streamlit
- Jenkins, Docker, GitHub

## Usage
- Enter a review (e.g., "Great movie!").
- Select a model and click "Predict".
- View history in the app or logs at `C:\Project\sentiment-logs\history.log`.

## Improvements
- Automated Docker network (`sentiment-net`) creation.
- Model files hosted in repo (completed 2025-07-26).

## License
MIT License .
