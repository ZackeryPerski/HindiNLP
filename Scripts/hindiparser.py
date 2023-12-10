import pandas as pd
import unittest
import re

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
verb_supports = []

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

def parseAdjectives(words):
    global adjectives
    unparsedWords = words
    while len(unparsedWords) > 0:
        current_word = unparsedWords[-1]
        try:
            adjectives.index(current_word)
            unparsedWords.pop()
        except ValueError:
            return unparsedWords
    return []

def parseObjectAndDescription(words):
    global objects, adjectives
    '''
        #returns a list of unparsed words, failure_state (as a bool), int index pointing to the word that failed. if no failure this is -1.

        if you manage to parse everything here without failure, this means that what was parsed instead was the adj_phrase+subject part of the derivation, outside of this function
        There is already an if statement that checks for this, just return an empty list.
    '''
    unparsedWords = words
    fault_position = -1
    if len(unparsedWords)>0:
        current_word = unparsedWords[-1]
        try:
            objects.index(current_word)
            unparsedWords.pop()
        except ValueError:
            return (unparsedWords, False, fault_position) #More words left to parse, but the first word is not an object word, meaning that this is a lambda transition out of OBJECT_AND_DESCRIPTION in the grammar.
    
    return (parseAdjectives(unparsedWords), False, -1)

    '''Looking at the grammar sheet, we're right linear for most things, so we'll be deriving and popping from the end of the list, as arriving at words what don't belong to a certain section tells us when we're done with that section.
        e.g. when we look at words[len(words)-1] === the last word, if this word is not an object, we stop deriving object, and we do NOT pop the word. If there is no object at all, then don't parse anything, and return.
        if there is at least one object, pop the object words off, then start trying to derive adjectives. Once you are out of adjectives, return the current list of unparsed words.
    '''


def parseAdverbPhrase(words):
    global adverbs
    unparsedWords = words
    fault_position = -1
    while len(unparsedWords)>1:
        current_word=unparsedWords[-1]
        try:
            adverbs.index(current_word)
            unparsedWords.pop()
        except ValueError:
            return (unparsedWords, False, fault_position)
    return ([], True, 0)

def parseAdverbFrequency(words):
    global frequency_adverbs
    unparsedWords = words
    fault_position = -1
    while len(unparsedWords)>1:
        current_word=unparsedWords[-1]
        try:
            frequency_adverbs.index(current_word)
            unparsedWords.pop()
        except ValueError:
            return (unparsedWords, False, fault_position)
    return ([], True, 0)




