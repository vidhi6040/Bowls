pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vidhi6040/Bowls.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t bowls-app .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 8000:8000 bowls-app'
            }
        }
    }
}