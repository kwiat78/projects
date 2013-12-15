#-*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from gi.repository import Gtk, Gdk
import math
from mpl_toolkits.mplot3d import Axes3D

import cairo

W = []

def sigm(x):
    return 1/(1+np.exp(-x))

def dsigm(x):
    a = 1/(1+np.exp(- x))
    return a*(1-a)


def rotate(S, l, m, a, b):
    
    x = S[0][0]+l*np.cos(a)+np.cos(b)*m
    #b=a+b#+np.pi
    y = S[1][0]+l*np.sin(a)+np.sin(b)*m
    N = np.array([[x],[y]])
    return (N+l+m)/(2*(l+m))

def rotate_2(S, l, m, a, b):
    
    Fx = S[0] +l*np.cos(a)
    Fy = S[1] -l*np.sin(a)
    F = (Fx,Fy)
    
    Nx = Fx +m*np.cos(b)
    Ny = Fy -m*np.sin(b)
    
    N = (Nx,Ny)
    return F,N


class GrafWidget(Gtk.DrawingArea):
    """Widget pozwalający na tworzenie czarno-białych obrazków o rozmiarze
    12x16 pixelów. Aby rysować należy przesuwać kursor gdy wciśnięty jest 
    lewy lub prawy przycisk myszki. lewy przycisk rysuje czarnym, prawy białym.
    
    """
    
    def __init__(self, net, start, l, m):
        """ Konstruktor
        
        active -- czy sygnały mają być obsługiwane.
        
        
        """
        Gtk.DrawingArea.__init__(self)
        self.connect("draw",self.draw_event_cb)
        self.net  = net
        self.start  = start
        self.end  = start
        self.next  = start
        self.l = l
        self.m = m
        self.a = self.l+ self.m
       # self.ends = []
       # self.nexts = []

        self.set_events(  Gdk.EventMask.BUTTON_PRESS_MASK    
                        | Gdk.EventMask.BUTTON_RELEASE_MASK
                        | Gdk.EventMask.POINTER_MOTION_MASK)
            
        self.connect("button-press-event", self.button_press_event)


        
    
        
    def draw_event_cb(self,widget,cr):
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        self.draw_graph(width, height, cr)
        
    def dra(self,O2):
        self.O2 =O2
        #self.button_press_event(None, None)
        
    def draw_graph(self, width, height, cr):
        """Przerysowuje widget na podstawie tablicy pól.
        
        """
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(1.0, 1.0, 1.0)
        cr.rectangle(0, 0, width , height)
        cr.fill()
        """
        for i in zip(self.ends,self.nexts):
            cr.set_source_rgba(0, 0, 0)
        
            cr.move_to(*(self.start+np.array([200,200])).tolist());
            cr.line_to(*i[0].tolist());
            cr.stroke();
            cr.move_to(*i[0].tolist());
            cr.set_source_rgba(0, 1, 0)
            cr.line_to(*i[1].tolist());
            cr.stroke();
        
        """
        
        
        
        cr.set_source_rgba(0, 0, 1)
        
        cr.move_to(300,0);
        cr.line_to(300,800);
        cr.stroke();
        
        cr.set_source_rgba(0, 0, 1)
        
        cr.move_to(0,400);
        cr.line_to(600,400);
        cr.stroke();
        
        cr.set_source_rgba(0, 0, 0)
        
        cr.move_to(*self.start.tolist());
        cr.line_to(*self.end.tolist());
        cr.stroke();
        cr.move_to(*self.end.tolist());
        cr.set_source_rgba(0, 1, 0)
        cr.line_to(*self.next.tolist());
        cr.stroke();
        """
        a,b = rotate_2(np.array([300,400]),self.l,self.m,np.pi/4,np.pi/2)
        cr.set_source_rgba(1, 0, 0)
        cr.move_to(300,400);
        cr.line_to(*a.tolist());
        cr.stroke();
        cr.line_to(*b.tolist());
        cr.stroke();
        """
        for i in self.O2:
            #print i
            #print (i[0]*600-300)+300, -(i[1]*600-300)+400
            cr.arc((i[0]*self.a*2-self.a)+300, -(i[1]*self.a*2-self.a)+400, 5, 0, 2*np.pi)
            cr.fill()
            
    
    def button_press_event(self, sender, event):
        
        X, Y=(event.x-300+self.a)/(2*self.a), (-event.y+400+self.a)/(2*self.a)
        #for i in self.O2:
        print event.x, event.y
        print (X,Y)   
        L = self.net.out_m(np.array([[X],[Y]]))
        """
            a = ((i[0]-0.2)/0.6)*np.pi
            b = ((i[1]-0.2)/0.6)*2*np.pi
        
        
            self.start=np.array([0,0])
            n,e = rotate_2(self.start,self.l, self.m,a,b)
            #print (n,e)
            self.ends  += [e+np.array([200,200])]#*10
            self.nexts += [n+np.array([200,200])]#*10
        
        """
    #    L = self.net.out([X,Y])
        print L
        a = ((L[0][0]-0.1)/0.8)*2*np.pi
        b = ((L[1][0]-0.1)/0.8)*2*np.pi
        print (a/np.pi*180,b/np.pi*180)
        #print (X,Y),(a,b)
        
        self.start=np.array([300,400])
        e,n = rotate_2([300,400],self.l, self.m,a,b)
        #print (n,e)
        
        self.start = self.start#*10
        self.end = np.array(e)#*10
        self.next = np.array(n)#*10
        
        self.queue_draw()


