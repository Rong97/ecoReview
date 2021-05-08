#! /usr/bin/python3
import os
from os import path as ppath
import subprocess
import tkinter as tk
from tkinter import ttk, Frame, Entry, Label, Button, Text


FONT = ('calibre',14,'bold')

class window(tk.Tk):

	texts = []

	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)

		container = ttk.PanedWindow(orient="horizontal")
		container.pack(side = "top",fill = "both",expand = True)
		container.grid_rowconfigure(0,weight = 1)
		container.grid_columnconfigure(0,weight = 1)
		vcmd = (self.register(self.validate),
                '%P')

		fram1 = Frame(self)

		# adding label to search box
		Label(fram1,text = "Context to find: ").pack(side = "left")

		# adding of single line text
		self.edit = Entry(fram1,justify = 'center',font = FONT )

		#positioning of text box
		self.edit.pack(side = "left", fill = "both", expand = 1)

		# setting focus
		self.edit.focus_set()

		# add label
		Label(fram1,text = "Number of match:").pack(side = 'left')

		# adding number entry
		self.num_match = Entry(fram1,justify = 'center' ,width = 4 , 
			font = FONT,validate = 'key', validatecommand = vcmd)
		self.num_match.insert(0,"2")
		self.num_match.pack(side = 'left')


		# adding of search button
		butt = Button(fram1,text = "Find")
		butt.pack(side = "right")
		butt.config(command = self.find)
		fram1.pack(side = "top",fill = 'both' , expand = True)
		self.bind('<Return>', self.callback)

		# text box in root window
		fram2 = Frame(self)

		tk.Grid.columnconfigure(fram2,0,weight = 1 )
		tk.Grid.columnconfigure(fram2,1,weight = 1 )


		fram2_l = Frame(fram2,padx = 10)
		fram2_l.grid(row = 0, column = 0 , sticky = "news")
		fram2_r = Frame(fram2,padx = 10)
		fram2_r.grid(row = 0, column = 1 , sticky = "news")
		self.text1 = Text(fram2_l,font = FONT)
		self.text2 = Text(fram2_r,font = FONT)

		# text input area at index 1 in text window
		self.text1.insert('3.0','''Displying the Definition''')
		self.text1.pack()
		self.text2.insert('3.0','''Displaying the Test Bank''')
		self.text2.pack()
		fram2.pack(side = "bottom")

		## attraching into texts array
		self.texts.append(self.text1)
		self.texts.append(self.text2)



	def find(self):

		contents = [] # array to store content

		# claer "prev_" content and remove 'found' tags
		for text in self.texts:
			text.delete("1.0",tk.END)
			text.tag_remove('found','1.0')
		# self.text1.delete("1.0",tk.END)
		# #remove tag 'found' from index 1 to END 
		# self.text1.tag_remove('found', '1.0')
		#returns to widget currently in focus 
		s = self.edit.get()
		num = int(self.num_match.get())
		
		# fatching content from "cmd"
		content1 = grep_context("*.docx",s,num)
		content2 = grep_context("*.txt",s,num)

		contents.append(content1)
		contents.append(content2)

		for text,content  in zip(self.texts,contents):
			text.insert("1.0",content)
			if s:
				idx = '1.0'
			while 1: 
				#searches for desried string from index 1 
				idx = text.search(s, idx, nocase=1,stopindex=tk.END)
				if not idx: break
				#last index sum of current index and
				#length of text s
				lastidx = '%s+%dc' % (idx, len(s))
				#overwrite 'Found' at idx 
				text.tag_add('found', idx, lastidx)
				idx = lastidx
			#mark located string as red 
			text.tag_config('found', foreground='red')
		self.edit.focus_set()

		
		# # paste content on the Text
		# self.text.insert("1.0",content)
		# if s:
		# 	idx = '1.0'
		# 	while 1: 
		# 	#searches for desried string from index 1 
		# 		idx = self.text.search(s, idx, nocase=1,stopindex=tk.END)
		# 		if not idx: break
		# 		#last index sum of current index and
		# 		#length of text s
		# 		lastidx = '%s+%dc' % (idx, len(s))
		# 		#overwrite 'Found' at idx 
		# 		self.text.tag_add('found', idx, lastidx)
		# 		idx = lastidx
		# 	#mark located string as red 
		# 	self.text.tag_config('found', foreground='red')
		# self.edit.focus_set()

	def callback(self, event):
		self.find()

	def validate(self, P):
	    if str.isdigit(P) or P == "":
	        return True
	    else:
	        return False








def grep_context(filename,context,num_match = 2):
    # p = os.popen('catdoc -w "%s" | grep -m2 "The"' % filename,
    	# stdin=os.PIPE, stdout=os.PIPE, stderr=os.STDOUT, close_fds=True)

    # p1 = subprocess.run(command1 , shell = True)
    # command = 'catdoc %s *.txt | grep -m%d "%s" -A12' % (filename,num_match,context)
    # command = 'cat %s *.txt | grep -m%d "%s" -A12' % (filename,num_match,context)
    if "*.txt" in filename:
    	command = 'cat %s | grep -m%d "%s" -A12' % (filename,num_match,context)
    else:
    	command = 'docx2txt %s | grep -m%d "%s" -A12' % (filename,num_match,context)
    p = subprocess.run(command,
    		shell = True,
    		capture_output= True,
    		text = True)
    if p.returncode != 1:
    	content = p.stdout
    else:
    	# content = os.system(command)
    	content = p.stderr
    return content


if __name__ == '__main__':
    # print(grep_context("*.doc","The"))
    if not ppath.exists("ttb"):
    	os.makedirs("ttb")
    	os.makedirs("sources")

    ##converting all docx formating file into plain txt file
    # for f in os.listdir():
    # 	if f.endswith(".pdf"):
    # 		subprocess.run(['pdftotext',f])

    for file in os.listdir():
    	command = ''
    	if file.startswith('ss_'):
    		fname = file[:-4] + '.txt'
    		command = 'docx2txt "%s" > "sources/%s" '%(file,fname)
    		# subprocess.run(command,capture_output=False, shell = True,text = True)
    	elif file.startswith('ch'):
    		fname = file[:-4] + '.txt'
    		print(file,fname)
    		command = 'antiword "%s" > ttb/"%s" '%(file,fname)
    		print(command)
    	subprocess.run(command,capture_output=False, shell = True,text = True)


    # root = window()
    # root.resizable(True, True) 
    # root.mainloop()

    ## finishing, removing all those created txt files.
    for dir in ['ttb','sources']:
    	for f in os.listdir(dir):
    		if f.endswith('.txt'):
    			os.remove(dir+'/' + f)


