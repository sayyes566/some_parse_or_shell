
import os, os.path
from shutil import copyfile


#path_insert_list_by_source_file
path_insert_list = "/home/kristen/python_parse/save/insert_list_test/"
#path_insert_list = "/home/kristen/python_parse/save/insert_list1025/"

fack_file = "/home/kristen/python_parse/testcase/fake_3/keypairs.py"

def fake_source_file(source_file):
    fake = source_file.replace("/usr/lib/python2.7/dist-packages/nova", "")
    fake_arr = fake.split("/")
    fake_file = ''
    for f in fake_arr:
        fake_file += f+"_"
    return fake_file[:-1]
    
#read each file in this folder
for filename in os.listdir(path_insert_list):
    #reset
    bool_source_exist = False   
    str_backup_file = ""
    """
    if("server_usage" in filename):
        source_file = "test_source_2.py"
    else:
        source_file = "test_source.py"
    """
    with open(path_insert_list +  filename, "r") as lin:
        #read line
        for line in lin:
            aline = line.split("::")
            #print aline[0] 
            #get source file path + name
            if(aline[0] == "filepath"):
                source_file = aline[1]
                source_file = fack_file
                #print source_file
                bool_source_exist = True
            elif(aline[0] != "filepath" and bool_source_exist):
                tab = " " * int(aline[1])
                # read source file and insert a line
                e = open(source_file, "r")
                contents = e.readlines()
                contents.insert(int(aline[0]), tab + aline[2])
                #print contents
                e.close()
                #write to source file
                f = open(source_file, "w")
                contents = "".join(contents)
                f.write(contents)
                f.close()
    lin.close()

