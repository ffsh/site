pipeline {
    agent any
    environment{
        PYTHONUNBUFFERED = 1
        SECRET = credentials('jenkins-secret')
    }
    parameters {
        booleanParam(name: 'CLEAN', defaultValue: false, description: 'Clean the Repo?')
        string(name: 'TARGET', defaultValue: "", description: "[unused] Enter a specific target, default all.")
        choice(name: 'BRANCH', choices: ['dev', 'test', 'rc', 'stable'], description: 'Pick something')
    }
    stages {
        stage('Git checkout'){
            steps{
                sh "git checkout ${BRANCH}"
                sh "git fetch"
                sh "git reset --hard origin/${BRANCH}"
                sh "git submodule update"
            }
        }
        stage('Clean'){
            steps{
                sh "echo ${CLEAN}"
                script{
                    if(params.CLEAN){
                        sh "./build.py -c dirclean -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT}"
                    }else{
                        sh "echo 'skipping cleaning'"
                    }
                }
            }
        }
        stage('Update') {
            steps {
                sh "./build.py -c update -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT} --log 'V=w'"
            }
        }
        stage('Build') {
            steps {
                sh "./build.py -c build -b ${BRANCH} -n ${BUILD_NUMBER} -w ${WORKSPACE} --commit ${GIT_COMMIT} --cores '9' --log 'V=w' --silent"
            }
        }
        stage('Sign'){
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