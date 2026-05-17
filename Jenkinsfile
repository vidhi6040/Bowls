pipeline {
    agent any

    environment {
        IMAGE_NAME = "bowls-app"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vidhi6040/Bowls.git'
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker --version'
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Stop Old Container (if any)') {
            steps {
                bat 'docker rm -f bowls-container || exit 0'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 8000:8000 --name bowls-container %IMAGE_NAME%'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS 🎉 App is running!'
        }
        failure {
            echo 'Pipeline FAILED ❌ Check logs'
        }
    }
}