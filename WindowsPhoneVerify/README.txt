1. requirement

   ----windows 8.1
   ----VS 2013 with update 3 above

2.phone registration
  
  before using windows phone for development, phone registration is needed.
  ----i) registration tool
         C:\Program Files (x86)\Microsoft SDKs\Windows Phone\v8.1\Tools\Phone Registration\PhoneReg.exe
		 
  ----2) development account
         you can use any development account for the registration
		 below is zhangdong's account: 
		       dongzha@cisco.com/Ustc13866724357
         http://wikicentral.cisco.com/display/WX2/Devices+for+WME+build+pipeline		 
  ----3) use account account in 2) via tool in 1) for the registration
         any question, please refer to :
		 https://msdn.microsoft.com/en-us/library/windows/apps/ff769508(v=vs.105).aspx

3. window phone verify:

    ----run bat script file:
         .\WP8UTSlaveVerify.bat
    ----if the return value of above script is 0, 
	     congratulation, windows phone for the slave can work now!
		if not, please refer to the prompt.