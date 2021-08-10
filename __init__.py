from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import os
from word2number import w2n

from .filehandler import FileHandler
from .exceptions import FileNotUniqueError
from functools import partial


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
        func = "average"
        filename = message.data.get('file')
        col = message.data.get('colname').lower()

        try:
            file_handler = FileHandler(filename)
            df = file_handler.content
            # if search_one is not none -> intent with rows
            if message.data.get('lower') is not None:

                # user will more likely say to index=0 row=1, etc. -> sub -1
                row1 = w2n.word_to_num(message.data.get('lower'))
                row2 = w2n.word_to_num(message.data.get('upper'))
                mean = round(df.loc[df.index[(row1 - 1):row2], col].mean(), 3)
            else:
                mean = round(df[col].mean(), 3)

            self.speak_dialog('mean', {'colname': col, 'avg': mean})
        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})
        except KeyError:
            self.speak_dialog('Key.error', {'colname': col, 'func': func})


def create_skill():
    return Statistant()
