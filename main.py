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
        # self.tabControl.add(self.tab4, text='Modelling')

        self.tabControl.pack(expand=1, fill="both")

        ''' Model Tab'''
        tk.Label(self.tab1, text="Choose Model type (operator G):").grid(column=0,row=0,padx=30,pady=30)

        self.ModelType = tk.StringVar(self.tab1)

        model_options = {1: 'H(t-r/c)/(2*pi*c*sqrt(abs(c^2*t^2-r^2)))',
                         2: 'H(t)*sqrt(4*pi*c*t)*exp(-r^2/(4*c*t))'}
        self.ModelType.set(model_options[1])  # default value
        dropdown1 = tk.OptionMenu(self.tab1, self.ModelType, *model_options.values())
        dropdown1.grid(column=1,row=0)

        tk.Label(self.tab1, text="Choose the function y:").grid(column=0,row=2,padx=30,pady=30)

        self.func = tk.StringVar(self.tab1)
        func_options = {1: 't^4+x1^4+x2^4', 2: 't^3+x1^3+x2^3', 3: 't*x1*x2', 4: 'choose from file'}
        self.func.set(func_options[1])  # default value
        dropdown2 = tk.OptionMenu(self.tab1, self.func, *func_options.values())
        dropdown2.grid(column=1,row=2)


        ''' Domain Tab'''
        tk.Label(self.tab2, text="Space time conditions").grid(column=0,row=0,padx=30,pady=30)
        tk.Label(self.tab2, text="End time:").grid(column=0,row=1)
        self.end_time = tk.Entry(self.tab2, width=10)
        self.end_time.insert(0, '1')
        self.end_time.grid(column=1,row=1)
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
        button = tk.Button(self.tab3,
                           text='Сформулювати умову задачі з "'+self.file_1+'",т-ки для поч. умов:"'+self.init+'", крайов. умов.: "'+ self.boun+'"',
                           command=self.run)#, **{'font': font_, 'bg': 'orange', 'bd': 6, 'padx': 10, 'pady': 10})
        button.grid(column=0,row=0,padx=30,pady=30)
        # button.pack(**{'side': tk.TOP, 'padx': 10})



    def set_a_b(self): # TODO: this method for input a, b
        tk.Label(self.tab2, text="You have chosen " + str(self.dim.get())).grid(column=0, row=4, padx=30, pady=30)

    def set_u0(self): # TODO: this method gonna create matrix of u0 coordinates for input
        tk.Label(self.tab4, text="You have chosen " + str(self.u0_amount.get()) + " number of coords").grid(column=0, row=2, padx=30, pady=30)

    def set_M_Gamma(self): # TODO: this method gonna create matrix of u0 coordinates for input
        tk.Label(self.tab4, text="You have chosen " + str(self.M_Gamma_amount.get()) + " number of coords").grid(column=0, row=11, padx=30, pady=30)

    def run(self):
        data = LoadTheData(self.file_1, self.init, self.boun)
        system = SystemBuilder(data, float(self.end_time.get()), self.ModelType.get(), self.func.get())
        solution = SolveTheIntegral(system).solve()
        ShowTheSolution(solution, data)


root = tk.Tk()
root.title("Lab 3")
root.geometry("600x400")
app = Interaction(master=root)

root.mainloop()
root.destroy()
