from Tkinter import *
from steg import *
import ttk
import steg
import gaussian_pyramid
import tkFileDialog 


class AppWindow(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.initUI()
			
	def initUI(self):
		self.parent.title("lbsSteg")

		note = ttk.Notebook(self.parent)
		self.encodeTab = Frame(note)
		self.decodeTab = Frame(note)
		note.add(self.encodeTab, text = "Encode")
		note.add(self.decodeTab, text = "Decode")
		
		#All UI Elements of encode tab
		self.hostName = StringVar()
		self.guestName = StringVar()
		self.greyscale = StringVar()
		self.placeHolder = StringVar()

		self.hostLabel = ttk.Label(self.encodeTab,text = 'Host Image:').grid(column=0,row=0,sticky=W)
		self.host_entry = ttk.Entry(self.encodeTab, width=50, textvariable=self.hostName)
		self.host_entry.grid(column=1, row=0,columnspan = 2)
		self.hostButton = Button(self.encodeTab,text = "Browse", command = self.onOpenHost).grid(column=3,row=0)
		
		self.guestLabel = ttk.Label(self.encodeTab,text = 'Guest Image:').grid(column=0,row=1,sticky=W)
		self.guest_entry = ttk.Entry(self.encodeTab, width=50, textvariable=self.guestName)
		self.guest_entry.grid(column=1, row=1,columnspan=2)
		self.guestButton = Button(self.encodeTab,text = "Browse", command = self.onOpenGuest).grid(column=3,row=1)

		self.greyscaleCheck = ttk.Checkbutton(self.encodeTab,text= "Greyscale",variable = self.greyscale)
		self.greyscaleCheck.grid(column =0, row = 2,sticky=W)
		self.placeHolderCheck = ttk.Checkbutton(self.encodeTab,text= "Placeholder",variable = self.placeHolder)
		self.placeHolderCheck.grid(column =1, row = 2,sticky=W)

		
		scalevar = IntVar()
		scalevar.set(2)

		self.bitsLabel = ttk.Label(self.encodeTab,text = 'Bits to use:')
		self.bitsLabel.grid(column=0,row=4,sticky=W)	
		self.bitsScale = Scale(self.encodeTab,variable=scalevar,orient=HORIZONTAL, length=300,from_=1, to=8, tickinterval=1,showvalue = 0).grid(column = 1, row = 4, columnspan = 2,sticky=W)
		self.sizeLabel = ttk.Label(self.encodeTab,text = 'Reductions:').grid(column=0,row=5,sticky=W)
		self.reductionScale = Scale(self.encodeTab,orient=HORIZONTAL, length=300,from_=0, to=2 , tickinterval=1,showvalue = 0)
		self.reductionScale.grid(column = 1, row = 5, columnspan = 2,sticky=W)
		self.encodeButton =  Button(self.encodeTab,text = "Encode", command = self.encodeImage).grid(column=3,row=5)
       

		#All UI Elements of decode tab
		self.decodeImageName = StringVar()
		self.outputName = StringVar()
		
		self.decodeImageLabel = ttk.Label(self.decodeTab,text = 'Decode Image:').grid(column=0,row=0)
		self.decodeImageEntry = ttk.Entry(self.decodeTab, width=50, textvariable=self.decodeImageName)
		self.decodeImageEntry.grid(column=1, row=0,columnspan = 2)
		self.decideImageButton = Button(self.decodeTab,text = "Browse", command = self.onOpenOutput).grid(column=3,row=0)

		self.outpuNameLabel = ttk.Label(self.decodeTab,text = 'Output Name:').grid(column=0,row=1)
		self.outputNameEntry = ttk.Entry(self.decodeTab, width=50, textvariable=self.outputName)
		self.outputNameEntry.grid(column=1, row=1,columnspan = 2)

		self.decodeButton =  Button(self.decodeTab,text = "Decode", command = self.decodeImage).grid(column=3,row=3)
		
		note.pack()
		for child in self.encodeTab.winfo_children(): child.grid_configure(padx=5, pady=5)
		for child in self.decodeTab.winfo_children(): child.grid_configure(padx=5, pady=5)

	def onOpenHost(self):
		dlg = tkFileDialog.Open(filetypes = [('jpg', '*.jpg'),('gif', '*.gif'),('png','*.png'), ('All files', '*')])
		fl = dlg.show()

		if fl != '':
			self.hostImage = cv2.imread(fl,3)
			self.hostName.set(fl)

	def onOpenOutput(self):
		dlg = tkFileDialog.Open(filetypes = [('jpg', '*.jpg'),('gif', '*.gif'),('png','*.png'), ('All files', '*')])
		fl = dlg.show()

		if fl != '':
			self.decodeImageName.set(fl)
			self.imageForDecode = cv2.imread(self.decodeImageName.get(),3)

	def onOpenGuest(self):
		dlg = tkFileDialog.Open(filetypes = [('jpg', '*.jpg'),('gif', '*.gif'),('png','*.png'), ('All files', '*')])
		fl = dlg.show()

		if fl != '':
			self.busy()
			self.guestImage = cv2.imread(fl,3)
			self.guestPyramid = gaussian_pyramid.gaussPyramid(self.guestImage,2)
			self.guestName.set(fl)
			self.notbusy()
	
	def encodeImage(self):
		if self.hostName.get() and self.guestName.get():
			options = ''
			if self.greyscale.get() is '1':
				options+='1'
			else:
				options += '0'
			if self.placeHolder.get() is '1':
				options+='1'
			else:
				options += '0'
			cv2.imwrite("encoded.png",encode(self.hostImage,self.guestPyramid[self.reductionScale.get()],options))

	def decodeImage(self):
		if self.outputName.get() and self.decodeImageName.get():
			cv2.imwrite(self.outputName.get(),decode(self.imageForDecode))
	
	
	def busy(self):
		self.parent.config(cursor="watch")
		self.parent.update_idletasks()

	def notbusy(self):
		self.parent.config(cursor="")
		self.parent.update_idletasks()

def main():
  
	root = Tk()
	appWindow = AppWindow(root)
	root.geometry("650x250+300+300")
	root.mainloop()

    

if __name__ == '__main__':
    main()  