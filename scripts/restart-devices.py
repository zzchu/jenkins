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
        return len(self.udid_ls)

    def print_udid(self):
        if len(self.udid_ls)>0:
            for id in self.udid_ls:
                print id
                
    def reboot(self):
        if len(self.udid_ls)>0:
            print "Rebooting android..."
            for id in self.udid_ls:
                reboot_cmd="%s -s %s reboot"%(self.adb_location,id)
                subprocess.call(reboot_cmd, shell=True)
                print "Rebooted device %s"%(id)
            print "Going to sleep 45 seconds and wait for android back ..."
            time.sleep(45)
            print "Done waiting for android reboot"
        else:
            print "No android devices connected"
    
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
        start_adb_cmd = self.adb_location + " devices"
        lines = []
        restart_adb_count = 0
        while restart_adb_count < 40 and len(lines)<len(self.udid_ls):
            print restart_adb_cmd
            res = subprocess.check_output(restart_adb_cmd, shell=True)
            print res
            time.sleep(4)
            print start_adb_cmd
            android_devices = subprocess.check_output(start_adb_cmd, shell=True, universal_newlines=True).strip()
            print android_devices
            lines = re.findall('([a-zA-Z0-9]+).*device$',android_devices,flags=re.MULTILINE)
            restart_adb_count += 1
        if restart_adb_count == 40:
            print "Unable to restart the adb server and find attached device"
            return False    
        return self.capture_ip()


class Ios():
    def __init__(self):
        check_iosdeploy_cmd="sh ios-deploy.sh version"
        res=subprocess.check_output(check_iosdeploy_cmd, shell=True)
        if not res:
            raise Exception("ios-deploy is not installed correctly")
        self.udid_ls=[]

    def capture_udid(self):
        list_dev_cmd="sh ios-deploy.sh list"
        ios_devices = subprocess.check_output(list_dev_cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True).strip()
        self.udid_ls=re.findall('.* Found.*\(([a-zA-Z0-9]+)\) connected through USB.$',ios_devices,flags=re.MULTILINE)
        return len(self.udid_ls)
    
    def print_udid(self):
        if(len(self.udid_ls)>0):
            for id in self.udid_ls:
                print id

    def install_test_app(self):
        for id in self.udid_ls:
            install_cmd="sh ios-deploy.sh install %s MediaSessionIntegrationTest.app"%id
            res = subprocess.check_output(install_cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True).strip()
            print res

    def obtain_ip(self):
        found_ip=True
        for id in self.udid_ls:
            cmd = "sh ios_uiautomation.sh %s ip getip.js" % id
            # This returns array of 'bytes'
            ip = subprocess.check_output(
                cmd,
                shell=True).strip()
            #ip = ip.decode('utf-8')
            if ip:
                print "%s Found IP address: %s" % (id,ip)
            else:
                print "%s CANNOT find IP address" % id
                found_ip=False
        return found_ip

    def unlock(self):
        for id in self.udid_ls:
            cmd = "sh ios_uiautomation.sh %s unlock unlock.js" % id
            res = subprocess.check_output(
                 cmd,
                 shell=True).strip()
            print res

    def reboot(self):
        print "Rebooting iphone..."
        subprocess.call(
            "ruby restart_device.rb",
            shell=True)
        print "Sleep 45 seconds to wait ios back"
        time.sleep(45)
        print "Done waiting for ios reboot"
        ios.install_test_app()
        self.unlock()
        return self.obtain_ip()



if __name__ == '__main__':
    try:
        android=Android()
        num=android.capture_udid()
        if num>0: 
            android.reboot()
            if android.restart_adb():
                print "SUCCESS, all android devices restart!"
            else:
                print "FAILED, some android devices not back, please check"
        else:
            print "No android devices connected"
    except Exception,e:
        print "Error: " + str(e)
        
    try:
        ios=Ios()
        num=ios.capture_udid()
        if num>0:
            #ios.print_udid()
            #ios.install_test_app()
            #ios.obtain_ip()
            if ios.reboot():
                print "SUCCESS, all ios devices restart!"
            else:
                print "FAILED, some ios devices not back, please check"
        else:
            print "No ios devices connected"
    except Exception,e:
        print "Error: " + str(e)
