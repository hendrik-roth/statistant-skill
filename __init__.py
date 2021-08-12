from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import os

from word2number import w2n
from functools import partial


from .filehandler import FileHandler
from .statistantcalc import StatistantCalc
from .exceptions import FileNotUniqueError


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

                mean = calc.mean_interval(lower, upper, col)
            elif message.data.get('first') is not None:
                first_val = w2n.word_to_num(message.data.get('first'))
                sec_val = w2n.word_to_num(message.data.get('second'))

                mean = calc.mean_2_cells(first_val, sec_val, col)
            else:
                mean = calc.mean(col)

            self.speak_dialog('mean', {'avg': mean})

        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})


def create_skill():
    return Statistant()
