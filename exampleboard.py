import tkinter as QLearning
class GameBoard(QLearning.Frame):
    def __init__(self, parent, rows=5, columns=5, size=120, color1="red"):
        '''size is the size of a square, in pixels'''
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.pieces = {}
        QLearning.Frame.__init__(self, parent)
        self.canvas = QLearning.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=600, height=600, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        for row in range(self.rows):
            color = self.color1
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")

if __name__ == "__main__":
    root = QLearning.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()
