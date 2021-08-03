######################### VARS
# Logs
LOG_SCRIPT="/tmp/deploy_api_blog.log"

# APP
PATH_APP="/var/www/api_blog_helmcode_com"

sudo /bin/rm -rf $PATH_APP/* >> $LOG_SCRIPT