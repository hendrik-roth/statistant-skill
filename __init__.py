from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import os
from word2number import w2n

from .filehandler import FileHandler
from .exceptions import FileNotUniqueError


class Statistant(MycroftSkill):
    def __init__(self):
        # init Skill
        super().__init__()

        # init directory named "statistant" in home directory if it does not exists
        # directory is for reading files
        directory = "statistant"
        parent_dir = os.path.expanduser("~")
        path = os.path.join(parent_dir, directory)
        if not self.file_system.exists(path):
            os.mkdir(path)

    @intent_file_handler('mean.intent')
    def handle_mean(self, message):
        filename = message.data.get('file')
        col = message.data.get('col').lower()

        try:
            file_handler = FileHandler(filename)
            df = file_handler.content
            mean = round(df[col].mean(), 3)

            self.speak_dialog('mean', {'col': col, 'avg': mean})
        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})

    @intent_file_handler('mean2.intent')
    def handle_mean_rows(self, message):
        filename = message.data.get('file')
        col = message.data.get('col').lower()

        # TODO think of solution for index -> will user say index or will be row "one" = index 0?
        row1 = w2n.word_to_num(message.data.get('row1'))
        row2 = w2n.word_to_num(message.data.get('row2'))

        try:
            file_handler = FileHandler(filename)
            df = file_handler.content

            mean = round(df.loc[df.index[row1:row2], col].mean(), 3)

            self.speak_dialog('mean2', {'avg': mean})
        except FileNotFoundError:
            self.speak_dialog('FileNotFound.error', {'filename': filename})
        except FileNotUniqueError:
            self.speak_dialog('FileNotUnique.error', {'filename': filename})


def create_skill():
    return Statistant()
