from ask import Ask
from intents import Intent
from skills.knowledgeSkill import KnowledgeSkill
from skills.exitSkill import ExitSkill
from skills.fileSystemSkill import FileSystemSkill
from skills.noopSkill import NoopSkill
from skills.randomSkill import RandomSkill


SKILL_DICT = {
    Intent.UNKNOWN: NoopSkill,
    Intent.NOTHING: NoopSkill,
    Intent.EXIT: ExitSkill,
    Intent.FILE_SYSTEM: FileSystemSkill,
    Intent.RANDOM: RandomSkill,
    Intent.KNOWLEDGE: KnowledgeSkill,
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
    if ask.utt == 'flip a coin' or ask.utt.startswith('roll a d') or ask.utt.startswith('roll the d'):
        intent = Intent.RANDOM
    if words[0] == 'what':
        intent = Intent.KNOWLEDGE

    ask.skill = SKILL_DICT[intent]()

    return intent
