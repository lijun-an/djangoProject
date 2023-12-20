from django.test import TestCase


# Create your tests here.
def func(*args):
    print(args)


func(1, 2, 3, 4)

