from classes import *
from grille1 import *
from main import *
import numpy as np
from sklearn.linear_model import LinearRegression
scores = []
for i in range(5):
    monde = Monde(25,25)
    x = []
    y = []
    for j in range(100):
        x.append(j)
        y.append(len(monde.Moutons))
        monde.activite_moutons()
        
    x,y = np.array(x),np.array(y)
    x,y = x.reshape(-1,1),y.reshape(-1,1)
    model = LinearRegression()
    model.fit(x,y)
    a = model.score(x,y)
    scores.append(a)
        
