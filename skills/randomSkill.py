
from enum import Enum
import random
from ask import Ask
from skills.skill import Skill
from text_to_num import text2num

class RandomSubIntent(Enum):
    FLIP_COIN = 1
    ROLL_DICE = 2


class RandomSkill(Skill):
    def find_sub_intent(self, ask: Ask):
        if ask.utt == 'flip a coin':
            return RandomSubIntent.FLIP_COIN
        if ask.utt.startswith('roll a d') or ask.utt.startswith('roll the d'):
            return RandomSubIntent.ROLL_DICE
        return ""

    def find_execution_data(self, ask: Ask):
        print(f"Finding execution data for {ask.sub_intent}")
        if ask.sub_intent == RandomSubIntent.ROLL_DICE:
            words = ask.utt.split()
            die_face = 6
            last_word = words[words.__len__()-1]
            if not last_word.startswith('d'):
                try:
                    die_face = text2num(last_word, "en")
                except:
                    die_face = 6

            return [1, die_face]
        else:
            return 1
    
    def execute_ask(self, ask: Ask):
        if ask.sub_intent == RandomSubIntent.FLIP_COIN:
            result = random.randint(0, 1)
            if result == 0:
                ask.talkback = "I flipped Heads"
            else:
                ask.talkback = "I flipped Tails"
        else: 
            if ask.sub_intent == RandomSubIntent.ROLL_DICE:
                num_dice = ask.execution_data[0]
                die_face = ask.execution_data[1]
                for i in range(num_dice):
                    result = random.randint(1, die_face)
                    if i == 0:
                        ask.talkback = f"I rolled a {result}"
                    else:
                        ask.talkback = ask.talkback + f", and a {result}"

                