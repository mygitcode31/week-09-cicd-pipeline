pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mydockerimage31/week9-cicd-pipeline'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate') {
            steps {
                sh '''
                    set -eu
                    python3 --version
                    test -f app.py
                    test -f test_app.py
                    test -f Dockerfile
                    python3 -m py_compile app.py test_app.py
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m unittest -v test_app'
            }
        }

        stage('Package') {
            steps {
                sh '''
                    set -eu
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
                    set -eu
                    docker build \
                      --pull \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    set -eu
                    mkdir -p reports

                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      -v "$WORKSPACE/reports:/reports" \
                      aquasec/trivy:latest \
                      image --scanners vuln \
                      --format table \
                      --output /reports/trivy-image-scan.txt \
                      ${IMAGE_NAME}:${IMAGE_TAG}

                    cat reports/trivy-image-scan.txt
                '''
                archiveArtifacts artifacts: 'reports/trivy-image-scan.txt',
                                 allowEmptyArchive: false,
 				 fingerprint: true
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                    set -eu
                    docker rm -f week10-smoke-test >/dev/null 2>&1 || true

                    cleanup() {
                        docker rm -f week10-smoke-test >/dev/null 2>&1 || true
                    }
                    trap cleanup EXIT

                    docker run -d \
                      --name week10-smoke-test \
                      -p 18000:8000 \
                      ${IMAGE_NAME}:${IMAGE_TAG}

                    for i in $(seq 1 20); do
                        if docker exec week10-smoke-test \
                          python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" \
                          >/dev/null 2>&1; then
                            echo "Application health check passed."
                            exit 0
                        fi
                        sleep 2
                    done

                    docker logs week10-smoke-test
                    echo "Application health check failed."
                    exit 1
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
                        set -eu
                        set +x

                        echo "$DOCKER_TOKEN" | docker login \
                          --username "$DOCKER_USER" \
                          --password-stdin

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
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
            echo 'Tests, image scan, smoke test and image publishing completed.'
        }
        failure {
            echo 'Pipeline failed. Review the failed stage and console output.'
        }
    }
}
