#THE RANDOM NUMBER GENERATOR
import random

#INITIALIZE TAXI GRID, POPULATE CELLS WITH -1, EXCEPT FOR THE COLOR PLACES FOR THE TAXI'S PICKUP AND DELIVERY.
#IN THAT CASE VALUES ARE 20
taxiGrid = [[-1 for i in range(5)] for j in range(5)]
taxiGrid[0][0]=20
taxiGrid[0][4]=20
taxiGrid[4][0]=20
taxiGrid[4][3]=20

#THE DIRECTIONS FOR EACH CELL OR STATE
direction=["NORTH", "SOUTH", "EAST", "WEST"]


#TAXI'S CURRENT LOCATION -- THE NUMBERS GENERATED HERE ARE THE ROW AND COLUMN OF THE GRID
navRow=random.randint(0,4)
navCol=random.randint(0,4)

#THE LIST OF PLACES FOR THE TAXI TO GO FOR PICKUP AND DELIVERY OF PASSENGER
place=["RED", "GREEN", "YELLOW", "BLUE"]

#PICK A SOURCE AND DESTINATION CORRESPONDING TO THE ORDER OF THE PLACE ON THE LIST ABOVE
sourcePlace=random.randint(0,3)
destPlace=random.randint(0,3)

#THIS WHILE LOOP ENSURES THAT THE SOURCE AND DESTINATION ARE NOT THE SAME
while destPlace == sourcePlace:
 destPlace=random.randint(0,3)

#THE ROWS AND COLUMNS OF THE COLOR PLACES
if place[sourcePlace]=="RED":
 colorLocationSourceRow=0
 colorLocationSourceCol=0
if place[sourcePlace]=="GREEN":
 colorLocationSourceRow=0
 colorLocationSourceCol=4
elif place[sourcePlace]=="YELLOW":
 colorLocationSourceRow=4
 colorLocationSourceCol=0
elif place[sourcePlace]=="BLUE":
 colorLocationSourceRow=4
 colorLocationSourceCol=3
if place[destPlace]=="RED":
 colorLocationDestRow=0
 colorLocationDestCol=0
if place[destPlace]=="GREEN":
 colorLocationDestRow=0
 colorLocationDestCol=4
elif place[destPlace]=="YELLOW":
 colorLocationDestRow=4
 colorLocationDestCol=0
elif place[destPlace]=="BLUE":
 colorLocationDestRow=4
 colorLocationDestCol=3
#INITILIZE q	
q=0
#INITALIZE qTable
qTable=[]

#THE qVals LIST IS WHERE TO PUT THE STATE ACTION PAIR VALUES FOR EACH TIMESTEP
qVals=[]

#alpha IS PART OF THE Q UPDATING FOMULA
alpha=0.25

#HERE THE VALUE OF epsilon IS USED FOR THE EPSILON GREEDY POLICY
#SUCH THAT IF THE EPSILON GREEDY POLICY VALUE IS GREATER THAN 0.5, USE THE DETERMINISTIC,
#OTHERWISE USE THE STOCHASTIC (RANDOM)
epsilon=0.5

#INITIALIZE TIMESTEP
t=0

#THIS PRINT STATEMENT WILL BE DISPLAYED FOR EACH TIMESTEP, TO REMIND THE USER WHERE THE PASSENGER IS FROM
#AND GOING TO
print("PASSENGER AT LOCATION " + place[sourcePlace] + " IS GOING TO LOCATION " + place[destPlace])
qVals=[]
#CURRENT POSITION OF THE TAXI
print ("Our taxi is at location " + str(navRow) + ", " + str(navCol))

#REWARD VALUE FOR FIRST POSITION THE TAXI IS IN
reward=taxiGrid[navRow][navCol]
#WHERE DOES OUR TAXI PICK UP THE PASSENGER?  DEPENDS ON THE CELL WHERE THE PASSENGER IS WAITING.
#THE TAXI IS NOW ON ITS WAY TO THE PASSENGER AT THE SOURCE
#
#THIS IS WHERE IT'S COMPLEX.  
#THE CALCULATIONS BELOW MAKE ESTIMATES OF NORTH, SOUTH, WEST AND EAST, CORRESPONDING TO WHERE THE TAXI IS GOING.
#THE SUBSCRIPTS ARE ZERO INDEXED.
#FOR INSTANCE, RED IS ON THE NORTHWEST CORNER OF THE GRID, THUS THE LARGER ESTIMATE VALUES LEAN TOWARD
#THE NORTH AND WEST DIRECTIONS.  HERE, IN GENERAL THE ACTION VALUE IS THE REWARD AT THE CURRENT STATE (-1), PLUS
#THE SUM OF ALL -1'S IN THE ROWS OF COLUMNS TOWARD THE TAXI, AND THE COLUMNS TOWARD THE CURRENT ROW THE TAXI IS IN.
#ALTHOUGH VARIABLE navRow IS THE CURRENT ROW OF THE TAXI, IT'S ALSO USED FOR THE ROWS ABOVE WHERE THE TAXI IS.
#FOR EXAMPLE, IF THE TAXI IS IN ROW 3 (WHICH IS THE FOURTH ROW), THERE ARE ACTUALLY THREE ROWS ABOVE THE TAXI.
#THAT MULTIPLIED BY THE COLUMNS AND -1 + 20--WHICH IS THE DESTINATION REWARD VALUE--RESULTS IN THE TOTAL ESTIMATE.
if place[sourcePlace]=="RED":
 northEst= reward + 20 + (-1) * (navCol+1)  * (navRow)
