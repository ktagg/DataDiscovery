import sys
import csv

goodsInfoDictionary = dict()
goodsCountDictionary = dict()

class Goods:
    def __init__(self,flavor,food,price,type):
        self.flavor = flavor
        self.food = food
        self.price = price
        self.type = type
        
def parseReceipts():
    for x in range(50):
        goodsCountDictionary[x] = 0
        
    with open('1000/1000-out1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rowCount = 0
        for row in csv_reader:
            print "Receipt"+ row[0]
            for s in row[1:]:
                print int(s.strip())
                goodsCountDictionary[int(s.strip())] += 1
                #if(goodsCountDictionary.has_key(int(s.strip()))):
                 #   goodsCountDictionary[s] += 1                    
            rowCount += 1 
    for i in goodsCountDictionary:
        print i, goodsCountDictionary[i] 
                  
def parseGoods():
    with open('goods.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lineCount = 0
        for row in csv_reader:
            if (lineCount > 0):
                print "ID"+ row[0]
                marketGood = Goods(row[1], row[2],row[3],row[4])
                goodsID = lineCount - 1
                
                goodsInfoDictionary[goodsID] = marketGood
                lineCount += 1
            else:
                lineCount += 1
                                               
                       
def apriori(T, I, minSup):
    F = 1
    k = 2
    while F != NULL:
        C = candidateGen(F, k-1)
        for c in C:
            count[c] = 0
        for t in T:
            for c in C:
                if c == t:
                    count[c] + 1
        k = k + 1
    return F

#parseGoods()
parseReceipts()