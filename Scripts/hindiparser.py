import pandas as pd
import unittest

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
    print("This project was created by Akarsh, Hiranmai, Uma, and Zack for Foundations of Automata at Eastern Michigan University")
    print("This is a simple parser, designed to check the validity of statements made for a subset of Hindi, particularly focused on present tense sentence structures.")
    print("When prompted for a sentence you will need to write in Hindi. The program will evaluate your sentence and tell you if your sentence was valid.")
    print("When you want to quit, type the word 'quit' on the prompt screen.")

def mainFunction():
    while True:
        print("Enter a phrase in present tense Hindi to be checked")
        phrase = input("Phrase: ")
        phrase = phrase.strip() #removes leading and trailing whitespace.
        if(phrase == 'quit'):
            quit()
        else:
            if(inputPhrases(phrase)):
                print("That was a valid phrase!")
            else:
                print("That was an invalid phrase!")

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
    #Here we had at least one object word, we're going to remove additional object words here, if there are any before attempting to remove adjectives.
    while len(unparsedWords)>0:
        current_word = unparsedWords[-1]
        try:
            objects.index(current_word)
            unparsedWords.pop()
        except ValueError:
            break
    return (parseAdjectives(unparsedWords), False, -1)


def parseAdverbPhrase(words):
    global adverbs
    unparsedWords = words
    fault_position = -1
    while len(unparsedWords)>0:
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
    while len(unparsedWords)>0:
        current_word=unparsedWords[-1]
        try:
            frequency_adverbs.index(current_word)
            unparsedWords.pop()
        except ValueError:
            return (unparsedWords, False, fault_position)
    return ([], True, 0)


def parseSubjectString(words):
    '''Sometimes subjects are represented by multiple words. We need at least one subject however to finish parsing. A failure here is significantly meaningful.'''
    global subjects, adjectives
    unparsedWords = words
    fault_position = -1
    if len(unparsedWords)>0:
        current_word = unparsedWords[-1]
        try:
            subjects.index(current_word)
            unparsedWords.pop()
        except ValueError:
            return (unparsedWords, True, len(unparsedWords)-1) #fault out here. At this point we need to parse at least one subject word to proceed.
    #Here we had at least one subject word, we're going to remove additional object words here, if there are any before attempting to remove adjectives.
    while len(unparsedWords)>0:
        current_word = unparsedWords[-1]
        try:
            subjects.index(current_word)
            unparsedWords.pop()
        except ValueError:
            break
    return (unparsedWords, False, -1)


def parseComplexVerbString(words):
    global verb_supports, manner, verbs
    #Step1 Remove verb stem, if it exists.
    try:
        verb_supports.index(words[len(words)-1]) #If non-existent, it's fine. but if it does exist, then we pop it off and move on.
        words.pop() #Removes the verb_supports word from the end of the derivation. I've been told there is only ever 1 of these after a verb, hense the non-recursion here. 
    except ValueError:
        print("No verb_supports, moving on.")
    #Step2 Remove manner word, if it exists.
    try:
        manner.index(words[len(words)-1])
        words.pop() #Consumes the manner word from the string.
    except ValueError:
        print("No manner words, moving on.")
    #Step3 Remove at least one verb.
    try:
        verbs.index(words[len(words)-1]) #Checks to see if the word exists within the list of verbs. If this doesn't throw a ValueError Exception, then it exists, and we continue.
        words.pop()
    except ValueError:
        return (words, True, len(words)-1)
    #Step4 Remove any additional verbs utilizing a while loop.
    try:
        while len(words)>0:
            current_word = words[-1]
            verbs.index(current_word)
            words.pop()
    except ValueError:
        return (words, False, -1)


def validSentenceStructure(words):
    global subjects, objects, verbs, adverbs, frequency_adverbs, adjectives, time, manner
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
    words, fault, faultPos = parseComplexVerbString(words)
    if(len(words)==0):
        return (False, "No subject present in the sentence.")
    if(fault):
        return (False, "No verb present in string, expected verb at position: "+str(faultPos)+". Saw the word: "+words[faultPos]+" instead.")
    
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
    words, fault, faultPos = parseSubjectString(words)
    if(len(words)==0):
        return (True, "Parsing Successful.")
    if fault:
        return (False, "Parsing failed at position: "+str(faultPos)+" at word: "+words[faultPos])
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
    dataset = dataset.T #Makes it so that the dataset is actually in column format.
    objects=dataset[0].tolist()
    subjects=dataset[1].tolist()+objects
    adjectives=dataset[2].tolist()
    verbs=dataset[3].tolist()
    adverbs=dataset[4].tolist()
    time=dataset[5].tolist()
    manner=dataset[6].tolist()
    frequency_adverbs=dataset[7].tolist()
    verb_supports = dataset[8].tolist()
    return


