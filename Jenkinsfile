pipeline{
    agent any

    environment {
        SONAR_PROJECT_KEY = "LLMOPS"
        SONAR_SCANNER_HOME = tool "SonarQubeScanner"
        AWS_REGION = "us-east-1"
        ECR_REPO = 'llmops-repo'
        IMAGE_TAG = 'Latest'
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
    }
}