pipeline {

    agent { label "build" }

    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        
        stage("env cleanup") { 
            steps {
                sh "docker image prune -f"
            }
        }
    
        stage("build docker image") {
            steps {
                sh "docker build -t commit_info . "
            }
        }
        
        stage("Launch service") {        
            steps { 
                //sh "docker rm -f suku_commit_info"
                //sh "docker run  --name suku_commit_info commit_info"
                sh "docker run  commit_info"
            }
        } 
    }
 }

