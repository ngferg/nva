from ask import Ask
from intents import Intent
from skills.fileSystemSkill import FileSystemSkill
from skills.noopSkill import NoopSkill



SKILL_DICT = {
    Intent.UNKNOWN: NoopSkill,
    Intent.NOTHING: NoopSkill,
    Intent.EXIT: NoopSkill,
    Intent.FILE_SYSTEM: FileSystemSkill,
}
    
def find_intent(ask: Ask):
    words = ask.utt.split()
    intent = Intent.UNKNOWN
    if words.__len__() == 0 or words[0].__len__() == 0:
        intent = Intent.NOTHING
    if words[0] == 'open':
        intent = Intent.FILE_SYSTEM
    if words[0] == 'exit' or words[0] == 'cancel':
        intent = Intent.EXIT
    
    ask.skill = SKILL_DICT[intent]()

    return intent

