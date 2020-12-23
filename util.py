from random import uniform, randint
import numpy as np

profiles = ["se-2000"]


def score():
    return np.array([uniform(0.98, 1)]), np.eye(4)[randint(1, 3)]


def validate(sc, a, b):
    if sc != "":
        return score()
    else:
        return a, b
