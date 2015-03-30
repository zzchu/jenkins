if [ "$1" = "version" ];then
   ios-deploy --version
fi
if [ "$1" = "list" ];then
   ios-deploy -c
fi
if [ "$1" = "install" ];then
   ios-deploy -r --id $2 --bundle $3
fi 
