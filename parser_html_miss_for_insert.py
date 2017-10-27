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
g_now_tag = ""
g_now_id = ""
g_now_class = ""
g_now_function = ""
g_now_line_number = 0
g_pre_id = ""
g_num_tab_space_before_data = 0
g_num_tab_space_before_def = 0
g_num_insert_lines = 0
g_num_def_start = 0
g_num_def_end = 0
g_bool_find_def = False
g_bool_find_function = False
g_bool_find_t_id = False
g_bool_find_miss_statement = False
g_bool_find_source_file_path = False
g_bool_find_import = False
g_bool_find_end = False
g_bool_problem_file = False
g_chek_two_line_end = False
g_write_text = ""
g_touch_path = "/home/ubuntu/kentzu/temp1020/"
#stack, FIFO
g_list_def_start_miss_end = [] #input def start line, first miss line and end line number ex:[(4,6,10),(15,19,24)..]
g_list_def_name = [] #input function name. ex:[ funcA, funcB..]
g_list_def_return_exist = [] # input def return exist or not ex:[True, False, ...]
g_list_def_miss_exist = [] #input def miss exist or not
g_list_def_space = [] 
g_list_pointer = -1
g_miss_count = 0

mis_num =""

class MyHTMLParser(HTMLParser):
    
    
    def check_miss(self, miss_list):
        lens = len(miss_list)
        if (lens != 0):
            if (miss_list[-1]):
                return True
        return False
        
    def check_return(self, return_list):
        lens = len(return_list)
        if (lens != 0):
            if (return_list[-1]):
                return True
        return False
    
    def init_stack(self):
        global g_list_def_miss_exist, g_list_def_name,g_list_def_start_miss_end,g_list_def_return_exist,g_list_pointer
        g_list_def_name.append("")
        g_list_def_start_miss_end.append([0,0,0])
        g_list_def_return_exist.append(False)
        g_list_def_miss_exist.append(False)
        g_list_def_space.append(0)
        
    def pop_all(self):
        global g_list_def_miss_exist, g_list_def_name,g_list_def_start_miss_end,g_list_def_return_exist,g_list_pointer
        if(len(g_list_def_name) == g_list_pointer + 1 and len(g_list_def_name) > 0):
            g_list_def_name.pop()
        if(len(g_list_def_start_miss_end) == g_list_pointer + 1 and len(g_list_def_start_miss_end) > 0):
            g_list_def_start_miss_end.pop()
        if(len(g_list_def_return_exist) == g_list_pointer + 1 and len(g_list_def_return_exist) > 0):
            g_list_def_return_exist.pop()
        if(len(g_list_def_miss_exist) == g_list_pointer + 1 and len(g_list_def_miss_exist) > 0):
            g_list_def_miss_exist.pop()
        g_list_pointer -= 1
    
    def final_write(self):
        global g_list_def_miss_exist, g_list_def_name,g_list_def_start_miss_end,g_list_def_return_exist,g_list_pointer,g_miss_count,g_list_def_space,g_num_insert_lines,g_write_text
        file_last_line = 0
        if g_miss_count == 0 :
            return False
        else:
            if(g_num_insert_lines == 0): #some api does not import anything, and we just write a filepath in reday insert text file
                g_write_text  += str(0)+ "::"+str(0)+"::import os\n" 
                g_num_insert_lines += 1
            index = 0
            for miss in g_list_def_miss_exist:
                if (miss):
                    if(g_list_def_return_exist[index]):
                        start_line = g_num_insert_lines + g_list_def_start_miss_end[index][1] -1
                        end_line =  g_num_insert_lines + g_list_def_start_miss_end[index][2]
                        space = g_list_def_space[index] + 4
                        if(end_line ==650):
                            print "==3=="
                    else:
                        start_line = g_num_insert_lines + g_list_def_start_miss_end[index][1] -1
                        if ( index + 1 == len(g_list_def_return_exist)): #last func
                            file_last_line =  g_num_insert_lines + g_now_line_number + 1
                            end_line = file_last_line + 1
                            if(end_line ==650):
                                print "==2=="
                                print g_now_line_number
                        else:
                            last = index + 1
                            end_line =  (g_list_def_start_miss_end[last][0] - 1) 
                            end_line += g_num_insert_lines
                            if(end_line ==650):
                                print "==1=="
                        space = g_list_def_space[index] + 4
                    g_num_insert_lines += 2
                    g_write_text  += str(start_line)+ "::"+str(space)+"::os.system(\"touch "+ g_touch_path+ file_title + "_"+g_list_def_name[index]+" \")\n" 
                    if (file_last_line >0):
                        g_write_text  += str(file_last_line)+ "::"+str(space)+":: \n" 
                    g_write_text  += str(end_line)+ "::"+str(space)+"::os.system(\"touch "+ g_touch_path+ file_title + "_"+g_list_def_name[index]+"_end \")\n" 
                index  += 1
            return True
                  
        
    
    def reset_global(self):
        global g_print,g_now_tag,g_now_id,g_now_class,g_now_function,g_num_tab_space_before_def,g_num_insert_lines,g_num_def_start,g_num_def_end,g_bool_find_def,g_bool_find_function,g_bool_find_t_id,g_bool_find_miss_statement,g_num_tab_space_before_data,g_now_line_number,g_pre_id,g_chek_two_line_end,g_bool_find_import,g_write_text,g_bool_find_source_file_path,g_bool_find_end,g_touch_path,mis_num,g_list_def_miss_exist, g_list_def_name,g_list_def_start_miss_end,g_list_def_return_exist,g_list_pointer,g_miss_count
        g_write_text = ""
        g_bool_find_import = False
        g_bool_problem_file = False
        g_print = "" # print strings
        g_now_tag = ""
        g_now_id = ""
        g_now_class = ""
        g_now_function = ""
        g_now_line_number = 0
        g_pre_id = ""
        g_num_tab_space_before_data = 0
        g_num_tab_space_before_def = 0
        g_num_insert_lines = 0
        g_num_def_start = 0
        g_num_def_end = 0
        g_bool_find_def = False
        g_bool_find_function = False
        g_bool_find_t_id = False
        g_bool_find_miss_statement = False
        g_bool_find_source_file_path = False
        g_bool_find_import = False
        g_bool_find_end = False
        g_bool_problem_file = False
        g_chek_two_line_end = False
        g_write_text = ""
        #stack, FIFO
        g_list_def_start_miss_end = [] #input def start line and end line number ex:[(4,10),(15,24)..]
        g_list_def_name = [] #input function name. ex:[ funcA, funcB..]
        g_list_def_return_exist = [] # input def return exist or not ex:[True, False, ...]
        g_list_def_miss_exist = [] #input def miss exist or not
        g_list_pointer = -1
        g_miss_count = 0
        
    def handle_starttag(self, tag, attrs):
        global g_print,g_now_tag,g_now_id,g_now_class,g_now_function,g_num_tab_space_before_def,g_num_insert_lines,g_bool_find_source_file_path
        
        #print "Start tag:", tag
        g_now_tag = tag

        if tag == "b":
            g_bool_find_source_file_path = True
            print "tag ==b=",tag
        for attr in attrs:
            if ( "id" in attr): # ex attr = (id, t10) => right td id in the table.
                g_now_id = attr
            
            if ( "class" in attr):
                g_now_class = attr


    def handle_endtag(self, tag):
        # find html end tag in a line ex: </p>
        global g_print
        #print "End tag  :", tag

    def handle_data(self, data):
        # find html data in a line. ex: <>if a is not b:</>
        global g_print,g_now_tag,g_now_id,g_now_class,g_now_function,g_num_tab_space_before_def,g_num_insert_lines,g_num_def_start,g_num_def_end,g_bool_find_def,g_bool_find_function,g_bool_find_t_id,g_bool_find_miss_statement,g_num_tab_space_before_data,g_now_line_number,g_pre_id,g_chek_two_line_end,g_bool_find_import,g_write_text,g_bool_find_source_file_path,g_bool_find_end,g_touch_path,mis_num,g_list_def_miss_exist, g_list_def_name,g_list_def_start_miss_end,g_list_def_return_exist,g_list_pointer,g_list_def_space,g_miss_count
        
        
        # write: file path (api) 
        if (g_bool_find_source_file_path):
            g_write_text  += "filepath::"+ data +" \n" 
            g_bool_find_source_file_path = False

        # start search in id=tnumber    
        if ( "id" in g_now_id and  "t" in g_now_id[1] and (g_now_id[1].replace("t", "")).isdigit() ):
            g_bool_find_t_id = True
            
            if( g_pre_id != g_now_id):
                # tab space number of data
                space = data.split(" ")
                g_num_tab_space_before_data = len(space) - 1
               
                
                # get line number
                line_number = g_now_id[1].replace("t", "") # get line number
                g_pre_id = g_now_id
                if(line_number.isdigit()):
                    g_now_line_number = int(line_number)
                    
                    #print g_now_line_number
                
                # write: import os
                if(not g_bool_find_import and "key" in g_now_class and (data == "from" or data == "import")):
                    g_write_text  += str(g_now_line_number) + "::0::import os\n" 
                    g_num_insert_lines += 1
                    g_bool_find_import = True
                
        if (g_bool_find_t_id): # start to read line at id=tnumber
        
            #1. find def   
            if data == "def" and g_num_tab_space_before_data <= 4 :
                
                #reset g_bool_find_miss_statement
                g_bool_find_miss_statement = False
                #pointer + 1
                g_list_pointer += 1
                print "============##" , g_list_pointer
                #initail
                self.init_stack()
                #que -> (start, end=0)
                g_list_def_start_miss_end[g_list_pointer] = [g_now_line_number,0, 0] #end number inital = 0
                print 'g_list_def_start_miss_end', g_list_def_start_miss_end
                print  '\n'
                g_bool_find_def = True
                g_list_def_space[g_list_pointer] = g_num_tab_space_before_data
            
             
           #2. get function name
            elif (g_bool_find_def and  "nam"  in g_now_class ):
                g_bool_find_function = True
                #g_now_function = data
                '''
                if(g_list_pointer > 0):
                    #previous function's miss is exist 
                    if(self.check_miss(g_list_def_miss_exist)):
                        #previous function's return is not exist
                        print "not miss"
                        if(not self.check_return(g_list_def_return_exist)):
                            #previous function's end line didn't write
                            print "not return"
                            if(g_list_def_start_miss_end[-2][1] == 0):
                                #que pre -> (start, end = now_func -1)
                                print "$$", g_list_def_start_miss_end[-1][0] -1
                                g_list_def_start_miss_end[-2][1] = (g_list_def_start_miss_end[-1][0] -1)
                '''
                    #else:
                        # previous function is not miss than pop all
                        #print "pop all"
                        #self.pop_all()
                    
                                
                g_list_def_name[g_list_pointer]= data
                print "#######################################"
                print g_list_def_name[g_list_pointer]
                g_bool_find_def = False
                print "g_list_pointer", g_list_pointer
                print  '\n'
                print "g_list_def_miss_exist", g_list_def_miss_exist
                print  '\n'
                print "g_list_def_name", g_list_def_name
                print  '\n'
            
            #?. find class or any other space < 4, than fake return = 0      
            elif g_list_pointer >= 0 and g_num_tab_space_before_data <= g_list_def_space[g_list_pointer] and g_now_class[1] != "pln" and g_now_class[1] !="strut":
                
                if(self.check_miss(g_list_def_miss_exist)):
                    if(not self.check_return(g_list_def_return_exist)):
                        print "?????????????", g_num_tab_space_before_data, g_now_line_number, g_now_class
                        print data
                        print g_list_def_start_miss_end
                        g_list_def_return_exist[g_list_pointer] = True
                        g_list_def_start_miss_end[-1][2] = g_now_line_number 
                    
                    
            #4. find return   
            elif data == "return" and g_num_tab_space_before_data <= (g_list_def_space[g_list_pointer] + 4):
                #previous function's miss is exist 
                if(self.check_miss(g_list_def_miss_exist)):
                    g_list_def_return_exist[g_list_pointer] = True
                    print "wwwwwwwwwwwwwwwwww"
                    g_list_def_start_miss_end[-1][2] = g_now_line_number
                #else:
                    # previous function is not miss than pop all
                    #self.pop_all()
                
                #g_num_def_end = g_now_line_number
                #g_bool_find_end = True
                
          
            if(g_bool_find_function and g_list_def_space[g_list_pointer]+4 == g_num_tab_space_before_data ):
               g_list_def_start_miss_end[-1][1] = g_now_line_number
               g_bool_find_function = False
                
            #3. check if miss line in this function 
            if ("stm mis" in g_now_class and not g_bool_find_miss_statement):
                print "*==xxxxxxxxxxxxx", str(g_now_line_number)
                print g_list_pointer
                print g_write_text
                if(g_list_pointer >= 0 and len(g_list_def_start_miss_end) == g_list_pointer+1):
                    #g_list_def_start_miss_end[-1][1] = g_now_line_number
                    g_bool_find_miss_statement = True
                    g_miss_count += 1
                    g_list_def_miss_exist[g_list_pointer] = True
                
            g_bool_find_t_id = False
      
        
        
            
            
                
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

