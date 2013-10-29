#-*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import scipy.misc as sp
import numpy as np
import os
import cairo

class PictureWidget(Gtk.DrawingArea):
    """Widget pozwalający na tworzenie czarno-białych obrazków o rozmiarze
    12x16 pixelów. Aby rysować należy przesuwać kursor gdy wciśnięty jest 
    lewy lub prawy przycisk myszki. lewy przycisk rysuje czarnym, prawy białym.
    
    """
    
    def __init__(self):
        """ Konstruktor
        
        """
        
        Gtk.DrawingArea.__init__(self)
        self.set_events(  Gdk.EventMask.BUTTON_PRESS_MASK    
                        | Gdk.EventMask.BUTTON_RELEASE_MASK
                        | Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect("draw",self.draw_widget) #akcja rysowania
        self.connect("motion_notify_event",self.move) #poruszanie kursorem
        self.connect("button-press-event", self.button_press_event) # przyciskanie
        
        self.len = 50   #długość pola
        self.pola =np.ones((16,12)) #tablica pól
        
    def move(self,sender,event):
        """Metoda wywoływana gdy kursor jest poruszany. Pobiera informacje o 
        jego pozycji i wciśniętym przycisku. Następnie modyfikuje odpowiedno 
        pola i przerysowuje widget.
        
        """
        _,x, y, state = event.window.get_pointer()
        if x < 0 or x >= 600 or y < 0 or y >= 800:
            return
            
        if state & Gdk.ModifierType.BUTTON1_MASK:
            self.pola[(y/50)][(x/50)]=0
            self.queue_draw()
        if state & Gdk.ModifierType.BUTTON3_MASK:
            self.pola[(y/50)][(x/50)]=1
            self.queue_draw()
       
    def draw_widget(self, widget, cr):
        """Przerysowuje widget na podstawie tablicy pól.
        
        """
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(1.0, 1.0, 1.0,1.0)
        cr.rectangle(0, 0, width , height)
        cr.fill()
       
        for y in xrange(16):
            for x in xrange(12):
                self.draw_square(cr,(x*50,y*50))
        self.cairo = cr
        
    
    def button_press_event(self,widget,event):
        """Metoda wywoływana gdy przycisk jest wciskany. Pobiera informacje o 
         wciśniętym przycisku. Następnie modyfikuje odpowiedno 
        pola i przerysowuje widget.
        
        """
        
        X,Y=int(event.x)/50 , int(event.y)/50
        
        if event.button == 1:
            self.pola[Y][X]= 0
        if event.button == 3:
            self.pola[Y][X]= 1

        self.queue_draw()
                

        
    def draw_square(self, cr, node):
        """Rysuje jeden pixel.
        
        node -- (x,y) współrzędne pixela do narysowania
        
        """
        x, y = node
        X,Y = int(x)/50,int(y)/50
        
        up =(X*50, Y*50)
        
        cr.rectangle(up[0],up[1],50,50)
        if not self.pola[Y][X]: 
            cr.set_source_rgba(0,0,0)
        else:
            cr.set_source_rgba(255,255,255)
        cr.fill()


def img_read(path):
    """ Pobiera obrazek (*.png) na podstawie ścieżki i przekształca go do 
    odpowiedniej formy.
    
    path -- ścieżka do obrazka.
    
    """ 
    x=sp.imread(path).astype(float)
    y = x[:,:,0]
    y = (y==255)*1
    return y    

def img_save(path, img):
    """ Zapisuje tablice jako obrazek (*.png) i zapisuje jako path. 
    
    
    path -- nazwa obrazka
    img -- tablica do zapisania
    
    """ 
    img *= 255
    s = [[[i,i,i,255] for i in j] for j in img]
    sp.imsave(path,s)

def img_noise(p,img):
    """Dodaje do obrazka szum. Na podstawie p-stwa p zmienia niezależnie każdy
    element tablicy. Losuje zmienną z rozkładu U(0,1) jeśli wylosowana liczba 
    jest mniejsza od p zmienia wartość w tablicy 0->1 1->0.
    
    p -- p-stwo zmienienia pojedynczego elementu.
    img -- tablica, do której dodawany będzie szum. 
    
    """
    for i in xrange(16):
        for j in xrange(12):
            s=np.random.random()
            if(s<p):
                img[i][j] = 1-img[i][j]            
                                                                                                                           
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
     
    tmax = t = 0
    max_ = w = np.random.randn(16,12)
    max_theta=theta=np.random.randn()
    p = Perceptron(w,theta)
    for _ in xrange(T):
        u = np.random.randint(0,len(E))
        c = p.out(E[u])
        if c==C[u]:
            t+=1
            if t>tmax:
                tmax+=1
                max_ = w
                max_theta = theta
        else:
            t=0
            Err =C[u]-c
            w += (Err*E[u])
            theta -= Err
            p = Perceptron(w,theta)

    return Perceptron(max_,max_theta) 


class App:
    """Głowna klasa z GUI 
    
    """
    def __init__(self):
        """Konstruktor

        """
        self.window = Gtk.Window()
        self.window.set_title("OCR")
        self.window.set_default_size(600,800)
        self.window.connect("delete-event", Gtk.main_quit)
        
        hbox2 = Gtk.HBox()
        hbox = Gtk.HBox()
        vbox = Gtk.VBox()
        
        self.matryca = PictureWidget()
        self.matryca.set_size_request(600,800)
        self.window.set_resizable(False)
        
        load = Gtk.Button("Otwórz")
        load.connect("clicked",self.open_file)
        
        save = Gtk.Button("Zapisz")
        save.connect("clicked",self.save_file)
        
        noise = Gtk.Button("Zaszum")
        noise.connect("clicked",self.add_noise)
        
        reset = Gtk.Button("Wyczyść")
        reset.connect("clicked",self.clear)
        
        lern = Gtk.Button("Naucz")
        lern.connect("clicked",self.lern)
        
        check = Gtk.Button("Sprawdź")
        check.connect("clicked",self.check)
        
        self.wynik = Gtk.Label()
        self.wynik.set_markup("<b>Rozpoznano:</b>")
        self.wynik.set_justify(Gtk.Justification.CENTER)
        
        self.img=np.ones((16,12))
        self.put_img()
        
        
        hbox2.pack_start(load, 0, 1, 0)
        hbox2.pack_start(save, 0, 1, 0)
        hbox2.pack_start(noise, 0, 1, 0)
        hbox2.pack_start(reset, 0, 1, 0)
        hbox2.pack_start(lern, 0, 1, 0)
        hbox2.pack_start(check, 0, 1, 0)
        hbox.add(self.matryca)
        hbox.pack_start(self.wynik, 0, 1, 0)
        vbox.add(hbox2)
        vbox.add(hbox)
        
        
        self.window.add(vbox)
        
        self.window.show_all()
        
        self.lern(None)
    
           
    def open_file(self, sender):
        """Otwiera dialog, który pozwala na wybór obrazka który bedzie
        wyświetlany w ramce.
        
        """
        dialog = Gtk.FileChooserDialog("Otwórz",self.window ,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            path=dialog.get_filename()
            self.img = img_read(path)
            self.put_img()
        dialog.destroy()
        
    def save_file(self, sender):
        """Otwiera dialog, który pozwala na zapis obrazka który jest
        wyświetlany w ramce.
        
        """
        dialog = Gtk.FileChooserDialog("Zapisz",self.window ,
        Gtk.FileChooserAction.SAVE,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            path=dialog.get_filename()
            img_save(path,self.matryca.pola)
        dialog.destroy()
    
    def clear(self, sender):
        """Ustawia obrazek w ramce na pusty.(same jedynki)
        
        """
        self.img=np.ones((16,12))
        self.put_img()
    
    def check(self,sender):
        """Oblicza funkcje aktywujące wszystkich perceptronów. I wypisuje nazwy 
        tych, które zwrócą 1. 
        
        """
        x = "Rozpoznano:"
        s = map(lambda c: self.P[c].out(self.img),xrange(26))
        for i,j in enumerate(s):
            if j==1:
                x += ("\n"+chr(i+ord('A')))
        self.wynik.set_markup("<b>"+x+"</b>")
        self.wynik.set_justify(Gtk.Justification.CENTER)
        
    
    def lern(self,sender):
        
        """Uczy wszystkie preceptrony.
        
        """
        E = []
        C = map(lambda _:[],xrange(26))
        
        for i in xrange(26):
            ls = os.listdir("./letters/"+chr(i+ord('A')))
            ls = filter(lambda x: x.endswith(".png"),ls)

            for k in xrange(26):
                C[k]+= len(ls)*[2*(k == i)-1]
            
            for j in ls:
                E.append(img_read("./letters/"+chr(i+ord('A'))+"/"+j))
                
        self.P = map(lambda x: PLA(E,C[x],1000),xrange(26))  
    
    def add_noise(self, sender):
        """Dodaje szum do aktualnego obrazka.
        
        """
        img_noise(0.005,self.img)
        self.put_img()
    
    def put_img(self):
        """Przerysowuje obrazek.
        
        """
        self.matryca.pola=self.img
        self.matryca.queue_draw()

        
if __name__ == "__main__":
    application = App()
    Gtk.main()