import requests
import json
from enum import Enum
from ask import Ask
from skills.skill import Skill
from text_to_num import text2num

class KnowledgeSubIntent(Enum):
    UNKNOWN = 0
    ARITHMETIC = 1
    LLAMA = 2

class KnowledgeErrors(Enum):
    NOT_IMPLEMENTED = 0
    MATH_FORMAT_ERROR = 1

class KnowledgeSkill(Skill):
    def find_sub_intent(self, ask: Ask):
        words = ask.utt.split()
        if words.__contains__('plus'):
            return KnowledgeSubIntent.ARITHMETIC
        return KnowledgeSubIntent.LLAMA

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
                
        return ask.utt + ". Note: this will be read by a voice assistant, be concise"
    
    def execute_ask(self, ask: Ask):
        if ask.execution_data == KnowledgeErrors.NOT_IMPLEMENTED:
            ask.talkback = "Sorry, I don't know"
            return
        if ask.execution_data == KnowledgeErrors.MATH_FORMAT_ERROR:
            ask.talkback = "Math not formatted properly, please try again."
            return
        if ask.sub_intent == KnowledgeSubIntent.LLAMA:
            payload = {
                    "model": "llama3.2",
                    "prompt": ask.execution_data
            }
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            lines = response.text.splitlines()
            ask.execution_data = ""
            for line in lines:
                word = json.loads(line)['response']
                ask.execution_data += word 
        
        ask.talkback = ask.execution_data
        print("\n")