def validSentenceStructure(words):
    global subjects, objects, verbs, adverbs, frequency_adverbs, adjectives, time, manner
    '''
        Parsing strategy: There are four required productions needed to have a complete formal present tense sentence:
        1. Subject.
        2. Verb.
        3. A word indicative of present tense.
        4. Proper punctuation.

        3 out of 4 of these requirements are needed to be performed at the end of the sentence, so our strategy is to derive those first before going into the weeds with recursive productions.
        As we read these productions, we consume the associated characters/words, so that progress is being made.

        Once we have passed these 3 requirements, we dive into potentially recursive statements. The way I intend to handle this will be according to the grammar on the sheet.
        For the recursive portions of the grammar they are linearly recursive, with expansion on the right. That means that it's going to be easier to start consuming from the right, and stopping
        when we've run out of words that fit the particular mold going towards the left. This will also help us spot when certain types of issues occur, such as end of input words.

        This function returns two things partnered together as a tuple: (<bool>pass_status,<string>message)
        This will tell the user if the phrase was correct, or if it was incorrect, what went wrong. 
    '''

    #We start the parser with basic spot checking. There are certain minimal rules to be followed before we seek out recursive parts of the grammar.
    #First check, a formal present tense sentence needs at least 3 words in the form: subject verb tense+punctuation.
    if(len(words)<=2):
        return (False, "A complete formal present tense sentence cannot be framed with less than three words.")
    
    #Second check, the final word needs to be followed by a punctuation mark of some kind.
    lastWord = words[len(words)-1]
    lastSymbol = lastWord[len(lastWord)-1]
    if (not(lastSymbol=="|" or lastSymbol=="?" or lastSymbol=="!")):
        return (False, "A complete sentence needs to end with a full stop '|', a question mark '?', or an exclamation point '!'.")
    lastWord = lastWord[:-1] #We consume the punctuation mark off of the final word.  

    #Third check, the final word needs to be one of the following tense words. These are all of the valid words that represents 'present tense'.
    if(not(lastWord=="है" or lastWord == "हूँ" or lastWord == "हैं" or lastWord == "हो" or lastWord == "ता" or lastWord == "ते" or lastWord == "ती")):
        return (False, "A sentence cannot be in present tense without one of these ending present tense words: 'है' 'हूँ' 'हैं' 'हो' 'ता' 'ते' 'ती'")
    words.pop() #We now consume this word from the stack of words by popping it off the end of the list.

    #Fourth check, the word before the tense word is our second required word component. Unlike prior components, verbs may have a supporting word that plays a similar role to our
    #verbs ending in 'ing'
    try:
        verb_supports.index(words[len(words)-1]) #If non-existent, it's fine. but if it does exist, then we pop it off and move on.
        words.pop() #Removes the verb_supports word from the end of the derivation. I've been told there is only ever 1 of these after a verb, hense the non-recursion here. 
    except ValueError:
        print("No verb_supports, moving on.")
    try:
        manner.index(words[len(words)-1])
        words.pop() #Consumes the manner word from the string.
    except ValueError:
        print("No manner words, moving on.")
    try:
        verbs.index(words[len(words)-1]) #Checks to see if the word exists within the list of verbs. If this doesn't throw a ValueError Exception, then it exists, and we continue.
        words.pop()
    except ValueError:
        return (False, "A complete sentence requires at least one verb (with optional verb manner and assist word), placed before the tense word in the sentence.")
    #At this point, we have passed all of the easy checks, and have potentially 1 or more words left to check.

    #At this step we may complete, as there is a lot of overlap between an object and it's description and a subject and it's description.
    #If it's actually an adj_phrase and subject and not an adj_phrase and an object, we would be out of words by the time it's done parsing.
    words, failed, position = parseObjectAndDescription(words) #returns a list of unparsed words.
    if(failed):
        return (False, "There was an issue at position: "+str(position)+" during the parsing of Object and Description.")
    if(len(words)==0):
        return (True, "Parsing successful.")
    
    #Continue. Since len>0, this means that there are still words to go. Next is to check for singular manner again.
    try:
        manner.index(words[len(words)-1])
        words.pop() #Consumes the manner word from the string.
    except ValueError:
        print("No manner words, moving on.")
    if(len(words)==0):
        return (False, "Manner cannot precede the adjective phrase and the subject.")
    
    #Continue. Next check is to see if there are time words. When describing time, you only use one word, so no need for a function.
    try:
        time.index(words[len(words)-1])
        words.pop() #consumes the time word from the string.
    except ValueError:
        print("No time words, moving on.")
    if(len(words)==0):
        return (False, "Time cannot precede the adjective phrase and the subject.")
    
    #Continue. Next check to see if we have an adverb phrase to remove.
    words, failed, position = parseAdverbPhrase(words)
    if(len(words)==0):
        return (False, "Adverbs cannot precede the adjective phrase and the subject.")
    if(failed):
        return (False, "Parsing failed at position: "+position+" during parsing of the adverb phrase.")
    
    #Continue. There's some instances where we have a stem for the adverbs for timing.
    words, failed, position = parseAdverbFrequency(words)
    if(len(words)==0):
        return (False, "Frequency adverbs cannot precede advective phrase and the subject.")
    if(failed):
        return (False, "Parsing failed at postion: "+position+" during parsing of the adverbs for frequency.")
    
    #At this point, we only have subject and adj_phrases left to parse out. A subject is always a single word, so we'll use try method.
    try:
        subjects.index(words[len(words)-1])
        words.pop()
    except ValueError:
        return (False, "Subject expected at position:"+str(len(words)-1)+". Saw: "+words[-1]+", instead.")
    if(len(words)==0):
        return (True, "Parsing Successful.")
    
    #Parse out final leading adjectives.
    words = parseAdjectives(words)
    if(len(words)==0):
        return (True, "Parsing Successful.")
    else:
        return (False, "Adjective phrase expected at position:"+str(len(words)-1)+". Saw: "+words[-1]+", instead.")
    



