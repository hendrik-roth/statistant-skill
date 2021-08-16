import os
from functools import partial

from mycroft import MycroftSkill, intent_file_handler
from word2number import w2n

from .exceptions import FileNotUniqueError
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

    def do_basic_stats(self, message, func):
        """
        Function for performing basic statistical functions.
        This function contains reading the file with FileHandler and calculating specific
        function with StatistantCalc.

        Parameters
        ----------
        func
        message

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

        return result

    @intent_file_handler('mean.intent')
    def handle_mean(self, message):
        """
        Function for handling mean intent.
        A user can ask Mycroft for calculating the average (mean) of a column or of specific rows in a column.

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

            # if lower is not none -> intent with rows and other calculation, else just normal .mean calc
            if message.data.get('lower') is not None:

                lower = w2n.word_to_num(message.data.get('lower'))
                upper = w2n.word_to_num(message.data.get('upper'))

                mean = calc.stats_basic(func, col, True, lower, upper)
            elif message.data.get('first') is not None:
                first_val = w2n.word_to_num(message.data.get('first'))
                sec_val = w2n.word_to_num(message.data.get('second'))

                mean = calc.mean_2_cells(first_val, sec_val, col)
            else:
                mean = calc.stats_basic(func, col)

            self.speak_dialog('mean', {'avg': mean})

        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})

    @intent_file_handler('median.intent')
    def handle_median(self, message):
        """
        function for handling median intent

        Parameters
        ----------
        message
        """
        func = "median"
        median = self.do_basic_stats(message, func)
        if median is not None:
            self.speak_dialog('median', {'median': median})

    @intent_file_handler('mode.intent')
    def handle_mode(self, message):
        """
        function for handling median intent

        Parameters
        ----------
        message
        """
        func = "mode"
        mode = self.do_basic_stats(message, func)
        if mode is not None:
            self.speak_dialog('mode', {'mode': mode})

    @intent_file_handler('min.intent')
    def handle_mode(self, message):
        """
        function for handling median intent

        Parameters
        ----------
        message
        """
        func = "min"
        mode = self.do_basic_stats(message, func)
        if mode is not None:
            self.speak_dialog('min', {'min': mode})


def create_skill():
    return Statistant()
