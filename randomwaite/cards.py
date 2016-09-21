"""Defines the TarotCard class and enumerates all of the cards. Exports them
all in CARDS.
"""
from random import choice
from typing import Tuple

# TODO support for reversed

class TarotCard:
    __slots__ = ['name', 'search']

    def __init__(self, name:str, search:Tuple[str]) -> None:
        self.name = name
        self.search = search

    @property
    def search_term(self) -> str:
        return choice(self.search)

    def __repr__(self):
        return '<TarotCard: {}>'.format(self.name)

    def __str__(self):
        return self.name

def get_tarot_card() -> TarotCard:
    return choice(CARDS)


# TODO actually fill in search terms
# TODO i'm still really unsure if I should be subclassing TarotCard for each
# card.

CARDS = [
    # minor arcana
    # cups
    TarotCard('Ace of Cups',
              ('love', 'intimacy', 'feelings', 'compassion', 'beginning',
               'possibility', 'relationship', 'deeper', 'romantic',
               'friendship', 'seed', 'gift', 'opportunity', 'offer',
    )),
    TarotCard('Two of Cups',
              ('Partnerships', 'unions', 'energies', 'bond', 'Beauty', 'power',
               'electric', 'vibrations', 'romance', 'sexual', 'energy',
               'relationship', 'reconciliation', 'harmony', 'peace',
    )),
    TarotCard('Three of Cups',
              ('groups', 'together', 'goal', 'community', 'helping', 'caring',
               'organizations', 'social', 'services', 'support',)),
    TarotCard('Four of Cups',
              ('reflection', 'inaction', 'quiet', 'deliberation',
               'contemplation', 'bad', 'undesirable', 'tribulation',
               'sacrifice', 'meditation', 'distraction', 'direction',
               'ignoring',
    )),
    TarotCard('Five of Cups',
              ('emotional', 'dejection', 'disappointment', 'sorrow', 'failure',
              'appreciate', 'time',
    )),
    TarotCard('Six of Cups',
              ('innocence' 'nostalgia' 'provincial' 'rustic' 'simple' 'children' 'youth' 'love',)),
    TarotCard('Seven of Cups',
              ('cloud' 'transient' 'impractical' 'imagination' 'wishful' 'thinking' 'delusion' 'choice' 'temptation' 'confusion',)),
    TarotCard('Eight of Cups',
              ('breaking' 'cracking' 'splitting' 'leaving' 'disillusion' 'abandon' 'abandonment')),
    TarotCard('Nine of Cups',
              ('wish' 'fulfilled' 'fulfillment' 'goal' 'desire' 'satisfaction'
              'satisfied' 'full' 'sated' 'smug' 'smugness' 'pleased' 'content'
              'contentment' 'contented' 'luxurious' 'luxury',)),
    TarotCard('Ten of Cups',
              ('rainbow', 'town', 'country', 'local', 'contentment', 'content',
              'love', 'friendship', 'friends', 'friend', 'trust', 'idyllic',
              'ideal', 'peace',)),
    TarotCard('Page of Cups',
              ('spiritual', 'arts', 'imagination', 'psychic', 'creative',
              'creativity', 'youth', 'party',)),
    TarotCard('Knight of Cups',
              ('change', 'excitement', 'exciting', 'changes', 'changing',
              'excited', 'romantic', 'romance', 'love', 'invitation',
              'opportunity', 'offer', 'offers', 'bored', 'stimulation',
              'boring', 'bore',)),
    TarotCard('Queen of Cups',
              ('queen', 'virtue', 'golden', 'gold', 'mother', 'friend',
              'throne',)),
    TarotCard('King of Cups',
              ('king', 'mature', 'throne', 'sceptre', 'heart', 'love', 'music',
              'art', 'sea', 'ocean', 'aid', 'mentor', 'teacher', 'healer',
              'gentle', 'patient', 'diplomacy',)),
    # pentacles
    TarotCard('Ace of Pentacles', ('',)),
    TarotCard('Two of Pentacles', ('',)),
    TarotCard('Three of Pentacles', ('',)),
    TarotCard('Four of Pentacles', ('',)),
    TarotCard('Five of Pentacles', ('',)),
    TarotCard('Six of Pentacles', ('',)),
    TarotCard('Seven of Pentacles', ('',)),
    TarotCard('Eight of Pentacles', ('',)),
    TarotCard('Nine of Pentacles', ('',)),
    TarotCard('Ten of Pentacles', ('',)),
    TarotCard('Page of Pentacles', ('',)),
    TarotCard('Knight of Pentacles', ('',)),
    TarotCard('Queen of Pentacles', ('',)),
    TarotCard('King of Pentacles', ('',)),
    # wands
    TarotCard('Ace of Wands',
              ('creation', 'invention', 'enterprise', 'principle', 'beginning',
              'source', 'birth', 'family', 'origin', 'virility', 'enterprises',
              'money', 'fortune', 'inheritance', 'commencement', 'creativity',
              'invention', 'beginning')),
    TarotCard('Two of Wands',
              ('courage', 'daring', 'courageous', 'journey', 'journey',
              'power', 'bold', 'boldness', 'brave', 'bravery', 'travel',)),
    TarotCard('Three of Wands',
              ('sea', 'ocean', 'journey', 'creation', 'mission', 'optimism',
              'enterprise', 'commerce', 'trade', 'achievement', 'travel',)),
    TarotCard('Four of Wands',
              ('harmony', 'positive', 'positivity', 'work', 'provincial',
              'haven', 'refuge', 'domestic', 'domesticity', 'concord',
              'harmony', 'peace', 'home', 'house', 'dwelling',)),
    TarotCard('Five of Wands',
              ('imitation', 'play', 'sham', 'struggle', 'fight', 'tussle',
              'combat', 'acquisition', 'struggles', 'fighting', 'fights',
              'warfare', 'conflict', 'anxiety', 'strife',)),
    TarotCard('Six of Wands',
              ('organization', 'cleanliness', 'order', 'orderly',
              'organizations', 'mobilization', 'success', 'triumph', 'victory',
              'honor', 'competent', 'complete', 'completion',)),
    TarotCard('Seven of Wands',
              ('striving', 'strive', 'protect', 'fence', 'cope', 'coping',
              'resistance', 'resist', 'resisting', 'perseverance', 'strength',
              'tenacity', 'courage',)),
    TarotCard('Eight of Wands',
              ('action', 'swift', 'swiftness', 'speed', 'quick', 'quickness',
              'journey', 'flight', 'flying', 'fly', 'motion', 'haste', 'hasty',
              'communication', 'communicate', 'telecommunications', 'news',
              'information', 'data',)),
    TarotCard('Nine of Wands',
              ('order', 'discipline', 'protected', 'protect', 'fence', 'wall',
              'castle', 'unassailable', 'health', 'wellbeing', 'stability',
              'tenacity', 'tenacious',)),
    TarotCard('Ten of Wands',
              ('overload', 'overloaded', 'exhausted', 'burden', 'burdened',
              'exhaustion', 'tired', 'overwork', 'work', 'responsibility',)),
    TarotCard('Page of Wands',
              ('adventure', 'adventurous', 'ambition', 'ambitious',
              'energetic', 'active', 'skill', 'skilled', 'drive', 'progress',
              'grow', 'growth', 'move', 'moving', 'enthusiasm', 'messenger',
              'message',)),
    TarotCard('Knight of Wands',
              ('travel', 'progress', 'traveling', 'idea', 'ideas',
              'inventions', 'forward', 'knowledge', 'battle', 'instinct',
              'intuition', 'creativity', 'journey',)),
    TarotCard('Queen of Wands',
              ('queen', 'throne', 'nurture', 'nurturing', 'feminine',
              'vivacious', 'intensity', 'fire', 'toughness', 'independence',
              'sunflower', 'spontaneous', 'chaste', 'chastity', 'helpful',
               'mother', 'help', 'giving', 'panther')),
    TarotCard('King of Wands',
              ('king', 'throne', 'passion', 'mature', 'infinite', 'infinity',
              'lion', 'salamander', 'authority', 'finances', 'money',
              'finance', 'honesty', 'mediation', 'mediate', 'professional',
              'fire', 'desert')),
    # swords
    TarotCard('Ace of Swords', ('',)),
    TarotCard('Two of Swords', ('',)),
    TarotCard('Three of Swords', ('',)),
    TarotCard('Four of Swords', ('',)),
    TarotCard('Five of Swords', ('',)),
    TarotCard('Six of Swords', ('',)),
    TarotCard('Seven of Swords', ('',)),
    TarotCard('Eight of Swords', ('',)),
    TarotCard('Nine of Swords', ('',)),
    TarotCard('Ten of Swords', ('',)),
    TarotCard('Page of Swords', ('',)),
    TarotCard('Knight of Swords', ('',)),
    TarotCard('Queen of Swords', ('',)),
    TarotCard('King of Swords', ('',)),
    # major arcana
    TarotCard('The Tower', ('',)),
    TarotCard('The Star', ('',)),
    TarotCard('The Hermit', ('',)),
    TarotCard('The Fool', ('',)),
    TarotCard('The Devil', ('',)),
    TarotCard('Temperance', ('',)),
    TarotCard('The Sun', ('',)),
    TarotCard('The Chariot', ('',)),
    TarotCard('Strength', ('',)),
    TarotCard('The High Priestess', ('',)),
    TarotCard('The Moon', ('',)),
    TarotCard('The World', ('',)),
    TarotCard('The Lovers', ('',)),
    TarotCard('The Magician', ('',)),
    TarotCard('The Empress', ('',)),
    TarotCard('The Emperor', ('',)),
    TarotCard('Justice', ('',)),
    TarotCard('The Hierophant', ('',)),
    TarotCard('Judgement', ('',)),
    TarotCard('Wheel of Fortune', ('',)),
    TarotCard('Death', ('death',)),
    TarotCard('The Hanged Man', ('',)),
]
