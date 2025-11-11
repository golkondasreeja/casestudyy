pipeline {
  agent any
  stages {
    stage('Run Selenium Tests') {
      steps {
        echo "Running Selenium Tests for BookMood"
        bat 'pip install -r requirements.txt'
        bat 'start /B python app.py'
        bat 'ping 127.0.0.1 -n 5 > nul'
        bat 'pytest -v'
      }
    }
    stage('Build Docker Image') {
      steps {
        bat 'docker build -t bookmood:v1 .'
      }
    }
    stage('Docker Login') {
      steps {
        bat 'docker login -u yourdockerhubusername -p yourpassword'
      }
    }
    stage('Push Docker Image') {
      steps {
        bat 'docker tag bookmood:v1 yourdockerhubusername/bookmood:latest'
        bat 'docker push yourdockerhubusername/bookmood:latest'
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        bat 'kubectl apply -f deployment.yaml --validate=false'
        bat 'kubectl apply -f service.yaml'
      }
    }
  }
  post {
    success {
      echo '✅ BookMood Pipeline completed successfully!'
    }
    failure {
      echo '❌ Pipeline failed. Check logs.'
    }
  }
}
