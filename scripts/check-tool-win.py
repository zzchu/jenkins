import os,sys
import subprocess
import shutil

nodelist=os.environ['nodelist']
print os.getcwd()
if os.environ['NODE_NAME'] not in nodelist:
	sys.exit()
pipe=os.popen("ruby -v")
ruby=pipe.read()
print ruby
pipe.close()

if not ruby.find("not recognized as an internal or external command"):
	print "no ruby found, please install it"
	sys.exit()

pipe=os.popen("gem -v")
gem=pipe.read()
print gem
pipe.close()
if not gem.find("not recognized as an internal or external command"):
	print "no rubygem found, please install it"
	sys.exit()

action=os.environ['action']
if action=="install":
	os.system("gem install cucumber -v 1.3.18")
	pipe=os.popen("gem which cucumber")
	cucumber_exe=pipe.read()
	pipe.close()
	cucumber_dir=os.path.dirname(cucumber_exe)
	cucumber_fomatter_dir=os.path.join(cucumber_dir,"cucumber","formatter")
	print "copy rerun.rb and junit.rb to cucumber"
	shutil.copy("rerun.rb", cucumber_fomatter_dir)
	shutil.copy("junit.rb", cucumber_fomatter_dir)
	print "copy ta failed cases analyze tool to build-all"
	build_all_dir=os.path.abspath(os.path.join(os.getcwd(),"..","..","build-all"))
	if not os.path.exists(build_all_dir):
		os.mkdir(build_all_dir)
	shutil.copy("analyze-failed.py",build_all_dir)
	shutil.copy("analyze-failed-rerun.py",build_all_dir)