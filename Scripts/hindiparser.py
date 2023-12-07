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
    #SUBJECT ADJ_PHRASE OBJECT VERB
    return False

def structure2():
    #SUBJECT VERB OBJECT
    return False

def structure3():
    #SUBJECT VERB
    return False

def structure4():
    #ADJ_PHRASE SUBJECT AD_VERB_FREQUENCY OBJECT VERB
    return False

def structure5():
    #SUBJECT AD_VERB_FREQUENCY AD_VERB_PHRASE OBJECT VERB
    return False

def structure6():
    #SUBJECT AD_VERB_FREQUENCY AD_VERB_PHRASE TIME OBJECT VERB
    return False

def structure7():
    #SUBJECT AD_VERB_FREQUENCY AD_VERB_PHRASE TIME MANNER OBJECT VERB
    return False

def loadWords():
    print("To be implemented")

def isHindi(sentence):
    return structure1() or structure2() or structure3() or structure4() or structure5() or structure6() or structure7()


class TestStringMethods(unittest.TestCase):

    def test_real_sentence1(self):
        self.assertTrue(isHindi("वह घर पर है"))

    def test_real_sentence2(self):
        self.assertTrue(isHindi("मैंने किताब पढ़ी"))

    def test_real_sentence3(self):
        self.assertTrue(isHindi("चिड़िया चली गई"))
    
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
    


