"""Defines the TarotCard class and enumerates all of the cards. Exports them
all in CARDS.
"""
from random import choice, random
from typing import Tuple

from .sentiment import Sentiment, NEGATIVE, POSITIVE, NEUTRAL

INVERSE_CHANCE = .1

class TarotCard:
    __slots__ = ['name', 'keywords', 'sentiment', 'inverted']

    def __init__(self, name:str = 'Some Card',
                 keywords:Tuple[str] = ['some', 'card'],
                 sentiment:Sentiment = NEUTRAL) -> None:
        self.name = name
        self.keywords = keywords
        self.sentiment = sentiment
        self.inverted = False

    @property
    def search_term(self) -> str:
        return choice(self.keywords)

    def invert(self) -> None:
        self.inverted = not self.inverted
        self.sentiment = self.sentiment.inverse

    def __repr__(self):
        return '<TarotCard: {}>'.format(self.name)

    def __str__(self):
        return self.name

def draw_tarot_card() -> TarotCard:
    card = TarotCard(**choice(CARD_DATA))
    if random() < INVERSE_CHANCE:
        print("inverting card...")
        card.invert()

    return card


CARD_DATA = [
    # minor arcana
    # cups
    dict(name='Ace of Cups',
         sentiment=POSITIVE,
         keywords=('love', 'intimacy', 'feelings', 'compassion', 'beginning',
                   'possibility', 'relationship', 'deeper', 'romantic',
                   'friendship', 'seed', 'gift', 'opportunity', 'offer',)),
    dict(name='Two of Cups',
         sentiment=POSITIVE,
         keywords=('Partnerships', 'unions', 'energies', 'bond', 'Beauty', 'power',
                   'electric', 'vibrations', 'romance', 'sexual', 'energy',
                   'relationship', 'reconciliation', 'harmony', 'peace',)),
    dict(name='Three of Cups',
         sentiment=POSITIVE,
         keywords=('groups', 'together', 'goal', 'community', 'helping', 'caring',
                   'organizations', 'social', 'services', 'support',)),
    dict(name='Four of Cups',
         sentiment=NEUTRAL,
         keywords=('reflection', 'inaction', 'quiet', 'deliberation',
                   'contemplation', 'bad', 'undesirable', 'tribulation',
                   'sacrifice', 'meditation', 'distraction', 'direction',
                   'ignoring',)),
    dict(name='Five of Cups',
              sentiment=NEGATIVE,
              keywords=('emotional', 'dejection', 'disappointment', 'sorrow', 'failure',
                        'appreciate', 'time',)),
    dict(name='Six of Cups',
              sentiment=POSITIVE,
              keywords=('innocence', 'nostalgia', 'provincial', 'rustic', 'simple',
                        'children', 'youth', 'love',)),
    dict(name='Seven of Cups',
              sentiment=NEUTRAL,
              keywords=('cloud', 'transient', 'impractical', 'imagination', 'wishful',
                        'thinking', 'delusion', 'choice', 'temptation', 'confusion',)),
    dict(name='Eight of Cups',
              sentiment=NEGATIVE,
              keywords=('breaking', 'cracking', 'splitting', 'leaving', 'disillusion',
                        'abandon', 'abandonment',)),
    dict(name='Nine of Cups',
              sentiment=POSITIVE,
              keywords=('wish', 'fulfilled', 'fulfillment', 'goal', 'desire', 'satisfaction',
                        'satisfied', 'full', 'sated', 'smug', 'smugness', 'pleased', 'content',
                        'contentment', 'contented', 'luxurious', 'luxury',)),
    dict(name='Ten of Cups',
              sentiment=POSITIVE,
              keywords=('rainbow', 'town', 'country', 'local', 'contentment', 'content',
                        'love', 'friendship', 'friends', 'friend', 'trust', 'idyllic',
                        'ideal', 'peace',)),
    dict(name='Page of Cups',
              sentiment=POSITIVE,
              keywords=('spiritual', 'arts', 'imagination', 'psychic', 'creative',
                        'creativity', 'youth', 'party',)),
    dict(name='Knight of Cups',
              sentiment=NEUTRAL,
              keywords=('change', 'excitement', 'exciting', 'changes', 'changing',
                        'excited', 'romantic', 'romance', 'love', 'invitation',
                        'opportunity', 'offer', 'offers', 'bored', 'stimulation',
                        'boring', 'bore',)),
    dict(name='Queen of Cups',
              sentiment=POSITIVE,
              keywords=('queen', 'virtue', 'golden', 'gold', 'mother', 'friend',
                        'throne',)),
    dict(name='King of Cups',
              sentiment=POSITIVE,
              keywords=('king', 'mature', 'throne', 'sceptre', 'heart', 'love', 'music',
              'art', 'sea', 'ocean', 'aid', 'mentor', 'teacher', 'healer',
              'gentle', 'patient', 'diplomacy',)),
    # wands
    dict(name='Ace of Wands',
              sentiment=NEUTRAL,
              keywords=('creation', 'invention', 'enterprise', 'principle', 'beginning',
                        'source', 'birth', 'family', 'origin', 'virility', 'enterprises',
                        'money', 'fortune', 'inheritance', 'commencement', 'creativity',
                        'invention', 'beginning')),
    dict(name='Two of Wands',
              sentiment=NEUTRAL,
              keywords=('courage', 'daring', 'courageous', 'journey', 'journey',
                        'power', 'bold', 'boldness', 'brave', 'bravery', 'travel',)),
    dict(name='Three of Wands',
              sentiment=POSITIVE,
              keywords=('sea', 'ocean', 'journey', 'creation', 'mission', 'optimism',
              'enterprise', 'commerce', 'trade', 'achievement', 'travel',)),
    dict(name='Four of Wands',
              sentiment=POSITIVE,
              keywords=('harmony', 'positive', 'positivity', 'work', 'provincial',
              'haven', 'refuge', 'domestic', 'domesticity', 'concord',
              'harmony', 'peace', 'home', 'house', 'dwelling',)),
    dict(name='Five of Wands',
              sentiment=NEGATIVE,
              keywords=('imitation', 'play', 'sham', 'struggle', 'fight', 'tussle',
                        'combat', 'acquisition', 'struggles', 'fighting', 'fights',
                        'warfare', 'conflict', 'anxiety', 'strife',)),
    dict(name='Six of Wands',
              sentiment=POSITIVE,
              keywords=('organization', 'cleanliness', 'order', 'orderly',
                        'organizations', 'mobilization', 'success', 'triumph', 'victory',
                        'honor', 'competent', 'complete', 'completion',)),
    dict(name='Seven of Wands',
              sentiment=NEUTRAL,
              keywords=('striving', 'strive', 'protect', 'fence', 'cope', 'coping',
                        'resistance', 'resist', 'resisting', 'perseverance', 'strength',
                        'tenacity', 'courage',)),
    dict(name='Eight of Wands',
              sentiment=NEUTRAL,
              keywords=('action', 'swift', 'swiftness', 'speed', 'quick', 'quickness',
                        'journey', 'flight', 'flying', 'fly', 'motion', 'haste', 'hasty',
                        'communication', 'communicate', 'telecommunications', 'news',
                        'information', 'data',)),
    dict(name='Nine of Wands',
              sentiment=POSITIVE,
              keywords=('order', 'discipline', 'protected', 'protect', 'fence', 'wall',
              'castle', 'unassailable', 'health', 'wellbeing', 'stability',
              'tenacity', 'tenacious',)),
    dict(name='Ten of Wands',
              sentiment=NEGATIVE,
              keywords=('overload', 'overloaded', 'exhausted', 'burden', 'burdened',
                        'exhaustion', 'tired', 'overwork', 'work', 'responsibility',)),
    dict(name='Page of Wands',
              sentiment=NEUTRAL,
              keywords=('adventure', 'adventurous', 'ambition', 'ambitious',
                        'energetic', 'active', 'skill', 'skilled', 'drive', 'progress',
                        'grow', 'growth', 'move', 'moving', 'enthusiasm', 'messenger',
                        'message',)),
    dict(name='Knight of Wands',
              sentiment=POSITIVE,
              keywords=('travel', 'progress', 'traveling', 'idea', 'ideas',
                        'inventions', 'forward', 'knowledge', 'battle', 'instinct',
                        'intuition', 'creativity', 'journey',)),
    dict(name='Queen of Wands',
              sentiment=NEUTRAL,
              keywords=('queen', 'throne', 'nurture', 'nurturing', 'feminine',
                        'vivacious', 'intensity', 'fire', 'toughness', 'independence',
                        'sunflower', 'spontaneous', 'chaste', 'chastity', 'helpful',
                        'mother', 'help', 'giving', 'panther')),
    dict(name='King of Wands',
              sentiment=NEUTRAL,
              keywords=('king', 'throne', 'passion', 'mature', 'infinite', 'infinity',
                        'lion', 'salamander', 'authority', 'finances', 'money',
                        'finance', 'honesty', 'mediation', 'mediate', 'professional',
                        'fire', 'desert')),
]

