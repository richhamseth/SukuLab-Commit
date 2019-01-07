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
                sh "sudo docker build -t daily . "
            }
        }

        stage("env cleanup") { 
            steps {
                sh "sudo docker image prune -f"
            }
        }
        
        stage("Launch service") {        
            steps {
                sh "sudo docker run -it --name daily daily "
            }
        } 
    }
 }

