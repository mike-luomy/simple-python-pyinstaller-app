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
                sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py --cov=test_calc.py --cov-report=csv:coverage.csv'
                sh 'py.test --cov=test_calc.py --cov-report=csv:coverage.csv'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                    junit 'coverage.csv'
                    
                }
            }
        }
        stage('Coverage Report') {
            steps {
                plot([
                    group: 'Coverage Reports',
                    csvFileName: 'coverage.csv',
                    title: 'Test Coverage',
                    yaxis: 'Coverage',
                    style: 'line',
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
