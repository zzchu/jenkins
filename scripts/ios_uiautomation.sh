BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR=`dirname $BASEDIR`
#echo "10.128.65.51"
#exit 0
# This sceript needs calabash, and thus has to run within ios dir
#IOSDIR=$BASEDIR/ios
#cd $IOSDIR
#echo "DIAG the ios dir is $IOSDIR"
app_path=`pwd`"/MediaSessionIntegrationTest.app"

rm -rf /tmp/uiautomation_out.trace/
rm -rf /tmp/uiautomation_out
mkdir -p /tmp/uiautomation_out

#echo "App path =  $app_path"
#export DEVICE_TARGET=`system_profiler SPUSBDataType | sed -n -e '/iPad/,/Serial/p' -e '/iPhone/,/Serial/p' | grep "Serial Number:" | awk -F ": " '{print $2}'`

#echo "Device IP not provided attempting to fetch it."
mkdir -p /tmp/uiautomation_out
ip_cmd="instruments -w $1 -t /Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.bundle/Contents/Resources/Automation.tracetemplate $app_path -e UIASCRIPT $3  -e UIARESULTSPATH /tmp/uiautomation_out -D /tmp/uiautomation_out"
if [ -f /Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.xrplugin/Contents/Resources/Automation.tracetemplate ]; then
    # xcode 6
    #ip_cmd="instruments -w $DEVICE_TARGET -t /Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.xrplugin/Contents/Resources/Automation.tracetemplate $app_path -e UIASCRIPT ./tools/getip.js  -e UIARESULTSPATH /tmp/uiautomation_out -D /tmp/uiautomation_out"
    #ip_cmd="xcrun instruments  -w $DEVICE_TARGET -D /tmp/uiautomation_out -t \"Automation\" \"com.webex.sq\" -e UIARESULTSPATH /tmp/uiautomation_out -e UIASCRIPT  ./tools/getip.js"
    ip_cmd="-D /tmp/uiautomation_out -t /Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.xrplugin/Contents/Resources/Automation.tracetemplate MediaSessionIntegrationTest.app -e UIARESULTSPATH /tmp/uiautomation_out -e UIASCRIPT $3"
    ip_cmd="instruments -w $1 ${ip_cmd}"
fi

if [ "$2" = "ip" ]; then
	#echo instruments -w $DEVICE_TARGET ${ip_cmd}
	device_ip_result=`$ip_cmd`

	device_ip=`echo "$device_ip_result" | grep 'Pass:' | awk -F ': ' '{print $2}'`
	rm -rf instrumentscli*
	echo "$device_ip"
fi

if [ "$2" = "unlock" ]; then
	$ip_cmd
	echo "$1 unlocked"
fi

exit 0
