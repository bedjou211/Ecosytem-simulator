from jeu1_0 import *
import matplotlib.pyplot as plt
import random
import sys
def variations_pop():
    world = Jeu_console(25,25)
    x = []
    y_lions = []
    y_moutons = []
    i = 0
    qui = False
    while i <= 200 :
        x.append(i)
        y_lions.append(len(world.Lions))
        y_moutons.append(len(world.Moutons))
        world.activite_moutons()
        world.activite_lions()
        plt.plot(x,y_moutons,color='green',label="Moutons")
        plt.plot(x,y_lions,color = 'red',label = "Lions")
        plt.title("SIMULATION ECOSYSTMÈME")
        plt.pause(0.05)
        i+= 1
    plt.show()  
