#!/usr/bin/python
#Author Stanley Shi(wshi2@cisco.com) 2015-8-3

import os
import re
import sys
import shutil
import ConfigParser
import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


FolderLevel=4
IsCheckOutCode=1
SrcRoot=""
ConfigFile=sys.path[0]+os.sep+"UnsafeCScanner.cfg"
CSVReportFile="ScanResult.csv"
SummaryReportFile="Result.html"
GitCheckOutList=sys.path[0]+os.sep+"gitcheckoutlist.txt"
UnsafeFunctionList="_snprintf,memcmp16,strcpyfldout,strspn,_strtok_l,strcspn,strstr,_tccmp,strtok,strtok,_tcscat,strtolowercase,_tcschr,strtouppercase,_tcsclen,strisalphanumeric,strxfrm,_tcscmp,strisascii,strzero,_tcscoll,strisdigit,vsprintf,_tcscpy,strishex,wcscat,_tcscspn,wcschr,_tcslen,wcscmp,_tcsncat,wcscpy,_tcsnccat,wcsicmp,_tcsnccmp,sprintf,_tcsnccpy,strbrk,_tcsncmp,strcasecmp,strlen,_tcsncpy,strcasestr,wcslen,_tcspbrk,strcat,strncat,wcsncat,_tcsrchr,strchr,strncmp,wcsncmp,_tcsstr,strcmp,strncpy,wcsncpy,_tcstok,strcmpfld,strnlen,wcsnicmp,_tcsxfrm,strcoll,strpbrk,wcsrchr,_tcsxfrm_l,strcpy,strprefix,wcsstr,_vstprintf,strcpyfld,strrchr,wcstok,strcpyfldin,strremovews,_stprintf,_tcsicmp,memcpy,memset,memmove,memcmp"
ExcludeFolders="opensource,openssl"
IsForECIntegration=1
IsSendMailByManualRun=0
mailfrom="cctg-sec@cisco.com"
mailto="wshi2@cisco.com"
mailsubject="UnsafeC Status:"

totalDefects=0

#Init config from configuration file
def InitConfigration():
	if os.path.exists(ConfigFile):
		global FolderLevel
		global IsCheckOutCode
		global IsForECIntegration
		global GitCheckOutList
		global SrcRoot
		global CSVReportFile
		global SummaryReportFile
		global UnsafeFunctionList
		global ExcludeFolders
		global LocalOutputFolder
		global IsSendMailByManualRun
		global mailfrom
		global mailto
		global mailsubject
		global totalDefects
		
		
		cf = ConfigParser.ConfigParser()
		cf.read(ConfigFile)
		
		FolderLevel=int(cf.get("PROJECT", "FolderLevel"))
		IsCheckOutCode=int(cf.get("PROJECT", "IsCheckOutCode"))
		GitCheckOutList=cf.get("PROJECT", "GitCheckOutList")
		SrcRoot=cf.get("PROJECT", "SrcRoot")
		LocalOutputFolder=cf.get("PROJECT","LocalOutputFolder")
		
		if os.path.exists(LocalOutputFolder) == False:
			os.makedirs(LocalOutputFolder)
		
		
		CSVReportFile=LocalOutputFolder+os.sep+cf.get("SYSTEM", "CSVReportFile")
		SummaryReportFile=LocalOutputFolder+os.sep+cf.get("SYSTEM", "SummaryReportFile")
		
		if os.path.exists(CSVReportFile):
			print "delete CSVReportFile:"+CSVReportFile
			os.remove(CSVReportFile)		
		
		if os.path.exists(SummaryReportFile):
			print "delete SummaryReportFile:"+SummaryReportFile
			os.remove(SummaryReportFile)		
		
		UnsafeFunctionList=cf.get("SYSTEM", "UnsafeFunctionList")
		ExcludeFolders=cf.get("SYSTEM", "ExcludeFolders")
		IsForECIntegration=int(cf.get("SYSTEM", "IsForECIntegration"))
		IsSendMailByManualRun=int(cf.get("SYSTEM", "IsSendMailByManualRun"))
		
		mailfrom=cf.get("SYSTEM", "mailfrom")
		mailto=cf.get("SYSTEM", "mailto")
		mailsubject=cf.get("SYSTEM", "mailsubject")
		
		

		

