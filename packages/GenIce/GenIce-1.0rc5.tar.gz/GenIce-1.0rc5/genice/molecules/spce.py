# coding: utf-8
import math
import numpy as np


oh = 0.10000
hangle = 109.47 * math.pi / 180 / 2
mass=18
ohz = oh * math.cos(hangle)
ohy = oh * math.sin(hangle)
oz  = -ohz*2/mass


sites = np.array([[0, 0,oz],
                  [0, ohy,ohz+oz],
                  [0,-ohy,ohz+oz]]) # nm

labels = ["Ow","Hw","Hw"]
name = "SOL"
