#-*- coding: utf-8 -*-
#!/usr/bin/env python


import gtk

from matplotlib.figure import Figure
import numpy as np



from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar


class Net:
    
   
    def __init__(self,E,C):
        self.E = E
        self.C = C
        self.neu = []
        self.perc = []
        #for i in xrange(N):
        #    self.neu += [[[],[],0]]
        self.neu = [[[],[],0]]
        self.neu[0][0] += [0,1]
        self.perc.append(Perceptron2(np.random.randn(3)))
        self.PLAwR(10000,0)
        
        self.neu += [[[0,1],[0],0]]
        self.perc.append(Perceptron2(np.random.randn(4)))
        
        self.PLAwR(10000,1)
        for i,j in enumerate(self.perc):
            print "*",i, j.wagi, "*"
        
        o =  map(lambda x: self.out(x),E)
        print "&",sum((np.array(C)-np.array(o))**2),"&"
        
        self.neu += [[[0,1],[1],0]]
        self.perc.append(Perceptron2(np.random.randn(4)))
        
        self.PLAwR(10000,2)
        for i,j in enumerate(self.perc):
            print "*",i, j.wagi, "*"
        
        o =  map(lambda x: self.out(x),E)
        print "&",sum((np.array(C)-np.array(o))**2),"&"
        
        self.neu += [[[0,1],[2],0]]
        self.perc.append(Perceptron2(np.random.randn(4)))
        
        self.PLAwR(10000,3)
        for i,j in enumerate(self.perc):
            print "*",i, j.wagi, "*"
        
        o =  map(lambda x: self.out(x),E)
        print "&",sum((np.array(C)-np.array(o))**2),"&"
        
        self.neu += [[[0,1],[3],0]]
        self.perc.append(Perceptron2(np.random.randn(4)))
        self.PLAwR(10000,4)
        for i,j in enumerate(self.perc):
            print "*",i, j.wagi, "*"
        
        o =  map(lambda x: self.out(x),E)
        print "&",sum((np.array(C)-np.array(o))**2),"&"
        
        self.neu += [[[0,1],[4],0]]
        self.perc.append(Perceptron2(np.random.randn(4)))
        self.PLAwR(10000,5)
        for i,j in enumerate(self.perc):
            print "*",i, j.wagi, "*"
        
        o =  map(lambda x: self.out(x),E)
        print "&",sum((np.array(C)-np.array(o))**2),"&"
        
        self.neu += [[[0,1],[5],0]]
        self.perc.append(Perceptron2(np.random.randn(4)))
        self.PLAwR(10000,6)
        for i,j in enumerate(self.perc):
            print "*",i, j.wagi, "*"
        
        o =  map(lambda x: self.out(x),E)
        print "&",sum((np.array(C)-np.array(o))**2),"&"
        
        #self.perc.append(Perceptron(np.random.randn(3)))
        
       
       
        
        #for i,j in Edges:
        #   self.neu[j][1].append(i)
            
    def out(self,X):
        for l,i in enumerate(self.neu):
        #  print i[1]
            S = [1]
            for u in i[0]:
                S.append(X[u])
            for u in i[1]:
                S.append(self.neu[u][2])
                
            #S = [1]+i[0]+i[1]
            #print S
            self.neu[l][2]=self.perc[l].out(S)
            print l,S,self.neu[l][2]
        return self.neu[len(self.neu)-1][2]
      
    
    def PLAwR(self, T, i):
        
        t = t_pocket = 0
        s = 1+len(self.neu[i][0])+len(self.neu[i][1])
        w = w_pocket = np.random.randn(s)
        
        self.perc[i] = Perceptron2(w)
        ok_pocket = sum(map(lambda x,y:self.out(x)==y,self.E,self.C)) 
        
        for _ in xrange(T):
            u = np.random.randint(0,len(self.E))
            c = self.out(self.E[u])
            if c==self.C[u]:
                t+=1
                if t>t_pocket:
                    temp = self.perc[i]
                    self.perc[i]=Perceptron2(w)
                    ok = sum(map(lambda x,y:self.out(x)==y,self.E,self.C))
                    if ok>ok_pocket:
                        w_pocket = w
                        t_pocket = t
                        ok_pocket = ok
                    else:
                        self.perc[i] = temp
            else:
                t=0
                Err =self.C[u]-c
                ############
                 
                S = [1]
                for k in self.neu[i][0]:
                    S.append(self.E[u][k])
                for k in self.neu[i][1]:
                    S.append(self.neu[k][2])
                
                #print S
                ###########
                q = np.array(S)
              #  print q
                w += (Err*q)
                
                self.perc[i]=Perceptron2(w)
        #return Perceptron(max_)
        self.perc[i] = Perceptron2(w_pocket)
         
        
        



