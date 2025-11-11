pipeline {
  agent any
  stages {
    stage('Check Python Setup') {
      steps {
        bat '''
        echo Checking Python and pip installation...
        python --version
        pip --version
        echo Showing current directory contents:
        dir
        '''
      }
    }

    stage('Run Selenium Tests') {
  steps {
    echo "Running Selenium Tests for BookMood"
    // Use python -m pip instead of pip
    bat 'python -m pip install --upgrade pip'
    bat 'python -m pip install -r requirements.txt --verbose || exit /b 1'
    bat 'start /B python app.py'
    bat 'ping 127.0.0.1 -n 5 > nul'
    bat 'pytest -v || exit /b 1'
  }
}


    stage('Build Docker Image') {
      steps {
        bat 'docker build -t bookmood:v1 .'
      }
    }

    stage('Docker Login') {
      steps {
        // ⚠️ Use Jenkins credentials instead of putting username/password directly
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        bat 'docker tag bookmood:v1 sreeja20082004/bookmood:latest'
        bat 'docker push sreeja20082004/bookmood:latest'

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
