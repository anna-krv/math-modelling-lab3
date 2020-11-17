from data_loader import LoadTheData
from solver import SolveTheIntegral
from system_builder import SystemBuilder
from display_solution import ShowTheSolution


import tkinter as tk
import tkinter.font as font
from tkinter import ttk


class Interaction:
    def __init__(self, master):
        self.master = master
        font_ = font.Font(size=10, weight='bold')
        self.file_1 = 'model.txt'
        self.init = 'init.txt'
        self.boun = 'boun.txt'

        self.tabControl = ttk.Notebook(self.master)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Model')
        self.tabControl.add(self.tab2, text='Domain')
        self.tabControl.add(self.tab3, text='Conditions')
        self.tabControl.add(self.tab4, text='Modelling')

        self.tabControl.pack(expand=1, fill="both")

        ''' Model Tab'''
        tk.Label(self.tab1, text="Choose Model type:").grid(column=0,row=0,padx=30,pady=30)

        ModelType = tk.StringVar(self.tab1)
        ModelType.set("L1, G1")  # default value

        dropdown1 = tk.OptionMenu(self.tab1, ModelType, "L1, G1", "L2, G2", "L3, G3")
        dropdown1.grid(column=1,row=0)

        tk.Label(self.tab1, text="Choose the function:").grid(column=0,row=2,padx=30,pady=30)

        func = tk.StringVar(self.tab1)
        func.set("f1(x)")  # default value

        dropdown2 = tk.OptionMenu(self.tab1, func, "f1(x)", "f2(x)", "f3(x)")
        dropdown2.grid(column=1,row=2)


        ''' Domain Tab'''
        tk.Label(self.tab2, text="Space time conditions").grid(column=0,row=0,padx=30,pady=30)
        tk.Label(self.tab2, text="End time:").grid(column=0,row=1)
        end_time = tk.Entry(self.tab2, width=10)
        end_time.grid(column=1,row=1)
        tk.Label(self.tab2, text="Coordinates:").grid(column=0,row=2,padx=30,pady=30)

        self.dim = tk.IntVar() # dim for dimensions or the chosen coordinates
        rad1 = tk.Radiobutton(self.tab2, text='(x1)', value=1, variable=self.dim)
        rad2 = tk.Radiobutton(self.tab2, text='(x1,x2)', value=2, variable=self.dim)
        btn = tk.Button(self.tab2, text="OK", command=self.set_a_b)
        rad1.grid(column=0, row=3)
        rad2.grid(column=1, row=3)
        btn.grid(column=2, row=3, padx=30)

        ''' Conditions Tab '''
        # self.frame = tk.Frame(self.master) # sorry, i ruined your button :) (having troubles with setting up the button decor: font etc.)
        # self.frame.pack(side=tk.TOP, pady=40)
        button = tk.Button(self.tab3, text='Сформулювати умову задачі з файлу "'+self.file_1+'"',
                           command=self.run)#, **{'font': font_, 'bg': 'orange', 'bd': 6, 'padx': 10, 'pady': 10})
        button.grid(column=0,row=0,padx=30,pady=30)
        # button.pack(**{'side': tk.TOP, 'padx': 10})

        ''' Modelling Tab '''
        tk.Label(self.tab4, text='Number of coordinates (x,0) for modelling func u0').grid(column=0,row=0,padx=30,pady=30)
        self.u0_amount = tk.Spinbox(self.tab4, from_=0, to=20, width=5)
        self.u0_amount.grid(column=1,row=0)
        btn = tk.Button(self.tab4, text="OK", command=self.set_u0)
        btn.grid(column=2, row=0, padx=30)

        tk.Label(self.tab4, text='Number of coordinates (x, t) for modelling func M_Gamma').grid(column=0, row=10, padx=30, pady=30)
        self.M_Gamma_amount = tk.Spinbox(self.tab4, from_=0, to=20, width=5)
        self.M_Gamma_amount.grid(column=1, row=10)
        btn = tk.Button(self.tab4, text="OK", command=self.set_M_Gamma)
        btn.grid(column=2, row=10, padx=30)

    def set_a_b(self): # TODO: this method for input a, b
        tk.Label(self.tab2, text="You have chosen " + str(self.dim.get())).grid(column=0, row=4, padx=30, pady=30)

    def set_u0(self): # TODO: this method gonna create matrix of u0 coordinates for input
        tk.Label(self.tab4, text="You have chosen " + str(self.u0_amount.get()) + " number of coords").grid(column=0, row=2, padx=30, pady=30)

    def set_M_Gamma(self): # TODO: this method gonna create matrix of u0 coordinates for input
        tk.Label(self.tab4, text="You have chosen " + str(self.M_Gamma_amount.get()) + " number of coords").grid(column=0, row=11, padx=30, pady=30)

    def run(self):
        data = LoadTheData(self.file_1,self.init,self.boun)
        system = SystemBuilder(data)
        solution = SolveTheIntegral(system)
        ShowTheSolution(solution)


root = tk.Tk()
root.title("Lab 3")
root.geometry("600x400")
app = Interaction(master=root)

root.mainloop()
root.destroy()
