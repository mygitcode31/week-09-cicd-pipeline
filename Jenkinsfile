
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mydockerimage31/week9-cicd-pipeline'
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Checking Python application files..."
                    python3 --version
                    test -f app.py
                    test -f test_app.py
                    test -f Dockerfile
                    python3 -m py_compile app.py test_app.py
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m unittest -v test_app'
            }
        }

        stage('Package') {
            steps {
                sh '''
                    mkdir -p dist
                    cp app.py test_app.py Dockerfile dist/
                    tar -czf application.tar.gz -C dist .
                    ls -lh application.tar.gz
                '''
                archiveArtifacts artifacts: 'application.tar.gz',
                                 fingerprint: true
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKER_TOKEN" | docker login \
                          --username "$DOCKER_USER" \
                          --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished: ${currentBuild.currentResult}"
        }
        success {
            echo 'Application tested and Docker image published.'
        }
        failure {
            echo 'Pipeline failed. Check the stage console output.'
        }
    }
}
