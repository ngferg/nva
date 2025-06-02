from enum import Enum
import subprocess

from ask import Ask
from skills.skill import Skill

class FileSystemSubIntent(Enum):
    OPEN_APP = 1

class FileSystemSkill(Skill):
    def find_sub_intent(self, ask: Ask):
        words = ask.utt.split()
        if words[0] == 'open':
            return FileSystemSubIntent.OPEN_APP
        if words.__len__() > 1:
            words = words[1:]
            return " ".join(words).strip()
    
    def find_execution_data(self, ask: Ask):
        words = ask.utt.split()
        if ask.sub_intent == FileSystemSubIntent.OPEN_APP and words.__len__() > 1:
            words = words[1:]
            return " ".join(words).strip()
        return ""
    
    def execute_ask(self, ask: Ask):
        app = find_app(ask.execution_data)

        if app.__len__() > 0:
            subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a", app])
        else:
            app = find_app(ask.sub_intent.replace(" ", ""))
            if app.__len__() > 0:
                subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a", app])
    

def find_app(name: str) -> str:
    find = ["find", "/Applications", "-iname", "*" + name + "*.app", "-print"]
    
    result = subprocess.run(find, capture_output=True, text=True, check=True)
    return result.stdout.split('\n')[0]
