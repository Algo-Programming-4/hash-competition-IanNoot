class Word:
    def __init__(self, value):
        self.value = value
        self.count = 1
    
    def increment(self):
        self.count += 1
        
    def __str__(self):
        return(f"{self.value}, {self.count}")


class HashTable:
    def __init__(self):
        self.table = [None]
        self.ratio = 0
        self.bonus = 0



def create_hash(Words, hashRatio, firstLetterBonus):

    interval = 1.1
    bucketScore = 0
    chainLengthScore = 0
    
    val1 = tryloop(Words, hashRatio, firstLetterBonus / interval / interval)[0]
    
    val2 = tryloop(Words, hashRatio, firstLetterBonus * interval * interval)[0]

    
    #print("|\n|\n|\n")
    #print(val1)
    #print(val2)
    
    iterations = 0
    iterationMax = 9999
    
    ##Increase firstLetterBonus
    if val1 > val2:
        #print("A")
        firstLetterBonus *= interval
        while val1 > val2  and iterations < iterationMax:
            val1 = val2
            
            firstLetterBonus *= interval
            val2 = tryloop(Words, hashRatio, firstLetterBonus)[0]
            print(f"{iterations}, {val1}, {val2}")
            
            iterations += 1
            
        firstLetterBonus /= interval
    
    ## Decrease firstLetterBonus
    elif val1 < val2:
        #print("B")
        firstLetterBonus /= interval
        while val1 < val2  and iterations < iterationMax:
            val1 = val2
            
            firstLetterBonus /= interval
            val2 = tryloop(Words, hashRatio, firstLetterBonus)[0]
            iterations += 1
            
            print(f"{iterations}, {val1}, {val2}")
            
        firstLetterBonus *= interval
    
    
    print("\n\n SPLIT \n\n")
    
    
    interval = 1.1
    
    val1a = tryloop(Words, hashRatio / interval, firstLetterBonus)[0]
    val1b = tryloop(Words, hashRatio / interval / interval, firstLetterBonus)[0]
    val2a = tryloop(Words, hashRatio * interval, firstLetterBonus)[0]
    val2b = tryloop(Words, hashRatio * interval * interval, firstLetterBonus)[0]
    
    val1 = (val1a + val1b) / 2
    val2 = (val2a + val2b) / 2
    
    # print(val1)
    # print(val2)
    
    iterations = 0
    
    
    ##Increase HashRatio
    if val1 > val2:
        #print("A")
        hashRatio *= interval
        while val1 > val2 and iterations < iterationMax:
            val1 = tryloop(Words, hashRatio, firstLetterBonus)[0]
            
            hashRatio *= interval
            val2 = tryloop(Words, hashRatio, firstLetterBonus)[0]
            
            print(f"{iterations}, {val1}, {val2}")
            iterations += 1
            
            
        hashRatio /= interval
    
    ## Decrease HashRatio
    elif val1 < val2:
        #print("B")
        hashRatio /= interval
        while val1 < val2 and iterations < iterationMax:
            val1 = tryloop(Words, hashRatio, firstLetterBonus)[0]
            hashRatio /= interval
            val2 = tryloop(Words, hashRatio, firstLetterBonus)[0]
            iterations += 1
            print(f"{iterations}, {val1}, {val2}")
        hashRatio *= interval
    
    
    
    outputTable = HashTable()
    
    outputTable.table = tryloop(Words, hashRatio, firstLetterBonus)[1]
    bucketScore = tryloop(Words, hashRatio, firstLetterBonus)[2]
    chainLengthScore = tryloop(Words, hashRatio, firstLetterBonus)[3]
    outputTable.ratio = hashRatio
    outputTable.bonus = firstLetterBonus
    
    
    return (outputTable, bucketScore, chainLengthScore)
    



def tryloop(Words, hashRatio, firstLetterBonus):
    
    hashmap = [None] * (int(len(Words) / hashRatio))
    length = len(hashmap)
    #print(length)
    chainLengthScore = 0
    bucketScore = length
    
    for i in Words:

        hash = 0
        k = 1
        
        ##Find value of word
        for j in i:
            hash += ord(j) * k
            k += firstLetterBonus

        hash = hash % length
        hash = int(hash)
        
        ##If the hash location is empty
        if hashmap[hash] == None:
            hashmap[hash] = []
        
        ##If the hash location isn't empty
        else:
            c = False
            for j in hashmap[hash]:
                if j.value == i:
                    j.count += 1
                    i = ""
                    c = True
            if c == False:
                chainLengthScore += 1
        
        if i != "":
            word = Word(i)
            hashmap[hash].append(word)
    
    #print(f"  -  {bucketScore}, {chainLengthScore}")
    
    return ((bucketScore + chainLengthScore), hashmap, bucketScore, chainLengthScore)



def words_in(word_list):


    bucketScore = 0
    chainLengthScore = 0


    hashmap = [None] * 1

    #print("HERE")

    func_cached = create_hash(word_list, 1, 1)

    hashmap = func_cached[0]
    hashtable = hashmap.table
    
    bucketScore = func_cached[1]
    chainLengthScore = func_cached[2]


    ##Count Score and Print final
    fullBuckets = 0
    index = 0
    for i in hashtable:
        output = ""
        if i != None:
            fullBuckets += 1
            x = 0
            for j in i:
                output = output + f"{j.value}, {j.count}, {index}, "
                
                if x > 0:
                    chainLengthScore += 1
                    
                x += 1
        else:
            bucketScore += 1
    
        index += 1




    # print(f"\n\nPercentage Full: {fullBuckets / len(hashmap)}")
    # print(f"Num Empty Buckets: {bucketScore}")
    # print(f"Num Bucket Overfills: {chainLengthScore}")
    # print(f"\nTotal Score: {bucketScore + chainLengthScore*2} ")
    # print(f"\n\n Contents:")
    # for i in hashmap:
    #     print("________________\n")
    
    #     if i != None:
    #         for j in i:
    #             print(j)       
    # print("________________\n")
    
    # print(global_length)
    
    return (bucketScore, chainLengthScore, hashmap)
    
    
    
def lookup_word_count(word, hashmap): 
    
    hash = 0
    k = 1
    x = 0
    
    table = hashmap.table
    length = len(hashmap.table)    
    bonus = hashmap.bonus
    
    ##Find value of word
    for i in word:
        hash += ord(i) * k
        k += bonus
    
    ##Get index
    hash = hash % length
    hash = int(hash)
    
    ##Find key in index
    for i in table[hash]:
        x += 1
        
        if i.value == word:
            return (word.count, x)
    
    return(0, x)
        
    