class Net:
    def __init__(self, nl):
        self.length = len(nl) - 2
        self.layers = []

        for i in xrange(self.length+1):
            self.layers+=[np.random.randn(nl[i]+1, nl[i+1])]
        
    def out(self,x):
        for l in self.layers:
            x = np.array([1]+x.tolist())
            x = sigm(np.dot(l.transpose(),x))
        return x

    def out_m(self,x):
        self.i=[]
        self.s=[]
        self.o=[]
        for l in self.layers:
            x = np.array([[1]]+x.tolist())
            self.i += [x]
            y = np.dot(l.transpose(),x)
            self.s += [y]
            z = sigm(np.dot(l.transpose(),x))
            self.o += [z]
            x =z
        return x
    
    def lern(self,E,C,T):
        print self.layers
        for t in xrange(T):
            
            if t % 10000==0:
                print t
                A = map(lambda x,y:(self.out_m(x)-y)**2,E,C)
                W.append( sum(sum((A))))
            
            
            self.d=[]
            u = np.random.randint(0,len(E))
            o = self.out_m(E[u])
            
           # print "^^", self.o
            
            err = o-C[u]
            delta = err*o*(1-o)
            self.d =[delta]
            #print delta
            
            
            #for oo,l in enumerate(reversed(self.layers)):
            for oo in xrange(self.length,0,-1):
                
 #               for ooo in  self.o:
#                    print ooo
                
                #print oo
                
                
                #print oo
                #print "(",delta , self.layers[oo].transpose() ,")"#,delta ,")"
                #err = np.dot(delta,self.layers[oo].transpose())
                
                #print "d_t" , delta.transpose()
                #print "l_",oo,self.layers[oo].transpose()
                
                err = np.dot(delta.transpose(),self.layers[oo].transpose())
                
                err = np.array([err[0].take(range(1,len(err[0])))])
                
                
                
                #print "err", err
                #print err
                #print self.length
                #print oo
                #print
                """!!!!!""" 
                y = self.o[oo-1]
                #y = self.o[oo]
               # print "err", err
                #print "y", y
                
                delta = err.transpose()* y*(1-y)
                #print "delta", delta
                #delta = delta.transpose()
                #delta = np.array([delta.take(range(1,len(delta[0])))])
                #delta = delta.transpose()
                self.d = [delta] +self.d 
                #print delta
            #print self.d
         #   print self.d
            
            
            
            for i,l in enumerate(self.layers):
              #   print i
                #print (self.d[i],self.i[i].transpose())
                 self.layers[i] -= 0.01*np.dot(self.d[i],self.i[i].transpose()).transpose()
   
    
