#-*- coding: utf-8 -*-

from gi.repository import Gtk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt




   
class Perceptron:
    """Przechowuje wage i próg, pozwala na obliczenie wartości funkcji 
    aktywującej na zadanej tablicy.
    
    """

    def __init__(self, w, p):
        """ Konstruktor 
        
        w -- waga
        p -- próg
        
        """
        self.wagi = w
        self.prog = p
        
    def out(self, img):
        """Funkcja aktywująca
        
        img -- wejście
        
        """
        
        return 2*(sum(sum(img*self.wagi))>=self.prog)-1
   
def PLA(E, C, T):
    """Algorytm uczący
    
    E -- przykłady uczące
    C -- poprawne odpowiedźi
    T -- ilość iteracji
    
    """
    
    t=0
    tmax=0
    max_ = w=np.random.randn(16,12)
    max_theta=theta=np.random.randn()
    p = Perceptron(w,theta)
    for _ in xrange(T):
        u = np.random.randint(0,len(E))
        c = p.out(E[u])
        if c==C[u]:
            t+=1
            if t>tmax:
                tmax+=1
                max_ =w
                max_theta = theta
        else:
            t=0
            Err =C[u]-c
            w += (Err*E[u])
            theta -= Err
            p = Perceptron(w,theta)
    return Perceptron(max_,max_theta) 



     
class App:
    """Głowna klasa z GUI i mechanizmem

    """
    def __init__(self):
        """Konstruktor

        """
        self.window = Gtk.Window()
        self.window.set_title("OCR")
        self.window.set_default_size(600,800)
        
        f, ax = plt.subplots()
        
        s = matplotlib.axes.Axes(f,[0.15, 0.1, 0.7, 0.3])
        
        ax =  matplotlib.widgets.Cursor(s)
    
        
        

        
        self.window.connect("delete-event", Gtk.main_quit)

        self.window.show_all()
   
        
if __name__ == "__main__":
    application = App()
    Gtk.main()