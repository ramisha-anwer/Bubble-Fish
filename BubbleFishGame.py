import tkinter as tk
from tkinter import messagebox
from random import randint
import time
import winsound
import json
import leaderscores

MOVES_PER_SECOND = 15
GAME_SPEED = 200 // MOVES_PER_SECOND
ENDGAME=False
customized=False

class fish(tk.Canvas):
        
    def __init__(self):
        super().__init__(root,
            width=screen_width, height=screen_height, highlightthickness=0
        )
        
        self.direction = "Right"
        self.healthcounter=5
        self.score = 0
        
#-------------SHARK INCREMENTS---------
        
        self.a = 3
        self.b =3
        
#-------------FISH INCREMENTS----------
        
        self.c = 0
        self.d = 0
        
#---------------BUBBLE INCREMENTS-------------
        
        self.e = 0
        self.f = -5
        
        self.load_assets()
        self.create_objects()
        
        self.bind_all("<Key>", self.on_key_press)
        self.bind_all("<space>", self.pause)
        self.place(x=0,y=0,relwidth=1,relheight=1)
        self.after(GAME_SPEED, self.perform_actions)
        self.scoreFile='HighScores_1.json'
        self.highScores = json.loads(open(self.scoreFile, 'r').read())

    def load_assets(self):
        try:
            self.bg=tk.PhotoImage(file="Assets/2_game_background/2_game_background2.png")
            self.bg2=tk.PhotoImage(file="Assets/2_game_background/2_game_background3.png")
            self.fish = tk.PhotoImage(file="Assets/fish2.png")
            self.fish_left = tk.PhotoImage(file='Assets/fish2-leftr.png')
            self.fish=self.fish.subsample(4)            
            self.bubble1 = tk.PhotoImage(file="Assets/Bubble_3.png")
            self.bubble2 = tk.PhotoImage(file="Assets/Bubble_2.png")
            self.bubble3 = tk.PhotoImage(file="Assets/Bubble_1.png")
            self.health1=tk.PhotoImage(file="Assets/health_bar1.png")
            self.health1=self.health1.subsample(2)
            self.health2=tk.PhotoImage(file="Assets/health_bar2.png")
            self.health2=self.health2.subsample(2)
            self.health3=tk.PhotoImage(file="Assets/health_bar3.png")
            self.health3=self.health3.subsample(2)
            self.health4=tk.PhotoImage(file="Assets/health_bar4.png")
            self.health4=self.health4.subsample(2)
            self.health5=tk.PhotoImage(file="Assets/health_bar5.png")
            self.health5=self.health5.subsample(2)
            self.health6=tk.PhotoImage(file="Assets/health_bar6.png")
            self.health6=self.health6.subsample(2)
            self.score_bg=tk.PhotoImage(file="Assets/score_bg.png")
            self.score_bg=self.score_bg.subsample(4)           
            self.sharkimg = tk.PhotoImage(file='Assets/sharkr.png')
            
        except IOError as error:
            root.destroy()
            raise

    def create_objects(self):
        global fishimg
        if screen_width==1366 and screen_height==768:
            self.create_image(0,0,image=self.bg,anchor="nw")
        elif screen_width==1536 and screen_height==864:
            self.create_image(0,0,image=self.bg2,anchor="nw")
        fishimg=self.create_image(100,100, image=self.fish, tag="fish")
        self.create_image(100,45,image=self.score_bg)
        self.create_image(100,700, image=self.bubble1, tag="bubble")
        self.create_image(400,600, image=self.bubble2, tag="bubble2")
        self.create_image(800,500, image=self.bubble3, tag="bubble3")
        self.scoretext=self.create_text(100,35,text=f"Score:{self.score}",tag="score",font=("Comic Sans MS",18))
        self.create_text(490,20,text="HP",font=("Comic Sans MS",10))
        self.create_image(screen_width//2,20,image=self.health1,tag="health1")
        self.shark = self.create_image(screen_width//2,screen_height//2-200,image=self.sharkimg,tag='shark')
        self.menubtn=tk.Button(self,text="Menu",bg="#40e0d0",activebackground="#ff00ff",font=("Comic Sans MS",12), command = mainmenu)
        self.menubtn.place(x=screen_width-120, y=10)
        self.cheatbtn=tk.Button(self,text="Cheats",bg="#40e0d0",activebackground="#ff00ff",font=("Comic Sans MS",12),command=self.cheats)
        self.cheatbtn.place(x=screen_width-120, y=70)

    def on_key_press(self, e):
        global paused 
        new_direction = e.keysym
        if customized:
            if choice=="wasd":
                all_directions = ("w", "s", "a", "d")
            else:
                all_directions = ("Up", "Down", "Left", "Right")
        else:
            all_directions = ("Up", "Down", "Left", "Right")
        if (new_direction in all_directions):
            self.direction = new_direction
        if new_direction == "b":            
            self.pause("<b>")
            self.BosskeyCode("<b>")

#----------------FISH MOVEMENT-----------------
        
    def move_fish(self):
        global fishimg,game_start
        if self.direction == 'Up' or self.direction == 'w':            
            self.c = 0
            self.d = -6
            if self.score > 30:
                self.c = 0
                self.d = -9
            fish_coords=self.bbox(fishimg)
            if fish_coords[1]<11:
               return None

        if self.direction == 'Down' or self.direction == 's' :            
            self.c = 0
            self.d = 6
            if self.score > 30:
                self.c = 0
                self.d = 9
            fish_coords=self.bbox(fishimg)
            if fish_coords[3]>screen_height-20:
               return None
           
        if self.direction == 'Right'or self.direction == 'd':           
            self.c = 6
            self.d = 0
            if self.score > 30:
                self.c = 9
                self.d = 0
            self.itemconfigure(fishimg,image=self.fish)
            fish_coords=self.bbox(fishimg)
            if fish_coords[2]>=screen_width-10:
               return None            
                
        if self.direction == 'Left'or self.direction == 'a':            
            self.c = -6
            self.d = 0
            if self.score > 30:
                self.c = -9
                self.d = 0
            self.itemconfigure(fishimg,image=self.fish_left)
            fish_coords=self.bbox(fishimg)
            if fish_coords[0]<10:
               return None
            
        self.move(fishimg,self.c,self.d)
        
        if self.check_bubble1_collision():
                winsound.PlaySound("Assets/pop-audio.wav", winsound.SND_ASYNC)
                self.score+=1
                self.itemconfig(self.scoretext,text=f"Score:{self.score}")
                self.set_new_bubble_position()
        if self.check_bubble2_collision():
                winsound.PlaySound("Assets/pop-audio.wav", winsound.SND_ASYNC)
                self.score+=1
                self.itemconfig(self.scoretext,text=f"Score:{self.score}")
                self.set_new_bubble_position2()
        if self.check_bubble3_collision():
                winsound.PlaySound("Assets/pop-audio.wav", winsound.SND_ASYNC)
                self.score+=1
                self.itemconfig(self.scoretext,text=f"Score:{self.score}")
                self.set_new_bubble_position3()
            
        if self.check_shark_collision():
            winsound.PlaySound("Assets\SharkCollisionTrack.wav", winsound.SND_ASYNC)
            self.healthcounter-=1
            if self.healthcounter == 4:
                self.itemconfigure("health1",image=self.health2)
            if self.healthcounter == 3:
                self.itemconfigure('health1',image=self.health3)
            if self.healthcounter == 2:
                self.itemconfigure('health1',image=self.health4)
            if self.healthcounter == 1:
                self.itemconfigure('health1',image=self.health5)
            if self.healthcounter == 0:
                self.itemconfigure('health1',image=self.health6)
                
            self.coords(self.shark,1000,500)
        if self.healthcounter==0:
            self.end_game()
#---------------SHARK MOVEMENT---------------------

    def shark_movement(self):        
        bounds = self.bbox(self.shark)
        if bounds[0] < 0 or bounds[2] > screen_width-20:
            self.a = -self.a
        if bounds[1] < 0 or bounds[3] > screen_height-20:
            self.b = -self.b
        self.move(self.shark,self.a,self.b)

#------------------BUBBLE MOVEMENT-----------------           
    def move_bubble1(self):
        bounds = self.bbox('bubble')
        if bounds[1] < 1:
            self.set_new_bubble_position()
        self.move('bubble',self.e,self.f)
                
    def move_bubble2(self):
        bounds = self.bbox('bubble2')
        if bounds[1] < 1:
            self.set_new_bubble_position2()
        self.move('bubble2',self.e,self.f)
                
    def move_bubble3(self):
        bounds = self.bbox('bubble3')
        if bounds[1] < 1:
            self.set_new_bubble_position3()
        self.move('bubble3',self.e,self.f)

#---------------BUBBLE POSITIONS------------------
        
    def set_new_bubble_position(self):
        x_position = randint(200,800)
        y_position = screen_height-400
        self.coords('bubble',x_position,y_position)
           
    def set_new_bubble_position2(self):
        x_position = randint(20,1300)
        y_position = screen_height-200
        self.coords('bubble2',x_position,y_position)
           
    def set_new_bubble_position3(self):
        x_position = randint(100,700)
        y_position = screen_height-300
        self.coords('bubble3',x_position,y_position)

#----------------BUBBLE COLLISIONS-------------

    def check_bubble1_collision(self):
        fish_coords=self.bbox(fishimg)
        bubblebounds=self.bbox("bubble")
        if bubblebounds[0] <fish_coords[2] < bubblebounds[2] and  bubblebounds[1] < fish_coords[3] < bubblebounds[3]:
            return True
        if bubblebounds[0] <fish_coords[0] < bubblebounds[2] and  bubblebounds[1] < fish_coords[1] < bubblebounds[3]:
            return True
        
    def check_bubble2_collision(self):
        fish_coords=self.bbox(fishimg)
        bubblebounds2=self.bbox("bubble2")
        if bubblebounds2[0] <fish_coords[2] < bubblebounds2[2] and  bubblebounds2[1] < fish_coords[3] < bubblebounds2[3]:
            return True
        if bubblebounds2[0] <fish_coords[0] < bubblebounds2[2] and  bubblebounds2[1] < fish_coords[1] < bubblebounds2[3]:
            return True
        
    def check_bubble3_collision(self):
        fish_coords=self.bbox(fishimg)
        bubblebounds3=self.bbox("bubble3")
        if bubblebounds3[0] <fish_coords[2] < bubblebounds3[2] and  bubblebounds3[1] < fish_coords[3] < bubblebounds3[3]:
            return True
        if bubblebounds3[0] <fish_coords[0] < bubblebounds3[2] and  bubblebounds3[1] < fish_coords[1] < bubblebounds3[3]:
            return True

#----------------SHARK COLLISION------------------
        
    def check_shark_collision(self):
        fish_coords=self.bbox(fishimg)
        sharkbounds=self.bbox(self.shark)
        if fish_coords[2] in range(sharkbounds[0] ,sharkbounds[2]+1) and fish_coords[3] in range (sharkbounds[1] ,sharkbounds[3]+1):
            return True
        if fish_coords[0] in range(sharkbounds[0] ,sharkbounds[2]+1) and fish_coords[1] in range (sharkbounds[1] ,sharkbounds[3]+1):           
            return True

    def difficulty(self):
        if self.score == 15:
            self.a = -5
            self.b = 5
        if self.score == 30:
            self.a = -7
            self.b = 7
        if self.score == 50:
            self.a = -9
            self.b = 9
            
    def perform_actions(self):
        if game_start==True:
            if paused==False:
                self.move_fish()
                self.move_bubble1()
                self.move_bubble2()
                self.move_bubble3()
                self.shark_movement() 
                self.difficulty()       

        self.after(GAME_SPEED, self.perform_actions)

    def pause(self,event):
        global paused, g
        if paused == True:
            self.itemconfig(g, text ="Go")
            time.sleep(1)
            paused = False
            self.delete(g)
        elif paused == False:
            paused = True
            g = self.create_text(screen_width/2, screen_height/2, fill = "white", font = ("Comic Sans MS",40), text = "Paused")
                
    def BosskeyCode(self,event): 
        newWindow = tk.Toplevel(root) 
        newWindow.title("MS ExcelSheet")
        newWindow.geometry("1600x1000")
        bga=tk.PhotoImage(file="Assets/excelsheet.png")
        maincanvasx=tk.Canvas(newWindow,width=1600,height=1000)
        maincanvasx.pack()
        maincanvasx.create_image(700,350,image=bga) 
        maincanvasx.image = bga

    def cheats(self):
        global paused, cheat_text, cheat_input, cheat_window, cheat_window_button, add_cheat_button
        paused = True
        self.unbind_all("<Key>")
        self.unbind_all("<space>")
        self.cheat_text = tk.Label(self, bg = "#40e0d0", font = "Comic Sans MS 20 bold", text = "Enter cheat and press the button below.")
        self.cheat_text.place(x=screen_width//2-220,y=screen_height//2-100)
        cheat_input = tk.Entry(self, font = "Comic Sans MS 15")
        cheat_window = self.create_window(screen_width//2-100, screen_height//2-50, anchor = "nw", window = cheat_input)
        add_cheat_button = tk.Button(self, text = "Apply", pady = 10, bg = "#ff00ff", fg = "white", command = self.apply_cheat)
        cheat_window_button = self.create_window(screen_width//2-50, screen_height//2-10, anchor = "nw", window = add_cheat_button)
        
    def apply_cheat(self):
        global paused, cheat_input, cheat_window, cheat_window_button, add_cheat_button, cheat_lives, cheat_spikes, score, txt, score_text

        cheat = cheat_input.get()
        if cheat == "restore":
            self.healthcounter=5
            self.create_image(screen_width//2,20,image=self.health1,tag="health1")
        if cheat=="plus10":
            self.score+=10
            self.itemconfig(self.scoretext,text=f"Score:{self.score}")       
        self.bind_all("<Key>", self.on_key_press)
        self.bind_all("<space>", self.pause)
        
        self.delete(cheat_window)
        self.delete(cheat_window_button)
        cheat_input.destroy()
        add_cheat_button.destroy()
        self.cheat_text.destroy()
        paused = False
        
    def end_game(self):
        global restart, ENDGAME
        self.unbind_all("<Key>")
        self.unbind_all("<space>")
        self.unbind_all("<b>")
        ENDGAME = True
        self.delete(tk.ALL)
        self.menubtn.destroy()
        self.cheatbtn.destroy()
        winsound.PlaySound("Assets\EndGameTrack.wav", winsound.SND_ASYNC)
        self.gameover = tk.PhotoImage(file="Assets/gameover2.png")
        if screen_width==1366 and screen_height==768:
            self.create_image(0,0,image=self.bg,anchor="nw")
        elif screen_width==1536 and screen_height==864:
            self.create_image(0,0,image=self.bg2,anchor="nw")
        self.create_image(screen_width // 2-70, screen_height // 2-100, image=self.gameover)
        restart = tk.Button(self, bg="#ff00ff", text="PLAY AGAIN",font=("Comic Sans MS",20), command=open_game)
        restart.place(x=screen_width // 2 - 150, y=screen_height - 200)
        menu = tk.Button(self, bg="#ff00ff", text="MENU",font=("Comic Sans MS",20), command=mainmenu)
        menu.place(x=screen_width // 2-100, y=screen_height - 280)
        leaderboard1 = tk.Button(self, bg="#ff00ff", text="LEADERBOARD",font=("Comic Sans MS",20), command=leaderscores.openScores)
        leaderboard1.place(x=screen_width // 2 - 150, y=screen_height - 120)
        if self.score > min(self.highScores[1]):
            for i in range(len(self.highScores[1])):
                if self.score > self.highScores[1][i]:
                    self.highScores[1].insert(i, self.score)
                    self.setScore(i)
                    break

    def setScore(self,scorePosIndex):
        def closeForm(event=None):
            if event is not None:
                self.highScores[0].insert(scorePosIndex, nameEntry.get())
                self.highScores[0].pop()
                self.highScores[1].pop()
                f = open(self.scoreFile, 'w')
                json.dump(self.highScores, f)
                f.close()
                scoreForm.destroy()
                leaderscores.openScores()

        scoreForm = tk.Toplevel(root, width=300, height=150, bg='#780552')
        scoreForm.resizable(0, 0)
        label1 = tk.Label(scoreForm, text='Enter your name', width=17, bg='#780552', font=('Felix Titling', 24))
        nameEntry = tk.Entry(scoreForm, width=15, bg='#810541', font=('Felix Titling', 24))
        submitBtn = tk.Button(scoreForm, text='Submit', bg='#810541', font=('Felix Titling', 24))
        submitBtn.bind('<Button-1>', closeForm)
        label1.grid(row=0, column=0, padx=30, pady=10)
        nameEntry.grid(row=1, column=0, pady=10)
        submitBtn.grid(row=2, column=0, pady=10)
        scoreForm.wm_title('New High Score!')
        scoreForm.protocol('WM_DELETE_WINDOW', closeForm)


def instructions():
    tk.messagebox.showinfo(title="How to Play?", message="Move with the controls you selected. By default, those are the arrow keys \nPress spacebar to pause the game \nPress the 'b' key for boss key \nActivate cheats by entering 'restore' or 'plus10'!")
    
#-------------CONTROLS-------------
    
def openNewWindow(): 
    global var1,var2,customized
    newWindow = tk.Toplevel(root) 
    newWindow.title("Controls") 
    newWindow.geometry("650x400") 
    newWindow.configure(bg="#20B2AA") 
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    tk.Label(newWindow, text="Customise Controls \n Note: Default control setting is Arrow Keys",bg="#20B2AA",font="Helvetica 24").place(x=10,y=10)
    tk.Checkbutton(newWindow, text="Arrow Keys",font="Helvetica 18",bg="#20B2AA", variable=var1).place(x=200,y=150)
    tk.Checkbutton(newWindow, text="WASD keys",font="Helvetica 18",bg="#20B2AA", variable=var2).place(x=200,y=220)
    tk.Button(newWindow, text='Save', bg="#ff00ff",fg="white",font="Helvetica 18",command=savecontrols).place(x=230,y=300)
    print ("var1:",var1,"var2:",var2)
    customized=True
    
def savecontrols():
    global choice
    if var2.get()==1:
        choice="wasd"
    elif var1.get()==1:
        choice="arrowkeys"
    else:
        choice="arrowkeys"
        
def open_game():
    global game_start,paused
    winsound.PlaySound(None, winsound.SND_PURGE)
    game_start = True
    paused=False
    maincanvas.destroy()
    if ENDGAME==True:
        restart.destroy()
    board = fish()
#--------------START SCREEN--------------
    
def mainmenu():
    global maincanvas,background_image,background_image2,playbtn,titlepic,crab
    winsound.PlaySound("Assets/BubbleSoundTrack.wav", winsound.SND_ASYNC)
    maincanvas=tk.Canvas(root,width=screen_width,height=screen_height)
    crab=tk.PhotoImage(file="Assets/crab.png")
    crab=crab.subsample(5)
    titlepic=tk.PhotoImage(file="Assets/titler.png")
    if screen_width==1366 and screen_height==768:
        background_image = tk.PhotoImage(file="Assets/2_game_background/2_game_background2.png")
        bgimage=maincanvas.create_image(0,0,image=background_image,anchor="nw")
    if screen_width==1536 and screen_height==864:
        background_image2 = tk.PhotoImage(file="Assets/2_game_background/2_game_background3.png")
        bgimage2=maincanvas.create_image(0,0,image=background_image2,anchor="nw")
    maincanvas.create_image(screen_width//2,screen_height//4,image=titlepic)
    maincanvas.create_image(100,screen_height-150,image=crab)

    playbtn=tk.PhotoImage(file="Assets/playtext.png")
    playbtn=playbtn.subsample(4)
    playmain = tk.Button(maincanvas, image=playbtn,bg="#ff00ff",borderwidth=0,activebackground="#40e0d0",relief="raised",  command = open_game)
    playmain.place(x=screen_width//2-200, y=screen_height//2)
    quitbtn = tk.Button(maincanvas, text="QUIT",bg=	"#40e0d0",font=("Comic Sans MS",16), command = quit)
    quitbtn.place(x=screen_width//2-200, y=screen_height//2+270)
    leaderboardbtn=tk.Button(maincanvas,text="LeaderBoard",bg="#40e0d0",font=("Comic Sans MS",16),command=leaderscores.openScores)
    leaderboardbtn.place(x=screen_width//2-30,y=screen_height//2+180)
    customizebtn=tk.Button(maincanvas,text="Controls",bg="#40e0d0",font=("Comic Sans MS",16),command=openNewWindow)
    customizebtn.place(x=screen_width//2-200,y=screen_height//2+180)
    helpbtn=tk.Button(maincanvas,text="Help",bg="#40e0d0",font=("Comic Sans MS",16),command=instructions)
    helpbtn.place(x=screen_width//2-30,y=screen_height//2+270)
    maincanvas.place(x=0,y=0,relwidth=1,relheight=1)


root = tk.Tk()
root.title("Bubble Fish")
root.resizable(True,True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("600x400")
print (screen_width,screen_height)

canvas1 = tk.Canvas(root, width = 600, height = 400,bg="#20B2AA")
canvas1.pack()

entry1 = tk.Entry (root) 
canvas1.create_window(300, 200, window=entry1)
label1=tk.Label(text="Choose a window Size\n1. 1366x768\n2. 1536x864\n\nEnter your choice (1 or 2)",bg="#20B2AA",font="Helvetica 18")
canvas1.create_window(300, 100, window=label1)

def createroot():
    global screen_height,screen_width
    if entry1.get() == 1:
        screen_width=1366
        screen_height=768
    if entry1.get()==2:
        screen_width=1536
        screen_height=864
    root.geometry(f"{screen_width}x{screen_height}")
    mainmenu()
button1 = tk.Button(text='Save',font="Helvetica 18", command=createroot)
canvas1.create_window(300, 250, window=button1)


root.mainloop()
