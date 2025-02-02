pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        APP_URL = "http://localhost:5000"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Check Shell') {
            steps {
                sh 'echo "Current Shell: $SHELL"'
                sh 'ps -p $$'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Security Scans') {
            steps {
                parallel (
                    "Static Analysis (Bandit)": {
                        sh ". $VENV_DIR/bin/activate && bandit -r . -ll -ii -f txt -o bandit_report.txt || true"
                    },
                    "Secrets Scanning (GitLeaks)": {
                        sh "gitleaks detect --source . --verbose"
                    }
                )
            }
        }

        stage('Run Tests') {
            steps {
                sh ". $VENV_DIR/bin/activate && pytest tests/"
            }
        }

        stage('Build & Run Application') {
            steps {
                sh "docker build -t my-python-app:${BUILD_NUMBER} ."
                sh "docker run -d -p 5000:5000 --name my-app my-python-app:${BUILD_NUMBER}"
                sleep(time: 10, unit: 'SECONDS')
            }
        }

        stage('DAST Security Test (OWASP ZAP)') {
            steps {
                sh '''
                docker run --rm -v $(pwd):/zap/wrk:rw -t owasp/zap2docker-stable zap-baseline.py \
                -t $APP_URL -r zap_report.html || true
                '''
            }
        }

        stage('Push to Docker Registry') {
            when {
                branch 'main'
            }
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: 'https://index.docker.io/v1/']) {
                    sh "docker tag my-python-app:${BUILD_NUMBER} my-docker-repo/my-python-app:latest"
                    sh "docker push my-docker-repo/my-python-app:latest"
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh "./deploy.sh"
            }
        }
    }

    post {
        always {
            sh "docker stop my-app || true"
            sh "docker rm my-app || true"
            archiveArtifacts artifacts: 'zap_report.html', fingerprint: true
            cleanWs()
        }
    }
}
