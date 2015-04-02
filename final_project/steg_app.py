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
		
		'''
		**********************************************
		All UI Elements of encode tab
		**********************************************
		'''

		#UI Element Vars
		self.hostName = StringVar()
		self.guestName = StringVar()
		self.greyscale = StringVar()
		self.placeHolder = StringVar()
		self.bitScaleValue = IntVar()
		self.bitScaleValue.set(2)     #Set default value to 2 because its my preferred option :^)

		#Row 0 Elements
		self.hostLabel = Label(self.encodeTab,text = 'Host Image:')
		self.hostLabel.grid(column=0,row=0,sticky=W)
		self.host_entry = ttk.Entry(self.encodeTab, width=50, textvariable=self.hostName)
		self.host_entry.grid(column=1, row=0,columnspan = 2)
		self.hostButton = Button(self.encodeTab,text = "Browse", command = self.onOpenHost)
		self.hostButton.grid(column=3,row=0)
		
		#Row 1 Elements
		self.guestLabel = Label(self.encodeTab,text = 'Guest Image:')
		self.guestLabel.grid(column=0,row=1,sticky=W)
		self.guest_entry = ttk.Entry(self.encodeTab, width=50, textvariable=self.guestName)
		self.guest_entry.grid(column=1, row=1,columnspan=2)
		self.guestButton = Button(self.encodeTab,text = "Browse", command = self.onOpenGuest)
		self.guestButton.grid(column=3,row=1)

		#Row 2 Elements
		self.greyscaleCheck = ttk.Checkbutton(self.encodeTab,text= "Greyscale",variable = self.greyscale,command = self.updateSpaceAvailability)
		self.greyscaleCheck.grid(column =0, row = 2,sticky=W)
		self.placeHolderCheck = ttk.Checkbutton(self.encodeTab,text= "Placeholder",variable = self.placeHolder)
		self.placeHolderCheck.grid(column =1, row = 2,sticky=W)

		#Row 4 Elements
		self.bitsLabel = Label(self.encodeTab,text = 'Bits to use:')
		self.bitsLabel.grid(column=0,row=4,sticky=W+N)	
		self.bitsScale = Scale(self.encodeTab,variable=self.bitScaleValue,orient=HORIZONTAL, length=300,from_=1, to=8, tickinterval=1,showvalue = 0,command =self.updateSpaceAvailability)
		self.bitsScale.grid(column = 1, row = 4, columnspan = 1,sticky=W)
		self.bitsRequired = Label(self.encodeTab,text = 'Bits Required:')
		self.bitsRequired.grid(column=2,row=4,sticky=W+N)
		self.guestBits = Label(self.encodeTab,text = '')
		self.guestBits.grid(column=3,row=4,sticky=N)
		
		#Row 5 Elements
		self.sizeLabel = ttk.Label(self.encodeTab,text = 'Reductions:')
		self.sizeLabel.grid(column=0,row=5,sticky=W+N)
		self.reductionScale = Scale(self.encodeTab,orient=HORIZONTAL, length=300,from_=0, to=2 , tickinterval=1,showvalue = 0,command =self.updateSpaceAvailability)
		self.reductionScale.grid(column = 1, row = 5, columnspan = 1,sticky=W)
		self.bitsAvailable = Label(self.encodeTab,text = 'Bits Available:')
		self.bitsAvailable.grid(column=2,row=5,sticky=W+N)
		self.hostBits = Label(self.encodeTab,fg='black',text = '')
		self.hostBits.grid(column=3,row=5,sticky=N)
		
		#Row 6 Elements
		self.encodeButton =  Button(self.encodeTab,text = "Encode", command = self.encodeImage)
		self.encodeButton.grid(column=3,row=6)
       

		'''
		**********************************************
		All UI Elements of decode tab
		**********************************************
		'''

		#UI Element Vars
		self.decodeImageName = StringVar()
		self.outputName = StringVar()
		
		#Row 0 Elements
		self.decodeImageLabel = ttk.Label(self.decodeTab,text = 'Decode Image:')
		self.decodeImageLabel.grid(column=0,row=0)
		self.decodeImageEntry = ttk.Entry(self.decodeTab, width=50, textvariable=self.decodeImageName)
		self.decodeImageEntry.grid(column=1, row=0,columnspan = 2)
		self.decideImageButton = Button(self.decodeTab,text = "Browse", command = self.onOpenEncoded)
		self.decideImageButton.grid(column=3,row=0)

		#Row 1 Elements
		self.outputNameLabel = ttk.Label(self.decodeTab,text = 'Output Name:')
		self.outputNameLabel.grid(column=0,row=1)
		self.outputNameEntry = ttk.Entry(self.decodeTab, width=50, textvariable=self.outputName)
		self.outputNameEntry.grid(column=1, row=1,columnspan = 2)

		#Row 2 Elements
		self.decodeButton =  Button(self.decodeTab,text = "Decode", command = self.decodeImage)
		self.decodeButton.grid(column=3,row=3)



		note.pack()
		#add padding between all elements
		for child in self.encodeTab.winfo_children(): child.grid_configure(padx=5, pady=5)
		for child in self.decodeTab.winfo_children(): child.grid_configure(padx=5, pady=5)

	def onOpenHost(self):
		dlg = tkFileDialog.Open(filetypes = [('jpg', '*.jpg'),('png','*.png'), ('All files', '*')])
		fl = dlg.show()

		if fl != '':
			self.hostImage = cv2.imread(fl,3)
			self.hostName.set(fl)
			self.updateSpaceAvailability()

	def onOpenEncoded(self):
		dlg = tkFileDialog.Open(filetypes = [('png','*.png')])
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
			self.updateSpaceAvailability()
			self.notbusy()
	
	def encodeImage(self):
		
		if self.hostName.get() and self.guestName.get():
			self.busy()
			options = self.createOptionsString()
			cv2.imwrite("encoded.png",encode(self.hostImage,self.guestPyramid[self.reductionScale.get()],options))
			self.notbusy()
	
	def decodeImage(self):
		if self.outputName.get() and self.decodeImageName.get():
			self.busy()
			cv2.imwrite(self.outputName.get(),decode(self.imageForDecode))
			self.notbusy()
	
	def updateSpaceAvailability(self, vars = None):
		if self.hostName.get():
			self.hostBits['text'] = availableBitCount(self.hostImage,int(self.bitScaleValue.get()))
		if self.guestName.get():
			self.guestImage = self.guestPyramid[self.reductionScale.get()]
			self.guestBits['text'] = bitsRequired(self.guestImage,self.createOptionsString())
		if self.hostName.get() and self.guestName.get():
			if float(self.guestBits['text']) > float(self.hostBits['text']):
				self.guestBits['fg'] = "red"
			else:
				self.guestBits['fg'] = "black"

	def createOptionsString(self):
		options = ''
		bPerPix = int(self.bitScaleValue.get())
		if bPerPix ==0:
			bPerPix = 8
		options += (bin(bPerPix)[2:]).zfill(3)
		if self.greyscale.get() is '1':
			options+='1'
		else:
			options += '0'
		if self.placeHolder.get() is '1':
			options+='1'
		else:
			options += '0'
		return options

	def busy(self):
		self.parent.config(cursor="watch")
		self.parent.update_idletasks()

	def notbusy(self):
		self.parent.config(cursor="")
		self.parent.update_idletasks()

def main():
  
	root = Tk()
	appWindow = AppWindow(root)
	root.geometry("650x300+300+300")
	root.mainloop()

    

if __name__ == '__main__':
    main()  