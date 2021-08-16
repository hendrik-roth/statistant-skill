import os
from functools import partial

from mycroft import MycroftSkill, intent_file_handler
from word2number import w2n

from .exceptions import FileNotUniqueError, FunctionNotFoundError
from .filehandler import FileHandler
from .statistantcalc import StatistantCalc


class Statistant(MycroftSkill):
    def __init__(self):
        # init Skill
        super().__init__()

        # init directory named "statistant/source_files" in home directory if it does not exists for reading files
        # init directory named "statistant/results" in home directory if it does not exists to save results
        # directory is for reading files
        parent_dir = os.path.expanduser("~")
        directories = ("statistant/source_files", "statistant/results")
        concat_root_path = partial(os.path.join, parent_dir)
        make_directory = partial(os.makedirs, exist_ok=True)
        for path_items in map(concat_root_path, directories):
            make_directory(path_items)

    def handle_basic_stats(self, message, func):
        """
        Function for performing basic statistical functions.
        This function contains extracting filename, col, lower and upper from utterance;
        reading the file with FileHandler and calculating specific
        function with StatistantCalc.

        Parameters
        ----------
        func
            Function which should be performed.
            Possible function names are: average, median, mode, variance, standard deviation, minimum, maximum, sum
        message
            User Utterance of intent

        Returns
        -------
        result
            Result of statistical calculation (one value)

        """
        result = None

        filename = message.data.get('file')
        col = message.data.get('colname').lower()
        lower = message.data.get('lower')
        upper = message.data.get('upper')

        if lower is not None:
            lower = w2n.word_to_num(lower)
            upper = w2n.word_to_num(upper)

        try:
            file_handler = FileHandler(filename)
            calc = StatistantCalc(file_handler.content)
            if lower is not None and upper is not None:
                result = calc.stats_basic(func, col, True, lower, upper)
            else:
                result = calc.stats_basic(func, col)

        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})
        except FunctionNotFoundError:
            self.speak_dialog('FunctionNotFound.error', {'func': func})

        return result

    @intent_file_handler('mean.intent')
    def handle_mean(self, message):
        """
        Function for handling special mean intent.
        A user can ask Mycroft for calculating the average (mean) of 2 specific rows in a column of a file.

        Parameters
        ----------
        message
        """
        func = "average"
        filename = message.data.get('file')
        col = message.data.get('colname').lower()

        try:
            file_handler = FileHandler(filename)
            calc = StatistantCalc(file_handler.content)

            first_val = w2n.word_to_num(message.data.get('first'))
            sec_val = w2n.word_to_num(message.data.get('second'))

            mean = calc.mean_2_cells(first_val, sec_val, col)

            self.speak_dialog('mean', {'avg': mean})

        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})

    @intent_file_handler('basicstats.intent')
    def handle_statistical_basic(self, message):
        """
        function for handling minimum intent

        Parameters
        ----------
        message
        """
        func = message.data.get('function')
        result = self.handle_basic_stats(message, func)
        if result is not None:
            self.speak_dialog('basicstats', {'function': func, 'result': result})


def create_skill():
    return Statistant()
