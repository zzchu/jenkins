import time
import uuid
import os
import sys
import subprocess
import re

class Process():
    def __init__(self):
        self.runnable = None
        
    def run_nonblocking(self, command, shell, working_dir='', env=None):
        if len(working_dir) == 0:
            working_dir = os.getcwd()

        self.runnable = subprocess.Popen(
            command,
            shell=shell,
            env=env,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=working_dir)

    def wait(self, timeout):
        if self.runnable:
            #LOGGER.info('Waiting for the %s to run to completion.' % self.name)
            try:
                self.runnable.wait(timeout=timeout)
                self.runnable = None
            except subprocess.TimeoutExpired:
                #LOGGER.exception('WARNING: %s run expired' % self.name)
                self.stop()

    def stop(self):
        if self.runnable:
            #LOGGER.info('Stopping %s ' % self.name)
            self.runnable.terminate()
            self.runnable = None

class Android():
    def __init__(self):
        if "ANDROID_HOME" in os.environ:
            android_home = os.environ["ANDROID_HOME"]
        else:
            raise Exception("ANDROID_HOME environment not set")
        self.adb_location = os.path.join(
            android_home,
            "platform-tools",
            "adb")
        self.udid_ls=[]

    def capture_udid(self):
        list_dev_cmd=self.adb_location + " devices"
        android_devices = subprocess.check_output(list_dev_cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True).strip()
        self.udid_ls=re.findall('([a-zA-Z0-9]+).*device$',android_devices,flags=re.MULTILINE)

    def print_udid(self):
        if(len(self.udid_ls)>0):
            for id in self.udid_ls:
                print id
                
    def reboot(self):
        print "Rebooting android..."
        for id in self.udid_ls:
            reboot_cmd="%s -s %s reboot"%(self.adb_location,id)
            subprocess.call(reboot_cmd, shell=True)
            print "Rebooted device %s"%(id)
        print "Going to sleep 45 seconds and wait for android back ..."
        time.sleep(45)
        print "Done waiting for android reboot"
    
    def capture_ip(self):
        found_ip=True
        for id in self.udid_ls:
            get_ip_cmd="%s -s %s shell ifconfig wlan0"%(self.adb_location,id)
            res=subprocess.check_output(get_ip_cmd, shell=True)
            ip=re.match('.*ip ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*',res)
            if ip is not None :
                print id + " Found IP address: " + ip.group(1)
            else:
                found_ip=False
                print id + "CANNOT find IP address"
        return found_ip
          
    def restart_adb(self):
        # kill and restart the adb server
        restart_adb_cmd = self.adb_location + " kill-server"
        print restart_adb_cmd
        res = subprocess.check_output(restart_adb_cmd, shell=True)
        print res
        time.sleep(4)
        start_adb_cmd = self.adb_location + " devices"
        print start_adb_cmd
        lines = []
        restart_adb_count = 0
        while restart_adb_count < 40 and len(lines)<len(self.udid_ls)+1:
            android_devices = subprocess.check_output(start_adb_cmd, shell=True, universal_newlines=True).strip()
            lines = android_devices.splitlines()
            restart_adb_count += 1
        if restart_adb_count == 40:
            print "Unable to restart the adb server and find attached device"
            return False    
        return self.capture_ip()

class Ios():
    def __init__(self):
        check_iosdeploy_cmd="ios-deploy --version"
        res=subprocess.check_output(check_iosdeploy_cmd, shell=True)
        if not res:
            raise Exception("ios-deploy is not installed correctly")
        self.udid_ls=[]

    def capture_udid(self):
        list_dev_cmd="ios-deploy -c"
        ios_devices = subprocess.check_output(list_dev_cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True).strip()
        self.udid_ls=re.findall('.*\(([a-zA-Z0-9]+)\) connected through USB$',ios_devices,flags=re.MULTILINE)
    
    def print_udid(self):
        if(len(self.udid_ls)>0):
            for id in self.udid_ls:
                print id

    def obtain_ip(self):
        cmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "build_scripts/get_ios_ip.sh")
        # This returns array of 'bytes'
        ip = subprocess.check_output(
            cmd,
            shell=True).strip()
        ip = ip.decode('utf-8')
        LOGGER.info("Found iPhone/Pad IP address of '%s'" % (ip,))
        if not is_valid_ipv4(ip):
            LOGGER.error("Failed to find the ip address of the iphone - found '%s'" % (ip))
        self.phone_ip = ip
        return ip

    def get_ip(self):
        return self.phone_ip

    def reboot(self):
        print "Rebooting iphone..."
        self.run_blocking(
            "bundle exec restart_device.rb",
            shell=True,
            working_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ios"))
        time.sleep(45)
        print "Done waiting for ios reboot"

if __name__ == '__main__':
    try:
        android=Android()
        android.capture_udid()
        #android.print_udid()
        #android.capture_ip()
        android.reboot()
        if android.restart_adb() :
            print "SUCCESS, all android devices restart!"
        else:
            print "FAILED, some android devices not back, please check"
    except Exception,e:
        print "Error: " + str(e)
    try:
        ios=Ios()
        ios.capture_udid()
        ios.print_udid()
    except Exception.e:
        print "Error: " + str(e)