# TODO actually fill in search terms
TODO = [
    # pentacles
    dict(name='Ace of Pentacles', keywords=('',)),
    dict(name='Two of Pentacles', keywords=('',)),
    dict(name='Three of Pentacles', keywords=('',)),
    dict(name='Four of Pentacles', keywords=('',)),
    dict(name='Five of Pentacles', keywords=('',)),
    dict(name='Six of Pentacles', keywords=('',)),
    dict(name='Seven of Pentacles', keywords=('',)),
    dict(name='Eight of Pentacles', keywords=('',)),
    dict(name='Nine of Pentacles', keywords=('',)),
    dict(name='Ten of Pentacles', keywords=('',)),
    dict(name='Page of Pentacles', keywords=('',)),
    dict(name='Knight of Pentacles', keywords=('',)),
    dict(name='Queen of Pentacles', keywords=('',)),
    dict(name='King of Pentacles', keywords=('',)),
    # swords
    dict(name='Ace of Swords', keywords=('',)),
    dict(name='Two of Swords', keywords=('',)),
    dict(name='Three of Swords', keywords=('',)),
    dict(name='Four of Swords', keywords=('',)),
    dict(name='Five of Swords', keywords=('',)),
    dict(name='Six of Swords', keywords=('',)),
    dict(name='Seven of Swords', keywords=('',)),
    dict(name='Eight of Swords', keywords=('',)),
    dict(name='Nine of Swords', keywords=('',)),
    dict(name='Ten of Swords', keywords=('',)),
    dict(name='Page of Swords', keywords=('',)),
    dict(name='Knight of Swords', keywords=('',)),
    dict(name='Queen of Swords', keywords=('',)),
    dict(name='King of Swords', keywords=('',)),
    # major arcana
    dict(name='The Tower', keywords=('',)),
    dict(name='The Star', keywords=('',)),
    dict(name='The Hermit', keywords=('',)),
    dict(name='The Fool', keywords=('',)),
    dict(name='The Devil', keywords=('',)),
    dict(name='Temperance', keywords=('',)),
    dict(name='The Sun', keywords=('',)),
    dict(name='The Chariot', keywords=('',)),
    dict(name='Strength', keywords=('',)),
    dict(name='The High Priestess', keywords=('',)),
    dict(name='The Moon', keywords=('',)),
    dict(name='The World', keywords=('',)),
    dict(name='The Lovers', keywords=('',)),
    dict(name='The Magician', keywords=('',)),
    dict(name='The Empress', keywords=('',)),
    dict(name='The Emperor', keywords=('',)),
    dict(name='Justice', keywords=('',)),
    dict(name='The Hierophant', keywords=('',)),
    dict(name='Judgement', keywords=('',)),
    dict(name='Wheel of Fortune', keywords=('',)),
    dict(name='Death', keywords=('death',)),
    dict(name='The Hanged Man', keywords=('',)),
]
