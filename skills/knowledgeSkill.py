
from enum import Enum
from ask import Ask
from skills.skill import Skill
from text_to_num import text2num

class KnowledgeSubIntent(Enum):
    UNKNOWN = 0
    ARITHMETIC = 1

class KnowledgeErrors(Enum):
    NOT_IMPLEMENTED = 0
    MATH_FORMAT_ERROR = 1

class KnowledgeSkill(Skill):
    def find_sub_intent(self, ask: Ask):
        words = ask.utt.split()
        if words.__contains__('plus'):
            return KnowledgeSubIntent.ARITHMETIC
        return KnowledgeSubIntent.UNKNOWN

    def find_execution_data(self, ask: Ask):
        words = ask.utt.replace("what", "").replace("is", "").strip().split()
        if words.__contains__('plus'):
            operand_index = words.index('plus')
            if words.__len__() > operand_index + 1:
                try:
                    x = text2num(' '.join(words[0:operand_index]).strip(), "en")
                    y = text2num(' '.join(words[operand_index+1:]).strip(), "en")
                    z = x + y
                    return f"{x} plus {y} is {z}"
                except:
                    return KnowledgeErrors.MATH_FORMAT_ERROR
            else:
                return KnowledgeErrors.MATH_FORMAT_ERROR
                
        return KnowledgeErrors.NOT_IMPLEMENTED
    
    def execute_ask(self, ask: Ask):
        if ask.execution_data == KnowledgeErrors.NOT_IMPLEMENTED:
            ask.talkback = "Sorry, I don't know"
            return
        if ask.execution_data == KnowledgeErrors.MATH_FORMAT_ERROR:
            ask.talkback = "Math not formatted properly, please try again."
            return
        
        ask.talkback = ask.execution_data
        print("\n")
