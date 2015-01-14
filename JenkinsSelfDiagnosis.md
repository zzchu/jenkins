How to setup windows slave

1.	Set “never go to sleep” and “never turn off display”, 
	Go to control panel -> Power options

2.	Set log on without password,
	http://www.7tutorials.com/log-automatically-windows-7-without-typing-your-password
	In command prompt, run netplwiz.exe and uncheck “Users must enter a username …”

3.	Install Git and configure SSH key
http://guides.beanstalkapp.com/version-control/git-on-windows.html
•	Download from http://msysgit.github.io/ and install
•	Set HOME for cmd, add “HOME=%USERPROFILE%” into environmental variables
•	Generate and add SSH keys, use “ssh-keygen -t rsa” to generate key and add rsa.pub into GitHub account settings

4.	Set up ssh server
http://www.techrepublic.com/blog/tr-dojo/set-up-a-free-ssh-server-on-windows-7-with-freesshd/
Download freeSSHd from http://www.freesshd.com/?ctt=download and install

5.	VS
•	Download visual studio 2013 express for windows from http://www.visualstudio.com/en-us/downloads/download-visual-studio-vs.aspx
•	Download visual studio 2013 express for desktop and install 
•	Download nasm from http://www.nasm.us/pub/nasm/releasebuilds/2.11.06/win32/ and install
•	Download visual studio 2010 from http://www.visualstudio.com/en-us/downloads/download-visual-studio-vs.aspx and install

6.	Setup android development environment
•	Download jdk/jre from http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html and install
•	Download Android sdk and ndk, run SDK manager to install other tools and API
•	add path to system environment variables, examples, 
“set PATH=%PATH%;C:\Program Files (x86)\adt-bundle-windows-x86_64-20140702\sdk\platform-tools
 set PATH=%PATH%;C:\Program Files (x86)\android-ndk-r10
 set PATH=%PATH%;C:\Program Files (x86)\adt-bundle-windows-x86_64-20140702\sdk\tools
 set ANDROID_HOME=C:\Program Files (x86)\adt-bundle-windows-x86_64-20140702\sdk
set ANDROID_NDK_HOME=C:\Program Files (x86)\android-ndk-r10”

7.	Ruby and WME TA env
http://socrateos.blogspot.com/2014/04/installing-ruby-193-on-my-windows-81.html
•	Download RubyInstaller from http://rubyinstaller.org/downloads/ and install
•	Download rubygems from https://rubygems.org/pages/download and install

8.	Python and debug tool environment
•	Download python2.7 from https://www.python.org/downloads/release/python-279/ and install
•	Add C:\Python27\Scripts and C:\Python27 to environment variables
•	Setup debug tool py env
•	pip install python-dateutil
•	download numpy from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
•	download pymatlab from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymatlab
•	download scipy from http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
•	pip install matplotlib, docutils, sphinx, treelib
•	write py.bat to start python.exe for windows 'start "C:\Python27" python.exe' and put it under C:\Python27

9.	Configure Jenkins Slave node
•	Remember to add git path under tool chain
•	Set usage as used by tied jobs only
•	Recommand to use "Java Web Start" to launch windows slave