def loadWords():
    #TODO: Test this function.
    global subjects, objects, verbs, adverbs, frequency_adverbs, adjectives, time, manner, verb_supports
    dataframe = pd.read_csv('Automata.csv',skip_blank_lines=True)
    dataset = dataframe.values
    print(dataset.shape)
    dataset = dataset.T
    print(dataset.shape)
    objects=dataset[0].tolist()
    subjects.append(dataset[1].tolist())
    subjects.append(objects)
    adjectives=dataset[2].tolist()
    verbs=dataset[3].tolist()
    adverbs=dataset[4].tolist()
    time=dataset[5].tolist()
    manner=dataset[6].tolist()
    frequency_adverbs=dataset[7].tolist()
    verb_supports = dataset[8].tolist()
    return


def isHindi(sentence):
    words = sentence.split(" ")
    status, message = validSentenceStructure(words)
    evaluation = "Parsing Succssful" if status else "Parsing Failed: " + message
    print(evaluation)
    return status


class TestStringMethods(unittest.TestCase):

    def test_real_sentence1(self):
        self.assertTrue(isHindi("वह घर पर है|"))

    #def test_real_sentence2(self):
    #    self.assertTrue(isHindi())

    #def test_real_sentence3(self):
    #    self.assertTrue(isHindi())
    
    def test_real_sentence4(self): #passed.
        self.assertTrue(isHindi("सूरज उगता है|"))

    def test_real_sentence5(self):
        self.assertTrue(isHindi("बच्चे खेल रहे हैं|"))

    def test_real_sentence6(self):
        self.assertTrue(isHindi("महिलाएँ बाज़ार में खरीदारी करती हैं|"))

    def test_real_sentence7(self):
        self.assertTrue(isHindi("कुत्ता भोंक रहा है|"))

    def test_real_sentence8(self):
        self.assertTrue(isHindi("बच्चों ने गाना गाया|"))

    def test_real_sentence9(self):
        self.assertTrue(isHindi("मेरे दोस्त पार्क में खेल रहे हैं|"))

    def test_real_sentence10(self):
        self.assertTrue(isHindi("वह खुशी से हंस रहा है|"))

    def test_bad_sentence1(self):
        self.assertFalse(isHindi("मैंने सूरज खरीदती|"))

    def test_bad_sentence2(self):
        self.assertFalse(isHindi("घर में बाज गा रही है|"))

    def test_bad_sentence3(self):
        self.assertFalse(isHindi("पेड़ पर खाना खाया|"))

    def test_bad_sentence4(self):
        self.assertFalse(isHindi("बिल्ली रोती है|"))

    def test_bad_sentence5(self):
        self.assertFalse(isHindi("स्कूल बच्चों खेल रहे हैं|"))

    def test_bad_sentence6(self):
        self.assertFalse(isHindi("बाज़ार महिलाएँ खरीदते हैं|"))

    def test_bad_sentence7(self):
        self.assertFalse(isHindi("कुत्ता गाना गा रहा है|"))

    def test_bad_sentence8(self):
        self.assertFalse(isHindi("बच्चों किताब पढ़ते हैं|"))

    def test_bad_sentence9(self):
        self.assertFalse(isHindi("मेरे पार्क खेलते दोस्त हैं|"))

    def test_bad_sentence10(self):
        self.assertFalse(isHindi("वह हंसी से खुश है|"))

    def test_bad_sentence11(self):
        self.assertFalse(isHindi("मैंने किताब पढ़ी|")) #past tense fail

    def test_bad_sentence12(self):
        self.assertFalse(isHindi("चिड़िया चली गई|")) #past tense fail
    


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
    


