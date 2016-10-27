import tkinter
class Mainmenu:
    GameBoard = tkinter.Tk()
    def _init_():  
        Mainmenu.GameBoard.title("Q-Learning Agent")
        Mainmenu.GameBoard.geometry("600x600")
        Mainmenu.GameBoard.wm_iconbitmap('favicon.ico')
        lbl = tkinter.Label(Mainmenu.GameBoard, text="label")
        ent = tkinter.Entry(Mainmenu.GameBoard)   
        lbl.grid()
        ent.grid() 
        Mainmenu.GameBoard.configure(background ="coral")
    def addbutton():
        btn = tkinter.Button(Mainmenu.GameBoard, text ="click")
        btn.grid()
        Mainmenu.GameBoard.mainloop()
Mainmenu._init_()
Mainmenu.addbutton()
