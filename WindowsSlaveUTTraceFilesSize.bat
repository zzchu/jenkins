@echo off
set WorkingDir=%cd%
set RegisterFile64=C:/64RegApp.reg
set RegisterFile32=C:/32ResApp.reg
set RegisterFile=%RegisterFile64%

rem for 64 reg 
echo Windows Registry Editor Version 5.00         >%RegisterFile64%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\WebEx]          >>%RegisterFile64%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\WebEx\wbxtrace] >>%RegisterFile64%
echo "maxfiles"="15"   >>%RegisterFile64%
echo "tracesize"="20"  >>%RegisterFile64%


rem for 32 reg 
echo Windows Registry Editor Version 5.00                       >%RegisterFile32%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\WebEx]            >>%RegisterFile32%
echo [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\WebEx\wbxtrace]   >>%RegisterFile32%
echo "maxfiles"="15"   >>%RegisterFile32%
echo "tracesize"="20"  >>%RegisterFile32%

rem call regedit.exe and change seting for trace file size
echo WorkingDir is %WorkingDir%
echo RegisterFile is %RegisterFile%
regedit %WorkingDir%/%RegisterFile% 
pause


