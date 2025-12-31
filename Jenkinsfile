pipeline {
    agent any

    environment {
        AWS_REGION     = "ap-south-1"
        EKS_CLUSTER    = "flask-mysql-eks"
        ECR_REPO       = "flask-mysql-app"
        IMAGE_TAG      = "latest"
        K8S_NAMESPACE  = "flask-app"

        AWS_ACCOUNT_ID = sh(
            script: "aws sts get-caller-identity --query Account --output text",
            returnStdout: true
        ).trim()

        IMAGE_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
    }

    stages {

        stage("Checkout Code") {
            steps {
                git branch: "main",
                url: "https://github.com/InfoSoftronix/docker-flask-mysql-project.git"
            }
        }

        stage("SonarQube Code Analysis") {
            environment {
                SONAR_TOKEN = credentials('sonarqube-token')
            }
            steps {
                sh '''
                  sonar-scanner \
                  -Dsonar.projectKey=flask-mysql-app \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=http://sonarqube:9000 \
                  -Dsonar.login=$SONAR_TOKEN
                '''
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage("Build Docker Image") {
            steps {
                sh '''
                  docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                '''
            }
        }

        stage("Push Artifact to Nexus") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'nexus-username',
                        usernameVariable: 'NEXUS_USER',
                        passwordVariable: 'NEXUS_PASS'
                    )
                ]) {
                    sh '''
                      tar -czf flask-app.tar.gz *
                      curl -u $NEXUS_USER:$NEXUS_PASS \
                      --upload-file flask-app.tar.gz \
                      http://nexus:8081/repository/flask-repo/flask-app.tar.gz
                    '''
                }
            }
        }

        stage("AWS CLI Configuration") {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                      aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                      aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                      aws configure set region ${AWS_REGION}
                    '''
                }
            }
        }

        stage("Login to ECR") {
            steps {
                sh '''
                  aws ecr get-login-password --region ${AWS_REGION} |
                  docker login --username AWS --password-stdin \
                  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                '''
            }
        }

        stage("Push Image to ECR") {
            steps {
                sh '''
                  docker tag ${ECR_REPO}:${IMAGE_TAG} ${IMAGE_URI}
                  docker push ${IMAGE_URI}
                '''
            }
        }

        stage("Configure kubectl") {
            steps {
                sh '''
                  aws eks update-kubeconfig \
                  --region ${AWS_REGION} \
                  --name ${EKS_CLUSTER}
                '''
            }
        }

        stage("Deploy via Helm") {
            steps {
                sh '''
                  helm upgrade --install flask-app helm/flask-app \
                  --namespace ${K8S_NAMESPACE} \
                  --create-namespace \
                  --set image.repository=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO} \
                  --set image.tag=${IMAGE_TAG}
                '''
            }
        }

        stage("Deploy Monitoring (Prometheus + Grafana)") {
            steps {
                sh '''
                  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
                  helm repo add grafana https://grafana.github.io/helm-charts
                  helm repo update

                  helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
                  -n monitoring --create-namespace
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Executed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Logs"
        }
    }
}
