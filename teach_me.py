import pickle, dateparser, os
from difflib import SequenceMatcher

class teach_me():

    ''' AUTHOR: Himanshu Sharma '''

    def __init__(self):
        ''' Initialising two lists containing stored direct_words and indirect_words. '''
        
        self.direct_words = []
        self.indirect_words = []
        self.learning_worked = 0
        self.proxies_worked = 0

    def similar(self, string1, string2):
        ''' Compares two strings and returns the fractional similarity between them. '''
        return SequenceMatcher(None, string1, string2).ratio()

    def load(self):
        ''' Loads all the words in direct_words.dat and indirect_words.dat
            in self.direct_words and self.indirect_words repectively and then
            returns the tuple containing these two lists. '''
        
        dw = open("direct_words.dat", "rb")
        try:
            while True:
                self.direct_words = pickle.load(dw)
        except:
            dw.close()

        idw = open("indirect_words.dat", "rb")
        try:
            
            while True:
                self.indirect_words = pickle.load(idw)
        except:
            idw.close()

        return self.direct_words, self.indirect_words

    def teach(self, time_string, store_it = True):
        ''' Teach the algorithm new phrases so that it can learn from faliures.
            Takes in a time_string whose result was wrong according to timeparse.
            Finds correct time (still depends on dateparser module). '''
        print dateparser.parse(time_string)

        if store_it:
            ch = raw_input("Is this correct? (y/n) ").upper()
            if(ch == "Y"):
                f = open("Phrases.dat", "rb")
                fw = open("temp.dat", "wb")
                try:
                    phrases = []
                    while True:
                        phrases = pickle.load(f)
                        if(time_string not in phrases):
                            phrases.append(time_string)
                        pickle.dump(phrases, fw)
                except:
                    f.close()
                fw.close()
                os.remove("Phrases.dat")
                os.rename("temp.dat", "Phrases.dat")

                print "Next time if this or similar phrase occurs I will parse the correct result."
                print "Thank You."
                
            else:
                print "Sorry, I didn't work upto your expectations."

    def proxify_it(self):
        ''' Stores a proxy phrase for given error phrase. For eg: 'after 10 min' implies
            same thing as 'in 10 min.' so if algorithm has already learnt about 'in 10 min.'
            we can give a proxy phrase for error phrase 'after 10 min' as 'in 10 min.'.'''
        
        print "But I can do one more thing for you to solve this."

        f = open("Phrases.dat", "rb")
        try:
            phrases = []
            while True:
                phrases = pickle.load(f)
        except:
            f.close()
        i= 1
        for phrase in phrases:
            print i, phrase

        print '''If from any of these phrase which I learnt so far, you find something similar to
this phrase then tell me by typing the phrase exactly as I remember it. If you don't type 0.'''
        error_phrase = raw_input("Please enter error phrase: ")
        proxy_phrase = raw_input("Now enter proxy phrase: ")
        if proxy_phrase <> '0':
            
            if proxy_phrase in phrases:
                
                f1 = open("proxy_phrases.dat", "rb")
                f2 = open("temp.dat", "wb")
                try:
                    proxies = {}
                    while True:
                        proxies = pickle.load(f1)
                        proxies.update({error_phrase.upper(): proxy_phrase})
                        pickle.dump(proxies, f2)
                except:
                    f1.close()
                f2.close()
                os.remove("proxy_phrases.dat")
                os.rename("temp.dat", "proxy_phrases.dat")

    def what_I_learnt(self, time_string):
        ''' Extracts out phrases which the algorithm has learnt and finds
            occurrence of similar phrases in the time_string. Finds the correct
            part of time_string which on passing to dateparser.parse() will give
            the correct time. '''
        self.learning_worked = 0
        f = open("Phrases.dat", "rb")
        try:
            phrases = []
            while True:
                phrases = pickle.load(f)
        except:
            f.close()
        
        for i in phrases:
            
            if self.similar(i.upper(), time_string.upper()) > 0.4:
                
                words_in_time_string = time_string.split(" ")
                
                words_in_i = i.split(" ")
                started = False
                main_string = ''
                for word in words_in_time_string:
                    if started and word.upper <> words_in_i[-1].upper():
                        main_string += word + ' '
                    elif word.upper() == words_in_i[0].upper():
                        main_string += word + ' '
                        started = True
                    elif word.upper() == words_in_i[-1].upper():
                        main_string += word
                        started = False
                
                self.teach(main_string, False)
                self.learning_worked = 1
                ch = raw_input("Correct?? (y/n) ").upper()
                if ch == "N":
                    self.proxify_it()
                else:
                    self.proxies_worked = 1

    def help_from_proxies(self, time_string):
        ''' Basically extracts each proxy phrases and uses what_I_learnt()
            when the correct phrase is found. '''
        
        self.proxies_worked = 0
        f = open("proxy_phrases.dat", "rb")
        try:
            proxies = {}
            while True:
                proxies = pickle.load(f)
        except:
            f.close()

        for proxy in proxies:
            
            if self.similar(proxy, time_string.upper()) > 0.6:
                words_in_proxy = proxy.split(' ')
                words_in_time_string = time_string.split(' ')
                
                started = False
                main_string = ''
                for word in words_in_time_string:
                    if started and word.upper <> words_in_proxy[-1].upper():
                        main_string += word + ' '
                    elif word.upper() == words_in_proxy[0].upper():
                        main_string += word + ' '
                        started = True
                    elif word.upper() == words_in_proxy[-1].upper():
                        main_string += word
                        started = False
                
                words_in_main_string = main_string.split(' ')
                words_in_proxies_proxy = proxies[proxy].split(' ')
                words_in_proxies_proxy = [z.upper() for z in words_in_proxies_proxy]
                commons = list(set(words_in_proxy).intersection(words_in_proxies_proxy))
                
                for common in commons:
                    words_in_proxies_proxy[words_in_proxies_proxy.index(common)] = words_in_main_string[words_in_proxy.index(common)]
                
                main = ''
                for k in range(len(words_in_proxies_proxy)):
                    if k == len(words_in_proxies_proxy) -1:
                        main += words_in_proxies_proxy[k]
                    else:
                        main += words_in_proxies_proxy[k] + ' '
                #print main
                self.what_I_learnt(main)

    def doomsday_self_destruct(self):
        ''' Self destruct simply deletes Phrases.dat and creates a new blank Phrases.dat. '''
        print "You are going to delete everything which I learnt so far. Continue?? (y/n) "
        ch = raw_input().upper()
        if ch == "Y":
            os.remove("Phrases.dat")
            f = open("Phrases.dat", "wb")
            pickle.dump([], f)
            f.close()
            os.remove("proxy_phrases.dat")
            f = open("proxy_phrases.dat", "wb")
            pickle.dump({}, f)
            f.close()
        print "I am a dumb machine now."
                
teach_me = teach_me()
