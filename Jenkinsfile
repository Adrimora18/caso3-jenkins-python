pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    stages {
        stage('1 - Obtener codigo GitHub') {
            steps {
                checkout scm
            }
        }

        stage('2 - Crear entorno Python') {
            steps {
                sh 'python3 -m venv .venv'
            }
        }

        stage('3 - Instalar dependencias') {
            steps {
                sh '.venv/bin/python -m pip install -r requirements.txt'
            }
        }

        stage('4 - Pruebas unitarias') {
            steps {
                sh '''
                    mkdir -p reports
                    .venv/bin/python -m pytest -q --junitxml=reports/pytest.xml
                '''
            }
        }

        stage('5 - Calidad flake8') {
            steps {
                sh '''
                    .venv/bin/flake8 app.py tests server \\
                        --output-file=reports/flake8.txt
                    if [ ! -s reports/flake8.txt ]; then
                        echo "Sin errores de estilo" > reports/flake8.txt
                    fi
                '''
            }
        }

        stage('6 - Seguridad bandit') {
            steps {
                sh '''
                    .venv/bin/bandit app.py \\
                        -f json -o reports/bandit.json
                '''
            }
        }

        stage('7 - Resumen de calidad') {
            steps {
                sh '''
                    printf 'XYZ SOLUTIONS - Informe de calidad\\n' > reports/resumen-calidad.txt
                    printf 'Pruebas: ver pytest.xml\\n' >> reports/resumen-calidad.txt
                    printf 'Flake8: ver flake8.txt\\n' >> reports/resumen-calidad.txt
                    printf 'Bandit: ver bandit.json\\n' >> reports/resumen-calidad.txt
                    cat reports/resumen-calidad.txt
                '''
            }
        }

        stage('8 - Empaquetar') {
            steps {
                sh '''
                    mkdir -p dist
                    tar -czf dist/xyz-solutions-app.tar.gz app.py
                    ls -lh dist/
                '''
            }
        }

        stage('9 - Desplegar en pruebas') {
            steps {
                sh '''
                    set -eu
                    mkdir -p /opt/despliegue/current.new
                    tar -xzf dist/xyz-solutions-app.tar.gz \\
                        -C /opt/despliegue/current.new
                    rm -rf /opt/despliegue/current
                    mv /opt/despliegue/current.new /opt/despliegue/current
                    echo "Aplicacion publicada en volumen compartido"
                '''
            }
        }

        stage('10 - Verificar endpoint health') {
            steps {
                sh '''
                    curl --fail --silent --show-error \\
                        --retry 5 --retry-delay 1 \\
                        http://servidor-pruebas:5000/health \\
                        | tee reports/health.json
                    .venv/bin/python -c "import json; d=json.load(open('reports/health.json')); assert d['status'] == 'ok'"
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/pytest.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/**/*,dist/**/*',
                allowEmptyArchive: true
        }
    }
}
