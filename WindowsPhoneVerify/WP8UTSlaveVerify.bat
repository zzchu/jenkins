@echo off
rem *************************************************************************************************
rem
rem   usage: WP8UTSlaveVerify.bat
rem
rem   2015/09/24 huashi@cisco.com
rem *************************************************************************************************

rem default setting
setlocal EnableDelayedExpansion
set CurrentWorkingDir=%cd%
set Platform=ARM
set Configuration=Release

rem basic setting 
call :BasicSetting
call :EnvironmentPathSetting
call :BasicCheck
if not %ERRORLEVEL%==0 (
		goto :ErrorReturn
)
call :CommonAppPostSetting
call :TestResultInitial
call :WP8UTVerifyForSlave
call :GetFinalTestReturnCode
call :OutputResult
echo  ReturnCode is %ReturnCode%
goto :EOF

rem function for setting 
rem **********************************************************************************************************
:BasicSetting
	set WMEUnitTestWorkingDir=%CurrentWorkingDir%
	set TestAppName=DolphinTestApp

	rem product ID can be found under APP project's property->WMAppManifest.xml->packaging
	set APPProductID=202a6815-ffd9-4a6f-a4e2-085198d360e7
	set APPPackageFileName=DolphinTestApp_%Configuration%_ARM.xap		
	set XMLFileName=dolphin_unittest_main.xml
	rem time in millisecond for ut runtime setting
	set MaxUTRunTime=2000
goto :EOF

:EnvironmentPathSetting
	rem VC2013 setting
	set VC2013Path=C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\IDE
	set VC2013BinPath=C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin
	set MSBuildPath=C:\Program Files (x86)\MSBuild\12.0\Bin
	rem tools setting
	set ISEToolPath=C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.1\Tools\IsolatedStorageExplorerTool
	set APPDeployToolPath=C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.1\Tools\AppDeploy
	rem set environment path
	set PATH=%PATH%;%VC2013Path%;%ISEToolPath%;%APPDeployToolPath%;%VC2013BinPath%;%MSBuildPath%
goto :EOF

rem *********************
:CommonAppPostSetting
    set vConfiguration=Release
	cd  %CurrentWorkingDir%
	set AppWorkingDir=%cd%
	set APPPackageDir=%cd%
	set APPPackageFile=%APPPackageDir%\%APPPackageFileName%
	
	rem UT trace log file and test result xml file setting
	set UTResultDir=%CurrentWorkingDir%\XML_%vConfiguration%_%TestAppName%
	set TempXMLDir=%UTResultDir%\IsolatedStore
	set XMLFileRelativePath=IsolatedStore\Shared
	set XMLFilePath=%UTResultDir%\%XMLFileRelativePath%\%XMLFileName%
	set UTResultFile=%UTResultDir%\%XMLFileName%

	rem the same function with sleep command on linux
	set PingIP=192.0.2.2
goto :EOF

rem function for setting 
rem **********************************************************************************************************
:BasicCheck
	if not exist  "%VC2013Path%" (
		echo VC2013 has not been installed yet, please prepare your test environment first!	
		goto :ErrorReturn
	)
goto :EOF

rem  function for option
rem **********************************************************************************************************
:WP8UTVerifyForSlave
	rem default setting	
	call :OutputAppSetting
	set TestFlag=0
	call :Test
	call :TestSummary
goto :EOF

rem function for test result 
rem **********************************************************************************************************
:TestResultInitial
	set TestReleaseFlag=0
	set TestReleaseInfo=NULL
goto :EOF

:GetFinalTestReturnCode
	set ReturnCode=0
	if not %TestReleaseFlag% == 0 (
		set ReturnCode=1
	)	
goto :EOF

:TestSummary
	if not %TestFlag%==0 (
		set TestReleaseFlag=1
		set TestReleaseInfo=%TestReleaseInfo%----%TestAppName%--test--release--failed--%TestFailedLog%
	) else (
		set TestReleaseInfo=%TestReleaseInfo%----%TestAppName%--test--release--succeed
	)

goto :EOF

:Test
	rem remove previous APP, install latest App and run UT
	echo Removing previous App and install/launch latest UT App....
	AppDeployCmd   /uninstall %APPProductID% /targetdevice:de
	AppDeployCmd   /installlaunch %APPPackageFile% /targetdevice:de
	if not %ERRORLEVEL%==0 (
	 	set TestFlag=1
		set TestFailedLog=launch APP  and run UT failed
		echo %TestFailedLog%
		echo APPPackageFileName %APPPackageFile%
		goto :ErrorReturn
	)
	
	rem remove previous xml file for test result
	if exist %UTResultDir%  rd /s /q %UTResultDir%
	md %UTResultDir%

	rem waiting for UT test
	echo waiting for all cases in UT .....
	ping %PingIP%  -n 1  -w %MaxUTRunTime% >nul
	
	rem copy xml file from device
	ISETool ts de %APPProductID% %UTResultDir%
	copy %XMLFilePath%  %UTResultDir%
	if not %ERRORLEVEL%==0 (
        set TestFlag=1
		set TestFailedLog=copy UT output xml file failed
		goto :ErrorReturn
	)

	dir %TempXMLDir%
	echo TempXMLDir   is %TempXMLDir%
	if exist %TempXMLDir%   rd /s /q  %TempXMLDir%

	rem remove APP after test
	echo "remove APP after test......"
	AppDeployCmd   /uninstall %APPProductID% /targetdevice:de
	
goto :EOF

:OutputResult
	echo **********************************************************
	echo        %Action% summary list as below:
	echo **********************************************************
	echo TestReleaseFlag  is %TestReleaseFlag%
	echo TestReleaseInfo  is %TestReleaseInfo%
	echo **********************************************************
	
goto :EOF

:OutputAppSetting	
	echo ********************************************************
	echo       setting for %TestAppName%
	echo ********************************************************
	echo AppWorkingDir        is %AppWorkingDir%
	echo APPPackageFileName   is %APPPackageFileName%
	echo APPPackageFile       is %APPPackageFile%
	echo UT maximum runtime   is %MaxUTRunTime%(ms)
	echo UTResultDir          is %UTResultDir%
	echo Test result xml file is %UTResultFile%
	echo UTTraceDir           is %UTTraceDir%
	echo Test trace file      is %TraceFilePath%
	echo ********************************************************
goto :EOF

:ErrorReturn
endlocal
exit /b 2

:End
endlocal
exit /b %ReturnCode%
