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

class MyHTMLParser(HTMLParser):
    
    '''
    def __init__(self):
        global g_print
        # initialize the base class
        HTMLParser.__init__(self)
    '''
        
    def handle_starttag(self, tag, attrs):
        global g_print, g_mis, g_find_miss, g_tag_start, g_tag_end, g_start, g_line, g_nd, g_def, g_def_find, g_def_pre, g_miss_func
        #print "Start tag:", tag
        if(tag == 'p'):
          g_start = 1
          g_tag_start = 1 
          g_tag_end = 0
          g_find_miss = 0
          #g_mis += "g_tag_start     :" + str(g_tag_start) +"g_tag_end"  +str(g_tag_end)  + "tag" + tag +"\n"
        g_print += "Start tag:" + ''.join(tag) + "\n"
        for attr in attrs:
            if ( "id" in attr):
                #g_mis += "attr     :" + str(attr) + "\n"
                if ( "n" in attr[1]):
                    g_nd = 0
                elif ( "t" in attr[1]):
                    g_nd = 1 
                    g_line = attr[1].replace("t", "")
            if ( "class" in attr):
                if ("nam" in attr and g_def_find == 2):
                    #g_mis += "33333333333"
                    g_def_find = 3
                if ("key" in attr):
                    #g_mis += "11111111"
                    g_def_find = 1
                    
            if("stm mis" in attr and g_nd == 1):
                if(g_start == 1 and g_def_pre != g_def):
                    g_mis += "\n"
                    g_mis += g_line+ " def " + g_def + "\n"
                    g_miss_func += g_def + ","
                    g_def_pre  = g_def
                    g_start = 0
                g_find_miss = 1
                    
            
            g_print += "     attr:" + ''.join(attr) + "\n"
            #print "     attr:", attr

    def handle_endtag(self, tag):
        global g_print, g_mis, g_find_miss, g_tag_start, g_tag_end, g_tag
       
        if(tag == 'p'):
            if(g_find_miss == 1 and g_tag_start == 1 and g_tag_end == 0):
                g_mis +=  "\n"
            g_tag_start = 0 
            g_tag_end = 1
        g_print += "End tag  :"+ ''.join(tag) + "\n"
        #print "End tag  :", tag

    def handle_data(self, data):
        global g_print, g_mis, g_find_miss, g_tag_start, g_tag_end, g_tag, g_line, g_def_find, g_def, g_def_pre
        if(g_def_find == 1 and "def" == data ):
            g_def_find = 2
        if(g_def_find == 3 ):
            g_def_find = 0                    
            #g_mis += "==========="
            g_def = ''.join(data)
            #g_mis +=  "FFFFF" + g_def
            g_def_find = 0
        if(g_find_miss == 1 and g_tag_start == 1 and g_tag_end == 0):
          if(''.join(data) != ""):
              g_mis +=  ''.join(data) 
        g_print += "Data     :" + ''.join(data) + ", "
        
        #print "Data     :", data

    def handle_comment(self, data):
        global g_print
        g_print += "Comment  :" + ''.join(data) + "\n"
        #print "Comment  :", data

    def handle_entityref(self, name):
        global g_print
        c = unichr(name2codepoint[name])
        g_print += "Named ent:" + ''.join(c) + "\n"
        #print "Named ent:", c

    def handle_charref(self, name):
        global g_print
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        g_print += "Num ent  :" + ''.join(c) + "\n"
        #print "Num ent  :", c

    def handle_decl(self, data):
        global g_print
        g_print += "Decl     :" + ''.join(data) + "\n"
        #print "Decl     :", data

parser = MyHTMLParser()
#parser.feed('<img src="python-logo.png" alt="The Python logo">')

#f = open("_usr_lib_python2_7_dist-packages_cinderclient_client_py.html", "r")
#parser.feed(f.read())

#f1=open('./testfile', 'w+')
#f1.write(g_print.encode('utf8'))
#f1.close()
paths = []
paths.append('/home/kristen/python_parse/testcase/htmlcov_controll')
paths.append('/home/kristen/python_parse/testcase/htmlcov_compute')
#paths.append('/home/kristen/python_parse/testcase/fake_2')
#paths.append('/home/kristen/python_parse/testcase/fake_1')
for index in range(len(paths)):
    path = paths[index]
    print "path     :", path
    if index == 0 :
        g_mis +=  "\n controll\n"
        g_miss_func += "\n controll \n"
    else: 
         g_mis +=  "\n compute\n"
         g_miss_func += "\n compute \n"
         
    for filename in os.listdir(path):
        save_file = ""
        if("cinderclient" in filename):
            save_file = "cinder"
        if("glanceclient" in filename):
            save_file = "glance"
        if("keystoneclient" in filename):
            save_file = "keystonet"
        if("neutronclient" in filename):
            save_file = "neutron"
        if("nova" in filename):
            save_file = "nova"
        if(save_file != ""):
            file_title = filename.replace( "_usr_lib_python2_7_dist-packages_", "")
            g_mis += file_title + "\n"
            #g_miss_func += save_file  + "\n"
            f = open(path +"/" +filename, "r")
            parser.feed(f.read())
            f.close()
            #f1=open('./' + save_file, 'w+')
            #f1.write(g_mis.encode('utf8'))
            with open(save_file+".txt", "a") as myfile:
                myfile.write(g_mis.encode('utf8'))
                myfile.close()
            with open(save_file+"_func.txt", "a") as myfile:
                myfile.write(g_miss_func.encode('utf8'))
                myfile.close()
            g_mis = ""
            g_miss_func = ""



