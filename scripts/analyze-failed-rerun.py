import os,glob,errno,sys
import shutil,stat
import distutils.core
import pdb
import smtplib
from email.mime.text import MIMEText

wmepath=os.path.abspath(os.path.join(os.environ['WORKSPACE'], os.environ['repo_loc'], os.environ['wme_loc']))
wx2testpath=os.path.join(wmepath,"ta")
wx2testfeaturepath=os.path.join(wx2testpath, "ref-app")

tag=""
def get_tag():
    global tag
    tag=""
    #Collect failed case trace
    os.chdir(wx2testfeaturepath)
    with open ("rerun.txt", "r") as myfile:
        data=myfile.read().replace('\n', '').split(' ')
    if not data[0]:
        print "[INFO] no failed case, exit"
        custome_email()
        return  
    for item in data:
        tag=item.split(":")[-1]+","+tag
    tag=tag[:-1]
    print "[INFO] Failed tags: %s"%tag
	
def send_email(content,subject,to):
	msg=MIMEText(content)
	msg['Subject'] = subject
	msg['To'] = to
	msg['From'] = "jenkins@wme-jenkins.cisco.com"
	s = smtplib.SMTP('outbound.cisco.com:25')
	s.sendmail("jenkins@wme-jenkins.cisco.com", [to], msg.as_string())
	s.quit()
    
os.chdir(wx2testfeaturepath)
count=rerun=int(os.environ['rerun_times'])
linus=str(os.environ['win_linus_address'])
rerun_tags_prefix="rerun tags: "
rerun_tags=""
base_tag_ls=[]
unstable_tag_ls=[]

def find_unstable_tag():
    global tag
    global unstable_tag_ls,base_tag_ls
    after_rerun_ls=tag.split(",")
    if(len(after_rerun_ls)>0):
        for item in base_tag_ls:
            if item not in after_rerun_ls:
                unstable_tag_ls.append(item)

def custome_email():
    global unstable_tag_ls
    unstable_tag_set=set(unstable_tag_ls)
    if len(unstable_tag_set)>0:
        join_str=","
        rerun_tags=join_str.join(unstable_tag_set)
        print "Sending email to inform %s are unstable tags"%rerun_tags
        bld_num=os.environ['parent_project']+os.environ['parent_build_number']
        subject="[Jenkins Alert] Attention: WIN TA rerun tags for build %s"%bld_num
        content="%s%s\n%s"%(rerun_tags_prefix,rerun_tags,os.environ['BUILD_URL'])
        send_email(content, subject, "wme-buildpipeline-scrum@cisco.com")
    #send_email(content, subject, "qianden@cisco.com")

while os.stat("rerun.txt").st_size != 0 and count>0:
    get_tag()
    #before first rerun, read all failed tags into a base list
    if count==rerun:
        base_tag_ls=tag.split(",")
    else:
        find_unstable_tag()
    open('rerun.txt', 'w+').close()
    print "[INFO] cucumber ta_features --tags %s --tags @sanity --format pretty --format json --out report.json --format rerun --out rerun.txt --format junit --out junit"%tag
    os.system("cucumber ta_features --tags %s --tags @sanity --format pretty --format json --out report.json --format rerun --out rerun.txt --format junit --out junit LINUS_SERVER=%s"%(tag,linus))
	#rerun_tags+=tag+","
    count=count-1

get_tag()
find_unstable_tag()
custome_email()
	
if os.stat("rerun.txt").st_size != 0: 
    get_tag()
    target=max(glob.glob("trace/*/"), key=os.path.getmtime)
    failed_case_dir=os.path.join(os.getcwd(), "trace", "failed_case_trace")
    if not os.path.exists(failed_case_dir):
        os.mkdir(failed_case_dir)
    os.chdir(target)
    tag_arr=tag.split(",")
    for tag in tag_arr:
        found_logs=glob.glob("*%s*"%(tag))
        for log in found_logs:
            shutil.copy(log, failed_case_dir)
    #pdb.set_trace()
    #Analyze failed cases logs
    os.chdir(wx2testfeaturepath)
    python_script=os.path.abspath(os.path.join(os.environ['WORKSPACE'],os.environ['repo_loc'],"debug-tools","calling","wme","logtool","wmeparse.py"))
    os.system("py %s %s"%(python_script,failed_case_dir))
    report_dir=os.path.join(wx2testpath,"ref-app","trace","wme_result")
    os.chdir(failed_case_dir)
    shutil.copytree(failed_case_dir,report_dir,ignore=shutil.ignore_patterns('*log','wx2call_stats'))

    #Generate trace analyze htmls
    analyze_res_dir=os.path.join(wx2testpath,"trace-analyze-results")
    target_report_dir=os.path.join(analyze_res_dir,os.environ['BUILD_NUMBER'],"wme_result")
    site_dir=os.path.join(analyze_res_dir,"site")
    distutils.dir_util.copy_tree(report_dir,target_report_dir)
    if os.path.exists(site_dir):
        distutils.dir_util.remove_tree(site_dir)
    print os.path.join(wmepath,"jenkins","support-files","site")
    distutils.dir_util.copy_tree(os.path.join(wmepath,"jenkins","support-files","site"),site_dir)
    ruby_script=os.path.join(site_dir,"build_website_from_wme_trace.rb")
    os.chdir(analyze_res_dir)
    os.system("ruby %s %s"%(ruby_script,os.environ['BUILD_NUMBER']))

    

