# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:16:13 2022

@author: asche
"""
import numpy as np
import tkinter as tk
from fractions import Fraction

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title('TOA LightOut Puzzle Solver') #Controls the window title.
        self.pack()
        self.createWidgets()
        self.grid(padx=20, pady=20)
        #initialize light array coefficient matrix
        a11 = np.array([1,1,0,1,0,0,0,0])
        a12 = np.array([1,1,1,0,0,0,0,0])
        a13 = np.array([0,1,1,0,1,0,0,0])
        a21 = np.array([1,0,0,1,0,1,0,0])
        a23 = np.array([0,0,1,0,1,0,0,1])
        a31 = np.array([0,0,0,1,0,1,1,0])
        a32 = np.array([0,0,0,0,0,1,1,1])
        a33 = np.array([0,0,0,0,1,0,1,1])
        self.coeff_mat = np.array([a11,a12,a13,a21,a23,a31,a32,a33])
        #for changing behavior of button presses
        self.solved = False
                
    def createWidgets(self):
        self.light_state = np.zeros(8)
        floors = [i for i in range(8)]
        xPos = 0
        yPos = 0
        #create dict of buttons to press and draw them 
        self.button = {}
        for floor in floors:
            if(yPos == 3):
                xPos = xPos + 1
                yPos = 0
            if(yPos == 1 & xPos == 1):
                yPos = 2
            if self.light_state[floor] == 0:
                self.button[floor] = tk.Button(self, width=3, text=floor+1, 
                                               padx = 5, pady=5, bg='tomato',
                    command = lambda f=floor: self.pressed(f))
                self.button[floor].grid(row=xPos, column =yPos)
            elif self.light_state[floor] == 1:
                self.button[floor] = tk.Button(self, width=3, text=floor+1,
                                               padx = 5, pady=5, bg='tomato',
                    command = lambda f=floor: self.pressed(f))
                self.button[floor].grid(row=xPos, column =yPos)
            yPos = yPos +1
        
        #draw solution button
        yPos = 1
        xPos = 3
        self.SOLVE = tk.Button(self, text='SOLVE', fg='black',
                    command=self.solve).grid(row = xPos, column = yPos,
                                             padx = 5, pady=5)
        yPos = 0 
        xPos = 4
        #create dict of buttons for output and draw them 
        self.output = {}
        for floor in floors:
            if(yPos == 3):
                xPos = xPos + 1
                yPos = 0
            if(yPos == 1 and xPos == 5):
                yPos = 2
            if self.light_state[floor] == 0:
                self.output[floor] = tk.Button(self, width=3, text=floor+1, 
                                               padx = 5, pady=5, bg='tomato')
                self.output[floor].grid(row=xPos, column =yPos)
            elif self.output[floor] == 1:
                self.button[floor] = tk.Button(self, width=3, text=floor+1, 
                                               padx = 5, pady=5, bg='powder blue')
                self.output[floor].grid(row=xPos, column =yPos)
            yPos = yPos +1

        #create reset and quit buttons
        yPos = 1
        xPos = xPos + 1
        self.RESET = tk.Button(self, text='RESET', fg='green',
                    command=self.reset).grid(row = xPos, column = yPos,
                                             padx = 5, pady=5,)
        xPos = xPos + 1
        self.QUIT = tk.Button(self, text='QUIT', fg='tomato',
                    command=root.destroy).grid(row = xPos, column = yPos,
                                               padx = 5, pady=5,)
        
    def solve(self):
        #solve using method adapted from 
        #https://mathworld.wolfram.com/LightsOutPuzzle.html
        self.solved = True
        #solve system of equations in real number space
        temp = np.linalg.solve(self.coeff_mat, 1-self.light_state)
        #convert to fractions
        sol_frac = [Fraction(x).limit_denominator() for x in temp]
        #reduce fractions by gcd of denominator
        sol_gcd = np.gcd.reduce([x.denominator for x in sol_frac])
        #find only those buttons which need to be pressed odd # of times
        #rounding used because floats are dumb
        solution = np.rint(temp*sol_gcd % 2)
        #update output buttons
        for floor in range(8): 
            if solution[floor] == 0:
                self.output[floor].configure(bg='tomato')
            elif solution[floor] == 1:
                self.output[floor].configure(bg='powder blue')
        self.solved = True
            

    def reset(self):
        #reset output buttons and return behavior to original
        floors = [i for i in range(8)]
        for floor in floors:
            self.output[floor].configure(bg='tomato')
            self.button[floor].configure(bg='tomato')
        self.light_state = np.zeros(8)
        self.solved = False


    def pressed(self, index):
        #update buttons either individually (if not solved yet)
        if not self.solved:
            if self.button[index].cget('bg') == 'powder blue':   # Check current color
                self.button[index].configure(bg='tomato')
                self.light_state[index] = 0
            elif self.button[index].cget('bg') == 'tomato':   # Check current color
                self.button[index].configure(bg='powder blue')
                self.light_state[index] = 1
        #or update in groups as in the puzzle (if solved)
        if self.solved:
            self.light_state[np.where(self.coeff_mat[index])] =  1-self.light_state[np.where(self.coeff_mat[index])]
            for floor in np.where(self.coeff_mat[index])[0]:
                if self.button[floor].cget('bg') == 'powder blue':   # Check current color
                    self.button[floor].configure(bg='tomato')
                    self.light_state[floor] = 0
                elif self.button[floor].cget('bg') == 'tomato':   # Check current color
                    self.button[floor].configure(bg='powder blue')
                    self.light_state[floor] = 1

root = tk.Tk()

#get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width/5)
window_height = int(screen_height/2)
#fix to center and resize based on screen
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


#create grid for window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#set title
root.title('TOA Puzzle Solver')

#run
app = Application(master=root)
app.mainloop()