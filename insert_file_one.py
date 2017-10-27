
import os, os.path
from shutil import copyfile
import sys

filename = sys.argv[1]
#path_insert_list_by_source_file
#filename = "./insert_list1025/" + file
path_insert_list = "./insert_list1025/"

def fake_source_file(source_file):
    fake = source_file.replace("/usr/lib/python2.7/dist-packages/nova", "")
    fake_arr = fake.split("/")
    fake_file = ''
    for f in fake_arr:
        fake_file += f+"_"
    return fake_file[:-1]
    
#read each file in this folder
#for filename in os.listdir(path_insert_list):
    #reset
bool_source_exist = False   
str_backup_file = ""
"""
    if("server_usage" in filename):
        source_file = "test_source_2.py"
    else:
        source_file = "test_source.py"
"""
print "filename      ", filename
with open(path_insert_list +  filename, "r") as lin:
#read line
    for line in lin:
        aline = line.split("::")
        #get source file path + name
        if(aline[0] == "filepath"):
            source_file = aline[1]
            source_file = source_file.replace("\n", "")
	    source_file = source_file.strip()
            print "source_file       :"+ source_file +":"
            #str_backup_file = source_file + "_bak"
	    #print str_backup_file , ":= backup"
            #check source file exist
            if os.path.exists(source_file):
                print "\n file exist \n"
		bool_source_exist = True
                #fake_file = fake_source_file(source_file)
                #copyfile(source_file, fake_file)
                #source_file = fake_file
		#print "source fake", source_file
                    
		str_backup_file = source_file + "_bak"
		print "backup :" +str_backup_file
		# generate a backup file if it's not exist
                if (not os.path.exists(str_backup_file)):
                    copyfile(source_file, str_backup_file)
                        
        elif(aline[0] != "filepath" and bool_source_exist):
            tab = " " * int(aline[1])
        # read source file and insert a line
            e = open(source_file, "r")
            contents = e.readlines()
            contents.insert(int(aline[0]), tab + aline[2])
            e.close()
        #write to source file
            f = open(source_file, "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()
lin.close()

