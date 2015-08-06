#!/usr/bin/env python

import os, sys
import subprocess
import json
import time
import argparse

def run(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

gen_pass="8f083344f3c2cb6800f273bc1a000701"
ENV = {
  "integration" : "https://wme-jenkins.gen:%s@sqbu-jenkins.cisco.com:8443/view/Calliope/job/calliope-linus/publish%20to%20repo/"%gen_pass
}

def linus_install_rpm(rpm_file, build_number):
    os.system("yum -C --disablerepo='*' erase -y 'linus-*'")
    os.system("yum localinstall --disablerepo='*' -y %s" % rpm_file)
    os.system("chown -R linus /opt/calliope")
    os.system("sed -i -e 's/\\/calliope\/[^0-9.]*\\([0-9.]*\\)/\\/calliope\\/%s/g' /etc/monit.d/linus_monit.cfg" % build_number)
    os.system("monit reload")

def check_install_rpm(env="integration"):
    command = 'curl -s -k %s/api/json' % ENV[env]
    json_result = run(command)
    result = json.loads(json_result)
    rpm_file_name = result["artifacts"][0]["fileName"]
    build_num = result["number"]
    print "LINUS BUILD NUMBER IS %s"%build_num
    if(os.path.exists("/opt/calliope/%s" % build_num)):
        print "You already have the latest build: %s" % build_num
        return
    print "Start to download the RPM: %s" % rpm_file_name
    dst_rpm_file = "/tmp/%s" % rpm_file_name
    os.system('curl -o %s -k %s/artifact/_build/components/target/rpm/%s' % (dst_rpm_file, ENV[env], rpm_file_name))
    os.system("monit stop linus")
    linus_install_rpm(dst_rpm_file, build_num)
    time.sleep(5)
    os.system("monit start linus")

parser = argparse.ArgumentParser(description='you can provide specific build number to install and run')
parser.add_argument("-n", '--bldNum', help="provide the linus build number to install and run", default="none")
args = parser.parse_args()
if args.bldNum == "none":
    check_install_rpm()
else:
    ENV["integration2"]="https://wme-jenkins.gen:%s@sqbu-jenkins.cisco.com:8443/view/Calliope/job/calliope-linus/%s/"%(gen_pass,args.bldNum)
    check_install_rpm("integration2")
