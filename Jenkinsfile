pipeline {

    agent { label "build" }

    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
    
        stage("build docker image") {
            steps {
                sh "docker build -t commit_info . "
            }
        }

        stage("env cleanup") { 
            steps {
                sh "docker image prune -f"
            }
        }
        
        stage("Launch service") {        
            steps { 
                sh "docker run -d --name suku_commit_info commit_info"
            }
        } 
    }
 }

