import sys
import csv
from optparse import OptionParser
from collections import defaultdict
from itertools import combinations

global minSupport, minConfidence, transactions, freqDict, goods

class Node(object):
    def __init__(self):
        self.internalNode = dict()
        self.itemsets = []
        self.itemset = None

class Hash(object):
    def __init__(self, k):
        self.root = Node()
        self.leafs = []
        self.itemsets = []
        self.length = k

    def __len__(self):
        return len(self.itemsets)

    def exist(self, items):
        node = self.root
        for item in items:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        return node.itemset

    def add(self, itemset):
        node = self.root
        new = False
        for item in range(0, self.length - 1):
            if itemset[item] in node.internalNode:
                node = node.internalNode[itemset[item]]
            else:
                new = True
                n = Node()
                node.internalNode[itemset[item]] = n = Node()
                node = n
        if new == True:
            self.leafs.append(node)
        node.itemsets.append(itemset)
        self.itemsets.append(itemset)
        node.internalNode[itemset[-1]] = n = Node()
        n.itemset = itemset

    def update(self, itemset, freqSet):
        node = self.root
        for item in itemset:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        node.itemset.support = node.itemset.support + 1
        if node.itemset.support == int(minSupport * len(transactions)):
            freqSet.add(node.itemset)

    def returnSupport(self, items):
        node = self.root
        for item in items:
            if item in node.internalNode:
                node = node.internalNode[item]
        return node.itemset.support

class iset(object):
    def __init__(self, items):
        self.items = items
        self.maximal = True
        self.support = 0
    
    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        self.begin = 0
        return self

    def __next__(self):
        if self.begin >= len(self.items):
            raise StopIteration
        self.begin = self.begin + 1
        return self.items[self.begin - 1]

def Apriori():
    currentLSet = first()
    k = 2
    while(len(currentLSet) >= 1):
        freqDict[k - 1] = currentLSet
        currentCSet = joiner(currentLSet, k)
        freqSet = Hash(k)
        for t in transactions:
            for c in combinations(t, k):
                currentCSet.update(c, freqSet)
        currentLSet = freqSet
        maxconf(currentLSet, freqDict[k-1])
        k = k + 1

def first():
    itemset = defaultdict(int)
    for t in transactions:
        for i in t:
            itemset[i] = itemset[i] + 1
    all = defaultdict(int)
    for key, value in itemset.items():
        if value >= int(minSupport * len(transactions)):
            all[key] = [value, True]
    return all

def joiner(all, k):
    candidate = Hash(k)
    if k == 2:
        for c in combinations(all.keys(), 2):
            candidate.add(iset(c))
        return candidate
    for leaf in all.leafs:
        for i in range(0, len(leaf.itemsets)):
            for j in range(i+1, len(leaf.itemsets)):
                a = leaf.itemsets[i]
                b = leaf.itemsets[j]
                if a[k - 2] > b[k - 2]:
                    r = iset(a[0:k-2] + (b[k - 2], a[k - 2]))
                else:
                    r = iset(a[0:k - 2] + (a[k-2], b[k-2]))
                if trimmer(r, a, b, all) == True:
                    candidate.add(r)
    return candidate

def trimmer(itemset, a, b, freqSet):
    for c in combinations(itemset.items, freqSet.length):
        if c != a and c != b:
            if not freqSet.exist(c):
                return False
    return True

def maxconf(current, previous):
    if current.length == 2:
        for itemset in current.itemsets:
            a = itemset[0]
            b = itemset[1]
            if a in previous or b in previous:
                previous[a][1] = False
    else:
        for items in current.itemsets:
            for c in combinations(items, previous.length):
                itemset = previous.exist(c)
                if itemset != False:
                    itemset.maximal = False

def reader(file):
    for trans in file:
        t = list(map(int, trans[1:]))
        t.sort()
        transactions.append(t)

def readGoods(infile):
    next(infile)
    for good in infile:
        goods[int(good[0])] = good[1].replace("'", "") + " " + good[2].replace("'", "")

def printer():
    print('MinSupport:{}    MinConfidence:{}'.format(minSupport,minConfidence))
    for length, tree in freqDict.items():
        if length >= 2:
            fulltree = freqDict[length]
            lefttree = freqDict[length - 1]
            for iset in tree.itemsets:
                if iset.maximal == True:
                    items = iset.items
                    for c in combinations(items, length - 1):
                        if isinstance(lefttree, dict):
                            lsupp = lefttree[c[0]][0]
                        else:
                            lsupp = lefttree.returnSupport(c)
                        fsupp = fulltree.returnSupport(items)
                        if (float(fsupp) / lsupp) >= minConfidence:
                            right = set(items).difference(set(c))
                            actualSupport = round(float(fsupp)/float(len(transactions)),3)
                            left = ', '.join(goods[item] for item in c)

                            print('{} --> {} [confidence = {}] [support = {}]'.format(left, goods[next(iter(right))], round(float(fsupp) / lsupp, 2), actualSupport))

def itemprinter():
    for key, value in freqDict.items():
        if key == 1:
            for item,value in value.items():
                print('{} {}'.format(goods[item], float(value[0])/len(transactions)))
        if key >= 2:
            for itemset in value.itemsets:
                if itemset.maximal == True:
                    items = ', '.join(goods[item] for item in itemset.items)
                    print('{} {}'.format(items,float(itemset.support)/len(transactions)))


if __name__ == "__main__":
    transactions = []
    freqDict = dict()
    goods = dict()
    optparser = OptionParser()
    optparser.add_option('-i', '--inputDatabase', dest = 'input', help = 'the transaction file', default = None)
    optparser.add_option('-g', '--goods', dest = 'good', help = 'the goods file', default = None)
    optparser.add_option('-s', '--minSupport', dest = 'minS', help = 'minimum support value', default = 0.03, type = 'float')
    optparser.add_option('-c', '--minConfidence', dest = 'minC', help = 'minimum confidence value', default = 0.5, type = 'float')
    (options, args) = optparser.parse_args()
    if options.input is not None:
        reader(csv.reader(open(options.input, 'r')))
    else:
        print('No dataset filename specified\n')
        sys.exit()
    if options.good is not None:
        readGoods(csv.reader(open(options.good, 'r')))
    else:
        print('No goods name specified\n')
        sys.exit()
    minSupport = options.minS
    minConfidence = options.minC
    Apriori()
    itemprinter()
    printer()