"""Defines the TarotCard class and enumerates all of the cards. Exports them
all in CARDS.
"""
from random import choice
from typing import Tuple

from .sentiment import Sentiment, NEGATIVE, POSITIVE, NEUTRAL

class TarotCard:
    __slots__ = ['name', 'keywords', 'sentiment', 'inversed']

    def __init__(self, name:str = 'Some Card',
                 keywords:Tuple[str] = ['some', 'card'],
                 sentiment:Sentiment = NEUTRAL) -> None:
        self.name = name
        self.keywords = keywords
        self.sentiment = sentiment
        self.inversed = False

    @property
    def search_term(self) -> str:
        return choice(self.keywords)

    def invert(self) -> None:
        self.inversed = not self.inversed

    def __repr__(self):
        return '<TarotCard: {}>'.format(self.name)

    def __str__(self):
        return self.name

def get_tarot_card() -> TarotCard:
    return choice(CARDS)


# TODO actually fill in search terms

CARDS = [
    # minor arcana
    # cups
    TarotCard(name='Ace of Cups',
              sentiment=POSITIVE,
              keywords=('love', 'intimacy', 'feelings', 'compassion', 'beginning',
                        'possibility', 'relationship', 'deeper', 'romantic',
                        'friendship', 'seed', 'gift', 'opportunity', 'offer',)),
    TarotCard(name='Two of Cups',
              sentiment=POSITIVE,
              keywords=('Partnerships', 'unions', 'energies', 'bond', 'Beauty', 'power',
                        'electric', 'vibrations', 'romance', 'sexual', 'energy',
                        'relationship', 'reconciliation', 'harmony', 'peace',)),
    TarotCard(name='Three of Cups',
              sentiment=POSITIVE,
              keywords=('groups', 'together', 'goal', 'community', 'helping', 'caring',
                        'organizations', 'social', 'services', 'support',)),
    TarotCard(name='Four of Cups',
              sentiment=NEUTRAL,
              keywords=('reflection', 'inaction', 'quiet', 'deliberation',
                        'contemplation', 'bad', 'undesirable', 'tribulation',
                        'sacrifice', 'meditation', 'distraction', 'direction',
                        'ignoring',)),
    TarotCard(name='Five of Cups',
              sentiment=NEGATIVE,
              keywords=('emotional', 'dejection', 'disappointment', 'sorrow', 'failure',
                        'appreciate', 'time',)),
    TarotCard(name='Six of Cups',
              sentiment=POSITIVE,
              keywords=('innocence' 'nostalgia' 'provincial' 'rustic' 'simple'
                        'children' 'youth' 'love',)),
    TarotCard(name='Seven of Cups',
              sentiment=NEUTRAL,
              keywords=('cloud' 'transient' 'impractical' 'imagination' 'wishful'
                        'thinking' 'delusion' 'choice' 'temptation' 'confusion',)),
    TarotCard(name='Eight of Cups',
              sentiment=NEGATIVE,
              keywords=('breaking' 'cracking' 'splitting' 'leaving' 'disillusion'
                        'abandon' 'abandonment')),
    TarotCard(name='Nine of Cups',
              sentiment=POSITIVE,
              keywords=('wish' 'fulfilled' 'fulfillment' 'goal' 'desire' 'satisfaction'
                        'satisfied' 'full' 'sated' 'smug' 'smugness' 'pleased' 'content'
                        'contentment' 'contented' 'luxurious' 'luxury',)),
    TarotCard(name='Ten of Cups',
              sentiment=POSITIVE,
              keywords=('rainbow', 'town', 'country', 'local', 'contentment', 'content',
                        'love', 'friendship', 'friends', 'friend', 'trust', 'idyllic',
                        'ideal', 'peace',)),
    TarotCard(name='Page of Cups',
              sentiment=POSITIVE,
              keywords=('spiritual', 'arts', 'imagination', 'psychic', 'creative',
                        'creativity', 'youth', 'party',)),
    TarotCard(name='Knight of Cups',
              sentiment=NEUTRAL,
              keywords=('change', 'excitement', 'exciting', 'changes', 'changing',
                        'excited', 'romantic', 'romance', 'love', 'invitation',
                        'opportunity', 'offer', 'offers', 'bored', 'stimulation',
                        'boring', 'bore',)),
    TarotCard(name='Queen of Cups',
              sentiment=POSITIVE,
              keywords=('queen', 'virtue', 'golden', 'gold', 'mother', 'friend',
                        'throne',)),
    TarotCard(name='King of Cups',
              sentiment=POSITIVE,
              keywords=('king', 'mature', 'throne', 'sceptre', 'heart', 'love', 'music',
              'art', 'sea', 'ocean', 'aid', 'mentor', 'teacher', 'healer',
              'gentle', 'patient', 'diplomacy',)),
    # wands
    TarotCard(name='Ace of Wands',
              sentiment=NEUTRAL,
              keywords=('creation', 'invention', 'enterprise', 'principle', 'beginning',
                        'source', 'birth', 'family', 'origin', 'virility', 'enterprises',
                        'money', 'fortune', 'inheritance', 'commencement', 'creativity',
                        'invention', 'beginning')),
    TarotCard(name='Two of Wands',
              sentiment=NEUTRAL,
              keywords=('courage', 'daring', 'courageous', 'journey', 'journey',
                        'power', 'bold', 'boldness', 'brave', 'bravery', 'travel',)),
    TarotCard(name='Three of Wands',
              sentiment=POSITIVE,
              keywords=('sea', 'ocean', 'journey', 'creation', 'mission', 'optimism',
              'enterprise', 'commerce', 'trade', 'achievement', 'travel',)),
    TarotCard(name='Four of Wands',
              sentiment=POSITIVE,
              keywords=('harmony', 'positive', 'positivity', 'work', 'provincial',
              'haven', 'refuge', 'domestic', 'domesticity', 'concord',
              'harmony', 'peace', 'home', 'house', 'dwelling',)),
    TarotCard(name='Five of Wands',
              sentiment=NEGATIVE,
              keywords=('imitation', 'play', 'sham', 'struggle', 'fight', 'tussle',
                        'combat', 'acquisition', 'struggles', 'fighting', 'fights',
                        'warfare', 'conflict', 'anxiety', 'strife',)),
    TarotCard(name='Six of Wands',
              sentiment=POSITIVE,
              keywords=('organization', 'cleanliness', 'order', 'orderly',
                        'organizations', 'mobilization', 'success', 'triumph', 'victory',
                        'honor', 'competent', 'complete', 'completion',)),
    TarotCard(name='Seven of Wands',
              sentiment=NEUTRAL,
              keywords=('striving', 'strive', 'protect', 'fence', 'cope', 'coping',
                        'resistance', 'resist', 'resisting', 'perseverance', 'strength',
                        'tenacity', 'courage',)),
    TarotCard(name='Eight of Wands',
              sentiment=NEUTRAL,
              keywords=('action', 'swift', 'swiftness', 'speed', 'quick', 'quickness',
                        'journey', 'flight', 'flying', 'fly', 'motion', 'haste', 'hasty',
                        'communication', 'communicate', 'telecommunications', 'news',
                        'information', 'data',)),
    TarotCard(name='Nine of Wands',
              sentiment=POSITIVE,
              keywords=('order', 'discipline', 'protected', 'protect', 'fence', 'wall',
              'castle', 'unassailable', 'health', 'wellbeing', 'stability',
              'tenacity', 'tenacious',)),
    TarotCard(name='Ten of Wands',
              sentiment=NEGATIVE,
              keywords=('overload', 'overloaded', 'exhausted', 'burden', 'burdened',
                        'exhaustion', 'tired', 'overwork', 'work', 'responsibility',)),
    TarotCard(name='Page of Wands',
              sentiment=NEUTRAL,
              keywords=('adventure', 'adventurous', 'ambition', 'ambitious',
                        'energetic', 'active', 'skill', 'skilled', 'drive', 'progress',
                        'grow', 'growth', 'move', 'moving', 'enthusiasm', 'messenger',
                        'message',)),
    TarotCard(name='Knight of Wands',
              sentiment=POSITIVE,
              keywords=('travel', 'progress', 'traveling', 'idea', 'ideas',
                        'inventions', 'forward', 'knowledge', 'battle', 'instinct',
                        'intuition', 'creativity', 'journey',)),
    TarotCard(name='Queen of Wands',
              sentiment=NEUTRAL,
              keywords=('queen', 'throne', 'nurture', 'nurturing', 'feminine',
                        'vivacious', 'intensity', 'fire', 'toughness', 'independence',
                        'sunflower', 'spontaneous', 'chaste', 'chastity', 'helpful',
                        'mother', 'help', 'giving', 'panther')),
    TarotCard(name='King of Wands',
              sentiment=NEUTRAL,
              keywords=('king', 'throne', 'passion', 'mature', 'infinite', 'infinity',
                        'lion', 'salamander', 'authority', 'finances', 'money',
                        'finance', 'honesty', 'mediation', 'mediate', 'professional',
                        'fire', 'desert')),
]

