pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\Vidhi\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
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
                bat "%PYTHON% --version"
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "%PYTHON% -m pip install --upgrade pip"
                bat "%PYTHON% -m pip install -r requirements.txt"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Stop Old Container') {
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
}