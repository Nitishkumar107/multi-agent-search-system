pipeline{
    agent any

   environment {
        SONAR_PROJECT_KEY = "LLMOPS"
        SONAR_SCANNER_HOME = tool "sonarqube"
        AWS_REGION = "us-east-1"
        ECR_REPO = 'my-repo'
        IMAGE_TAG = 'latest'
   }

    stages{
        stage('cloning Github repo to Jenkins')
        {
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins.........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Nitishkumar107/multi-agent-search-system.git']])
                }
            }
        }
        stage('Sonarqube Analysis')
        {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')])
                {
                withSonarQubeEnv('sonarqube')
                {
                    sh """ 
                    ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonarqube:9000 \
                    -Dsonar.token=${env.SONAR_TOKEN}
                    """
                }}
            }
        }
    stage('Build and Push Docker Image to ECR')
    {
        steps{
            withCredentials([[$class:'AmazonWebServicesCredentialsBinding', credentialsId:'jenkins-aws-credentials']])
            {
                script{
                    def accountId = sh(script: 'aws sts get-caller-identity --query Account --output text', returnStdout: true).trim()
                    def ecr_url = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecr_url}
                    docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
                    docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecr_url}:${IMAGE_TAG}
                    docker push ${ecr_url}:${IMAGE_TAG}
                    """
                }
            }
        }
    }
}