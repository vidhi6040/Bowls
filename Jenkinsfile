pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t bowls-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop bowls-container || exit 0'
                bat 'docker rm bowls-container || exit 0'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 8000:8000 --name bowls-container bowls-app'
            }
        }
    }
}