pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/atul-harsh33108/movie-sentiment-app.git', branch: 'main'
            }
        }
        stage('Build') {
            steps {
                bat 'docker build -t movie-sentiment-app:latest .'
            }
        }
        stage('Test') {
            steps {
                bat 'docker run -d --name test-container -v C:\\Project\\sentiment-logs:/logs movie-sentiment-app:latest'
                bat 'ping 127.0.0.1 -n 11'
                bat 'docker cp test-container:/logs/history.log C:\\Project\\sentiment-logs\\test_history.log'
                bat 'docker stop test-container'
                bat 'docker rm test-container'
            }
        }
        stage('Deploy') {
            steps {
                bat 'docker network create sentiment-net || exit 0'
                bat 'docker stop movie-sentiment-app || exit 0'
                bat 'docker rm movie-sentiment-app || exit 0'
                bat 'docker run -d --name movie-sentiment-app -p 8501:8501 -v C:\\Project\\sentiment-logs:/logs --network sentiment-net movie-sentiment-app:latest'
            }
        }
    }
    post {
        always {
            bat 'docker image prune -f'
        }
    }
}