import codecs
import webbrowser
import StringIO
import markdown
import xml.etree.ElementTree as ET
'''
#######################################
Prepared Files: 
	slide_BACKGROUND.xhtml:
	slide_HEAD.xhtml
'''
DOCTYPE='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
#html
html_root = ET.Element("html")

#####head#####
head_root = ET.parse('slide_HEAD.xhtml').getroot()
print "Head_root : "+head_root.tag

# title_ele=head_root.find("title")
# title_ele.text="My title"
# for element in list(head_root):
# 	print element.tag
# bg_html=ET.tostring(head_root, method="html")
# output_bg_file= codecs.open("slide_HEAD.xhtml","a",encoding="utf-8")
# output_bg_file.write(bg_html)

#####body#####
body_root = ET.Element("body")

#####body > background#####
background_root = ET.parse('slide_BACKGROUND.xhtml').getroot()
print "BG_root : "+background_root.tag
body_root.append(background_root)
# for element in list(background_root):
# 	print element.tag
# bg_html=ET.tostring(background_root, method="html")
# output_bg_file= codecs.open("slide_BACKGROUND.xhtml","a",encoding="utf-8")
# output_bg_file.write(bg_html)

#####body > content#####
content_in_file= codecs.open("slide_plain_text_INPUT.txt","r",encoding="utf-8")
content_plain_text=content_in_file.read()
content_html="<body>"+markdown.markdown(content_plain_text)+"</body>"
# content_out_file= codecs.open("slide_content.xhtml","w",encoding="utf-8")
# content_out_file.write(content_html)
# content_out_file.close()
# content_root = ET.parse('slide_content.xhtml').getroot()
content_file=StringIO.StringIO(content_html)
content_root = ET.parse(content_file).getroot()
print "content_root : "+content_root.tag

#####edit div.slide to reset body#####
div_slide_ele=ET.Element("div")
div_slide_ele.set("class","slide cover")
for element in list(content_root):
	if str(element.tag)=="h1":
		body_root.append(div_slide_ele)
		div_slide_ele=ET.Element("div")
		div_slide_ele.set("class","slide")
	div_slide_ele.append(element)

#Adjust cover title
img_ele=ET.Element("img")
img_ele.set("src","http://www.w3.org/Talks/Tools/Slidy2/graphics/keys2.jpg")
img_ele.set("alt","Cover page images (keys)")
img_ele.set("class","cover")
br_ele=ET.Element("br")
br_ele.set("clear","all")
body_root.__getitem__(1).__getitem__(0).tag="h1"
body_root.__getitem__(1).insert(0,br_ele)
body_root.__getitem__(1).insert(0,img_ele)

body_root.append(div_slide_ele)
# body_html=ET.tostring(body_root, method="html")
# output_body_file= codecs.open("slide_body.html","w",encoding="utf-8")
# output_body_file.write(body_html)

#####head > title#####
head_root.__getitem__(1).text=content_root.__getitem__(0).text

#####finalize the whol html#####
html_root.append(head_root)
html_root.append(body_root)

html_html=DOCTYPE+ET.tostring(html_root, method="html")
output_html_file= codecs.open("slide.html","w",encoding="utf-8")
output_html_file.write(html_html)

#####Open the final slide.html by default browser#####
webbrowser.open_new("slide.html")