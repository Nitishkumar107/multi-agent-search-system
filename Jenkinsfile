pipeline{
    agent any

    environment {
        SONAR_PROJECT_KEY = "LLMOPS"
        SONAR_SCANNER_HOME = tool "Sonarqube"
        // AWS_REGION = "us-east-1"
        // ECR_REPO = 'llmops-repo'
        // IMAGE_TAG = 'Latest'
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
    }
}