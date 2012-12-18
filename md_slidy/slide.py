__author__ = 'Xiaoyang'
"""
Convert the output of Python_markdown to strict HTML with slidy
=============================================
1. Insert the head & body with slidy.css/js
2. Insert div.slide to related H1 chucks
"""
import markdown
import codecs
import xml.etree.ElementTree as ET

class slide(object):

    content=""
    title=None
    html=None
    head=None
    body=None
    tree=None

    def __init__(self,file_name):
        input_file=codecs.open(file_name,"r",encoding="utf-8")
        text=input_file.read()
        self.content="<body>"+markdown.markdown(text)+"</body>"
        output_file=codecs.open("output.xhtml","w",encoding="utf-8",errors="xmlcharrefreplace")
        output_file.write(self.content)
        output_file.close()


        self.html=ET.Element("html")
        self.html.set("lang","en")

        #head
        self.head=ET.Element("head")
        self.title=ET.Element("title")
        self.title.text=file_name
        self.edit_head()
        self.html.append(self.head)

        #body
        self.body=ET.parse("output.xhtml").getroot()        
        self.edit_div_slide()
        self.html.append(self.body)

        # print ET.tostring(self.html,method="html")
        # print self.head.text

        # output the final prezi file
        prezi_file=codecs.open("slidy.html","a",encoding="utf-8",errors="xmlcharrefreplace")
        temp=ET.tostring(self.body,method="html")
        prezi_file.write(temp)
        prezi_file.close

        return

    def edit_div_slide(self):
        old_body=self.body
        self.body=ET.Element("body")#Reset the body for new stracture
        new_div=ET.Element("div")
        new_div.set("class","slide")
        elements=list(old_body)
        
        for element in list(old_body):
            if element.tag == "h1":
                self.body.append(new_div)
                new_div=ET.Element("div")
                new_div.set("class","slide")
            new_div.append(element)

        self.body.append(new_div)

        list(self.body)[0].set("class","slide,cover")

        self.content=ET.tostring(self.body,method="html")
        
        return True

    def insert_style(self,href):
        style_ele=ET.SubElement(self.head, "link")
        style_ele.set("rel","stylesheet")
        style_ele.set("href",href) 
        style_ele.set("type","text/css")
        return True

    def insert_css(self,href):
        css_ele=ET.SubElement(self.head, "link")
        css_ele.set("rel","stylesheet")
        css_ele.set("href",href) 
        css_ele.set("type","text/css")
        return True
        
    def insert_js(self,src,*args):
        pass

    def edit_head(self):
        input_head=codecs.open("head_content.txt","r",encoding="utf-8")
        self.head.text=ET.tostring(self.title,method="html")+input_head.read()
        input_head.close()
                
        # ET.SubElement(self.head, "title").text=self.title#<title> </title>
        
        # md_ele=ET.SubElement(self.head, "meta")
        # md_ele.set("name" , "generator")
        # md_ele.set("content", "HTML Tidy for Linux/x86 (vers 1st November 2003), see www.w3.org")
        
        # md_ele=ET.SubElement(self.head, "meta")
        # md_ele.set("name","duration")
        # md_ele.set("content","5") 
        
        # md_ele=ET.SubElement(self.head, "meta")
        # md_ele.set("name","font-size-adjustment")
        # md_ele.set("content","-2")
        
        # hrefs=["http://www.w3.org/Talks/Tools/Slidy2/styles/w3c-blue.css",
        #        "http://www.w3.org/Talks/Tools/Slidy2/styles/slidy.css"]
        # # for href in hrefs:
        # #     self.insert_css(href)
        # self.insert_style(hrefs[0])
        # self.insert_css(hrefs[1])
        
        # srcs=["http://www.w3.org/Talks/Tools/Slidy2/scripts/slidy.js",
        #      "http://code.jquery.com/jquery-latest.js" ]
        # # for src in srcs:
        # #     self.insert_js(src)
        # script_ele=ET.SubElement(self.head, "script")
        # script_ele.set( "type","text/javascript")
        # script_ele.set("src",srcs[0])
        # script_ele.set("charset","utf-8")
        
        # script_ele=ET.SubElement(self.head, "script")
        # script_ele.set( "type","text/javascript")
        # script_ele.set("src",srcs[1] )
        return True

    def __repr__(self):
        return self.content



html_file=slide("input.txt")
# print html_file