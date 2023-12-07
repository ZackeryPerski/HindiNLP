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
            if(test(phrase)):
                print("That was a valid phrase!")
                print("")#TODO
            else:
                print("That was an invalid phrase!")
                print("")

def test():
    return structure1() or structure2() or structure3() or structure4() or structure5() or structure6() or structure7()

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



if __name__=="__main__":
    introduction()
    mainFunction()
    


