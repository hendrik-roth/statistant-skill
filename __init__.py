from mycroft import MycroftSkill, intent_file_handler


class Statistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('statistant.intent')
    def handle_statistant(self, message):
        self.speak_dialog('statistant')


def create_skill():
    return Statistant()