class Perceptron2:
    """Przechowuje wage i próg, pozwala na obliczenie wartości funkcji 
    aktywującej na zadanej tablicy.
    
    """

    def __init__(self, w):
        """ Konstruktor 
        
        w -- waga
        
        """
        self.wagi = w
        
        
    def out(self, X):
        """Funkcja aktywująca
        
        img -- wejście
        
        """
        #X=[1,img[0],img[1]]
        return 2*(sum(X*self.wagi)>0)-1
        
    

class Perceptron:
    """Przechowuje wage i próg, pozwala na obliczenie wartości funkcji 
    aktywującej na zadanej tablicy.
    
    """

    def __init__(self, w):
        """ Konstruktor 
        
        w -- waga
        
        """
        self.wagi = w
        
        
    def out(self, img):
        """Funkcja aktywująca
        
        img -- wejście
        
        """
        X=[1,img[0],img[1]]
        return 2*(sum(X*self.wagi)>0)-1
   
def PLA(E, C, T):
    """Algorytm uczący
    
    E -- przykłady uczące
    C -- poprawne odpowiedźi
    T -- ilość iteracji
    
    """
    
    t=0
    tmax=0
    max_ = w=np.random.randn(3)
    p = Perceptron(w)
    for _ in xrange(T):
        u = np.random.randint(0,len(E))
        c = p.out(E[u])
        if c==C[u]:
            t+=1
            if t>tmax:
                tmax+=1
                max_ =w
        else:
            t=0
            Err =C[u]-c
            q = np.array([1,E[u][0],E[u][1]])
            w += (Err*q)
            p = Perceptron(w)
    return Perceptron(max_) 



win = gtk.Window()
win.connect("destroy", lambda x: gtk.main_quit())
win.set_default_size(400,300)
win.set_title("Embedding in GTK")

hbox = gtk.HBox()

win.add(hbox)
vbox = gtk.VBox()

hbox.add(vbox)

vbox2 = gtk.VBox()
hbox.add(vbox2)

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

X = np.random.randn(25)+4
Y = np.random.randn(25)-3

X2 = np.random.randn(25)+4
Y2 = np.random.randn(25)+5

X3 = np.random.randn(25)-4
Y3 = np.random.randn(25)+5

X4 = np.random.randn(25)-4
Y4 = np.random.randn(25)-3

a.plot(X,Y,'r+')
a.plot(X2,Y2,'bo')
a.plot(X3,Y3,'r+')
a.plot(X4,Y4,'bo')

E=zip(X,Y)+zip(X2,Y2)+zip(X3,Y3)+zip(X4,Y4)
C=25*[1]+25*[-1]+25*[1]+25*[-1]
#p = PLA(E,C,10000)
p = Net(E,C)

o =  map(lambda x: p.out(x),E)

print C
print o
print "&",sum((np.array(C)-np.array(o))**2),"&"


g = Figure(figsize=(5,4), dpi=100)
b = g.add_subplot(111)

X,Y = -20*np.random.rand(2,10000)+10
E=zip(X,Y)
IX,IY = zip(*filter(lambda x:p.out(x)==1,E))
NX,NY = zip(*filter(lambda x:p.out(x)!=1,E))
print len(IX)
print len(NX)
b.plot(IX,IY,'r+')
b.plot(NX,NY,'bo')

print p.out([1,4])
print p.perc[0].wagi
print p.perc[1].wagi
print p.out([1,4])
print p.perc[0].wagi
print p.perc[1].wagi

#w =  p.wagi
C= np.array(xrange(-10,11,1))
#D = (w[0]+C*w[1])/(-w[2])
print C
#b.plot(C,D)

canvas = FigureCanvas(f)  # a gtk.DrawingArea
toolbar = NavigationToolbar(canvas, win)

canvas2 = FigureCanvas(g)  # a gtk.DrawingArea
toolbar2 = NavigationToolbar(canvas2, win)


vbox.pack_start(canvas)
vbox.pack_start(toolbar, False, False)

vbox2.pack_start(canvas2)
vbox2.pack_start(toolbar2, False, False)

win.show_all()
gtk.main()