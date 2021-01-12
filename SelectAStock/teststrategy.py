# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:15:46 2020

@author: 15406
"""
import backtrader as bt 
import datetime
import random
import sys
global txtPortfolio
global gotStockDataFrom
import os
import time
class TestStrategy(bt.Strategy):
    
    import matplotlib
   # import matplotlib.pyplot as plt
    global closeList
    global currentStep

    
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        global stockInfo
        global gotStockDataFrom
       # print ("SELF.DATAS[0].time =" + str(self.datas[0].datetime.time(1)))
       # if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
        #    print (self.datas[0].high)
       # print('%s, %s' % (dt.isoformat(), txt))
        if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
          self.datatime= self.datas[0].datetime.time(0)            
          print('%s, %s' % (dt.strftime("%m/%d/%Y"), str(self.datatime) + " " + txt))
          stockInfo+='%s, %s' % (dt.strftime("%m/%d/%Y"), str(self.datatime) + " " + txt + "\n")
        else:
         print('%s, %s' % (dt.strftime("%m/%d/%Y"), txt))
         stockInfo+='%s, %s' % (dt.strftime("%m/%d/%Y"), txt) + "\n"
        todaysDate=datetime.datetime.now().strftime("%m/%d/%Y")
        dtFormat=dt.strftime("%m/%d/%Y")
        #if dtFormat == todaysDate:
         #   print("RESETTING CURRENT STEP TO ZERO")
            #currentStep=0
       # global closeList
        
        #shortDate=dt.strftime("%b-%d-%y")
        shortDate=dt.strftime("%m/%d")
       # if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
       #  shortDate += str(self.datatime)[0:5]
       # if not shortDate in closeList:
        if 'Close' in txt:
         closeList.append(shortDate)

        
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.datatime=""
        self.dataclose = self.datas[0].close
        print(self.datas[0].datetime.date(0))
        self.datadate=self.datas[0].datetime.date(0)
        if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
          self.datatime= self.datas[0].datetime.time(0) 
          print ("TIME: " + str(self.datatime))
          
       #     self.datatime=self.datas[0].time
       # self.datahigh = self.datas[0].high
        # To keep track of pending orders
        self.order = None  
 
    def notify_order(self, order):
        global balance
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
                self.log('BOUGHT %2.f SHARES' % numberOfShares)
                balance -= order.executed.price
                self.log('CURRENT BALANCE: %.2f' % balance)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
                balance += order.executed.price
                self.log('CURRENT BALANCE: %.2f' % balance)
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None  
 

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
       
        
    def next(self):
        # Simply log the closing price of the series from the reference
        global gotStockDataFrom
        global closingCount
      # if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
      #    print("SELF.DATAS[0]: " + str(self.datas[0]))
      #    self.log('Close, %.2f' % self.dataclose[0]) 
      # else:
        closingCount += 1
        self.log('Close, %.2f' % self.dataclose[0])
        
       
        global baseline
        global Gt
        global oldReward
        global Return
        global reweighting
        global balance
        global closeValues
        
        global lblBuy
        global entBuyAmount
        global buyAmount
        global lastClosingPrice
        global buyingChoice
        global path
        global stockSymbolString
        global numberOfShares
        global netWorth
        global profit
        global lastClosingPrice
        global tradingAmount
        global currentPrice
        global tradingAmount
        global profitValues
        global dropCount
        global wasBought
        global currentStep
        global qTable
        global qCount
        global tradingDecisions
        global closings
        global model
        global externalRows
        global tradeOption
        global tradeAction
        global currentBalance
        algoChoice=0
        new_model=None
        advantageEst=0
        print (str(currentStep))
        qCount=len(qTable)
       # print (str(qCount))
        readCurrentPrice=0
        readTradingAmount=0
        readNetWorth=0
        readProfit=0
        readNumberOfShares=0
        todaysDate=datetime.datetime.now()
        buy_sell_hold=0
        qValues=[]
       # qTable=[]
        r=0
       # global portfolioFile
       # stockSymbolString=txtStockSymbol.get()
        currentPrice=self.dataclose[0]
        portFile='./portfolio/' + stockSymbolString + '.csv'
        profitValues=[]
        print ("PROFIT VALUES:")
        print (profitValues)
        #print(wasBought.name)
 
       # txtPortfolio.delete(0,END)
      #  txtPortfolio.insert(END,float(round(balance,2)))
      #  stockSymbolString=txtStockSymbol.get().upper()
        todaysDate=datetime.datetime.now().strftime('%m/%d/%Y')
     #   finalPortfolioValue=float(txtPortfolio.get())
        epsilon=0.4
        rClip=0
        gamma=0.7
        lastClosingPrice=self.dataclose[0]
 
        global plt
        currentStep += 1
     # print (str(currentStep))
        delayModifier=lastClosingPrice/365
        reward=float(balance) * float(delayModifier)
       # print ("TRACING REWARD VALUE: %.2f" % reward)
        closeValues.append(self.dataclose[0])
        if currentStep == 1:
            if baseline==0:
                baseline=reward
            Return=reward
            #print ("RETURN:" + str(Return))
        else:
            try:
               # print ("CALCULAING BASELINE")
               # print ("CURRENT STEP: " + str(currentStep))
                
               
                if currentStep < 5:
                    Return += reward * (gamma ** currentStep) #DISCOUNTED SUM
                    Gt=Return
                    advantageEst=Return/(currentStep) 
                    if currentStep==4: #DEFINE THE BASELINE
                        baseline=Return/4
                       
                else:
                 #   print ("BASELINE: %.2f" % baseline)
                    algoChoice=random.random()
                    if algoChoice > epsilon:
                        Return += reward
                       # print ("RETURN:" + str(Return))
                        Gt=Return
                      #  baseline=Gt/currentStep
                        advantageEst= Return/(currentStep) - baseline
                        buy_sell_hold=oldReward-reward
    
                        if oldReward == 0:
                            oldReward=reward                
                        else: #CALCULATE THE REWEIGHTING FACTOR
    
                            reweighting=reward/oldReward
                        oldReward=reward #SAVE THE CURRENT VALUE OF REWARDS
                        r=reweighting * advantageEst
                        print ("ADVANTAGE EST: " + str(advantageEst))
                        print("REWEIGHTING: " + str(reweighting))
                        print("REWARD:" + str(reward))
                       # print ("EPSILON: " + str(epsilon))
                        if reweighting  <= 1 -  epsilon and  advantageEst < 0:
                            rClip= (1 -  epsilon) * advantageEst
                        elif reweighting >= 1 +  epsilon and advantageEst > 0:
                            rClip= (1 +  epsilon) * advantageEst
                        else:
                            rClip= reweighting * advantageEst               
                        r = min(r, rClip )
                        print ("VALUE OF r:" + str(r) + ", VALUE OF rClip: " + str(rClip))
                    else:
                        algoChoice=0
                        tradeChoice=random.randint(0,1)
                        print('TRADE CHOICE ' + str(tradeChoice))
                        if tradeChoice == 1:
                            if not self.position:
                                buy_sell_hold=1
                            else:
                                buy_sell_hold=-1
                        else:
                            buy_sell_hold=0
  
            except:
                print ("**ERROR IN ALGORITHM", sys.exc_info()[0])
                

        dt=self.datas[0].datetime.date(0)
        qValues.append(dt.strftime("%m/%d/%Y")) 
        qValues.append(stockSymbolString)
        qValues.append(lastClosingPrice)
        if str(tradeAction.name) == 'HOLD':
            qValues.append('HOLD')
        elif str(tradeAction.name) == 'BUY':
             qValues.append('BUY')
        else:
             qValues.append('SOLD')                 
        qValues.append(balance)

        if buy_sell_hold != 0.0:
            if buy_sell_hold > 0:
                buy_sell_hold=1
            else:
                buy_sell_hold=-1
        qValues.append(buy_sell_hold)
        qTable.append(qValues)
        qCount=len(qTable)
      #  entClosingDate.delete(0,END)
     #   entClosingDate.insert(END,dt.strftime("%m/%d/%Y"))
     #   root.update()
     #   entClosingAmount.delete(0,END)
     #   entClosingAmount.insert(END,str(lastClosingPrice))
    #    root.update()
    
        if (os.path.exists('./portfolio/' + stockSymbolString + '.csv') and str(gotStockDataFrom.name) == 'PORTFOLIOFILE'):
              modTime=time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(portFile)))
              print (modTime)
              print (todaysDate.strftime('%m/%d/%Y'))         
              print('./portfolio/' + stockSymbolString + '.csv')
              print( os.path.exists('./portfolio/' + stockSymbolString + '.csv'))
              print (stockSymbolString)
              print ("FOR STOCK SYMBOL: " + stockSymbolString)
              print ("AMOUNT OF PURCHASE: " + str( tradingAmount))
              print ("CLOSING PRICE: " + str(currentPrice))
             # numberOfShares=floa(tradingAmount)/float(currentPrice)
             # numberOfShare="%.2f" % numberOfShares
            #  print (numberOfShares)
              print ("YOU BOUGHT " + str(numberOfShares))
              #balance -= float(tradingAmount)
              print ("YOUR BALANCE: " + str(balance))
              print ("BALANCE: " + str(type(balance)) + " NUMBER OF SHARES: " + str(type(numberOfShares)) + " CURRENT PRICE: " + str(type(currentPrice)))
              netWorth=float(balance) + float(numberOfShares) * float(currentPrice)
              netWorth=round(netWorth,2)
              print ("NET WORTH: " + str(netWorth))
              profit=netWorth-float(balance)
              profit=round(profit,2)
              print ("PROFIT: " + str(profit))
              portfolioRows=""
              portfolioFileName=stockSymbolString + ".csv"
             # currentPortfolioDate=str(currentPortfolioDate)[:10] 
              todaysDate=str(todaysDate)[:10]
              print ('CURRENT PORTFOLIO DATE: ' + str(currentPortfolioDate) + " TODAYS DATE: " + str(todaysDate))        
              csvRows=[self.datas[0].datetime.date(0), stockSymbolString, string(tradeAction.name),currentPrice, balance,netWorth,profit]      
              profitValues.append(profit)
              with open('./portfolio/' + portfolioFileName, 'a') as portfolioFile:
                     csvWriter=csv.writer(portfolioFile)
                     csvWriter.writerow(csvRows) 

       
 
        
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
       # print("REWARD: " + str(reward))
        
       # if str(wasBought.name) == 'YES':
       #   if oldReward > reward:
       #       if dropCount < 3:
       #           dropCount += 1
       #       else:
       #           dropCount=0
       #           entSellAmount.delete(0,END)
       #           entSellAmount.insert(END,float(netWorth))
       #           lblSell.pack()
       #           entSellAmount.pack()
       #           rbYesSell.pack()
       #           rbNoSell.pack()

                   # qTable.append(qValues)
                    
            # Not yet ... we MIGHT BUY if ...
       # if not self.position:
        # if self.dataclose[0] < self.dataclose[-1]:
                       # current close less than previous close
                    
           # if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
               # if (str(gotStockDataFrom.name) == 'CHECKHISTORY' or str(gotStockDataFrom.name) == 'FROMEXTERNALFILE'): #or str(gotStockDataFrom.name) == 'FROMEXTERNALFILE'
                 #   self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                 #   self.order = self.buy()
                      #  elif str(wasBought.name) == 'NO':
                      #        lblBuy.place(x=500,y=1100)
                      #        entBuyAmount.place(x=500,y=1150)
                      #        btnBuy.place(x=500,y=1200)
  

       # Already in the market ... we might sell
       # else:
       #     print("SELLING:")
       #   if (str(gotStockDataFrom.name) == 'CHECKHISTORY'  or str(gotStockDataFrom.name) == 'FROMEXTERNALFILE'):
         #    if len(self) >= (self.bar_executed + 5):
                 # SELL, SELL, SELL!!! (with all possible default parameters)
         #        self.log('SELL CREATE, %.2f' % self.dataclose[0])

                 # Keep track of the created order to avoid a 2nd order
            #     self.order = self.sell() 

       
        tradingDecisions.append(buy_sell_hold)
        closings.append(lastClosingPrice)
       # print(tradingDecisions)
       # print(closings)
        print ("QCOUNT = " + str(qCount))   
        print(not self.position)
        print(str(len(qTable)))             
        if not self.position:
            if len(qTable) >= 7:
                if qTable[qCount-1][5] == 1 and qTable[qCount-2][5] == 1:
                 if qTable[qCount-2][5] == 1 and qTable[qCount-3][5] == 1: 
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    percent=random.random()
                    if percent > 0.5: percent=0.5
                    buyAmount=percent * balance
                    balance -= buyAmount
                    print ('BUY AMOUNT: ' + str(buyAmount))
                    print ('LAST CLOSING: ' + str(lastClosingPrice))
                    numberOfShares=float(buyAmount)/float(lastClosingPrice)
                    print('SHARES: ' + str(numberOfShares))
                    qValues.clear()
                    qValues.append(dt.strftime("%m/%d/%Y")) 
                    qValues.append(stockSymbolString)
                    qValues.append(lastClosingPrice)
                    netWorth=balance + numberOfShares * lastClosingPrice
                    netWorth=round(netWorth,2)
                    qValues.append('BUY')
                    qValues.append(balance)
                   # qValues.append(reward)
                    qValues.append(0)
                   # qTable.append(qValues)
        else:
            if len(qTable) >= 7:
                if qTable[qCount-1][5] == -1 and qTable[qCount-2][5] == -1 and qTable[qCount-3][5] == -1:    
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])  
                    self.order = self.sell()
                    qValues.clear()
                    qValues.append(dt.strftime("%m/%d/%Y")) 
                    qValues.append(stockSymbolString)
                    qValues.append(lastClosingPrice)                   
                    qValues.append('SELL')
                    balance += numberOfShares * lastClosingPrice
                    netWorth=balance + numberOfShares * lastClosingPrice
                    netWorth=round(netWorth,2)
                    print ('BALANCE AFTER SALE: ' + str(balance))
                    qValues.append(balance)
                    qValues.append(0)
        print(dt.strftime("%m/%d/%Y"))

        print ('EXTERNAL ROWS: ' + str(externalRows) + " CLOSING COUNT: " + str(closingCount))
        if dt.strftime("%m/%d/%Y") == todaysDate or (str(gotStockDataFrom.name) == 'FROMEXTERNALFILE' and currentStep == externalRows):
        # if qCount == 21:
            try:
                tradingDecisions=np.array(*tradingDecisions)
                closings=np.array(*closings)
                print ("TRAINING:")
                
                model.fit(tradingDecisions, closings, epochs=100)
                print(model.predict([-1])[0][0])
                print(model.predict([0])[0][0])
                print(model.predict([1])[0][0])
                sellOption=abs(lastClosingPrice-float(model.predict([-1])))
                holdOption=abs(lastClosingPrice-float(model.predict([0])))
                buyOption=abs(lastClosingPrice-float(model.predict([1])))
                tradeOptions={'SELL':sellOption,'HOLD':holdOption,'BUY':buyOption}
                sortOptions=sorted(tradeOptions.items(),key=lambda x: x[1])
                mb.showinfo("TODAY'S TRADE OPTION FOR " + stockSymbolString, "For this stock today I say " + sortOptions[0][0])
                if sortOptions[0][0] == 'HOLD':
                 tradeAction=tradeOption.HOLD
                elif sortOptions[0][0] == 'BUY':
                   tradeAction=tradeOption.BUY
                else:
                    tradeAction=tradeOption.SELL
                print(todaysDate)
                print (dt.strftime("%m/%d/%Y"))
            except:
                print("SORRY, NOT TRAINING")
                pass
