from tkinter import*
import time,random,math,sys,tkinter

class Controller:
    def __init__(self):
        self.dot=[]
        self.pos=[]
        self.width=-1
        self.height=-1
        self.angle=-1
        self.speedRate=1
        self.distance=0
        self.checkP1=False
        self.checkP2=False
        return

    def speedBall4(self):
        self.speedRate = 4
        return
    def speedBall8(self):
        self.speedRate = 8
        return
    def stopBall(self):
        self.speedRate = 0
        return
    def resumeBall(self):
        self.speedRate = 1
        return
    
    def create_view(self):
        self.mybook = Tk()
        #input section
        #width
        print (">>> set canvas width, defalt:400")
        widthVal = sys.stdin.readline()
        if widthVal == "\n":
            self.width = 400
        else:
            self.width = int(widthVal)
        print (">>> set canvas height, defalt:500")
        #height
        heightVal = sys.stdin.readline()
        if heightVal == "\n":
            self.height = 500
        else:
            self.height = int(heightVal)
        maxLength = math.sqrt(pow(self.width,2)+pow(self.height,2))
        #angle
        print (">>>set initial angle, defalt:15")
        angle = sys.stdin.readline()
        if angle == "\n":
            self.angle = 15
        else:
            self.angle = int(angle)
        self.canvas = Canvas(self.mybook,width = self.width,height = self.height,background = "white")
        self.canvas.pack()

        #set icon
        print (">>>set start point, defalt:middle, random: -1")
        startPoint = sys.stdin.readline()
        if startPoint == "\n":
            d1=self.canvas.create_oval(self.width/2-5,self.height/2-5,self.width/2+5,self.height/2+5,fill="blue")
        elif startPoint == "-1\n":
            randX = random.randint(5,self.width)
            randY = random.randint(5,self.height)
            d1=self.canvas.create_oval(randX-5,randY-5,randX+5,randY+5,fill="blue")
        else:
            d1=self.canvas.create_oval(self.width/2-5,self.height/2-5,self.width/2+5,self.height/2+5,fill="blue")
        self.dot.append(d1)

        
        self.canvas.update()
        return
    def square_collection(self,lineStartX,lineStartY):
        if self.p1[0]<=5 or self.p1[0]>=self.width-5:
            self.angle = 180-self.angle
            self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*2*self.speedRate,-math.sin(self.angle*math.pi/180)*2*self.speedRate)
            self.p1 = self.canvas.coords(self.dot[0])
            self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
            self.canvas.update()
        elif self.p1[1]<=5 or self.p1[1]>=self.height-5:
            self.angle = 360-self.angle
            self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*2*self.speedRate,-math.sin(self.angle*math.pi/180)*2*self.speedRate)
            self.p1 = self.canvas.coords(self.dot[0])
            self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
            self.canvas.update()
        return
    
    def start_movement(self):
        self.p1 = self.canvas.coords(self.dot[0])
        lineStartX = self.p1[0]+5
        lineStartY = self.p1[1]+5
        self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*self.speedRate,-math.sin(self.angle*math.pi/180)*self.speedRate)
        self.p1 = self.canvas.coords(self.dot[0])
        self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
        lineStartX = self.p1[0]+5
        lineStartY = self.p1[1]+5
        self.square_collection(lineStartX,lineStartY)
        self.distance += math.sqrt(pow(lineStartX - self.p1[0]+5,2)+pow(lineStartY - self.p1[1]+5,2))
        #self.labelD = Label(self.mybook, text=str(self.distance), fg="green", font=("Helvetica", 10))
        #self.labelD.place(x=self.width-50,y=self.height+10)

        
        self.canvas.update()
        time.sleep(0.01)
        return

    def buttons(self):
        self.button = Button(self.mybook, text='*1', fg="blue", command = self.resumeBall)
        self.button.pack(side="left")
        self.button = Button(self.mybook, text='*4', command = self.speedBall4)
        self.button.pack(side="left")
        self.button = Button(self.mybook, text='*8', command = self.speedBall8)
        self.button.pack(side="left")
        self.button = Button(self.mybook, text='Stop', fg="red", command = self.stopBall)
        self.button.pack(side="left")
        self.button = Button(self.mybook, text='Quit', fg="red", command = self.mybook.destroy)
        self.button.pack(side="left")
        return

    def isOrbit(self):
        back=False
        return back
    

    def play(self):
        while True:
            self.start_movement()
            self.canvas.update()

            
c = Controller()
c.create_view()
c.buttons()
c.play()
