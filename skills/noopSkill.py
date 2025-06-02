
from ask import Ask
from skills.skill import Skill


class NoopSkill(Skill):
    def find_sub_intent(self, ask: Ask):
        return ""

    def find_execution_data(self, ask: Ask):
        return ""
    
    def execute_ask(self, ask: Ask):
        print("\n")