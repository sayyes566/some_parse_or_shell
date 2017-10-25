from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import glob, os

'''
web example: 

def show(self, req, resp_obj, id): 

<p id="t41" class="pln">    <span class="key">def</span> <span class="nam">show</span><span class="op">(</span><span class="nam">self</span><span class="op">,</span> <span class="nam">req</span><span class="op">,</span> <span class="nam">resp_obj</span><span class="op">,</span> <span class="nam">id</span><span class="op">)</span><span class="op">:</span><span class="strut">&nbsp;</span></p>

context = req.environ['nova.context']

<p id="t42" class="stm mis">        <span class="nam">context</span> <span class="op">=</span> <span class="nam">req</span><span class="op">.</span><span class="nam">environ</span><span class="op">[</span><span class="str">'nova.context'</span><span class="op">]</span><span class="strut">&nbsp;</span></p>
'''
g_print = "" # print strings
g_mis = "" # miss test content
g_miss_func = "" # miss test function
g_bool_find_miss = 0 # if find a miss line
g_bool_tag_first_word_in_line = 0 # a line head
g_bool_tag_end = 0 # a line end
g_first_word_in_line = 0 # ex: if auth(content):, if is a first word
g_bool_find_code = 0 # find code line (the table has two tds, one is number, another is code)
g_line_number = 0 # get line number
g_func_name = "" # strings of function name
g_func_name_pre = "" #strings of previous function name
g_func_name_tag_find = 0 # find class.key , ex: <span class="key">def</span>

class MyHTMLParser(HTMLParser):
    
    '''
    def __init__(self):
        global g_print
        # initialize the base class
        HTMLParser.__init__(self)
    '''
        
    def handle_starttag(self, tag, attrs):
        global g_print, g_mis, g_bool_find_miss, g_bool_tag_first_word_in_line, g_bool_tag_end, g_first_word_in_line, g_line_number, g_bool_find_code, g_func_name, g_func_name_tag_find, g_func_name_pre, g_miss_func
        #print "Start tag:", tag
        if(tag == 'p'): # "p" tag is in a line head
          g_first_word_in_line = 1
          g_bool_tag_first_word_in_line = 1 
          g_bool_tag_end = 0
          g_bool_find_miss = 0
          #g_mis += "g_bool_tag_first_word_in_line     :" + str(g_bool_tag_first_word_in_line) +"g_bool_tag_end"  +str(g_bool_tag_end)  + "tag" + tag +"\n"
        #g_print += "Start tag:" + ''.join(tag) + "\n"
        for attr in attrs:
            if ( "id" in attr): # ex attr = (id, t10) => right td id in the table.
                #g_mis += "attr     :" + str(attr) + "\n"
                if ( "n" in attr[1]): #left td is shown number of each line in the table. filter it.
                    g_bool_find_code = 0
                elif ( "t" in attr[1]): #right td is shown code of each line in the table. reserve it.
                    g_bool_find_code = 1 #find code line 
                    g_line_number = attr[1].replace("t", "") # get line number
            #search function name (query: class.nam and line after "def" word)
            if ( "class" in attr):
                if ("nam" in attr and g_func_name_tag_find == 2):
                    #g_mis += "33333333333"
                    g_func_name_tag_find = 3 #this line is tag of function name 
                if ("key" in attr): # "def" found 
                    #g_mis += "11111111"
                    g_func_name_tag_find = 1 # this line is def tag
                    
            if("stm mis" in attr and g_bool_find_code == 1): # mis means miss this line (red line)
                if(g_first_word_in_line == 1 and g_func_name_pre != g_func_name): # this line is new function, isn't the same as pre function
                    g_mis += "\n"
                    g_mis += g_line_number+ " def " + g_func_name + "\n"
                    g_miss_func += g_func_name + ","
                    g_func_name_pre  = g_func_name
                    g_first_word_in_line = 0
                g_bool_find_miss = 1
                    
            
            g_print += "     attr:" + ''.join(attr) + "\n"
            #print "     attr:", attr

    def handle_endtag(self, tag):
        global g_print, g_mis, g_bool_find_miss, g_bool_tag_first_word_in_line, g_bool_tag_end, g_tag
        #end this miss function 
        if(tag == 'p'):
            if(g_bool_find_miss == 1 and g_bool_tag_first_word_in_line == 1 and g_bool_tag_end == 0):
                g_mis +=  "\n"
            g_bool_tag_first_word_in_line = 0 
            g_bool_tag_end = 1
        #g_print += "End tag  :"+ ''.join(tag) + "\n"
        #print "End tag  :", tag

    def handle_data(self, data):
        global g_print, g_mis, g_bool_find_miss, g_bool_tag_first_word_in_line, g_bool_tag_end, g_tag, g_line_number, g_func_name_tag_find, g_func_name, g_func_name_pre
        if(g_func_name_tag_find == 1 and "def" == data ):
            g_func_name_tag_find = 2 #find "def" string
        if(g_func_name_tag_find == 3 ): # find string of function name
            g_func_name_tag_find = 0 # end                     
            g_mis += "==========="
            g_func_name = ''.join(data) # function name
            g_mis +=  "FFFFF" + g_func_name
            g_func_name_tag_find = 0
        if(g_bool_find_miss == 1 and g_bool_tag_first_word_in_line == 1 and g_bool_tag_end == 0):
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

paths.append('/home/kristen/python_parse/testcase/fake_3')
#paths.append('/home/kristen/python_parse/testcase/htmlcov_controll')
#paths.append('/home/kristen/python_parse/testcase/htmlcov_compute')
#paths.append('/home/kristen/python_parse/testcase/fake_2')
#paths.append('/home/kristen/python_parse/testcase/fake_1')
for index in range(len(paths)):
    path = paths[index]
    print "path     :", path
    '''
    if index == 0 :
        g_mis +=  "\n controll\n"
        g_miss_func += "\n controll \n"
    else: 
         g_mis +=  "\n compute\n"
         g_miss_func += "\n compute \n"
    '''
         
    for filename in os.listdir(path):
        save_file = ""
        '''
        if("cinderclient" in filename):
            save_file = "cinder"
        if("glanceclient" in filename):
            save_file = "glance"
        if("keystoneclient" in filename):
            save_file = "keystonet"
        if("neutronclient" in filename):
            save_file = "neutron"
        '''
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
            with open("./save/nova/"+save_file+".txt", "a") as myfile:
                myfile.write(g_mis.encode('utf8'))
                myfile.close()
            with open("./save/nova/"+save_file+"_func.txt", "a") as myfile:
                myfile.write(g_miss_func.encode('utf8'))
                myfile.close()
            g_mis = ""
            g_miss_func = ""



