import json
import unittest


def introduction():
    print("Welcome to the Hindi Parser!")
    print("")#TODO
    print("This project was created by Akarsh, Hiranmai, Uma, and Zack for Foundations of Automata at Eastern Michigan University")
    print("")#TODO
    print("This is a simple parser, designed to check the validity of statements made for a subset of Hindi, particularly focused on present tense sentence structures.")
    print("")#TODO
    print("When prompted for a sentence you will need to write in Hindi. The program will evaluate your sentence and tell you if your sentence was valid.")
    print("")#TODO
    print("When you want to quit, type the word 'quit' on the prompt screen.")
    print("")#TODO

def mainFunction():
    while True:
        print("Enter a phrase in present tense Hindi to be checked")
        print("")#TODO
        phrase = input("Phrase/#TODO: ")
        phrase = phrase.strip() #removes leading and trailing whitespace.
        if(phrase == 'quit'):
            quit()
        else:
            if(isHindi(phrase)):
                print("That was a valid phrase!")
                print("")#TODO
            else:
                print("That was an invalid phrase!")
                print("")



def structure1():
    return False

def structure2():
    return False

def structure3():
    return False

def structure4():
    return False

def structure5():
    return False

def structure6():
    return False

def structure7():
    return False

def loadWords():
    print("To be implemented")

def isHindi(sentence):
    return structure1() or structure2() or structure3() or structure4() or structure5() or structure6() or structure7()


class TestStringMethods(unittest.TestCase):

    def test_real_sentence1(self):
        self.assertTrue(isHindi())

    def test_real_sentence2(self):
        self.assertTrue(isHindi())

    def test_real_sentence3(self):
        self.assertTrue(isHindi())
    
    def test_real_sentence4(self):
        self.assertTrue(isHindi())

    def test_real_sentence5(self):
        self.assertTrue(isHindi())

    def test_real_sentence6(self):
        self.assertTrue(isHindi())

    def test_real_sentence7(self):
        self.assertTrue(isHindi())

    def test_real_sentence8(self):
        self.assertTrue(isHindi())

    def test_real_sentence9(self):
        self.assertTrue(isHindi())

    def test_real_sentence10(self):
        self.assertTrue(isHindi())

    def test_bad_sentence1(self):
        self.assertFalse(isHindi())

    def test_bad_sentence2(self):
        self.assertFalse(isHindi())

    def test_bad_sentence3(self):
        self.assertFalse(isHindi())

    def test_bad_sentence4(self):
        self.assertFalse(isHindi())

    def test_bad_sentence5(self):
        self.assertFalse(isHindi())

    def test_bad_sentence6(self):
        self.assertFalse(isHindi())

    def test_bad_sentence7(self):
        self.assertFalse(isHindi())

    def test_bad_sentence8(self):
        self.assertFalse(isHindi())

    def test_bad_sentence9(self):
        self.assertFalse(isHindi())

    def test_bad_sentence10(self):
        self.assertFalse(isHindi())


if __name__=='__main__':
    loadWords()
    while True:
        testingEnabled = input("Enter Testing Mode? [y/n]: ")
        if testingEnabled == 'y' or testingEnabled == 'n':
            break
    if testingEnabled == 'y':
        unittest.main()
    else:
        introduction()
        mainFunction()
    


