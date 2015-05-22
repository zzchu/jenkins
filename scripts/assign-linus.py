import os

node=os.environ["NODE_NAME"]
print "[INFO] NODE: %s"%node
sjc_linus=os.environ["sjc_linus_address"]
hz_linus=os.environ["hz_linus_address"]
path=os.path.abspath(os.path.join(os.environ['WORKSPACE']

win_linus_address=sjc_linus
if "SJC" not in node:
	win_linus_address=hz_linus
print "[INFO] win linus address is %s"%win_linus_address

os.chdir(path)
filename=""propsfile.linus_addr."+os.environ["parent_project"]
with open("filename", "w+") as text_file:
    text_file.write("win_linus_address=%s" % win_linus_address)