#NOTE HERE THAT THERE IS A REWARD OF -10 (PENALTY) FOR MAKING THE WRONG MOVE, NAMELY SOUTH.  APPLIES TO EAST AS WELL.
 southEst =-10 + 20 + (-1) * (navCol+1) * (navRow)
 westEst= reward + 21 + (-1) * (navCol-1)  * (navRow)
 eastEst=9 + (-1) * (navCol+1)  * (navRow)

#HERE GREEN IS NORTHEAST, THUS THE LARGER ESTIMATE VALUES APPLY TO NORTH AND EAST
elif place[sourcePlace]=="GREEN":
 northEst= reward + 20 + (-1) * (navCol+1) * (navRow)
 southEst =-10 + 20 + (-1) * (navCol+1)  * (navRow)
 westEst= 9 + (-1) * (navCol-1)  * (navRow)
 eastEst= reward + 21  + (-1) * (navCol+1)  * (navRow)

#HERE, THE YELLOW AND BLUE PLACES ARE SOUTHWARD, BELOW WHERE THE TAXI IS LOCATED.  THE CALCULATIONS DIFFER THERE.
elif place[sourcePlace]=="YELLOW":
 northEst= -10 + 20 + (-1) * (navCol+1) * (4-navRow)
 southEst = reward + 20 + (-1) * (navCol+1)  * (4-navRow)
 westEst= reward + 21  + (-1) * (navCol-1)  * (4-navRow)
 eastEst=9 + (-1) * (navCol+1)  * (4-navRow)
elif place[sourcePlace]=="BLUE":
 northEst= -10 + 20  + (-1) * (navCol-1)  * (4-navRow)
 southEst = reward + 20 + (-1) * (navCol+1)  * (4-navRow)
 westEst= 9 + (-1) * (navCol-1) * (4-navRow)
 eastEst=reward + 21 + (-1) * (navCol+1)  * (4-navRow)
#HERE, THE LIST OF STATE ACTION PAIR VALUES ARE STORED IN qVals.
qVals=[northEst, southEst, eastEst, westEst]
#THEN ADDED TO THE Q-TABLE
qTable.append(qVals)

#NOW THE TAXI MAKES ITS JOURNEY TO THE PASSENGERS PLACE
while not(navRow==colorLocationSourceRow and navCol==colorLocationSourceCol): 
#HERE IS OUR RANDOM GENERATOR FOR THE EPSILON GREEDY POLICY
 epsGreed=random.random()
#IF epsGreed IS LESS THAN epsilon THEN CHOOSE A DIRECTION AT RANDOM (EXPLORE)
 if epsGreed < epsilon:
  moveDir=random.randint(0,3)
  print ("EXPLORING...")
#OTHERWISE, CHOOSE THE DIRECTION FOR THE DETERMINISTIC METHOD BY FINDING THE LARGEST ACTION VALUE.
#THE LIST POSITION IN qVals THAT CONTAINS THE MAXIMUM VALUE DETERMINES THE APPROPRIATE DIRECTION. (EXPLOITING)
 else:
  pMax=0
  qMax=0
  for pos in range(4):
   if qVals[pos]>qMax:
    pMax=pos
    qMax=qVals[pos]
   moveDir=pMax
  print ("EXPLOITING...")
#THUS WHICHEVER METHOD THE TAXI CHOSE IS GENERATED IN THE moveDir VARIABLE.
#OBSERVE THAT IF THE TAXI HITS A WALL, IT STAYS IN THE CURRENT CELL POSITION.
 print ("Taxi goes ",)
#GOING NORTH
 if moveDir == 0:
  if navRow -1 < 0:
   navRow=navRow
  else:
   navRow-=1
  print (direction[moveDir])
