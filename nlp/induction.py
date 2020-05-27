from nltk import Nonterminal
from nltk import induce_pcfg
from nltk.tree import Tree
from typing import List
from nltk.grammar import PCFG, ProbabilisticProduction
from typing import Iterable
from bisect import bisect
import random

def sample_cdf(cdf):
    r = random.random() * cdf[-1]
    selection = bisect(cdf, r)
    return selection

def cdf(pdf):
    total = 0
    out = []
    for i in range(0, len(pdf)):
        total += pdf[i]
        out.append(total)
    return out


class FancyPCFG(PCFG):
    @staticmethod
    def fromCFG(cfg) -> "PCFG":
        return FancyPCFG(cfg.start(), cfg.productions())

    def __init__(self, start, productions, calculate_leftcorners=True):
        super().__init__(start, productions, calculate_leftcorners)
#        self.probs = {}
        self.next = {} # Nonterminal to [[float], [Nonterminal]]
        self.root = productions[0].lhs()

        for production in productions:
            lhs, prob, rhs = production.lhs(), production.prob(), production.rhs()
            # print(lhs, type(lhs), production.prob(), rhs, type(rhs[0]))
            if lhs not in self.next:
                self.next[lhs] = [[], []] # pdf, tuple of values
            self.next[lhs][0].append(prob) # pdf
            self.next[lhs][1].append(rhs) # tuple values
        for lhs, twosome in self.next.items():
            pdf, values = twosome
            self.next[lhs] = [cdf(pdf), values]


    def sample_rule(self, lhs: Nonterminal):
        cdf, values = self.next[lhs]
        index = sample_cdf(cdf)
        return values[index]

    def sample(self) -> Tree:
        tree = Tree(Nonterminal("NP"), [])
        self.build_tree(tree)
        return tree

    def build_tree(self, tree: Tree):
        children = self.sample_rule(tree.label())
        for child in children:
            if isinstance(child, Nonterminal):
                subtree = Tree(child, [])
                tree.append(subtree)
                self.build_tree(subtree)
            elif isinstance(child, str):
                tree.append(child)
            else:
                raise ValueError(f"Unexpected type {type(child)}")



def induce(trees: Iterable) -> FancyPCFG:
    productions = []
    for tree in trees:
#        tree.pretty_print()
        # perform optional tree transformations, e.g.:
        # tree.collapse_unary(collapsePOS = False)# Remove branches A-B-C into A-B+C
        # tree.chomsky_normal_form(horzMarkov = 2)# Remove A->(B,C,D) into A->B,C+D->D
        productions += tree.productions()
    S = Nonterminal('S')
    grammar = induce_pcfg(S, productions)
    return FancyPCFG.fromCFG(grammar)
