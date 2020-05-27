from basics import *
import nltk
from Propinquity import Propinquity
import defaultdict

class Phoneme:
    def __init__(self, phone, stress):
        self.phone = phone
        self.stress = stress

    @staticmethod
    def from_cmu(cmu_phoneme: list) -> 'Phoneme':
        stress = to_int(cmu_phoneme[-1])
        if stress is not None:
            return Phoneme(cmu_phoneme[:-1], stress)
        else:
            return Phoneme(cmu_phoneme, 0)

    @memoized
    def __repr__(self):
        return self.phone + str(self.stress or '')

    @property
    def is_stressed(self) -> bool:
        return self.stress > 0

class Pronounciation:
    def __init__(self, cmu_phonemes):
        self.phonemes = list(map(Phoneme.from_cmu, cmu_phonemes))

    def __repr__(self):
        return ' '.join(map(str, self.phonemes))

    @memoized
    def rhymes_with(self, other: 'Pronounciation'):
        return self._matches(other, lambda x, y: x.phone == y.phone, all)

    @memoized
    def rhythms_with(self, other: 'Pronounciation'):
        return self._matches(other, lambda x, y: x.is_stressed == y.is_stressed, all)

    @memoized
    def stressless_repr(self) -> List[str]:
        return list(map(lambda x: x.phone, self.phonemes))

    def _matches(self, other, phoneme_test, func):
        pairs = self._reversed_phoneme_pairs(other)
        agreement = [phoneme_test(x, y) for x, y in pairs]
        lst = list(reversed(agreement))
        return func(lst)

    def _reversed_phoneme_pairs(self, other):
        assert(type(other) is Pronounciation)
        return zip(reversed(self.phonemes), reversed(other.phonemes))

    def __eq__(self, other):
        agrmnt = map(lambda t: t[0].phone == t[1].phone, zip(self.phonemes, other.phonemes))
        return all(agrmnt)

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.phonemes)

class Word:
    def __init__(self, word, prns):
        self.word = word
        self.prns = prns

    def similarity(self, to: 'Word', using: Propinquity, min_max=min):
        other, dist = to, using
        agrmnt = map(lambda pair: dist(*pair), product(self.prns, other.prns))
        return min_max(agrmnt)

    def __lt__(self, other):
        return self.word < other.word

    def __eq__(self, other):
        return self.word == other.word

    def __hash__(self):
        return hash(self.word)

    def __repr__(self):
        return '%s [%s]' % (self.word, ' | '.join(map(str, self.prns)))

class SuffixRhythmPropinquity(Propinquity):
    def __call__(self, lhs: Pronounciation, rhs: Pronounciation):
        def func(lhs, rhs):
            return lhs._matches(rhs, lambda x, y: x.is_stressed == y.is_stressed, identity)
        return self._matches(lhs, rhs, func)

class RhymePropinquity(Propinquity):
    def __call__(self, lhs: Pronounciation, rhs: Pronounciation):
        func = lambda lhs, rhs: (lhs._matches(rhs, lambda x, y: x.phone == y.phone, identity))
        return self._matches(lhs, rhs, func)



class PDict:
    def __init__(self):
        self._cmu_raw = nltk.corpus.cmudict.dict()

    def preload(self, n=INT_MAX):
        source = seq(self._cmu_raw.items()).take(n)
        self.cmu = {word: Word(word, list(map(Pronounciation, v))) for word, v in source}

    def items(self):
        return self._cmu_raw.items()

    @memoized
    def __getitem__(self, key):
        return self.cmu[key]

    def filter(self, func):
        for word in self.cmu.values():
            if func(word): yield word


class RhymeGraph:
    def __init__(self):
        self.rhymes = defaultdict(list)

    def populate(self, pdict: PDict, predicate):
        self.adj = defaultdict(set)
        words = sorted(pdict.cmu.values(), key=lambda w: list(reversed(w.prns[0].stressless_repr())))
        for i, word1 in enumerate(words):
            if i % 1000 == 0: print(i * 100.0 / len(words))
            for word2 in words[i:]:
                #if word2.word == 'school':
                #    import pdb; pdb.set_trace()
#                print(list(reversed(word1.prns[0].stressless_repr().split())))
#                print(word1, word1.prns[0].stressless_repr()[-1])
#                print(word2, word2.prns[0].stressless_repr()[-1])
#                print('')
                if word1.prns[0].stressless_repr()[-2:] != word2.prns[0].stressless_repr()[-2:]: break
                if predicate(word1, word2):
                    self.adj[word1].add(word2)
                    self.adj[word2].add(word1)

    def export(self, basename):
        nodes = sorted(self.adj.keys())
        with open(f'{basename}.nodes', 'w') as f:
            f.write('\n'.join([w.word for w in nodes]))

        node_ids = indices_as_dict_values(nodes)
        with open(f'{basename}.adj', 'w') as f:
                lines = [' '.join([str(node_ids[w]) for w in self.adj[node]])
                            for node in nodes]
                f.write('\n'.join(lines))

def indices_as_dict_values(lst) -> dict:
    return {k:i for i, k in enumerate(lst)}




pdict = PDict()
pdict.preload()

def predicate(w1, w2):
    d1 = w1.similarity(to=w2, using=rhymep)
    d2 = w1.similarity(to=w2, using=rhythmp)

    rhyme_threshold = min(4, len(w1.prns[0].phonemes) - 1)
    if w1.word.endswith('ing'):
        rhyme_threshold += 2
    elif w1.word.endswith('ation'):
        rhyme_threshold += 4
    elif w1.word.endswith('ent'):
        rhyme_threshold += 3
    elif w1.word.endswith('ations'):
        rhyme_threshold += 5
    elif w1.word.endswith('mant'):
        rhyme_threshold += 2
    elif w1.word.endswith('ated'):
        rhyme_threshold += 4
    elif w1.word.endswith('s'):
        rhyme_threshold += 1
    return d1 >= rhyme_threshold and d2 >= 2

rhymep = RhymePropinquity()
rhythmp = SuffixRhythmPropinquity()

graph = RhymeGraph()
graph.populate(pdict, predicate)
graph.export('rhymes')
