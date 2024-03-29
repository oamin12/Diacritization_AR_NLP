#Imports
import pickle

def segment_sentences(sentence: str):
        words = sentence.split()
        res = []
        for word in words:
            if word in ['.']:
                res.append(word)
            else:
                if len(word) == 1:
                    res.append('S')
                else:
                    new_word = ''
                    begin = False
                    for i in range(0, len(word)):
                        if word[i] in ['.']:
                            if i == 0:
                                x = 'B'
                                new_word = word[i] + x
                                begin = True
                            else:
                                x = new_word[:-1] + 'E'
                                new_word = x + word[i]
                        elif i== 0:
                            if not begin:
                                new_word += 'B'
                        elif i == len(word)-1:
                            new_word += 'E'
                        else:
                            new_word += 'I'
                    res.append(new_word)
        return (' '.join(res)).strip()


class FeatureExtraction:
    
    def __init__(self):
            self.diacritics = set() #set
            self.diacritic2id = {} #dict
            self.arabic_letters = set() #set
            self.dictionary = {}
            
    def load_dataset(self):
        with open('./pickles/diacritics.pickle', 'rb') as file:
            self.diacritics = pickle.load(file)

        with open('./pickles/diacritic2id.pickle', 'rb') as file:
            self.diacritic2id = pickle.load(file)

        with open('./pickles/arabic_letters.pickle', 'rb') as file:
            self.arabic_letters = pickle.load(file)
        
        for letters in self.arabic_letters:
            self.dictionary[letters] = [0 for i in range(15)]
    
    
    def load_segmented_sentences(self, directory, filename):
        with open('./Dataset/' +directory+'/'+filename+'_stripped.txt','r', encoding='utf-8') as file:
            segmented_sentences = file.readlines()
            
        with open('./Dataset/' +directory+'/'+filename+'_segmented.txt', "w", encoding='utf-8') as file:
            for sentence in segmented_sentences:
                x = segment_sentences(sentence.strip())
                file.write(x + '\n')
            
    def get_letter_dictionary_from_file(self, path = './Dataset/training/train_words_replaced.txt'):
        
        with open(path, 'r', encoding='utf-8') as file:
            train_replace = file.readlines()
        list_of_words = []
        for sentence in train_replace:
            list_of_words.append(sentence.strip())

        for word in list_of_words:
            for i in range(len(word)):
                if word[i] in self.arabic_letters:
                    if word[i] not in self.dictionary:# if the letter is not in the dictionary (mesh mohem awy laken mesh damen el dataset be amana)
                        self.dictionary[word[i]] = [0 for i in range(15)]
                    if i+1 < len(word):
                        if word[i+1] in self.diacritics:
                            self.dictionary[word[i]][self.diacritic2id[word[i+1]]] = 1
                        elif word[i+1] == '١':
                            self.dictionary[word[i]][9] = 1
                        elif word[i+1] == '٢':
                            self.dictionary[word[i]][11] = 1
                        elif word[i+1] == '٣':
                            self.dictionary[word[i]][13] = 1
                        elif word[i+1] == '٤':
                            self.dictionary[word[i]][8] = 1
                        elif word[i+1] == '٥':
                            self.dictionary[word[i]][10] = 1
                        elif word[i+1] == '٦':
                            self.dictionary[word[i]][12] = 1
                        elif word[i+1] not in self.diacritics:
                            self.dictionary[word[i]][14] = 1
            
        for key in self.dictionary:
            self.dictionary[key] = ''.join(map(str, self.dictionary[key]))
            
        with open('./pickles/letter_diacritics_appearance.pickle', 'wb') as file:
            pickle.dump(self.dictionary, file)
                
        return self.dictionary
        
    def get_letter_dictionary_from_sentence(self, sentence):
        #split the sentence into words
        list_of_words = sentence.split()
        
        for word in list_of_words:
            for i in range(len(word)):
                if word[i] in self.arabic_letters:
                    if word[i] not in self.dictionary:# if the letter is not in the dictionary (mesh mohem awy laken mesh damen el dataset be amana)
                        self.dictionary[word[i]] = [0 for i in range(15)]
                    if i+1 < len(word):
                        if word[i+1] in self.diacritics:
                            self.dictionary[word[i]][self.diacritic2id[word[i+1]]] = 1
                        elif word[i+1] == '١':
                            self.dictionary[word[i]][9] = 1
                        elif word[i+1] == '٢':
                            self.dictionary[word[i]][11] = 1
                        elif word[i+1] == '٣':
                            self.dictionary[word[i]][13] = 1
                        elif word[i+1] == '٤':
                            self.dictionary[word[i]][8] = 1
                        elif word[i+1] == '٥':
                            self.dictionary[word[i]][10] = 1
                        elif word[i+1] == '٦':
                            self.dictionary[word[i]][12] = 1
                        elif word[i+1] not in self.diacritics:
                            self.dictionary[word[i]][14] = 1
            
        for key in self.dictionary:
            self.dictionary[key] = ''.join(map(str, self.dictionary[key]))
            
        return self.dictionary
                
                
    def get_sentence_diacritics_appearance(self, filepath, save_filename) -> list:
        
        with open(filepath, 'r', encoding='utf-8') as file:
            train_sentences_replace = file.readlines()

        list_of_diacritics_appearance_in_sentences = []
            
        list_of_sentences = []
        for sentence in train_sentences_replace:
            list_of_sentences.append(sentence.strip())
        print("5555", len(list_of_sentences))
        for sentence in list_of_sentences:
            string_of_diacritics_appearance_in_sentence = ""
            for letter in sentence:
                if letter in self.arabic_letters:
                    string_of_diacritics_appearance_in_sentence += self.dictionary[letter]+" "
                else:
                    string_of_diacritics_appearance_in_sentence += '0'*14+'1'+" "
            list_of_diacritics_appearance_in_sentences.append(string_of_diacritics_appearance_in_sentence.strip())
        
        with open('./pickles/' + save_filename + '.pickle', 'wb') as file:
            pickle.dump(list_of_diacritics_appearance_in_sentences, file)
        print("6666", len(list_of_diacritics_appearance_in_sentences))
        return list_of_diacritics_appearance_in_sentences
