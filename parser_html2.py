from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

g_print = ""
class MyHTMLParser(HTMLParser):
    
    '''
    def __init__(self):
        global g_print
        # initialize the base class
        HTMLParser.__init__(self)
    '''
        
    def handle_starttag(self, tag, attrs):
        global g_print
        print "Start tag:", tag
        g_print += "Start tag:" + ''.join(tag) + "\n"
        for attr in attrs:
            g_print += "     attr:" + ''.join(attr) + "\n"
            print "     attr:", attr

    def handle_endtag(self, tag):
        global g_print
        g_print += "End tag  :"+ ''.join(tag) + "\n"
        print "End tag  :", tag

    def handle_data(self, data):
        global g_print
        g_print += "Data     :" + ''.join(data) + "\n"
        print "Data     :", data

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

f = open("_usr_lib_python2_7_dist-packages_cinderclient_client_py.html", "r")
parser.feed(f.read())

f1=open('./testfile', 'w+')
f1.write(g_print.encode('utf8'))
f1.close()