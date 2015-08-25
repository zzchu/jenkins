@echo off
set RegisterFile=C:/64RegApp.reg
set RegisterFile32=C:/32ResApp.reg

rem for 64 reg 
echo Windows Registry Editor Version 5.00         >%RegisterFile%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\WebEx]          >>%RegisterFile%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\WebEx\wbxtrace] >>%RegisterFile%
echo "maxfiles"="15"   >>%RegisterFile%
echo "tracesize"="20"  >>%RegisterFile%


rem for 32 reg 
echo Windows Registry Editor Version 5.00                       >%RegisterFile32%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\WebEx]            >>%RegisterFile32%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\WebEx\wbxtrace]   >>%RegisterFile32%
echo "maxfiles"="15"   >>%RegisterFile32%
echo "tracesize"="20"  >>%RegisterFile32%

rem call regedit.exe and change seting for trace file size
rem regedit - 

