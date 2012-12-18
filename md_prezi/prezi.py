import codecs
import webbrowser
import StringIO
import sys
import markdown
import xml.etree.ElementTree as ET
'''
############# Prezi Class #############
Creat a web-based presentation file in a specific pattern (slidy, scroll, etc)
from a plain text with contents wrote in Modified Markdown Syntax

'''
class Prezi(object):

	DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'
	html_root = None
	head_root = None
	root_root = None
	background_root = None
	content_root = None
	input_file ="slide_plain_text_INPUT.txt"

	def __init__(self, file_name, prezi_pattern, *args):
		# Convey the palin text into html 
		# and create various roots, especially the self.hmtl_root, according to prezi_pattern
		# Arguments:
		# 	  file_name : string 'name.txt', the name of a plain text with contents wrote in Modified Markdown Syntax
		# prezi_pattern	: [slidy, scroll, html5, etc...]
		# 		  *args : decided by prezi_pattern; 
		#				  slidy:[deep_level [1,2], style_css, other_background]

		if not (file_name == None or file_name.strip() == ""):
			self.input_file = file_name

		# ----- html -----
		self.html_root = ET.Element("html")

		
		# ----- head > title, body > background + content( > div.slide) -----
		# Create and inilize roots
		if prezi_pattern == 'slidy':
			deep_level = args[0]
			style_css = ''#args[1]
			other_background = ''#args[3]
			self.init_slidy(deep_level, style_css, other_background)
		
		elif prezi_pattern == "scroll" :
			self.init_scroll()
		
		elif prezi_pattern == "html5" :
			self.init_html5()
		
		# elif prezi_pattern == "" :
		else :
			print "! Faild to match prezi_pattern !"
			sys.exit()


		#####finalize the whol html#####
		self.html_root.append(self.head_root)
		self.html_root.append(self.body_root)



	def init_slidy(self, deep_level, style_css, other_background):
		# [Slidy pattern] 

		# ----- head -----
		self.head_root = ET.parse('slide_HEAD.xhtml').getroot()
		print "self.Head_root : " + self.head_root.tag

		# ----- body -----
		self.body_root = ET.Element("body")

		# ----- body > background -----
		self.background_root = ET.parse('slide_BACKGROUND.xhtml').getroot()
		print "self.BG_root : " + self.background_root.tag
		self.body_root.append(self.background_root)

		# ----- body > content -----
		content_in_file= codecs.open(self.input_file,"r", encoding = "utf-8")
		content_plain_text=content_in_file.read()
		content_html="<body>"+markdown.markdown(content_plain_text)+"</body>"

		content_file=StringIO.StringIO(content_html)
		self.content_root = ET.parse(content_file).getroot()
		print "self.content_root : "+self.content_root.tag

		# ----- edit div.slide to reset body -----
		div_slide_ele=ET.Element("div")
		div_slide_ele.set("class","slide cover")
		if deep_level == 1:
			for element in list(self.content_root):
				if str(element.tag)=="h1":
					self.body_root.append(div_slide_ele)
					div_slide_ele=ET.Element("div")
					div_slide_ele.set("class","slide")
				div_slide_ele.append(element)
		elif deep_level == 2:
			print "! A little Deep, Coming soon !"
			sys.exit()
		else :
			print "! Too Deep, No Implementation !"
			sys.exit()

		# ----- head > title ----
		img_ele=ET.Element("img")
		img_ele.set("src","http://www.w3.org/Talks/Tools/Slidy2/graphics/keys2.jpg")
		img_ele.set("alt","Cover page images (keys)")
		img_ele.set("class","cover")
		br_ele=ET.Element("br")
		br_ele.set("clear","all")
		self.body_root.__getitem__(1).__getitem__(0).tag="h1"
		self.body_root.__getitem__(1).insert(0,br_ele)
		self.body_root.__getitem__(1).insert(0,img_ele)
		self.body_root.append(div_slide_ele)
		self.head_root.__getitem__(1).text=self.content_root.__getitem__(0).text
		


	def init_scroll(self):
		# [Slidy pattern]
		print "! Scroll Pattern Coming soon !"
		sys.exit()



	def init_html5(self):
		# [Slidy pattern]
		print "! HTML5 Pattern Coming soon !"
		sys.exit()


	
	def set_style(self, style_css):
		# Insert Rich Format to the presentation file by .css
		#
		pass



	def finalize(self ):
		# Create the html file used for presentation from self.html_root
		# and Open it by default browser

		#Create File
		html_html=self.DOCTYPE+ET.tostring(self.html_root, method="html") 
		output_html_file= codecs.open("index.html","w",encoding="utf-8")
		output_html_file.write(html_html)

		#Open
		webbrowser.open_new("index.html")


###### ----- text code ----- ######
# "slide_plain_text_INPUT.txt"
# file_name, prezi_pattern, *args
Prezi("", 'slidy',1).finalize()