from .exceptions import *
import random

class GuessAttempt(object):
    pass
    def __init__(self, guess, hit=None, miss=None):
      if hit and miss:
        raise InvalidGuessAttempt()
      
      self.guess = guess
      self.hit = hit
      self.miss = miss
        
      
    def is_hit(self):
      if self.hit == None:
        self.hit = False
            
      return self.hit
        
      
    def is_miss(self):
      if self.miss == None:
        self.miss = False
            
      return self.miss
  

class GuessWord(object):
    pass
    def __init__(self, answer):
      if len(answer) == 0:
        raise InvalidWordException()
   
      self.answer = answer
      self.masked = GuessWord.mask_word(answer)
    
    
    def perform_attempt(self, guess):
      if len(guess) != 1:
        raise InvalidGuessedLetterException
        
        
      self.masked = self.uncover_word(guess)
      attempt = GuessAttempt(guess)
      if guess.lower() in self.answer.lower():
        attempt.hit = True
      else:
        attempt.miss = True
            
      return attempt
    
    
    def uncover_word(self, guess):
      uncover_word = ''    
      for i in range(0, len(self.answer)):
        if guess.lower() == self.answer[i].lower():
          uncover_word += guess.lower()
        else:
          uncover_word += self.masked[i]
      return uncover_word
    
    
    @staticmethod
    def mask_word(answer):
      return '*' * len(answer)
      


class HangmanGame(object):
    pass
    WORD_LIST = ['rmotr', 'python', 'awesome']
  
    def __init__(self, list_of_words=[], number_of_guesses=5):
      self.list_of_words = list_of_words
      self.number_of_guesses = number_of_guesses
      self.remaining_misses = number_of_guesses
      self.previous_guesses = []
      if self.list_of_words == []:
        self.word = GuessWord(HangmanGame.select_random_word(HangmanGame.WORD_LIST))
      else:
        self.word = GuessWord(HangmanGame.select_random_word(self.list_of_words))
      
      
    @classmethod
    def select_random_word(cls, list_of_words):
      if list_of_words == []:
        raise InvalidListOfWordsException
      else:
        return random.choice(list_of_words)
  
    def is_won(self):
      return self.word.answer == self.word.masked
  
    def is_lost(self):
      return self.remaining_misses == 0 and self.is_won() == False
  
    def is_finished(self):
      return self.is_lost() or self.is_won()
  
    def guess(self, letter):
      if self.is_finished():
        raise GameFinishedException()
    
      self.previous_guesses.append(letter.lower())
      attempt = self.word.perform_attempt(letter)
      if attempt.is_miss():
        self.remaining_misses -= 1
            
      print(self.word.answer + ':' + self.word.answer)
      if self.is_won():
        raise GameWonException()
      elif self.is_lost():
        raise GameLostException()
        
      return attempt