def CheckOutCodeFromGit(gitRep):	
	PathItemList=gitRep.replace(".git","").split("/")
	fileName=PathItemList[len(PathItemList)-1]	
	targetFolder=(SrcRoot+os.sep+fileName).strip()
	
	print "targetFolder:"+targetFolder
	
	if os.path.exists(targetFolder):
		print "git pull targetFolder:"+targetFolder
		#os.system(r"rm -rf "+targetFolder)
		
		os.chdir(targetFolder)		
		os.system(r"git pull")
		os.chdir(SrcRoot)
		
	else:
		print r"git clone "+gitRep+r" "+targetFolder
		os.system(r"git clone "+gitRep+r" "+targetFolder)
	return
	

#Check all the lines with blacklist
def CheckUnsafeFunctions(filename):
	checkfile = open(filename)
	filelines = checkfile.readlines()
		
	linenum=0
	isInComment=False
	
	for fileline in filelines:
		linenum+=1		
		
		if fileline.find(r"/*")>-1:
			isInComment=True
			
		if fileline.find(r"*/")>-1:
			isInComment=False
			
		if isInComment==True:
			continue
		
		
		if fileline.find(r"//")>-1:
			fileline=fileline[0:fileline.find(r"//")]		
					
		KeywordList=UnsafeFunctionList.split(',')
		
		for unsafeFunc in KeywordList :
	
			matchobj = re.match(".*\\W" + unsafeFunc + "\\s*\\(.*",fileline)
			#matchobj = fileline.find(unsafeFunc)
			
			if matchobj:
				#print fileline
				WriteCSVReport(filename,linenum,fileline)
						
	checkfile.close();

	return

def isInNotExcludeList(filepath):
	ExcludeFoldersList=ExcludeFolders.split(',')

	for excludeitem in ExcludeFoldersList:

		if filepath.find(excludeitem)>-1:
			return False
	return True
	

	
#Write Out report
def WriteCSVReport(filepath,linenum,linecode):
	cvsfile=open(CSVReportFile,'a+')
	cvsfile.write(filepath.replace(SrcRoot,"",1)+','+str(linenum)+',"'+linecode.strip()+'"\n')
	cvsfile.close()
	
def WriteSummaryReport():

	
	global totalDefects
	
	writeSummaryReportHeader()
	
	if os.path.exists(CSVReportFile)==False:
		print "There is no issue found"
		writeSummaryReportTable("None",0)
		writeSummaryReportFooter()	
		return True
	
	cvsfile=open(CSVReportFile)
	cvslines=cvsfile.readlines()
	
	currentFolder=""
	counter=0
	
	for fileline in cvslines:
		if currentFolder=="" :
			currentFolder=getLevelFolderPath(fileline)
			print currentFolder
			
		if fileline.find(currentFolder)>-1:
			counter+=1
		else:			
			writeSummaryReportTable(currentFolder,counter)
			currentFolder=""
			totalDefects=totalDefects+counter
			counter=0
			
	if counter <> 0:
		
		writeSummaryReportTable(currentFolder,counter)
		currentFolder=""
		totalDefects=totalDefects+counter
		counter=0	
	else:
		writeSummaryReportTable(currentFolder,counter)
		
	cvsfile.close()	
	
	writeSummaryReportFooter()
	
	return True
	
	
	
def writeSummaryReportTable(module,num):
	repFile=open(SummaryReportFile,'a+')
	repFile.write("<TR><TD style='border:teal solid;border-width:0 1 1 0' Align=aLeft >"+module+"</TD><TD style='border:teal solid;border-width:0 1 1 0' Align=center>"+str(num)+"</TD></TR>\n")
	repFile.close()	

def writeSummaryReportHeader():
	repFile=open(SummaryReportFile,'w')
	repFile.write("<TABLE border = 1 style='border:teal solid;border-width:3 2 2 3'><font face=Calibri> <TR style='background:teal;color:white'><TH  Width= 480> Modules </TH><TH Width= 120> Issues</TH></TR>\n")
	repFile.close()

def writeSummaryReportFooter():
	repFile=open(SummaryReportFile,'a+')
	repFile.write("</Table>\n")
	repFile.close()
	
def getLevelFolderPath(filepath):
	
	LevelFolderPath=""
	
	if filepath.find(',')==-1:
		return LevelFolderPath
		
	tempfolders=filepath.split(',')[0]
	tempfolders=tempfolders.split(os.sep)	
	
	if len(tempfolders)<=FolderLevel:
		LevelFolderPath=filepath
		return LevelFolderPath
		
	else:	
		index=0
		LevelFolderPath=""
		while (index < FolderLevel):
			LevelFolderPath+=tempfolders[index]
			LevelFolderPath+=os.sep
			index+=1

		return LevelFolderPath
	

