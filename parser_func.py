from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import glob, os

g_print = ""
g_mis = ""
g_miss_func = ""
g_find_miss = 0
g_tag_start = 0
g_tag_end = 0
g_start = 0
g_nd = 0
g_line = 0
g_def = ""
g_def_pre = ""
g_def_find = 0

def parser_func(str_content):

    res = {}
    res_num = {}
    res_str = ""
    sort_num = list(range(1200))
    funcs = str_content.split(",")
    for func in funcs:
        func = func.strip()
        segments = func.split("_")
        for segment in segments:
            segment = segment.strip()
            if segment in res:
                res[segment] += "," + func
            else:
                res[segment] = func
            if segment in res_num:
                res_num[segment] += 1
            else:
                res_num[segment] = 0
                
    print ("print (sort_num)")
    print (sort_num)
    
    for  key in  res:
        res_str = "=========================\n"
        res_str += key +" "+ str(res_num[key])+ " \n"
        res_str += "=========================\n"
        res_str += res[key] + " \n"
        if (key != "" and key != " "):
            if res_num[key] in sort_num and isinstance(sort_num[res_num[key]], str):
                sort_num[res_num[key]] += res_str
            else:
                print (key) 
                print (res_num[key])
                sort_num[res_num[key]] = res_str
        '''
        res_str += key +" "+ str(res_num[key])+ ": \n"
        res_str += res[key] + " \n"
        '''
    res_str = ""
    print (sort_num)
    for  intt in  range(len(sort_num)):
        
        print ("=========================")
        print (intt)
        print ("=========================")
        print (sort_num[intt] )
        if (isinstance(sort_num[intt], str)):
            res_str += str(sort_num[intt] )
            
    print (res_str)
    print ("=========================")
    return res_str
    
#parser.feed('<img src="python-logo.png" alt="The Python logo">')

#f = open("_usr_lib_python2_7_dist-packages_cinderclient_client_py.html", "r")
#parser.feed(f.read())

#f1=open('./testfile', 'w+')
#f1.write(g_print.encode('utf8'))
#f1.close()
paths = []
paths.append('/home/kristen/python_parse/save/compute')
paths.append('/home/kristen/python_parse/save/controll')
#paths.append('/home/kristen/python_parse/testcase/fake_2')
#paths.append('/home/kristen/python_parse/testcase/fake_1')
for index in range(len(paths)):
    path = paths[index]
    print "path     :", path
   
    for filename in os.listdir(path):
        if "func" in filename:
            print (filename)
            f = open(path +"/" +filename, "r")
            g_mis = parser_func(f.read())
            f.close()
            
            with open("./save/func_compute/"+filename, "a") as myfile:
                myfile.write(g_mis.encode('utf8'))
                myfile.close()
            '''
            with open("./save/func_controll/"+filename, "a") as myfile:
                myfile.write(g_miss_func.encode('utf8'))
                myfile.close()
            '''
            g_mis = ""
        