def isHindiSentence(sentence):
    words = sentence.split(" ")
    status, message = validSentenceStructure(words)
    evaluation = "Parsing Succssful" if status else "Parsing Failed: " + message
    print(evaluation)
    return status

def inputPhrases(input):
    try:
        input = input.strip()
    except:
        return (False, "Input was not a valid string.")
    #fails if input is garbage.
    sentences = []
    current_sentence = ""
    #construct individual sentences from the larger input.
    for i in range(len(input)):
        char = input[i]
        current_sentence = current_sentence + char
        if char == "|" or char == "?" or char == "!":
            sentences.append(current_sentence)
            current_sentence = ""
    #test individual sentences
    for sentence in sentences:
        sentence = sentence.strip()
        status = isHindiSentence(sentence)
        if status == False:
            return False
    return True



class TestStringMethods(unittest.TestCase):

    def test_real_sentence1(self): #passed. 
        self.assertTrue(inputPhrases("वह घर पर है|"))

    def test_real_sentence2(self): #passed
        self.assertTrue(inputPhrases("स्कूल बच्चों खेल रहे हैं|"))

    def test_real_sentence3(self): #passed.
        self.assertTrue(inputPhrases("वह टीवी स्क्रीन देख रहा है|"))
    
    def test_real_sentence4(self): #passed.
        self.assertTrue(inputPhrases("सूरज उगता है|"))

    def test_real_sentence5(self): #passed.
        self.assertTrue(inputPhrases("बच्चे खेल रहे हैं|"))

    def test_real_sentence6(self): #passed!
        self.assertTrue(inputPhrases("महिलाएँ बाज़ार में खरीदारी करती हैं|"))

    def test_real_sentence7(self): #passed.
        self.assertTrue(inputPhrases("कुत्ता भोंक रहा है|"))

    def test_real_sentence9(self): #passed.
        self.assertTrue(inputPhrases("मेरे दोस्त पार्क में खेल रहे हैं|"))

    def test_real_sentence10(self): #passed.
        self.assertTrue(inputPhrases("वह खुशी से हंस रहा है|"))

    def test_real_paragraph1(self): #passed.
        self.assertTrue(inputPhrases("वह खुशी से हंस रहा है| मेरे दोस्त पार्क में खेल रहे हैं|"))

    def test_real_paragraph2(self):
        self.assertTrue(inputPhrases("वह सुंदर दिखती है| वह स्वादिष्ट खाना बनाती है| वह अपनी पढ़ाई में बहुत मेहनत करती है| मैं कुछ नहीं करता हूँ|"))

    def test_bad_sentence1(self): #passed
        self.assertFalse(inputPhrases("मैंने सूरज खरीदती|"))

    def test_bad_sentence2(self): #passed
        self.assertFalse(inputPhrases("घर में बाज गा रही है|"))

    def test_bad_sentence3(self): #passed
        self.assertFalse(inputPhrases("पेड़ पर खाना खाया|"))

    def test_bad_sentence4(self): #passed
        self.assertFalse(inputPhrases("बिल्ली रोती है|"))

    def test_bad_sentence5(self): #passed
        self.assertFalse(inputPhrases("बाज़ार महिलाएँ खरीदते हैं|"))

    def test_bad_sentence6(self): #passed
        self.assertFalse(inputPhrases("कुत्ता गाना गा रहा है|"))

    def test_bad_sentence7(self): #passed
        self.assertFalse(inputPhrases("बच्चों किताब पढ़ते हैं|"))

    def test_bad_sentence8(self): #passed
        self.assertFalse(inputPhrases("मेरे पार्क खेलते दोस्त हैं|"))

    def test_bad_sentence9(self): #passed
        self.assertFalse(inputPhrases("वह हंसी से खुश है|"))

    def test_bad_sentence10(self): #passed
        self.assertFalse(inputPhrases("मैंने किताब पढ़ी|"))

    def test_bad_sentence11(self): #passed
        self.assertFalse(inputPhrases("चिड़िया चली गई|"))

    def test_bad_sentence12(self): #passed.
        self.assertFalse(inputPhrases("बच्चों ने गाना गाया|"))
    


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
    


