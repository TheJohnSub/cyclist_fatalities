from peewee import *
from Incidents import *

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5


