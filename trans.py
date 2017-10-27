
import os, os.path,re
from shutil import copyfile


#path_insert_list_by_source_file
path_insert_list = "./insert_list/"

path_out_list = "./noend/"
#read each file in this folder
for filename in os.listdir(path_insert_list):
    #print "filename      ", filename
    #with open(path_insert_list +  filename, "r") as lin:
    with open(path_insert_list +'nova_api_openstack_compute_contrib_flavormanage', "r") as lin:
        #f = open(path_out_list+filename,'w')
        f = open(path_out_list+'nova_api_openstack_compute_contrib_flavormanage','w')
        #read line
        for line in lin:
            #print line
            if re.search(r"_end", line):
               pass

            else:
                  f.write(line)
        f.close()      

    lin.close()

