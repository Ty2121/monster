import json
import datetime
from time import time
import nltk
from nltk.corpus import cmudict

# download the phonetic dictionary
# nltk.download('cmudict')

phoneticsDic = cmudict.dict()


print(phoneticsDic["air"])
class words:
    
    def __init__(self,text,start,end) -> None:
        global phoneticsDic
        self.text = text
        self.phonetics = [['m','a','b']]
        try:
            self.phonetics = phoneticsDic[text.lower()]
        except:
            self.phonetics = [['m','a','b']]
        self.start = start
        self.end = end
        self.subWords = []
        self.distribute()

    def getText(self)->str:
        return self.text

    def distribute(self):
        vowels = {'a','e','i','o','u','y'}
        count = 0
        startVowel = False
        if self.text[0] in vowels:
            startVowel = True
        for l in self.text:
            if l in vowels:
                count = count + 1

        delta = self.end - self.start
        if count != 0:
            delta = delta / count
        i = 0 
        while i <= count:
            if startVowel:
                startVowel = False
                mouth = 1
            else: 
                startVowel = True
                mouth = 2
            self.subWords.append(self.subWord(mouth,self.start + (delta * i),self.start + (delta * i) + delta))
            i = i + 1




    def done(self,time) -> bool:
        if time > self.end:
            return True
        return False
    
    def early(self, time) -> bool:
        if time < self.start:
            return True
        return False
        
    def __str__(self):
        return ("The word : '" + self.text + "' Starting at: " + str(self.start) + " Ends at: " + str(self.end))
    
    def __repr__(self):
        return ("The word : '" + self.text + "' Starting at: " + str(self.start) + " Ends at: " + str(self.end))
    
    class subWord:
        def __init__(self,mouth,start,end)-> None:
            self.mouth = mouth 
            self.start = start
            self.end = end

        def done(self,time):
            if time > self.end:
                return True
            return False



# load the file mmade by collab
with open('text.json', 'r') as f:
    # Reading from json file
    timeStamp = json.load(f)['segments']
 
# create a list for the words
wordList = []

# add all the words into a list as objects
for sentence in timeStamp:
    for word in sentence['words']:
        wordList.append(words(word['text'],word['start'],word['end']))


## build tkinter window 
from tkinter import*
import pyglet
from PIL import ImageTk, Image
root = Tk()
player = pyglet.media.Player()
song = "/Users/Admin/Downloads/Monster_mash.mp3"
src = pyglet.media.load(song)
player.queue(src)

# current word counter 
currentWord = 0
currentSubWord = 0
subWordTimeStamp = None
full = {"a","o"}
half = {"e",'g','h',"i",'k','l',"n",'q','r','u','w','y'}
closed = {'b','c','d','f','m','p','s',"t",'v','x','z'}
# function to control the current word 
def time():
    # set timestamp 
    timestamp = datetime.datetime.now()
    word['text'] = wordList[currentWord]
    
    def innerFunction():
        global currentWord
        global image1
        global image2
        global image3
        global currentSubWord 
        global subWordTimeStamp
        # global full 
        # global half
        # global closed
        timePassed = datetime.datetime.now() - timestamp
        label['text'] = timePassed
        # calculate time for each expression 
        subTime =(wordList[currentWord].start - wordList[currentWord].end )/len(wordList[currentWord].phonetics[0])
        
        # sing face expressions
        full = {"a","o"}
        half = {"e",'g','h',"i",'k','l',"n",'q','r','u','w','y'}
        closed = {'b','c','d','f','m','p','s',"t",'v','x','z'}


        if wordList[currentWord].early(float(timePassed.total_seconds())):
                
                currentSubWord = 0
                word['text'] = "..."
                smily["image"] = image1
                subWordTimeStamp = datetime.datetime.now()
        else: # word in progress 
            if (datetime.datetime.now() - subWordTimeStamp).total_seconds() > subTime and currentSubWord + 1 < len(wordList[currentWord].phonetics[0]):
                currentSubWord = currentSubWord + 1
                subWordTimeStamp = datetime.datetime.now()
            if currentSubWord < len(wordList[currentWord].phonetics[0]):
                print(wordList[currentWord].phonetics[0][currentSubWord][0][0])
                if wordList[currentWord].phonetics[0][currentSubWord][0][0].lower() in full:
                    smily["image"] = image3
                elif wordList[currentWord].phonetics[0][currentSubWord][0][0].lower() in half:
                    smily["image"] = image2
                elif wordList[currentWord].phonetics[0][currentSubWord][0][0].lower() in closed:
                    smily["image"] = image1
                
        







            # smily["image"] = image2
            # if currentSubWord < len(wordList[currentWord].subWords):
            #     if wordList[currentWord].subWords[currentSubWord].done(timePassed.total_seconds()):
            #         if currentSubWord + 1 < len(wordList[currentWord].subWords):
            #             currentSubWord = currentSubWord + 1
            #     else:
            #         if wordList[currentWord].subWords[currentSubWord].mouth == 1 and currentSubWord !=0:
            #             smily["image"] = image1
            #         else: 
            #             smily["image"] = image2
                

                
        
        if wordList[currentWord].done(float(timePassed.total_seconds())):
            currentWord = currentWord + 1
            word['text'] = wordList[currentWord]
            # smily["image"] = image1
            currentSubWord = 0


        # self call  
        label.after(10, innerFunction)

            
    innerFunction()
            

def play():
    player.play()
    time()
def pause():
    player.pause()
label = Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
label.pack()
word = Label(root, text="", fg="black", font="Verdana 30 bold")
word.pack()

# smliys 

image1 = ImageTk.PhotoImage(Image.open("/Users/Admin/Library/CloudStorage/GoogleDrive-tyayal2121@gmail.com/My Drive/Matlab/Python/Monster_mash/close.png"))
image2 = ImageTk.PhotoImage(Image.open("/Users/Admin/Library/CloudStorage/GoogleDrive-tyayal2121@gmail.com/My Drive/Matlab/Python/Monster_mash/half.png"))
image3 = ImageTk.PhotoImage(Image.open("/Users/Admin/Library/CloudStorage/GoogleDrive-tyayal2121@gmail.com/My Drive/Matlab/Python/Monster_mash/open.png"))


smily = Label(root, image = image1)
smily.pack(side = "bottom", fill = "both", expand = "yes")
button_1 = Button(root,text = "Play", command = play)
button_1.pack()
button_2 = Button(root,text = "Pause", command = pause)
button_2.pack()
root.mainloop()