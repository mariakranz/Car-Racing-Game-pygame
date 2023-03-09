import pygame
import os
import random
import time

pygame.init()
pygame.display.set_caption('Samochody_gra')

pygame.mixer.init()

szer=400
wys=600
screen=pygame.display.set_mode((szer,wys))

path = "assets"
grafika=pygame.image.load(os.path.join(path, 'logo.jpg'))
grafika2=pygame.image.load(os.path.join(path, 'Droga.png'))

max_tps=70


def napisz(tekst,x,y,rozmiar):
    cz=pygame.font.SysFont("Arial",rozmiar)
    rend=cz.render(tekst,1,(255,0,0))
    screen.blit(rend,(x,y))

lista=('samochod.png','samochod_2.png','samochod_3.png','samochod_4.png')

class Przeszkoda():
    def __init__(self,y):
        self.y=y
        self.szerokosc=50
        self.wysokosc=80
        self.x=random.randint(100,300-self.szerokosc)
        self.ksztalt=pygame.Rect(self.x,self.y,self.szerokosc,self.wysokosc)
        self.los=random.randrange(4)
        self.grafika=pygame.image.load(os.path.join(path,lista[self.los]))     
    def rysuj(self):
        screen.blit(self.grafika,(self.x,self.y))
    def ruch(self,v):
        self.y=self.y+v
        self.ksztalt=pygame.Rect(self.x,self.y,self.szerokosc,self.wysokosc)
    def kolizja(self,player):  
        if self.ksztalt.colliderect(player):
            return True
        else:
            return False

x_gracz=175
y_gracz=500
szer_gracz=50
gracz_grafika=pygame.image.load(os.path.join(path,'samochod_gracz.png'))
gracz=pygame.Rect(x_gracz,y_gracz,szer_gracz,80)
v=10

samochody=[]
samochody.append(Przeszkoda(0))
przyspieszenie=0


clock=pygame.time.Clock()
delta=0.0


punkty=0
copokazuje='menu'


while True:
    delta+=clock.tick()/1000.0
    while delta>1/max_tps: 
        delta-=1/max_tps 
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if copokazuje!='rozgrywka':
                        gracz_grafika=pygame.image.load(os.path.join(path,'samochod_gracz.png'))
                        gracz=pygame.Rect(x_gracz,y_gracz,szer_gracz,80)
                        for s in samochody:
                            samochody.remove(s)
                            samochody.append((Przeszkoda(0)))
                            s.rysuj()
                        copokazuje='rozgrywka'
                        punkty=0
                        przyspieszenie=0
        if copokazuje=='menu':  
            screen.blit(grafika,(0,100))
            napisz("Naciśnij spację, aby zacząć",140,160,20)
            napisz("Omijaj samochody - UWAGA: poruszasz się z coraz większą prędkością",5,500,15)
            napisz("Sterowanie: strzałka w lewo i w prawo / klawisze 'A' i 'D'",5,550,15)
            
        elif copokazuje=='rozgrywka': 
            screen.blit(grafika2,(0,0))
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("assets/Race_Car.mp3")
                pygame.mixer.music.play()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
                if not keys[pygame.K_LEFT] and not keys[pygame.K_a]:
                    if x_gracz+v<300-szer_gracz:
                        x_gracz+=v
                        screen.blit(gracz_grafika,(x_gracz,y_gracz))
                        gracz=pygame.Rect(x_gracz,y_gracz,szer_gracz,80)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if not keys[pygame.K_RIGHT] and not keys[pygame.K_d] :
                    if x_gracz-v>100:
                        x_gracz-=v
                        screen.blit(gracz_grafika,(x_gracz,y_gracz))
                        gracz=pygame.Rect(x_gracz,y_gracz,szer_gracz,80)
            screen.blit(gracz_grafika,(x_gracz,y_gracz))
            for s in samochody:
                s.ruch(8+przyspieszenie)
                s.rysuj()
                if s.kolizja(gracz):
                    copokazuje="koniec"
                    pygame.mixer.music.load("assets/Crash.mp3")
                    pygame.mixer.music.play()
            for s in samochody:
                if s.y>=wys+80:
                    samochody.remove(s)
                    samochody.append((Przeszkoda(0)))
                    punkty+=1
            przyspieszenie+=0.0025
            napisz("Wynik: "+str(punkty),300,10,20)
        elif copokazuje=='koniec':
            screen.fill((0,0,0))
            screen.blit(grafika,(0,100))
            napisz("Niestety przegrywasz",50,240,25)
            napisz("Naciśnij spację, aby zagrać jeszcze raz",80,160,20)
            napisz("Twój wynik to: "+str(punkty),50,270,25)
            napisz("Autor: Maria Kranz",250,570,20)
        pygame.display.update()
  