#GOING SOUTH
 elif moveDir == 1:
  if navRow + 1 > 4:
   navRow =navRow
  else:
   navRow +=1
  print (direction[moveDir])
#GOING EAST
 elif moveDir == 2:
  if navCol + 1 > 4:
   navCol=navCol
  else:
   navCol +=1
  print (direction[moveDir])
#GOING WEST
 elif moveDir == 3:
  if navCol -1 < 0:
   navCol=navCol
  else:
   navCol -=1
  print (direction[moveDir])
#UPDATE Q-TABLE
 qTable.append(qVals)
 print (qVals)
 print (str(navRow) + ", " + str(navCol))
#UPDATE THE REWARD FOR THE CURRENT STATE AND ACTION
 reward=taxiGrid[navRow][navCol]
 print("PASSENGER AT LOCATION " + place[sourcePlace] + " IS GOING TO LOCATION " + place[destPlace])
 print ("Our taxi is at location " + str(navRow) + ", " + str(navCol))
#HERE AGAIN, THE DIRECTION ESTIMATES ARE CALCULATED DEPENDING ON WHERE THE TAXI TURNED AND WHERE IT'S GOING.
#ESTIMATES FOR RED
 if place[sourcePlace]=="RED":
  if navRow == 0:
    northEst=-1
  else:  
   northEst= reward + 20 + (-1) * (navCol-1)  + (-1) * (navRow-1)
  southEst =-10 + 20 + (-1) * (navCol+1)   + (-1) * (navRow)
  if navCol == 0:
    westEst=-1
  else:
   westEst= reward + 21 + (-1) * (navCol-1)  + (-1) * (navRow)
  eastEst=9 + (-1) * (navCol+1)  * (navRow)
#ESTIMATES FOR GREEN
 elif place[sourcePlace]=="GREEN":
  if navRow == 0:
   northEst=-1
  else:  
   northEst= reward + 20 + (-1) * (navCol+1) + (-1) * (navRow-1)
  southEst =-10 + 20 + (-1) * (navCol+1)  + (-1) * (navRow+1)
  westEst= 9  + (-1) * (navCol-1) + (-1) * (navRow)
  if navCol == 4:
    eastEst=-1
  else:
   eastEst= reward + 21 + (-1) * (navCol+1) + (-1) * (navRow)

#ESTIMATES FOR YELLOW
 elif place[sourcePlace]=="YELLOW":
  northEst= -10 + 20 + (-1) * (navCol+1)  + (-1) * (navRow+1)
  if navRow == 4:
   southEst=-1
  else:
   southEst = reward + 20 + (-1) * (navCol-1)  + (-1) * (navRow-1)
  if navCol == 0:
   westEst =-1
  else:
   westEst= reward + 21  + (-1) * (navCol-1) + (-1) * (navRow)
  eastEst=9 + (-1) * (navCol+1)  * (navRow +1)

#ESTIMATES FOR BLUE
 elif place[sourcePlace]=="BLUE":
  northEst= -10 + 20  + (-1) * (navCol)  + (-1) * (navRow + 1)
  if navRow == 4:
   southEst=-1
  else:
   southEst = reward + 20 + (-1) * (navCol)  + (-1) * (navRow + 1)
  if navCol ==4 and navRow == 4:
   westEst=reward + 21 + (-1) * (navCol-1)   + (-1) * (navRow)
  elif navCol == 0:
   westEst=-1
  else:
   westEst= 9 + (-1) * (navCol-1) +    (-1) * (navRow + 1)
  if navCol ==4:
   eastEst=-1
  else:
   eastEst=reward + 21 + (-1) * (navCol+1)   + (-1) * (navRow)
#A NEW TUPLE OF DIRECTION ESTIMATE VALUES FOR qVals
 qVals.clear()
 qVals=[northEst, southEst, eastEst, westEst ]  
#UPDATE Q-TABLE
 qTable.append(qVals)
#THE NEW Q VALUE FOR UPDATING THE FORMULA
 newQ=qVals[moveDir]
 q = q + alpha * (reward + newQ - q)
#COUNT THE TIMESTEP
 t+=1
#NOW REDUCE THE VALUE OF EPSILON TO HELP THE TAXI LEARN TO EMPHASIZE THE DETERMINISTIC METHOD
 if epsilon > 0.1:
  epsilon -= 0.00001

