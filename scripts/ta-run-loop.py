import os,glob,errno,sys
import shutil,stat
import distutils.core
import pdb
import smtplib
from email.mime.text import MIMEText

wmepath=os.path.abspath(os.path.join(os.environ['WORKSPACE'], os.environ['repo_loc'], os.environ['wme_loc']))
wx2testpath=os.path.join(wmepath,"ta")
wx2testfeaturepath=os.path.join(wx2testpath, "ref-app")

os.chdir(wx2testfeaturepath)
loop=int(os.environ['loop'])
linus=str(os.environ['linus_address'])
count=1
tag=str(os.environ['ta_tags'])

print "[INFO] LOOP RUN %s"%count
print "[INFO] cucumber ta_features --tags %s --tags @sanity --format pretty --format json --out report.json --format rerun --out rerun.txt --format junit --out junit"%tag
os.system("cucumber ta_features --tags %s --tags @sanity --format pretty --format json --out report.json --format rerun --out rerun.txt --format junit --out junit LINUS_SERVER=%s"%(tag,linus))
while os.stat("rerun.txt").st_size == 0 and count<loop:
	count=count+1
	print "[INFO] Loop RUN %s"%count
	print "[INFO] cucumber ta_features --tags %s --tags @sanity --format pretty --format json --out report.json --format rerun --out rerun.txt --format junit --out junit"%tag
	os.system("cucumber ta_features --tags %s --tags @sanity --format pretty --format json --out report.json --format rerun --out rerun.txt --format junit --out junit LINUS_SERVER=%s"%(tag,linus))