paths = []


#paths.append('/home/kristen/python_parse/testcase/controller_test')
paths.append('/home/kristen/python_parse/testcase/controller1024')

#paths.append('/home/kristen/python_parse/testcase/fake_3')
for index in range(len(paths)):
    path = paths[index]
    print "path     :", path
    #save_path = "/home/kristen/python_parse/save/insert_list1024/"
    save_path = "/home/kristen/python_parse/save/insert_list1025/"
    #save_path = "/home/kristen/python_parse/save/insert_list_test/"
    '''
    if index == 0 :
        g_collect_mis_content +=  "\n controll\n"
        g_collect_miss_func += "\n controll \n"
    else: 
         g_collect_mis_content +=  "\n compute\n"
         g_collect_miss_func += "\n compute \n"
    '''
         
    for filename in os.listdir(path):
        if("nova" in filename):
            print "=========2"
            parser.reset_global()
            
            file_title = filename.replace( "_usr_lib_python2_7_dist-packages_", "")
            file_title =  file_title.replace("_py.html", "")
            # read file
            f = open(path +"/" +filename, "r")
            parser.feed(f.read())
            print "g_list_def_start_miss_end",g_list_def_start_miss_end 
            print '\n'
            print "g_list_def_name", g_list_def_name 
            print '\n'
            print "g_list_def_return_exist", g_list_def_return_exist 
            print '\n'
            print "g_list_def_miss_exist", g_list_def_miss_exist 
            print '\n'
            print "g_list_pointer",g_list_pointer 
            print '\n'
            print "final" 
            print '\n'
            gen_write =  parser.final_write()
            print g_write_text
            print '\n'
            save_file = save_path+ file_title
            f.close()
            count_lines = len(g_write_text.split("::")) #if text contents "file name" + "import os", then doesn't wirte
            # write insert string in the file
            print "=========3"
            if(gen_write):
                print "=========4"
                with open(save_file, "w") as myfile:
                    myfile.write(g_write_text.encode('utf8'))
                    myfile.close()
                 
                    
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