TODO = [
    # pentacles
    TarotCard(name='Ace of Pentacles', keywords=('',)),
    TarotCard(name='Two of Pentacles', keywords=('',)),
    TarotCard(name='Three of Pentacles', keywords=('',)),
    TarotCard(name='Four of Pentacles', keywords=('',)),
    TarotCard(name='Five of Pentacles', keywords=('',)),
    TarotCard(name='Six of Pentacles', keywords=('',)),
    TarotCard(name='Seven of Pentacles', keywords=('',)),
    TarotCard(name='Eight of Pentacles', keywords=('',)),
    TarotCard(name='Nine of Pentacles', keywords=('',)),
    TarotCard(name='Ten of Pentacles', keywords=('',)),
    TarotCard(name='Page of Pentacles', keywords=('',)),
    TarotCard(name='Knight of Pentacles', keywords=('',)),
    TarotCard(name='Queen of Pentacles', keywords=('',)),
    TarotCard(name='King of Pentacles', keywords=('',)),
    # swords
    TarotCard(name='Ace of Swords', keywords=('',)),
    TarotCard(name='Two of Swords', keywords=('',)),
    TarotCard(name='Three of Swords', keywords=('',)),
    TarotCard(name='Four of Swords', keywords=('',)),
    TarotCard(name='Five of Swords', keywords=('',)),
    TarotCard(name='Six of Swords', keywords=('',)),
    TarotCard(name='Seven of Swords', keywords=('',)),
    TarotCard(name='Eight of Swords', keywords=('',)),
    TarotCard(name='Nine of Swords', keywords=('',)),
    TarotCard(name='Ten of Swords', keywords=('',)),
    TarotCard(name='Page of Swords', keywords=('',)),
    TarotCard(name='Knight of Swords', keywords=('',)),
    TarotCard(name='Queen of Swords', keywords=('',)),
    TarotCard(name='King of Swords', keywords=('',)),
    # major arcana
    TarotCard(name='The Tower', keywords=('',)),
    TarotCard(name='The Star', keywords=('',)),
    TarotCard(name='The Hermit', keywords=('',)),
    TarotCard(name='The Fool', keywords=('',)),
    TarotCard(name='The Devil', keywords=('',)),
    TarotCard(name='Temperance', keywords=('',)),
    TarotCard(name='The Sun', keywords=('',)),
    TarotCard(name='The Chariot', keywords=('',)),
    TarotCard(name='Strength', keywords=('',)),
    TarotCard(name='The High Priestess', keywords=('',)),
    TarotCard(name='The Moon', keywords=('',)),
    TarotCard(name='The World', keywords=('',)),
    TarotCard(name='The Lovers', keywords=('',)),
    TarotCard(name='The Magician', keywords=('',)),
    TarotCard(name='The Empress', keywords=('',)),
    TarotCard(name='The Emperor', keywords=('',)),
    TarotCard(name='Justice', keywords=('',)),
    TarotCard(name='The Hierophant', keywords=('',)),
    TarotCard(name='Judgement', keywords=('',)),
    TarotCard(name='Wheel of Fortune', keywords=('',)),
    TarotCard(name='Death', keywords=('death',)),
    TarotCard(name='The Hanged Man', keywords=('',)),
]