d = []
for i in range(11):
    d.append(i*np.pi/10.)
d*=10
print d

e = []
for i in range(11):
    ee= 10*[2*i*np.pi/10.]
    e+=ee

print d
print e




A = np.array(d)  
B = np.array(e)  


A = np.random.rand(10)*np.pi

B = np.random.rand(10)*2*np.pi

Out = map(lambda x,y:rotate(np.array([[0],[0]]),100,50,x,y),A,B)

print Out
#print In
#print Ou


IA = A/np.pi/2*0.8+0.1
IB = B/np.pi/2*0.8+0.1
I = map(lambda x,y:np.array([[x],[y]]),IA,IB)
I1 = map(lambda x,y:np.array([[x]]),IA,IB)
I2 = map(lambda x,y:np.array([[y]]),IA,IB)
#II = map(lambda x,y:[x,y],IA,IB)



N = Net([2,6,3,2])
   
N.lern(Out,I,4800000)
O2 = map(lambda x:N.out_m(x),Out)
print "O2",O2

#print  "Out2",Out2

#N2 = Net([3,10,12,14,1])
#N2.lern(Out2,I2,1000000,0.1)


#print Out

#O =np.array(map(lambda x:x.tolist(),I))
print Out
#O2 =map(lambda x:math.floor(N.out(x)[2]*1000),Out)
#print len(O2)
#print len(set(O2))
#O3 =(map(lambda x:[N.out(x).tolist()[1],N.out(x).tolist()[2]],Out))
#print I

#print Out

#print O3

U = np.array(range(0,len(W)))

#print S
#print W
plt.subplot(311)
plt.plot(U,W,)



U = np.array(range(0,len(A)))
S = map(lambda x:x[0][0],I)
W =  map(lambda x:N.out_m(x)[0][0],Out)
#print S
#print W
plt.subplot(312)
plt.plot(U,S,'r')
plt.plot(U,W,)
U = np.array(range(0,len(B)))
S = map(lambda x:x[1][0],I)
W =  map(lambda x:N.out_m(x)[1][0],Out)

plt.subplot(313)
plt.plot(U,S,'r')
plt.plot(U,W,)
plt.show()


X = np.arange(0,1,0.01)
Y = np.arange(0,1,0.01)
A = []
for i in X:
    
    B = []
    for j in Y:
        s =(N.out_m(np.array([[i],[j]]))[0][0]-0.2)/0.6*np.pi*2
        #s = np.sin(i)*5+np.sin(j)*10
        
        B.append(s)
    
    A +=[B]
#Z = map(lambda x,y:N.out([x,y])[1],X,Y)
Z = np.array(A)

#W = map(lambda x,y:N.out([x,y])[2],X,Y)
#print X
#print Y

#print Z

X,Y = np.meshgrid(X, Y)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X,Y,Z)

plt.show()


#S += (l*(np.cos(alpha)*np.array([0,1])+np.sin(alpha)*np.array([1,0])))



class App():
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("OCR")
        self.window.set_default_size(600,800)
        #vbox = Gtk.VBox()
        #hbox = Gtk.HBox()
        
        
        self.plansza = GrafWidget(N,np.array([0,0]),100,50)
        self.plansza.dra(Out)
        self.window.add(self.plansza)
        self.window.show_all()


if __name__ == "__main__":
    application = App()
    Gtk.main()

print np.dot(np.array([[1],[2]]).transpose(),np.array([[3],[4]]))

#print N.out_p([1,2])
#print N.In
#print N.O

"""
a = np.array([1,2])
a = a.reshape(2,1)
b = np.array([[1,2],[2,3],[3,4]])
print a
print b
print sigm(np.dot(b,a))
"""
 
        