from mycroft import MycroftSkill, intent_file_handler
import os


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

    @intent_file_handler('statistant.intent')
    def handle_statistant(self, message):
        self.speak_dialog('statistant')


def create_skill():
    return Statistant()

