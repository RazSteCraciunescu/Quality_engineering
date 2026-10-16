pipeline {
  agent any
  options { timestamps(); disableConcurrentBuilds() }
  environment {
    PYTHONUNBUFFERED = '1'
    CIVICSHIFT_DB = "${WORKSPACE}/var/jenkins.db"
  }
  stages {
    stage('Python quality') {
      steps {
        sh 'python3 -m venv .venv'
        sh '. .venv/bin/activate && python -m pip install -r requirements-dev.txt'
        sh '. .venv/bin/activate && python -m pytest -m "not browser" --junitxml=reports/generated/pytest-junit.xml'
        sh '. .venv/bin/activate && python scripts/validate_repository.py'
      }
      post { always { junit allowEmptyResults: true, testResults: 'reports/generated/pytest-junit.xml' } }
    }
    stage('Frontend quality') {
      steps {
        sh 'npm install'
        sh 'npm run build'
        sh 'npm run test:unit'
      }
    }
    stage('Container smoke') {
      steps {
        sh 'docker build -t civicshift:${BUILD_NUMBER} .'
        sh 'docker run --rm -d --name civicshift-${BUILD_NUMBER} -p 8000:8000 civicshift:${BUILD_NUMBER}'
        sh 'sleep 4 && curl --fail http://127.0.0.1:8000/api/health'
      }
      post { always { sh 'docker rm -f civicshift-${BUILD_NUMBER} || true' } }
    }
  }
  post {
    always { archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/generated/**,playwright-report/**' }
  }
}
