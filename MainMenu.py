import tkinter
class Mainmenu:
    def __init__(self,title,resolution):
        self.game_board = tkinter.Tk()  
        self.game_board.title(title)
        self.game_board.geometry(resolution)
        self.game_board.wm_iconbitmap('favicon.ico')
        self.label = tkinter.Label(self.game_board, text="Main Menu",width=25,font=('Courier',16))
        self.label.pack()
        self.label.place(x=125,y=50)
        self.game_board.configure(background ="black")
        self.buttons=[]
        self.butt_coords=[225,150]
    def addButton(self,button_text,action=None,):
        self.buttons.append(tkinter.Button(self.game_board,text=button_text,command=action))
        self.buttons[-1].pack()
        self.buttons[-1].place(x=self.butt_coords[0],y=self.butt_coords[1])
        self.butt_coords[1]+=60


    


