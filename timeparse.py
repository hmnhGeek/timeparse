import dateparser
from teach_me import *

class timeparse():

    ''' AUTHOR: Himanshu Sharma
        Imported modules: dateparser, teach_me (by Himanshu Sharma) '''

    def __init__(self):
        pass

    def time_string(self):
        ''' Basically a string which you pass to this
            module to deduce time from it. For example:
            'I was there 10 min ago.' is a time_string.'''

    def give_control(self, time_string):

        print "This isn't the time you were expecting? If not click 'y'. (y/n) "
        ch = raw_input().upper()

        if ch == "Y":
            phrase_error = raw_input("Which phrase do you think might have caused this error: ")

            if phrase_error.upper() in time_string.upper():
                teach_me.teach(phrase_error)
    
    def time_words(self, time_string):
        ''' Returns a tuple of the form (2 D array, 1 D array).
            Where 2D array contains indexes of direct words and indirect words.
            And 1D array contains the list of all the words in the time_string.'''
        
        direct_words, indirect_words = teach_me.load()

        detected = [[], []] # basicly to store indices of the words above.
        # 0th index stores direct_words and 1st index stores the indirect_words.
        
        words = time_string.split(" ")

        for word in words:
            for direct_word in direct_words:
                if direct_word in word.upper():
                    detected[0].append(words.index(word))
            for indirect_word in indirect_words:
                if indirect_word in word.upper():
                    detected[1].append(words.index(word))
        return detected, words

    def index_of_specials(self, array):
        ''' Returns the index of special words in words array.
            Special words are 'tomorrow' and 'yesterday'.'''
        
        for i in array:
            if "TOMORROW" in i.upper():
                return array.index(i)
            if "YESTERDAY" in i.upper():
                return array.index(i)

    def find_time(self, time_string):
        ''' Prints time which the algorithm deduces from the time_string. '''
        
        print " --------My Results--------"
        print
        try:
            teach_me.help_from_proxies(time_string)
        except:
            pass
        if not teach_me.proxies_worked:
            try:
                teach_me.what_I_learnt(time_string)
            except:
                pass
            
            if not teach_me.learning_worked:
                
                indexes, words = self.time_words(time_string)
                direct = indexes[0]
                indirect = indexes[1]
                investigate_further = True
                
                specialIndex = self.index_of_specials(words)
                try:
                    main_string = words[specialIndex] + ' ' + words[specialIndex+1] + ' ' + words[specialIndex+2] + ' ' +words[specialIndex+3]
                    date = str(dateparser.parse(main_string))[0:11]
                    time = str(dateparser.parse(words[specialIndex+2] + ' ' +words[specialIndex+3]))[11:]
                    print date + time

                    investigate_further = False
                except:
                    pass

                if investigate_further:
                    for i in direct:
                        if "NOW" in words[i].upper():
                            print dateparser.parse("now")
                        elif "AGO" in words[i].upper():
                            print dateparser.parse(words[i-2]+' '+words[i-1]+" ago")
                        else:
                            if i == 0:
                                main_string = words[0] + ' '+ words[1]
                            elif i == len(words)-1:
                                main_string = words[i-1] +  ' '+ words[i]
                            else:
                                main_string = words[i-1]+ ' '+ words[i]
                            
                            print dateparser.parse(main_string)

                    for i in indirect:
                        if words[i].upper() == "EVENING":
                            print dateparser.parse("6 pm")
                        elif words[i].upper() == "MORNING":
                            print dateparser.parse("6 am")
                        else:
                            print dateparser.parse("2 pm")
                            
                self.give_control(time_string)

    def self_destruct(self):
        teach_me.doomsday_self_destruct()
     
timeparse = timeparse()
