from data_loader import LoadTheData
from solver import SolveTheIntegral
from system_builder import SystemBuilder
from display_solution import ShowTheSolution


import tkinter as tk
import tkinter.font as font



class Interaction:
    def __init__(self, master):
        self.master = master
        font_ = font.Font(size=10, weight='bold')
        self.file = 'model.txt'
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.TOP, pady=40)
        button = tk.Button(self.frame, text='Сформулювати умову задачі з файлу "'+self.file+'"',
                           command=self.run, **{'font': font_, 'bg': 'orange', 'bd': 6,
                             'padx': 10, 'pady': 10})
        button.pack(**{'side': tk.RIGHT, 'padx': 10})

    def run(self):
        data = LoadTheData(self.file)
        system = SystemBuilder(data)
        solution = SolveTheIntegral(system)
        ShowTheSolution(solution)


root = tk.Tk()
root.title("Lab 3")
root.geometry("440x280")
app = Interaction(master=root)

root.mainloop()
root.destroy()