#!/bin/bash
# Autor: Barckcode
# Description: Script to restart Blog containers after deploy.

######################### VARS
# Logs
LOG_SCRIPT="/tmp/deploy_api_blog.log"

# Commands
DATE="$(date):"

# Services
PRO_APP="api_blog"

######################### SCRIPT
echo "*********************************************" >> $LOG_SCRIPT
echo $DATE >> $LOG_SCRIPT
/usr/bin/docker service update $PRO_APP --force >> $LOG_SCRIPT
echo "Deploy hecho con GitHubActions + S3 + CodePipeline + CodeDeploy" >> $LOG_SCRIPT
exit 0
