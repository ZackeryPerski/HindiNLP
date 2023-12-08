import pandas as pd
import unittest

'''
Things that can be null:
subject
object
But not both...
'''

subjects = []
objects = []
verbs = []
adverbs = []
frequency_adverbs = []
adjectives = []
time = []
manner = []


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


def validSentenceStructure(words):
    #This is the largest sentence structure.
    if(len(words)==1):
        return (False, "A complete sentence cannot be framed with a single word.")
    lastWord = words[len(words)-1]
    lastSymbol = lastWord[len(lastWord)-1]
    if (not(lastSymbol=="|" or lastSymbol=="?")):
        return (False, "A complete sentence needs to end with a full stop '|' or a question mark '?'")
    lastWord.pop() 
    if(not(lastWord=="है" or lastWord == "हूँ" or lastWord == "हैं" or lastWord == "हो" or lastWord == "ता" or lastWord == "ते" or lastWord == "ती")):
        return (False, "A sentence cannot be in present tense without one of these ending present tense words: 'है' 'हूँ' 'हैं' 'हो' 'ता' 'ते' 'ती'")
    words.pop()#removes the last word which at this point contained a proper ending for the sentence and was a present tense word. The rest of the sentence is now considered.
    #At this point we need to start checking individual words agains the structure.


def loadWords():
    global subjects, objects, verbs, adverbs, frequency_adverbs, adjectives, time, manner
    dataframe = pd.read_csv('Automata.csv',skip_blank_lines=True)
    dataset = dataframe.values
    objects=dataset[0]
    subjects.append(dataset[1])
    subjects.append(objects)
    adjectives=dataset[2]
    verbs=dataset[3]
    adverbs=dataset[4]
    time=dataset[5]
    manner=dataset[6]
    frequency_adverbs=dataset[7]
    return


def isHindi(sentence):
    words = sentence.split(" ")
    return validSentenceStructure(words)


class TestStringMethods(unittest.TestCase):

    def test_real_sentence1(self):
        self.assertTrue(isHindi("वह घर पर है"))

    def test_real_sentence2(self):
        self.assertTrue(isHindi("मैंने किताब पढ़ी")) #past tense fail

    def test_real_sentence3(self):
        self.assertTrue(isHindi("चिड़िया चली गई")) #past tense fail
    
    def test_real_sentence4(self):
        self.assertTrue(isHindi("सूरज उगता है"))

    def test_real_sentence5(self):
        self.assertTrue(isHindi("बच्चे खेल रहे हैं"))

    def test_real_sentence6(self):
        self.assertTrue(isHindi("महिलाएँ बाज़ार में खरीदारी करती हैं"))

    def test_real_sentence7(self):
        self.assertTrue(isHindi("कुत्ता भोंक रहा है"))

    def test_real_sentence8(self):
        self.assertTrue(isHindi("बच्चों ने गाना गाया"))

    def test_real_sentence9(self):
        self.assertTrue(isHindi("मेरे दोस्त पार्क में खेल रहे हैं"))

    def test_real_sentence10(self):
        self.assertTrue(isHindi("वह खुशी से हंस रहा है"))

    def test_bad_sentence1(self):
        self.assertFalse(isHindi("मैंने सूरज खरीदती"))

    def test_bad_sentence2(self):
        self.assertFalse(isHindi("घर में बाज गा रही है"))

    def test_bad_sentence3(self):
        self.assertFalse(isHindi("पेड़ पर खाना खाया"))

    def test_bad_sentence4(self):
        self.assertFalse(isHindi("बिल्ली रोती है"))

    def test_bad_sentence5(self):
        self.assertFalse(isHindi("स्कूल बच्चों खेल रहे हैं"))

    def test_bad_sentence6(self):
        self.assertFalse(isHindi("बाज़ार महिलाएँ खरीदते हैं"))

    def test_bad_sentence7(self):
        self.assertFalse(isHindi("कुत्ता गाना गा रहा है"))

    def test_bad_sentence8(self):
        self.assertFalse(isHindi("बच्चों किताब पढ़ते हैं"))

    def test_bad_sentence9(self):
        self.assertFalse(isHindi("मेरे पार्क खेलते दोस्त हैं"))

    def test_bad_sentence10(self):
        self.assertFalse(isHindi("वह हंसी से खुश है"))


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
    


