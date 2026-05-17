pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/vidhi6040/Bowls.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t bowls-app .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker rm -f bowls-container || exit 0'
                bat 'docker run -d -p 8000:8000 --name bowls-container bowls-app'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS 🚀 App running on localhost:8000'
        }
        failure {
            echo 'Pipeline FAILED ❌ Check logs'
        }
    }
}