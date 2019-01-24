from lxml import html
from tkinter import *
import requests
import random


class Gui():
	def __init__(self, master):
		self.master = master
		master.geometry("300x500")
		master.title("Name Generator")

		self.label = Label(master, text='Generator a name from two words!')
		self.label.pack()

		self.closeBtn = Button(master, text='Close', command=master.quit)
		self.closeBtn.pack(side=BOTTOM)

		self.wordEntryOne = Entry(master)
		self.wordEntryOne.pack(side=TOP)

		self.wordEntryTwo = Entry(master)
		self.wordEntryTwo.pack(side=TOP)

		self.charLimit = Spinbox(master, from_=0, to=20, width=5)
		self.charLimit.pack()

		self.genBtn = Button(master, text='Generate Name', command=self.main)
		self.genBtn.pack(side=TOP)
		self.clearBtn = Button(master, text="Reset", command=self.reset)
		self.clearBtn.pack(side=TOP)

		self.output = Text(master)
		self.output.pack(side=TOP)

		self.gen = None

	def reset(self):
		self.wordEntryOne.config(state='normal')
		self.wordEntryTwo.config(state='normal')
		self.charLimit.config(state='normal')
		self.output.delete(1.0,END)
		self.gen = None

	def wordCheck(self, wordOne, wordTwo):
		pageOne = requests.get('https://www.thesaurus.com/browse/%s' % wordOne)
		pageTwo = requests.get('https://www.thesaurus.com/browse/%s' % wordTwo)

		if pageOne.status_code != 200:
			print("First word is invalid")
			return False
		elif pageTwo.status_code != 200:
			print("Second word is invalid")
			return False
		else:
			return True

	def main(self):

		if self.gen != None:
			self.output.insert(END, '\n'+ self.gen.main())
			self.output.see('end')
		elif self.gen == None and self.wordCheck(self.wordEntryOne.get(),self.wordEntryTwo.get()) == True:
			#disable entry fields
			self.wordEntryOne.config(state='disabled')
			self.wordEntryTwo.config(state='disabled')
			self.charLimit.config(state='disabled')

			#create name generator
			self.gen = NameGen(self.wordEntryOne.get(), self.wordEntryTwo.get(),int(self.charLimit.get()))
			self.output.insert(END, self.gen.main())
			self.output.see('end')
			

class NameGen():
	def __init__(self, nameOne, nameTwo, limit):
		#Name Generator
		self.limit = limit
		self.synsOne = self.genSyns(nameOne)
		self.synsTwo = self.genSyns(nameTwo)

	#Generates one list of synonyms from given input, ref thesaurus.com
	def genSyns(self, word):
		syns = []
		page = requests.get('https://www.thesaurus.com/browse/%s' % word)
		tree = html.fromstring(page.content)

		for i in range(1,100):
			newSym = tree.xpath('//*[@id="initial-load-content"]/main/section/section/section[1]/ul/li[%d]/span/a//text()' % i)
			if newSym == None:
				break
			elif ' ' in str(newSym):
				pass
			elif '-' in str(newSym):
				pass
			else:
				syns.extend(newSym)
		return syns

	#Concant two names from each list together
	def randName(self):
		randOne = self.synsOne[random.randint(0,len(self.synsOne)-1)]
		randTwo = self.synsTwo[random.randint(0,len(self.synsTwo)-1)]
		randName = randOne + randTwo
		return randName

	#Generate name until one meets char limit and return it
	def limiter(self):
		name = self.randName()
		while len(name)>self.limit:
			name = self.randName()
		return name

	#Runs it all
	def main(self):
		return self.limiter()


root = Tk()
app = Gui(root)
root.mainloop()
