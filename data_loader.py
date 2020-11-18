"""Read data from file."""
import numpy as np
import math

def construct_lambda(expr):
    header = 'lambda x1,x2,t: '
    return eval(header+expr)
def array_convector(array):
    return array.astype(np.float)

class LoadTheData:
    def __init__(self, file, init, boun):
        with open(file) as f:
            area_o = f.readline().split('#')
            print(area_o)
            array = area_o[0].split(',')
            self.a, self.b, self.c, self.d = [float(x) for x in array]
            print(self.a, self.b, self.c, self.d)
            #t = area_o[1]

            #self.T = float(t)
            #print(self.T)
            self.Func = str(area_o[1]) #construct_lambda(str(area_o[2]))
            print(str(self.Func))
        with open(init) as i_p:
            self.i_points = [(float(x), float(y), 0.) for x,y in [s.replace('(', '').split(',') for s in
                                                     i_p.readline().split(')')[:-1]]]
            print(self.i_points)
            #init_points = i_points.astype(np.float)
            #print(str(init_points))
            
        
        with open(boun) as b_p:
   
            self.b_points = [(float(x), float(y), float(t)) for x, y, t in [s.replace('(', '').split(',') for s in
                                                     b_p.readline().split(')')[:-1]]]
            print(str(self.b_points))
            #boun_points = b_points.astype(np.float) 
            #print(str(boun_points))