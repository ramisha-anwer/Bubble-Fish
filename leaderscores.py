import json
import winsound
import tkinter as tk
class ScoreFrame:
    def __init__(self, root):
        self.root = root
        self.scoreFile = 'HighScores_1.json'
        self.scoreData = json.loads(open(self.scoreFile, 'r').read())
        print(self.scoreData)
        self.canvas=tk.Canvas(self.root,width=600,height=350,bg='#283747')
        self.canvas.pack()
        self.createWidgets()
    def createWidgets(self):
        headFont = ('TkHeadingFont', 17, 'bold')
        textFont = ('TkFixedFont', 15)
        self.frame = tk.Frame(self.canvas,padx=40,pady=40,bg='#283747')
        self.scoreFrame = tk.LabelFrame(self.frame, padx=10, pady=10, text='Hall of Fame', font=headFont, bg='#008080')
        self.frame.grid(column=0, row=0, columnspan=7, sticky='S')
        self.root.resizable(0, 0)
        for y in range(10):
            for x in range(3):
                if x == 0:
                    self.cell = tk.Label(self.scoreFrame, width=3, bg='#008080',font=('Helvetica',21))
                    self.cell.config(text=str(y+1))
                elif x == 1:
                    self.cell = tk.Label(self.scoreFrame, width=15, anchor='w', font=textFont,bg='#C71585')
                    self.cell.config(text=' ' + self.scoreData[x-1][y])
                elif x == 2:
                    self.cell = tk.Label(self.scoreFrame, width=10, anchor='e', font=textFont,bg='#008080')
                    self.cell.config(text='{:,}'.format(self.scoreData[x-1][y]) + ' ')
                self.cell.grid(row=y, column=x)
        self.spacer = tk.Label(self.root)
        self.OkBtn = tk.Button(self.frame, text="OK")
        self.OkBtn.bind('<Button-1>', self.closeWindow)
        self.scoreFrame.grid(column=0, row=0, columnspan=10, padx=20, pady=0, sticky='S')
        self.OkBtn.grid(column=3, row=1, padx=5, pady=15, sticky='N')
        self.spacer.pack()
        self.frame.pack()

    def closeWindow(self, event):
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.root.destroy()
        winsound.PlaySound("Assets/BubbleSoundTrack.wav", winsound.SND_ASYNC)
def openScores():
    winsound.PlaySound("Assets\LeaderBoardTrack.wav", winsound.SND_ASYNC)
    root = tk.Tk()
    root.geometry('600x550')
    root.config(bg='#283747')
    ScoreFrame(root)
    root.title('High Scores')
    root.mainloop()
if __name__ == '__main__':
    openScores()







