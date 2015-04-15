import os,sys
import shutil

#nodelist=os.environ['nodelist']
print os.getcwd()
#if os.environ['NODE_NAME'] not in nodelist:
#	sys.exit()

def read_command_output(command):
	pipe=os.popen(command)
	output=pipe.read()
	print output
	pipe.close()
	return output
	
def check_ruby():	
	ruby=read_command_output("ruby -v")
	if "not recognized as an internal or external command" in ruby:
		print "no ruby found, please install it"
		sys.exit()

	gem=read_command_output("gem -v")
	if "not recognized as an internal or external command" in gem:
		print "no rubygem found, please install it"
		sys.exit()

	action=os.environ['action']
	if action=="install":
		os.system("gem install -aIx cucumber")
		os.system("gem install cucumber -v 1.3.18")
		cucumber_exe=read_command_output("gem which cucumber")
		cucumber_dir=os.path.dirname(cucumber_exe)
		cucumber_fomatter_dir=os.path.join(cucumber_dir,"cucumber","formatter")
		print "copy rerun.rb and junit.rb to cucumber %s"%cucumber_fomatter_dir
		shutil.copy("rerun.rb", cucumber_fomatter_dir)
		shutil.copy("junit.rb", cucumber_fomatter_dir)
		'''
		print "copy ta failed cases analyze tool to build-all"
		build_all_dir=os.path.abspath(os.path.join(os.getcwd(),"..","..","build-all"))
		if not os.path.exists(build_all_dir):
			os.mkdir(build_all_dir)
		shutil.copy("analyze-failed.py",build_all_dir)
		shutil.copy("analyze-failed-rerun.py",build_all_dir)
		'''

check_ruby()