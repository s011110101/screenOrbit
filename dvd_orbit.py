from tkinter import*
import time,random,math,sys,tkinter

class Controller:
    def __init__(self):
        self.dot=[]
        self.pos=[]
        self.bond=[]
        self.width=-1
        self.height=-1
        self.angle=[-1,-1]
        self.lock=[]
        self.speedRate=1
        self.distance=0
        self.slopes=[] 
        self.intercepts=[]
        self.checkP1=False
        self.checkP2=False
        self.shape=-1
        return
    
    def create_view(self):
        self.mybook = Tk()

        #input section
        print(">>> set shape side number: defalt 4")
        shape = sys.stdin.readline()
        if shape == "\n":
            self.shape = 4
        else:
            self.shape = int(shape)
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
            self.angle = [math.cos(15/180*math.pi),math.sin(15/180*math.pi)]
        else:
            self.angle = [math.cos(angle/180*math.pi),math.sin(angle/180*math.pi)]
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
            startPoint = list(map(int,startPoint.split()))
            randX=startPoint[0]
            randY=startPoint[1]
            d1=self.canvas.create_oval(randX-5,randY-5,randX+5,randY+5,fill="blue")
        self.dot.append(d1)
        #set shape
        pivot = []
        for i in range(self.shape):
            coord=[]
            size = maxLength/4
            pivot.append((size*math.cos(2*math.pi/self.shape*i) + size*math.tan(2*math.pi/2/self.shape)*(-1)*(-math.sin(2*math.pi/self.shape*i))))
            pivot[-1]+=size*1.25
            coord.append(pivot[-1])
            pivot.append((size*math.sin(2*math.pi/self.shape*i) + size*math.tan(2*math.pi/2/self.shape)*(-1)*(math.cos(2*math.pi/self.shape*i))))
            pivot[-1]+=size*1.25
            coord.append(pivot[-1])
            self.bond.append(coord)
        self.canvas.create_polygon(*pivot,outline="black",fill="")
        self.canvas.update()
        self.bondary()
        self.lock = [True]*self.shape
        return
    '''
    def square_collision(self,lineStartX,lineStartY):
        if self.shape%2==0:
            if self.p1[0]<=10 or self.p1[0]>=self.width-10:
                self.angle = 180-self.angle
                self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*2,-math.sin(self.angle*math.pi/180)*2)
                self.p1 = self.canvas.coords(self.dot[0])
                self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
                self.canvas.update()
            elif self.p1[1]<=10 or self.p1[1]>=self.height-10:
                self.angle = 360-self.angle
                self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*2,-math.sin(self.angle*math.pi/180)*2)
                self.p1 = self.canvas.coords(self.dot[0])
                self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
                self.canvas.update()
        return
    '''
    def bondary(self):
        self.bond.reverse()
        #calculate slope
        slopes=[]
        intercepts=[]
        for i in range(self.shape):
            yDistance = self.bond[i][0]-self.bond[(i+1)%self.shape][0]
            #prevent zero division
            if yDistance == 0:
                yDistance = 1*10^-12
            slope = (self.bond[i][1]-self.bond[(i+1)%self.shape][1]) / yDistance
            slopes.append(slope)
            intercept = self.bond[i][1]-slope*self.bond[i][0]
            intercepts.append(intercept)
        self.slopes = slopes
        self.intercepts = intercepts
    #(360 / self.shape * ((the number of side) % (self.shape/1)) - incidence) is the reflection of any odd shape
    #(360 / self.shape * ((the number of side) % (self.shape/2)) - incidence) is the reflection of any even shape
    def oddCollision(self,lineStartX,lineStartY):
        slopes = self.slopes
        intercepts = self.intercepts
        #detect if out of lines
        for i in range(self.shape):
            x = self.p1[0]+5
            y = self.p1[1]+5
            #the sign inverse when the line get upper than the middle symmetric axis
            '''
            if self.shape%2==1:
                #print((i % (self.shape/2)+1)*360/self.shape*2)
                    #if (intercepts[i]>0 and y>slopes[i]*x+intercepts[i]) or (intercepts[i]<0 and y<slopes[i]*x+intercepts[i]):
                if abs(slopes[i]*x-y+intercepts[i])/math.sqrt(pow(slopes[i],2)+pow(-1,2))<10 :
                    self.angle = (360-(i+1)*360/self.shape)-self.angle
                    
                    self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*2,-math.sin(self.angle*math.pi/180)*2)
                    self.p1 = self.canvas.coords(self.dot[0])
                    self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
                    self.canvas.update()
            else:
                
                    #if (intercepts[i]>0 and y>slopes[i]*x+intercepts[i]) or (intercepts[i]<0 and y<slopes[i]*x+intercepts[i]):
                if abs(slopes[i]*x-y+intercepts[i])/math.sqrt(pow(slopes[i],2)+pow(-1,2))<10*self.speedRate :
                    slopeAngle = abs(math.atan(slopes[i])*180/math.pi)
                    self.angle = 360-self.angle+slopeAngle-slopeAngle
                    slopeAngle-self.angle-slopeAngle
                    #self.angle = (i % (self.shape/2)+1)*360/self.shape*2-self.angle
                    
                    self.canvas.move(self.dot[0],math.cos(self.angle*math.pi/180)*2,-math.sin(self.angle*math.pi/180)*2)
                    self.p1 = self.canvas.coords(self.dot[0])
                    self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
                    self.canvas.update()
                
                    #break
            '''
            #y=slope x + intercept
            #slope x - y + intercept = 0
            if abs(slopes[i]*x-y+intercepts[i])/math.sqrt(pow(slopes[i],2)+pow(-1,2))<10 and self.lock[i]:
                self.lock=[True]*self.shape
                self.lock[i]=False
                #unit vector of side
                point1 = [0, -intercepts[i]]
                point2 = [1, -(slopes[i] + intercepts[i])]
                u = [point1[0]-point2[0], point1[1]-point2[1]]
                v = [self.angle[0], self.angle[1]]
                #get projection of the speed vector
                scale = (u[0]*v[0] + u[1]*v[1]) / (u[0]*u[0] + u[1]*u[1]) 
                projV = [scale*u[0], scale*u[1]]
                #print(projV)
                perpenV = [v[0]-projV[0], v[1]-projV[1]]
                #print(perpenV)
                self.angle = [projV[0]-perpenV[0], projV[1]-perpenV[1]]
                #time.sleep(1)
                lineStartX = self.p1[0]+5
                lineStartY = self.p1[1]+5
                self.canvas.move(self.dot[0],self.angle[0],-self.angle[1])
                self.p1 = self.canvas.coords(self.dot[0])
                self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
                self.canvas.update()


            #time.sleep(1)
        return

    def getAngleX(self,n):
        angle=90-angle
        for i in range(n):
            angle=180-angle-360*2/self.shape
        return angle

    
    def start_movement(self):
        self.p1 = self.canvas.coords(self.dot[0])
        lineStartX = self.p1[0]+5
        lineStartY = self.p1[1]+5
        self.canvas.move(self.dot[0],self.angle[0]*self.speedRate,-self.angle[1]*self.speedRate)
        self.p1 = self.canvas.coords(self.dot[0])
        self.canvas.create_line(lineStartX,lineStartY,self.p1[0]+5,self.p1[1]+5,fill="black")
        lineStartX = self.p1[0]+5
        lineStartY = self.p1[1]+5
        self.oddCollision(lineStartX,lineStartY)
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

    #events for buttons
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
