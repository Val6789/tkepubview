#!/usr/bin/python3
import tkinter, zipfile, random, glob, sys, tkinterhtml, os

if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
	book = sys.argv[1]
else:
	print("Usage: tkepubview <File>")
	sys.exit()

class tkepubview(tkinter.Tk):
	def __init__(self,parent):
		# Extract the ePub file into a temp dir
		tempdir = "/tmp/tkepubview" + str(random.randint(0,10000))
		with zipfile.ZipFile(book, "r") as z: z.extractall(tempdir)

		# Get the pages (xhtml and html files) into an array
		self.pages = sorted(glob.glob(tempdir + "/**/*.*html", recursive=True))

		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()

		self.lb = tkinter.Listbox(self)
		self.lb.grid(column=0, row=0, sticky="NEWS")
		self.lb.bind("<<ListboxSelect>>", self.OnSelect)

		self.frame = tkinterhtml.HtmlFrame(self, horizontal_scrollbar="auto")
		self.frame.grid(column=1, row=0, sticky="NEWS")
		
		self.grid_columnconfigure(1,weight=1)
		self.grid_rowconfigure(0,weight=1)
			
		for i, p in enumerate(self.pages):
			self.lb.insert(tkinter.END, i)
		
		self.SetPage(0)
	
	def OnSelect(self, evt):
		self.SetPage(self.lb.curselection()[0])
		
	def SetPage(self, n):
		ff = open(self.pages[n])
		self.frame.set_content(ff.read())

if __name__ == "__main__":
	app = tkepubview(None)
	app.title("tkepubview - " + book)
	app.mainloop()
