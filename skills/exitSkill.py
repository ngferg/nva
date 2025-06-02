
from ask import Ask
from skills.skill import Skill

class ExitSkill(Skill):
    def find_sub_intent(self, ask: Ask):
        return ""

    def find_execution_data(self, ask: Ask):
        return ""
    
    def execute_ask(self, ask: Ask):
        ask.talkback = "Goodbye"
        print("\n")