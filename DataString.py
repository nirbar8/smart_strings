import regex
import pickle
from termcolor import colored
import sys

try:
    from config import category_scores, type_of_extraction_scores, scores_weights
except ImportError:
    print('Could not import config.py')
    sys.exit(1)

try:
    from config import suspicious_words_path
except ImportError:
    print('Warning: Could not import suspicious_words_path from config.py. Disabling scoring by suspicious words.')

class DataString:
    def __init__(self, string, type_of_extraction):
        self.string = string
        # remove the 's' at the end (e.g. static_strings -> static_string)
        self.type_of_extraction = type_of_extraction[:-1]
        self.length = len(string)
        # what kind of string is this? (e.g. DLL, URL, etc.)
        self.category = self.category(string)
        self._sus_word = None             # if the string has a suspicious word (e.g. process, virus, etc.)
        self._scores = dict()
        self._eval_scores()               # scores for different aspects of the string
        self.score = self._calc_score()   # overall sus score for the string

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        attr = []
        color = 'white'

        if self.type_of_extraction != 'static':
            attr.append('bold')
        if self.category == 'number':
            color = 'yellow'
        elif self.category == 'IP':
            color = 'yellow'
            attr.append('dark')
        elif self.category == 'URL':
            color = 'green'
        elif self.category == 'URI':
            color = 'green'
            attr.append('dark')
        elif self.category == 'DLL':
            color = 'blue'
        elif self.category == 'DLL_function':
            color = 'cyan'
        elif self.category == 'Text':
            color = 'grey'

        string = self.string
        string = colored(string, color, attrs=attr)
        string += ' ' * (60 - len(self.string))
        string += f'  (score: {self.score*100:.1f})  '
        properties = []
        if self.type_of_extraction != 'static_string':
            properties.append(self.type_of_extraction)
        # TODO: add configuration for verbosity
        # if self._sus_word:
            # properties.append(f'"{self._sus_word}"')
        properties.append(self.category)
        string += '[' + ', '.join(properties) + ']'

        # string += '\n'
        # for key, value in self._scores.items():
        #     string += f'  {key}: {value:.2f}  '

        return string

    @staticmethod
    def category(string):
        '''
        This function determines what kind of string this is.
        Options are: DLL name, DLL function name, URI, URL, Text, IP, number, random string.
        '''

        # number
        if regex.match(r'^\d+$', string):
            return 'number'

        # IP
        if regex.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', string):
            return 'IP'

        # URL
        if regex.match(r'^[A-Za-z]+://[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z]{2,3}[A-Za-z0-9-_:\/?&\.]*$', string):
            return 'URL'

        # URI - contains '/' or '\' (not together)
        if regex.match(r'^\w*(\/|\\)\w*$', string):
            return 'URI'

        # DLL name
        if regex.match(r'^[A-Za-z0-9_]+\.(dll|DLL|Dll)$', string):
            return 'DLL'

        # DLL function name - PascalCase, No spaces, No special characters
        if regex.match(r'^([A-Z][a-z]+)+(A|W)?$', string):
            return 'DLL_function'

        # Text
        if regex.match(r'^[A-Za-z0-9\s-_?!\'"+/=]+$', string) and len(string) > 5:
            return 'Text'

        # Random string
        return 'random'

    @staticmethod
    def _len_score(string):
        '''
        This function measures the length of the string and returns a score from 0 to 1.
        The longer the string, the more likely it is to be meaningful.

        Args:
            string (str): The string to measure.

        Returns:
            float: The score in [0, 1]. 0 is short, 1 is long.
        '''
        from math import tanh
        return tanh((len(string) / 4) - 1)

    @staticmethod
    def _randomness_score(string):
        '''
        This function measures the randomness of the string and returns a score from 0 to 1.
        The more random the string, the less likely it is to be meaningful.
        High score indicate that the string is NOT random.

        Args:
            string (str): The string to measure.

        Returns:
            float: The score in [0, 1]. 0 is random, 1 is not random.
        '''
        if len(string) < 2:
            return 1

        # measure the number of non-alpha characters
        non_alpha = len([c for c in string if not (ord('a') <= ord(
            c) <= ord('z') or ord('A') <= ord(c) <= ord('Z'))])
        non_alpha_percent = non_alpha / len(string)

        # measure the number of changes of types in the string
        chars_types = []
        for c in string:
            if ord('a') <= ord(c) <= ord('z'):
                chars_types.append('lower')
            elif ord('A') <= ord(c) <= ord('Z'):
                chars_types.append('upper')
            elif ord('0') <= ord(c) <= ord('9'):
                chars_types.append('number')
            else:
                chars_types.append('special')

        changes = 0
        for i in range(len(string) - 1):
            if chars_types[i] != chars_types[i + 1]:
                changes += 1
        changes_percent = changes / len(string)

        # average of the two metrics
        return 1 - (non_alpha_percent + changes_percent) / 2

    @staticmethod
    def _category_score(category):
        '''
        This function measures the category of the string to be interesting and meaningful.

        Args:
            category (str): The category of the string.

        Returns:
            float: The score in [0, 1]. 0 is not interesting, 1 is interesting.
        '''
        return category_scores[category]

    @staticmethod
    def _type_of_extraction_score(type_of_extraction):
        '''
        This function measures the type of extraction of the string to be interesting and meaningful.

        Args:
            type_of_extraction (str): The type of extraction of the string.

        Returns:
            float: The score in [0, 1]. 0 is not interesting, 1 is interesting.
        '''
        return type_of_extraction_scores[type_of_extraction]

    @staticmethod
    def _suspicious_text_score(string):
        '''
        This function measures the string to be suspicious and meaningful.

        Args:
            string (str): The string to measure.

        Returns:
            float: The score in [0, 1]. 0 is not suspicious, 1 is suspicious.
            word (str): The word that was found in the string. None if no word was found.
        '''

        try:
            from config import suspicious_words_path
        except ImportError:
            return 0, None

        try:
            words = pickle.load(open(suspicious_words_path, 'rb'))
        except FileNotFoundError:
            print(f'Error: suspicious_words_path is used but "{suspicious_words_path}" not found.')
            sys.exit(1)

        num_words = len(words)
        for i, word in enumerate(words):
            weight = (0.9 * ((num_words - i) / num_words)) ** 2  # words sorted by importance
            if word.lower() in string.lower():
                return weight, word
        return 0, None

    def _eval_scores(self):
        '''
        This function measures different aspects of the string 
        and inserts them into the scores dictionary.
        '''
        if len(self._scores) > 0:
            return

        self._scores['len_score'] = self._len_score(self.string)
        self._scores['randomness_score'] = self._randomness_score(self.string)
        self._scores['category_score'] = self._category_score(self.category)
        self._scores['type_of_extraction_score'] = self._type_of_extraction_score(
            self.type_of_extraction)
        self._scores['suspicous_text_score'], self._sus_word = self._suspicious_text_score(
            self.string)


    @staticmethod
    def weighted_average(scores, weights):
        '''
        This function calculates the weighted average of the scores.

        Args:
            scores (dict): The scores to average.
            weights (dict): The weights of the scores.

        Returns:
            float: The weighted average.
        '''
        return sum([scores[score] * weights[score] for score in scores]) / sum(weights.values())

    def _calc_score(self):
        '''
        This function calculates the overall score for the string.
        '''
        self._eval_scores()
        return self.weighted_average(self._scores, scores_weights)
