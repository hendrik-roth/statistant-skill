from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import os
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


def create_skill():
    return Statistant()