def SendMail():
		
	msg = MIMEMultipart('alternative')
	msg['Subject'] = mailsubject+"-"+ datetime.date.today().strftime('%Y-%m-%d')
	msg['From'] = mailfrom
	msg['To'] = mailto

	MailHead = """\
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"><style type="text/css">body {font-family: "Arial","sans-serif";font-size: 10pt;} p,ul {font-family: "Arial","sans-serif";font-size: 10pt;}table.reportTable {border-collapse: collapse;}.newTitle{background-color: red;color: white;font-weight: bold;}.todayTitle{background-color: blue;color: white;font-weight: bold;}.yesterdayTitle{background-color: #333333;color: white;font-weight: bold;}.reportCell {border: solid #BFBFBF 1pt;padding:3.75pt;font-size: 10pt; line-height: 150%;}.highlighted {color: red;font-weight: bold;}.secTipContainer {vertical-align: top;padding-left: 30px;width: 250px;}</style>
	<p>Hi All Engineers,</p>
	<p><span>Please check the issues in <span style="background-color:yellow;">ALL C&#43;&#43; codes</span> found by unsafeC. <span style="color:red;">All of them must be fixed ASAP before end of Sprint or code freeze.</span></p>
	<p><span>Total issue num: <b>"""+str(totalDefects)+"""</b></span></p>
	<p>Here is the issue summary status:</p>
	"""
	
	if os.path.exists(SummaryReportFile) == False:
		print "fail to get the report content."
		return
	
	repFile=open(SummaryReportFile,'r')	
	MailBody=repFile.read()
	
	
	
	MailBody+="<br><p>Download detail report <a href='http://10.224.56.204/reports/"+os.path.basename(CSVReportFile)+"'>here</a></p>"
	
	repFile.close()

	MailFoot ="""
	<span id="placeholder"></span>
	<p><b>While fix security issues, you should:</b></p>
	<ul>
	<li>Follow the <a href="http://wikicentral.cisco.com/display/CSGSEC/Safe+C+Lib+Usage+Quick+Guide">instruction</a> to fix issues</li>
	<li>Consult security team (cctg-sec@cisco.com) for further questions about the issue or solution</li>
	<li>Review with security team before suppressing any issues</li>
	<li>Add name of Dev owner who suppress the issue and security owner who reviewed the issue to comments of suppression</li>
	<li>Send code diff to security team after fixed security issues</li>
	<li>Send test scope suggestion to QA for the issue fix</li>
	</ul>
	<p>-Cisco WebEx Security Team</p>
	"""

	
	part2 = MIMEText(MailHead+MailBody+MailFoot, 'html')

	msg.attach(part2)

	s = smtplib.SMTP('outbound.cisco.com')
	s.sendmail(mailfrom,mailto, msg.as_string())
	s.quit()
		
	
def isAvalibaleFileType(filename):

	if filename.endswith(".cpp") or filename.endswith(".h") or filename.endswith(".c") or filename.endswith(".cc") or filename.endswith(".m") or filename.endswith(".mm") or filename.endswith(".hpp"):
		return True
	
	else:
		return False
		
	
#init the configration
InitConfigration()

#Start to run

if SrcRoot=="":
	Directory=raw_input("Please input directory:")
	SrcRoot=Directory
	

#Code checkout
if IsCheckOutCode == 1:
	
	
	#For EC integration
	if IsForECIntegration == 1:

		if os.path.exists(GitCheckOutList):
			GitListFile=open(GitCheckOutList)
			GitListLines=GitListFile.readlines()
			print "start to checkou code"
			for gitline in GitListLines:
				os.system(gitline)		
			print "finish to checkout code"
		else:
			print "there is no git checkout list from EC."
	
	else:
	#Manual Run checkout   
	
		if os.path.exists(GitCheckOutList):
			GitListFile=open(GitCheckOutList)
			GitListLines=GitListFile.readlines()
			
			for gitline in GitListLines:
				if "stash-eng-chn-sjc1.cisco.com/stash" in gitline:
					CheckOutCodeFromGit(gitline)
				else:
					CheckOutCodeFromGit(r"https://stash-eng-chn-sjc1.cisco.com/stash/scm/cctg/"+gitline+r".git")
		
		else:
			print "there is no git checkout list."
			


		
for root,dirs,files in os.walk(SrcRoot):
		
	for path in files:
		
		if isAvalibaleFileType(path)==True and isInNotExcludeList(root+os.sep+path)==True:	
			#print "Start Checking:"+root+'/'+path
			CheckUnsafeFunctions(root+os.sep+path)
			print "Finish Checking:"+root+os.sep+path
	


WriteSummaryReport()

if IsSendMailByManualRun==1:
	SendMail()