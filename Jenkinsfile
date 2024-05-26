pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                stash(name: 'compiled-results', includes: 'sources/*.py*')
            }
        }
        stage('Test') {
            agent any
            steps {
                sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py --cov=my_module --cov-report=csv:coverage.csv'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Coverage Report') {
            steps {
                plot([
                    csvFileName: 'coverage.csv',
                    title: 'Test Coverage',
                    yaxis: 'Coverage',
                    csvSeries: [[file: 'coverage.csv', label: 'Coverage']]
                ])
            }
        }
        stage('Deliver') {
            agent any
            steps {
                sh "pyinstaller --onefile sources/add2vals.py"
            }
            post {
                success {
                    archiveArtifacts 'dist/add2vals'
                }
            }
        }
        
    }
}
