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
                sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
                sh 'py.test --cov=sources --cov-report=xml:test-reports/coverage.xml sources/test_calc.py'
                // Convert coverage XML report to CSV
                sh 'python sources/convert_coverage_xml_to_csv.py test-reports/coverage.xml test-reports/coverage.csv'
            }
            post {
                always {
                    junit 'test-reports/results.xml'            
                }
            }
        }
        stage('Coverage Report') {
            agent any
            steps {
                plot([
                    //group: 'Coverage Reports',
                    csvFileName: 'test-reports/coverage.csv',
                    //title: 'Test Coverage',
                    //yaxis: 'Coverage',
                    style: 'line',
                    //csvSeries: [[file: 'coverage.csv']]
                    group: 'Coverage Reports',
                    title: 'Code Coverage',
                    yaxis: 'Coverage Percentage',
                    csvSeries: [[
                        file: 'test-reports/coverage.csv',
                        fileType: 'csv',
                        inclusionFlag: 'INCLUDE_BY_STRING',
                        url: '',
                        displayTableFlag: true,
                        title: 'Coverage Percentage',
                        yseries: [[
                            file: 'test-reports/coverage.csv',
                            label: 'Coverage',
                            format: '%.2f'
                        ]]
                    ]]
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
