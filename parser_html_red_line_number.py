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
#global variable
g_print = "" # print strings
g_collect_mis_content = "" # miss test content
g_collect_miss_func = "" # miss test function
g_bool_find_miss_line = 0 # if find a miss line
g_bool_find_p_tag = 0 # a line head start by <p> tag , ex: <p><span1 <span2 3..</p>
g_bool_tag_end = 0 # a line end
g_bool_collected_function_name = 0 # ex: if auth(content):, if is a first word
g_bool_find_code = 0 # find code line (the table has two tds, one is number, another is code)
g_bool_find_func_name_tag = 0 # find class.key , ex: <span class="key">def</span>
g_line_number = 0 # get line number
g_func_name = "" # strings of function name
g_func_name_pre = "" #strings of previous function name

g_bool_find_miss_function = 0
g_bool_found_first_import_line_number = 0
g_number_func_tab_space = 0
g_number_insert_line_now = 0
g_bool_ready_to_put_code_string = 0 
g_bool_skip_put_code = 0
g_collect_insert_text = ""
g_collect_temp = "" # for skiping exist "os.system()" 

class MyHTMLParser(HTMLParser):
    
    '''
    def __init__(self):
        global g_print
        # initialize the base class
        HTMLParser.__init__(self)
    '''
        
    def handle_starttag(self, tag, attrs):
        # find html tag in a line ex: <p id="t34"
        global g_print, g_collect_mis_content, g_bool_find_miss_line, g_bool_find_p_tag, g_bool_tag_end, g_bool_collected_function_name, g_line_number, g_bool_find_code, g_func_name, g_bool_find_func_name_tag, g_func_name_pre, g_collect_miss_func, g_bool_find_miss_function
        print "Start tag:", tag
        if(tag == 'p'): # "p" tag is in a line head
            g_bool_collected_function_name = 0
            g_bool_find_p_tag = 1 
            g_bool_tag_end = 0
            g_bool_find_miss_line = 0
            #g_collect_mis_content += "g_bool_find_p_tag     :" + str(g_bool_find_p_tag) +"g_bool_tag_end"  +str(g_bool_tag_end)  + "tag" + tag +"\n"
          #g_print += "Start tag:" + ''.join(tag) + "\n"
        for attr in attrs:
            if ( "id" in attr): # ex attr = (id, t10) => right td id in the table.
                #g_collect_mis_content += "attr     :" + str(attr) + "\n"
                if ( "n" in attr[1]): #left td is shown number of each line in the table. filter it.
                    g_bool_find_code = 0
                elif ( "t" in attr[1]): #right td is shown code of each line in the table. reserve it.
                    g_bool_find_code = 1 #find code line 
                    g_line_number = attr[1].replace("t", "") # get line number
            #search function name (query: class.nam and line after "def" word)
            if ( "class" in attr):
                if ("nam" in attr and g_bool_find_func_name_tag == 2):
                    #g_collect_mis_content += "33333333333"
                    g_bool_find_func_name_tag = 3 #this line is tag of function name 
                if ("key" in attr): # "def" found 
                    #g_collect_mis_content += "11111111"
                    g_bool_find_func_name_tag = 1 # this line is def tag
                    
            if("stm mis" in attr and g_bool_find_code == 1): # mis means miss this line (red line)
                if(g_bool_collected_function_name == 0 and g_func_name_pre != g_func_name): # this line is new function, isn't the same as pre function
                    
                    g_collect_mis_content += "\n"
                    g_collect_mis_content += g_line_number+ " def " + g_func_name + "\n"
                    # if this statement has miss than put function name in the collection
                    g_collect_miss_func += g_func_name + ","
                    g_func_name_pre  = g_func_name 
                    g_bool_collected_function_name = 1
                    g_bool_find_miss_function = 1
                g_bool_find_miss_line = 1
                    
            
            g_print += "     attr:" + ''.join(attr) + "\n"
            print "     attr:", attr

    def handle_endtag(self, tag):
        # find html end tag in a line ex: </p>
        global g_print, g_collect_mis_content, g_bool_find_miss_line, g_bool_find_p_tag, g_bool_tag_end, g_tag
        #end this miss function 
        if(tag == 'p'):
            if(g_bool_find_miss_line == 1 and g_bool_find_p_tag == 1 and g_bool_tag_end == 0):
                g_collect_mis_content +=  "\n"
            g_bool_find_p_tag = 0 
            g_bool_tag_end = 1
        #g_print += "End tag  :"+ ''.join(tag) + "\n"
        print "End tag  :", tag

    def handle_data(self, data):
        # find html data in a line. ex: <>if a is not b:</>
        global g_print, g_collect_mis_content, g_bool_find_miss_line, g_bool_find_p_tag, g_bool_tag_end, g_tag, g_line_number, g_bool_find_func_name_tag, g_func_name, g_func_name_pre, g_bool_found_first_import_line_number,g_number_insert_line_now ,g_bool_ready_to_put_code_string ,g_bool_skip_put_code,g_collect_insert_text ,g_collect_temp,g_number_func_tab_space,g_bool_find_miss_function
        if (g_bool_found_first_import_line_number == 0 and g_bool_find_func_name_tag == 1 
            and (data == "from" or data == "import")):
            g_bool_found_first_import_line_number = 1
            g_collect_insert_text += g_line_number + "::import os\n"
            g_number_insert_line_now += 1
        if(g_bool_ready_to_put_code_string == 1 and g_bool_skip_put_code == 0): 
            #check os.sysyem exist or not in the second line of function
            if ("os.system" not in data and g_bool_find_miss_function == 1):  
                g_collect_insert_text += g_collect_temp
                g_bool_find_miss_function = 0
            else:
                g_bool_skip_put_code = 1 # os.system is exist
            g_bool_ready_to_put_code_string = 0
            
            
            
        if(g_bool_find_func_name_tag == 1 and "def" == data ):
            g_bool_find_func_name_tag = 2 #find "def" string
        if(g_bool_find_func_name_tag == 3 ): # found the string of function name
            g_bool_skip_put_code = 0
            g_bool_find_func_name_tag = 0 # end   
            g_func_name = ''.join(data) # function name
            g_collect_temp = g_line_number + "::os.system(\"touch /home/ubuntu/kentzu/"+file_title+g_func_name+"\")\n"
            g_bool_ready_to_put_code_string = 1
            
      
            
           
            """                  
            g_collect_mis_content += "==========="
            g_func_name = ''.join(data) # function name
            g_collect_mis_content +=  "FFFFF" + g_func_name
            """
            g_bool_find_func_name_tag = 0
        if(g_bool_find_miss_line == 1 and g_bool_find_p_tag == 1 and g_bool_tag_end == 0):
          if(''.join(data) != ""):
              g_collect_mis_content +=  ''.join(data) 
        g_print += "Data     :" + ''.join(data) + ", "
        space = data.split(" ")
        line_space = len(space) - 1
        if g_bool_find_p_tag == 1:
            print "Data space:", line_space
        print "Data     :", data+"-----"

    def handle_comment(self, data):
        global g_print
        g_print += "Comment  :" + ''.join(data) + "\n"
        print "Comment  :", data

    def handle_entityref(self, name):
        global g_print
        c = unichr(name2codepoint[name])
        g_print += "Named ent:" + ''.join(c) + "\n"
        print "Named ent:", c

    def handle_charref(self, name):
        global g_print
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        g_print += "Num ent  :" + ''.join(c) + "\n"
        print "Num ent  :", c

    def handle_decl(self, data):
        global g_print
        g_print += "Decl     :" + ''.join(data) + "\n"
        print "Decl     :", data

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
        g_collect_mis_content +=  "\n controll\n"
        g_collect_miss_func += "\n controll \n"
    else: 
         g_collect_mis_content +=  "\n compute\n"
         g_collect_miss_func += "\n compute \n"
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
            g_collect_mis_content += file_title + "\n"
            #g_collect_miss_func += save_file  + "\n"
            f = open(path +"/" +filename, "r")
            parser.feed(f.read())
            f.close()
            """
            with open("./save/nova/"+save_file+".txt", "a") as myfile:
                myfile.write(g_collect_mis_content.encode('utf8'))
                myfile.close()
            """
            """
            with open("./save/nova/"+save_file+"_func.txt", "a") as myfile:
                myfile.write(g_collect_miss_func.encode('utf8'))
                myfile.close()
            g_collect_mis_content = ""
            g_collect_miss_func = ""
            """



