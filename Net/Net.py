#-*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np


class Net:
    
    #def __init__(self, N,Edges):
    def __init__(self,E,C):
        self.neu = []
        self.perc = []
        #for i in xrange(N):
        #    self.neu += [[[],[],0]]
        self.neu = [[[],[],0]]
        self.neu[0][0] += [0,1]
        self.perc.append(Perceptron(np.random.randn(3)))
        P = self.PLA(1000,0)
        
        
        print "*", self.perc, "*"
        
        #for i,j in Edges:
         #   self.neu[j][1].append(i)
            
    def out(self,X):
        for l,i in enumerate(self.neu):
            print i[1]
            S = [1]
            for u in i[0]:
                S.append(X[u])
            for u in i[1]:
                S.append(self.neu[u][2])
                
            #S = [1]+i[0]+i[1]
            #print S
            self.neu[l][2]=self.perc[l].out(S)
        return self.neu[len(self.neu)-1][2]
            #print self.neu
            #print i[0]
            #In = [1,X,]
    
    def PLA(self, T, i):
        
        t=0
        tmax=0
        s = 1+len(self.neu[i][0])+len(self.neu[i][1])
        print s
        
        max_ = w=np.random.randn(s)
    
        #p = Perceptron(w)
        self.perc[i] = Perceptron(w) 
        
        for _ in xrange(T):
            u = np.random.randint(0,len(E))
            c = self.out(E[u])
            if c==C[u]:
                t+=1
                if t>tmax:
                    tmax+=1
                    max_ =w
            else:
                t=0
                Err =C[u]-c
                ############
                 
                S = [1]
                for k in self.neu[i][0]:
                    S.append(E[u][k])
                for k in self.neu[i][1]:
                    S.append(self.neu[k][2])
                
                print S
                ###########
                q = np.array(S)
                print q
                w += (Err*q)
                p = Perceptron(w)
        #return Perceptron(max_)
        self.perc[i] = Perceptron(max_)
         
        
        



class Perceptron:
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
        #return sum(X*self.wagi)
    
#a = Perceptron(np.array([1,0.5,0.5]))
#print a.out([1,-2])

def PLA(E, C, T):
    """Algorytm uczący
    
    E -- przykłady uczące
    C -- poprawne odpowiedźi
    T -- ilość iteracji
    
    """
    
    t=0
    tmax=0
    max_ = w=np.random.randn(len(E[0]))
    
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
            q = np.array(E[u])
            w += (Err*q)
            p = Perceptron(w)
    return Perceptron(max_) 


X = np.random.randn(25)+4
Y = np.random.randn(25)-3

X2 = np.random.randn(25)+4
Y2 = np.random.randn(25)+5

E=zip(X,Y)+zip(X2,Y2)
C=25*[1]+25*[-1]



s = Net(E,C) 
print s.out([6,-2])
print s.out([6,6])
#s.PLA(10000,0)
#print s.neu
#s.out([6,2])
