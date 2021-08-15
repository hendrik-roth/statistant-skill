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
        filename = message.data.get('file')
        col = message.data.get('colname').lower()

        try:
            file_handler = FileHandler(filename)
            calc = StatistantCalc(file_handler.content)
            if message.data.get('lower') is not None:
                lower = w2n.word_to_num(message.data.get('lower'))
                upper = w2n.word_to_num(message.data.get('upper'))

                median = calc.stats_basic(func, col, True, lower, upper)
            else:
                median = calc.stats_basic(func, col)
            self.speak_dialog('median', {'median': median})
        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})
        except IndexError:
            self.speak_dialog('IndexError', {'func': func})

    @intent_file_handler('cluster.intent')
    def handle_cluster(self, message):
        func = "cluster analysis"
        filename = message.data.get('file')
        x_col = message.data.get('colname_x').lower()
        y_col = message.data.get('colname_y').lower()
        num_clusters = w2n.word_to_num(message.data.get('num_clusters'))

        try:
            file_handler = FileHandler(filename)
            calc = StatistantCalc(file_handler.content, filename)

            calc.cluster(x_col, y_col, num_clusters)

            self.speak_dialog('cluster', {'colname_x': x_col,
                                          'colname_y': y_col,
                                          'file': filename,
                                          'num_clusters': num_clusters})

        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        # todo: KeyError for x_colname and y_colname
        """except KeyError:
            self.speak_dialog('KeyError', {'colname': col, 'func': func})"""


def create_skill():
    return Statistant()
