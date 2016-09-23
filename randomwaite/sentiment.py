class Sentiment:
    def __init__(self, sentiment: str) -> None:
        self._sentiment = sentiment

    def __str__(self) -> str:
        return 'Sentiment<{}>'.format(self._sentiment)

    @property
    def inverse(self) -> 'Sentiment':
        if self._sentiment == 'positive':
            return Sentiment('negative')
        if self._sentiment == 'negative':
            return Sentiment('positive')

        return Sentiment('neutral')

    def invert(self) -> 'Sentiment':
        if self._sentiment == 'positive':
            return Sentiment('negative')
        if self._sentiment == 'negative':
            return Sentiment('positive')

        return self

    def __eq__(self, other) -> bool:
        return self._sentiment == other._sentiment

POSITIVE = Sentiment('positive')
NEGATIVE = Sentiment('negative')
NEUTRAL = Sentiment('neutral')
