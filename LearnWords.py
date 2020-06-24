import random
wordsFile=open("usa.txt","r")

wordsList=[]
for w in wordsFile:
 wordsList.append(w.strip())
alphabet="abcdefghijklmnopqrstuvwxyz"
letterValues={
         "a":4,"b":2,"c":3,"d":3,"e":4,"f":3,"g":3,"h":2,"i":3,"j":1,"k":2,"l":4,"m":3,"n":4,"o":2,"p":3,"q":1,"r":4,"s":4,"t":4,
          "u":1,"v":2,"w":1,"x":1,"y":2,"z":1
}
vocabulary=[]
qTable=[]
n=input("How many episodes")
qVals=[]
valid=bool(0)
for nEpisodes in range(int(n)):
 wordValue=0
 wordLength=random.randint(2,5)
 aWord=""
 for numOfLetters in range(wordLength):
  letNum=random.randint(0,25)
  aLetter=alphabet[letNum]
  aWord+=aLetter
  wordValue+=letterValues[aLetter]
 print ("I created a word called " + aWord + ", value: " + str(wordValue))
 if aWord in wordsList:
  print ("Fortunately there is such word as " + aWord)
  valid=bool(1)
  vocabulary.append(aWord)
 else:
  print("Just learned there is no such word.")
  valid=bool(0)
 qVals.append(aWord)
 qVals.append(wordValue)
 qVals.append(valid)
 print (qVals)
 qTable.append(qVals)
 qVals.clear()
print("NOW HERE IS WHAT I LEARNED, MY VOCABULARY FOR THE DAY:")
print (vocabulary)
#inputWord=input("enter a word to see if valid")
#inputWord=inputWord.strip()
#if inputWord in wordsList or inputWord.upper() in wordsList:
  #print ("Fortunately there is such word as " + inputWord)
#else:
  #print("Just learned there is no such word.")