#THE TAXI FINALLY MAKES IT TO WHERE IT'S PICKING UP THE PASSENGER
print ("FINALLY GETS THE GUY AT " + place[sourcePlace])
print ("NOW WE WILL DELIVER THE PASSENGER TO LOCATION " + place[destPlace])
print ("BUT WE'RE STILL AT " + str(navCol) + ", " + str(navRow) + "; HERE WE GO:")
#THIS IS THE SAME PROCEDURE AS ABOVE, BUT ON THE TAXI'S WAY TO THE PASSENGER'S DESTINATION
q=0
qTable=[]
alpha=0.25
epsilon=0.5
t=0
while not(navRow==colorLocationDestRow and navCol==colorLocationDestCol):
 epsGreed=random.random()
 if epsGreed < epsilon:
  moveDir=random.randint(0,3)
  print ("EXPLORING...")
 else:
  pMax=0
  qMax=0
  for pos in range(4):
   if qVals[pos]>qMax:
    pMax=pos
    qMax=qVals[pos]
   moveDir=pMax
  print ("EXPLOITING...")
 print ("Taxi goes ",)
 if moveDir == 0:
  if navRow -1 < 0:
   navRow=navRow
  else:
   navRow-=1
  print (direction[moveDir])
 elif moveDir == 1:
  if navRow + 1 > 4:
   navRow =navRow
  else:
   navRow +=1
  print (direction[moveDir])
 elif moveDir == 2:
  if navCol + 1 > 4:
   navCol=navCol
  else:
   navCol +=1
  print (direction[moveDir])
 elif moveDir == 3:
  if navCol -1 < 0:
   navCol=navCol
  else:
   navCol -=1
  print (direction[moveDir])
 qTable.append(qVals)
 print (qVals)
 print (str(navRow) + ", " + str(navCol))
 reward=taxiGrid[navRow][navCol]
 print("PASSENGER AT LOCATION " + place[sourcePlace] + " IS GOING TO LOCATION " + place[destPlace])
 print ("Our taxi is at location " + str(navRow) + ", " + str(navCol))
 if place[destPlace]=="RED":
  if navRow == 0:
    northEst=-1
  else:  
   northEst= reward + 20 + (-1) * (navCol-1)  + (-1) * (navRow-1)
  southEst =-10 + 20 + (-1) * (navCol+1)   + (-1) * (navRow)
  if navCol == 0:
    westEst=-1
  else:
   westEst= reward + 21 + (-1) * (navCol-1)  + (-1) * (navRow)
  eastEst=9 + (-1) * (navCol+1)  * (navRow)
 elif place[destPlace]=="GREEN":
  if navRow == 0:
   northEst=-1
  else:  
   northEst= reward + 20 + (-1) * (navCol+1) + (-1) * (navRow-1)
  southEst =-10 + 20 + (-1) * (navCol+1)  + (-1) * (navRow+1)
  westEst= 9  + (-1) * (navCol-1) + (-1) * (navRow)
  if navCol == 4:
    eastEst=-1
  else:
   eastEst= reward + 21 + (-1) * (navCol+1) + (-1) * (navRow)
 elif place[destPlace]=="YELLOW":
  northEst= -10 + 20 + (-1) * (navCol+1)  + (-1) * (navRow+1)
  if navRow == 4:
   southEst=-1
  else:
   southEst = reward + 20 + (-1) * (navCol-1)  + (-1) * (navRow-1)
  if navCol == 0:
   westEst =-1
  else:
   westEst= reward + 21  + (-1) * (navCol-1) + (-1) * (navRow)
  eastEst=9 + (-1) * (navCol+1)  * (navRow +1)
 elif place[destPlace]=="BLUE":
  northEst= -10 + 20  + (-1) * (navCol)  + (-1) * (navRow + 1)
  if navRow == 4:
   southEst=-1
  else:
   southEst = reward + 20 + (-1) * (navCol)  + (-1) * (navRow + 1)
  if navCol ==4 and navRow == 4:
   westEst=reward + 21 + (-1) * (navCol-1)   + (-1) * (navRow)
  elif navCol == 0:
   westEst=-1
  else:
   westEst= 9 + (-1) * (navCol-1) +    (-1) * (navRow + 1)
  if navCol ==4:
   eastEst=-1
  else:
   eastEst=reward + 21 + (-1) * (navCol+1)   + (-1) * (navRow)
 qVals.clear()
 qVals=[northEst, southEst, eastEst, westEst ]  
 qTable.append(qVals)
 newQ=qVals[moveDir]
 q = q + alpha * (reward + newQ - q)
 t+=1
 if epsilon > 0.1:
  epsilon -= 0.00001
print("FINALLY, OUR FRIENDLY CABBIE ARRIVES AT " + place[destPlace] + " AND DELIVERS THE PASSENGER THERE!")

 

 

