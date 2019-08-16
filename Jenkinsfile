

pipeline {
    agent any
    environment{
        PYTHONUNBUFFERED = 1
        SECRET = credentials('jenkins-secret')
    }
    stages {
        stage('Git checkout'){
            steps{
                sh "git checkout ${BRANCH}"
                sh "./build.py -c update -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT} --log 'V=w'"
            }
        }
        stage('Clean'){
            steps{
                script{
                    if(false){
                        sh "./build.py -c dirclean -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT}"
                    }
                }
            }
        }
        stage('Build') {
            steps {
                sh "./build.py -c build -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT} --cores '9' --log 'V=w' --silent"
            }
        }
        stage('Signing'){
            steps{
                sh "./build.py -c sign -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT} -s ${SECRET} --log 'V=w'"
            }
        }
        stage('Deploy') {
            steps {
                sh "./build.py -c publish -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT} -d '/var/www/firmware.grotax.de' --log 'V=w'"
            }
        }
    }
}