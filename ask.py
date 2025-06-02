class Ask:
    def __init__(self, utt: str):
        self.utt = utt.lower()
        from qb import find_intent
        self.intent = find_intent(self)
        self.sub_intent = self.skill.find_sub_intent(self)
        self.execution_data = self.skill.find_execution_data(self)
        self.talkback: str = ""

    def debug_print(self):
        print(f"utterance: '{self.utt}'\nintent: {self.intent}\nsub-intent: {self.sub_intent}\n")

