# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 20:15:25 2020

@author: 15406
"""
 
import datetime

import os.path, time  # To manage paths
from os import path
import sys
from tkinter import messagebox as mb
from tkinter import ttk
import tensorflow as tf
from tensorflow import keras
from scipy import stats
import numpy as np 
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import random
stockBought=False
import csv
global lblSource
closingCount=0
import matplotlib.pyplot as plt
import matplotlib.pyplot as randForst
import pandas as pd

global stockInfo

import backtrader as bt
global stockDataSource
global gotStockDataFrom
baseline=0
tradingDecisions=[]
closings=[]
xList=[]
myModel=[]
myProfits=[]
profitValues=[]
profit=0
netWorth=0
myNetWorth=[]
myDailyBalances=[]
origBalance=0
numberOfShares=0
currentNetWorth=0
currentProfit=0
import tkinter as tk
from tkinter import Label
from tkinter import *

from tkinter.ttk import *


prgClosings=None
global lblDate
global entClosingDate
global lblAmount
global entClosingAmount

root=tk.Tk()
root.withdraw()
lblCloseInfo=tk.Label(root,text="Here is some text.", font='Courier 13')
lblAnalysisInfo=tk.Label(root, font='Arial 14 bold')
class TestStrategy(bt.Strategy):
    
    import matplotlib
   # import matplotlib.pyplot as plt
    global closeList
    global currentStep
    global txtStockSymbol
    global txtPortfolio
    global currentPortfolioDate
    global oldReward
    global reweighting
    global myDailyBalances
    
    print('starting')
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        global stockInfo
        global gotStockDataFrom
       # print ("SELF.DATAS[0].time =" + str(self.datas[0].datetime.time(1)))
       # if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
        #    print (self.datas[0].high)
       # print('%s, %s' % (dt.isoformat(), txt))
       # if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
        #  self.datatime= self.datas[0].datetime.time(0)            
        #  print('%s, %s' % (dt.strftime("%m/%d/%Y"), str(self.datatime) + " " + txt))
        #  stockInfo+='%s, %s' % (dt.strftime("%m/%d/%Y"), str(self.datatime) + " " + txt + "\n")
     #   else:
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
        global stockDataSource
        global gotStockDataFrom
        print ('STARTING')
        self.datatime=""
        self.dataclose = self.datas[0].close
        print(self.datas[0].datetime.date(0))
        self.datadate=self.datas[0].datetime.date(0)
        
        root.title("PROGRESS")
        root.geometry("800x400+600+600")  
        root.configure(bg='#AAAAAA')
        root.deiconify()
        root.overrideredirect(False)

        lblCloseInfo.pack()
        lblAnalysisInfo.pack()
        root.update()

   
      #  prgClosings=ttk.Progressbar(tk, orient="horizontal", maximum=1000,  mode="determinate")
        
      #  prgClosings.start()
        #prgClosings.update()

#     if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':
 #         self.datatime= self.datas[0].datetime.time(0) 
  #        print ("TIME: " + str(self.datatime))
          
       #     self.datatime=self.datas[0].time
       # self.datahigh = self.datas[0].high
        # To keep track of pending orders
        self.order = None 
        baseline=0

 
    def notify_order(self, order):
        global balance
        global netWorth
        netWorth=0
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
        print (closingCount)
       
        global baseline
        global Gt

        global Return
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
        global txtStockSymbol
        global tk
        global stockDataSource
        global gotStockDataFrom
        global oldReward
        global reweighting
        global stockBought
        global myNetWorth
        global myDailyBalances
        global profit
        global netWorth
        global origBalance
        global currentNetWorth
        global currentProfit
        algoChoice=0
        new_model=None
        advantageEst=0
        print ("CURRENT STEP: " + str(currentStep))
        myDailyBalances.append(balance)
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
       
        print ("PROFIT VALUES:")
        print (profitValues)

        #print(wasBought.name)
 
       # tk.txtPortfolio.delete(0,tk.END)
       # tk.txtPortfolio.insert(tk.END,float(round(balance,2)))
      #  stockSymbolString=tk.txtStockSymbol.get().upper()
        todaysDate=datetime.datetime.now().strftime('%m/%d/%Y')
       # finalPortfolioValue=float(txtPortfolio.get())
        epsilon=0.4
        rClip=0
        gamma=0.7
        lastClosingPrice=self.dataclose[0]
 
        global plt
        global randForst
        currentStep += 1
        xList.append(currentStep)
      #  prgClosings.pack()
       # prgClosings=ttk.Progressbar(root, orient="horizontal", length=currentStep,  mode="indeterminate")
      #  prgClosings['value']=currentStep
     #   tk.update()
     #   time.sleep(1)
     #   tk.mainloop()
        

        #prgClosings['length']=currentStep
      #  ttk.mainloop()
        
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
  
            except NameError as error:
                print (error)
                print ("**ERROR IN ALGORITHM", sys.exc_info()[0])
                

        dt=self.datas[0].datetime.date(0)
        qValues.append(dt.strftime("%m/%d/%Y")) 
        qValues.append(stockSymbolString)
        qValues.append(lastClosingPrice)
      #  if str(tradeAction.name) == 'HOLD':
      #      qValues.append('HOLD')
      #  elif str(tradeAction.name) == 'BUY':
      #       qValues.append('BUY')
      #  else:
      #       qValues.append('SOLD')                 
        
        tradeChoice=None
        if buy_sell_hold != 0.0:
            if buy_sell_hold > 0:
                buy_sell_hold=1
                tradeChoice="BUY"
            else:
                buy_sell_hold=-1
                tradeChoice="SELL"
        else:
            tradeChoice="HOLD"
        qValues.append(tradeChoice) 
        qValues.append(balance)
        qValues.append(buy_sell_hold)  
        qTable.append(qValues)
        qCount=len(qTable)
 
        root.lift()
        root.attributes('-topmost', True)
        root.update()          
       # self.tk=tk
       # self.tk.entClosingDate.delete(0,tk.END)
       # self.tk.entClosingDate.insert(tk.END,dt.strftime("%m/%d/%Y"))
       # self.tk.entClosingDate.update()
       # self.tk.entClosingAmount.delete(0,tk.END)
       # self.tk.entClosingAmount.insert(tk.END,str(lastClosingPrice))
       # self.tk.entClosingAmount.update()
      #  root.update()
    
       # if (os.path.exists('./portfolio/' + stockSymbolString + '.csv') and str(gotStockDataFrom.name) == 'PORTFOLIOFILE'):
       #       modTime=time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(portFile)))
       #       print (modTime)
       #       print (todaysDate.strftime('%m/%d/%Y'))         
       #       print('./portfolio/' + stockSymbolString + '.csv')
       #       print( os.path.exists('./portfolio/' + stockSymbolString + '.csv'))
       #       print (stockSymbolString)
       #       print ("FOR STOCK SYMBOL: " + stockSymbolString)
       #       print ("AMOUNT OF PURCHASE: " + str( tradingAmount))
       #       print ("CLOSING PRICE: " + str(currentPrice))
       #      # numberOfShares=floa(tradingAmount)/float(currentPrice)
             # numberOfShare="%.2f" % numberOfShares
            #  print (numberOfShares)
       #       print ("YOU BOUGHT " + str(numberOfShares))
       #       #balance -= float(tradingAmount)
       #       print ("YOUR BALANCE: " + str(balance))
       #       print ("BALANCE: " + str(type(balance)) + " NUMBER OF SHARES: " + str(type(numberOfShares)) + " CURRENT PRICE: " + str(type(currentPrice)))
       #       netWorth=float(balance) + float(numberOfShares) * float(currentPrice)
       #       netWorth=round(netWorth,2)
       #       print ("NET WORTH: " + str(netWorth))
       #       profit=netWorth-float(balance)
       #       profit=round(profit,2)
        #      print ("PROFIT: " + str(profit))
       #       portfolioRows=""
        #      portfolioFileName=stockSymbolString + ".csv"
             # currentPortfolioDate=str(currentPortfolioDate)[:10] 
        #      todaysDate=str(todaysDate)[:10]
        #      print ('CURRENT PORTFOLIO DATE: ' + str(currentPortfolioDate) + " TODAYS DATE: " + str(todaysDate))        
        #      csvRows=[self.datas[0].datetime.date(0), stockSymbolString, str(tradeAction.name),currentPrice, balance,netWorth,profit]      
        #      profitValues.append(profit)
        #      with open('./portfolio/' + portfolioFileName, 'a') as portfolioFile:
        #             csvWriter=csv.writer(portfolioFile)
        #             csvWriter.writerow(csvRows) 

       
 
        
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
                    stockBought=True
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
                    currentNetWorth=netWorth
                   # myNetWorth.append(netWorth)
                    profit=netWorth-float(balance)
                    profit=round(profit,2) 
                    currentProfit=profit
                  #  myProfits.append(profit)
                    qValues.append('BUY')
                    qValues.append(balance)
                   # qValues.append(reward)
                    qValues.append(0)
                   # qTable.append(qValues)
                    newCloseText=stockSymbolString.upper() + "\n\r"
                    newCloseText+=str("DATE: " + dt.strftime("%m/%d/%Y")) + " CLOSING PRICE: " + str(lastClosingPrice) + "\n\r"
                    newCloseText+=" NET WORTH: " + str(netWorth) + "\n\r"
                    newCloseText+=" PROFIT: " + str(profit) + "\n\r"
                    newCloseText+= "BALANCE: " + str(round(balance,2)) +  " BUY"                      
                    lblCloseInfo['text']=newCloseText
                    root.lift()
                    root.attributes('-topmost', True)
                    root.update()  
 
                
        else:
            if len(qTable) >= 7:
                if qTable[qCount-1][5] == -1 and qTable[qCount-2][5] == -1 and qTable[qCount-3][5] == -1:    
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])  
                    self.order = self.sell()
                    stockBought=False
                    qValues.clear()
                    qValues.append(dt.strftime("%m/%d/%Y")) 
                    qValues.append(stockSymbolString)
                    qValues.append(lastClosingPrice)                   
                    qValues.append('SELL')
                    balance += numberOfShares * lastClosingPrice
                    netWorth=balance + numberOfShares * lastClosingPrice
                    netWorth=round(netWorth,2)
                    currentNetWorth=netWorth                   
                 #   myNetWorth.append(netWorth)
                    profit=netWorth-float(balance)
                    profit=round(profit,2)  
                    currentProfit=profit
                 #   myProfits.append(profit)                    
                    print ('BALANCE AFTER SALE: ' + str(balance))
                    qValues.append(balance)
                    qValues.append(0)
 
                    newCloseText=stockSymbolString.upper() + "\n\r"
                    newCloseText+=str("DATE: " + dt.strftime("%m/%d/%Y")) + " CLOSING PRICE: " + str(lastClosingPrice) + "\n\r"
                    newCloseText+=" NET WORTH: " + str(netWorth) + "\n\r"
                    newCloseText+=" PROFIT: " + str(profit) + "\n\r"
                    newCloseText+= "BALANCE: " + str(round(balance,2)) +  " SELL"                
                    lblCloseInfo['text']=newCloseText
                    root.lift()
                    root.attributes('-topmost', True)
                    root.update()
   
        myNetWorth.append(currentNetWorth)                  
        myProfits.append(currentProfit)

        #print ('EXTERNAL ROWS: ' + str(externalRows) + " CLOSING COUNT: " + str(closingCount))
        if dt.strftime("%m/%d/%Y") == todaysDate : #or (str(gotStockDataFrom.name) == 'FROMEXTERNALFILE' and currentStep == externalRows)
         if qCount == 21:
            try:
                print (qTable)
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
              #  mb.showinfo("TODAY'S TRADE OPTION FOR " + stockSymbolString, "For this stock today I say " + sortOptions[0][0])
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
        
        

def missing_portfolio_value():
     mb.showinfo("PORTFOLIO MISSING", "Please enter a numeric portfolio amount!")



     
def button_click(bt,tk,txtStockInfo, txtStockSymbol,  lblStockHistory, txtPortfolio, txtPortfolioData,  currentPortfolioDate,stockDataSource, gotStockDataFrom, closingCount, tradeAction, btnSavePortfolioFile, fullPath):
    global loadCSV
    global qTable
    global currentStep
    global tf
    global oldReward
    global reweighting
  #  global lblDate
  #  global entClosingDate
  #  global lblAmount
  #  global entClosingAmount
    global root
    global stockSymbolString

    #global currentPortfolioDate
    if str(gotStockDataFrom.name) != 'FROMEXTERNALFILE': gotStockDataFrom= stockDataSource.CHECKHISTORY
    print ("NOW GETTING HISTORY, SOURCE: " + str(gotStockDataFrom.name))
    print ("FULL PATH: " + str(fullPath))
   # sys.exit(0)
    
    currentStep=0
    oldReward=0
    reweighting=0
    qTable=[]
    txtStockInfo.delete('1.0',tk.END)
    stockSymbolString=txtStockSymbol.get().upper()
    lblStockHistory['text']="Stock history for " + stockSymbolString
    print ("YOU CLICKED FOR SYMBOL " + stockSymbolString)
   # txtPortfolio.insert(tk.END, '0')
    numPort=round(float(txtPortfolio.get()),0)
    print(isinstance(numPort,float))
    txtPortfolioData.delete('1.0',tk.END)
    if txtPortfolio.get().strip() == '' or txtPortfolio.get() == '0' or not isinstance(numPort,float):
        #missing_portfolio_value()
        return
    try:
        portfolioValue=float(txtPortfolio.get())
    except:
        portfolioValue=0
    global origBalance
    
    global stockInfo
    global balance
    stockInfo=""
    cerebro = bt.Cerebro()
    global plt
    global randForst
    global closeList
    global closeValues



    global numberOfShares
    global currentPrice
    global trading
    global netWorth
    global profit
    global tradingAmount
    global portfolioUpdated
    global tradingDecisions
    global closings
    global model
    global externalRows
    global baseline
    global theMean
    global np
    dfpredictors=[]
    oldReward=0
    reweighting=0
    origBalance=portfolioValue
   # print ("CURRENT PORTFOLIO DATE: " + str(currentPortfolioDate))
    itsFrom=None
    todaysDate=None
    qCount=0
    print("YOUR DATA SOURCE: " + gotStockDataFrom.name)
   # print( str(gotStockDataFrom.name) == 'CHECKHISTORY')
    #global portfolioValue
  #  print ('YOUR CURRENT PORTFOLIO: %.2f' % portfolioValue )
  #  print ('NUMBER OF SHARES: ' + str(numberOfShares))
 #   print ('CURRENT PRICE: ' + str(currentPrice))
  #  print ('NET WORTH: ' + str(netWorth))
    closeList=[]
    closeValues=[]
    profitValues=[]
    itsFrom=datetime.datetime.now()
    

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
   #datapath = os.path.join(modpath, './datas/orcl-1995-2014.csv')

    # Create a Data Feed
    todaysDate=datetime.datetime.now()
    halfYearBack=todaysDate + datetime.timedelta(days=-180)
    lastMonth=todaysDate + datetime.timedelta(days=-30)
    lastYear=todaysDate + datetime.timedelta(days=-365)
    print("FILENAME: " + str(fullPath))
    print("DATA SOURCE: " + str(gotStockDataFrom.name))
    if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE':  

        print('FROM EXTERNAL:')
       # sys.exit(0)
        data=bt.feeds.GenericCSVData(
            dataname=fullPath,
            fromdate=halfYearBack,
            todate=todaysDate,
            timeframe=bt.TimeFrame.Minutes,
            dtformat=('%Y.%m.%d'),
            tmformat=('%H:%M'),
            datetime=0,
            time=1,
            open=2,
            high=3,
            low=4,
            close=5,
            volume=6,
            
            reverse=False
            )
        
        cerebro.adddata(data)
        cerebro.broker.setcash(portfolioValue)
        balance=portfolioValue
        stockInfo += 'Starting Portfolio Value: %.2f' % portfolioValue + "\n"
        print (stockInfo)
        # Run over everything
        closingCount=0
        cerebro.run()

            
    # Print out the final result
        #finalPortfolioValue=cerebro.broker.getvalue()
        finalPortfolioValue=balance
        print('Final Portfolio Value: %.2f' % finalPortfolioValue)    # Plot the result
        stockInfo += 'Final Portfolio Value: %.2f' % finalPortfolioValue  
        txtPortfolio.delete(0,tk.END)
        txtPortfolio.insert(tk.END,float(round(finalPortfolioValue,2)))
        txtStockInfo.insert(tk.END, stockInfo)
        btnSavePortfolioFile["state"]="normal"
        btnSavePortfolioFile["bg"]='yellow'
        finalPortfolioValue=cerebro.broker.getvalue()
        #cerebro.plot(iplot= False)
        plt.suptitle("STOCK CLOSING DATA FOR " + stockSymbolString + " " + str(lastYear.strftime("%b-%d-%y")) + " - " + str(todaysDate.strftime("%b-%d-%y"))) #
      #  print (closeList)
        model=keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
        model.compile(optimizer='sgd', loss='mean_squared_error')
        new_model=None
        checkpoint_path = "training_1/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        # Create a callback that saves the model's weights
        cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)       
        try:
                tradingDecisions=np.array(tradingDecisions)
                closings=np.array(closings)
               
                if not path.exists('./saved_model_external/my_model'):
                    # Train the model with the new callback
                    model.fit(tradingDecisions, 
                              closings,  
                              epochs=50)  # Pass callback to training
                    
                   # model.save('saved_model_external/my_model')  
                    tf.saved_model.save(model,'./saved_model_external/my_model')
                else:
                   # model = keras.models.load_model('saved_model/my_model')
                   # loss, acc = model.evaluate(tradingDecisions, closings, verbose=2)
                   print("SAVED MODEL EXISTS --")
                  # model=keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
                  # model.compile(optimizer='sgd', loss='mean_squared_error')                   
                 #  new_model=keras.models.load_model('saved_model_external/my_model')
                 #  new_model.summary()
                 #  new_model.evaluate(tradingDecisions,  closings, verbose=2)
                  # print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
                  # model = tf.saved_model.load('./saved_model_external/my_model')
                   print ("LOADING SAVED MODEL TO NEW MODEL:")
                   new_model = keras.models.load_model('saved_model_external/my_model')
                  # print (new_model)
                   print("CALCULATING LOSS & ACCURACY:")
                   acc=new_model.evaluate(tradingDecisions, closings, verbose=2)
                   print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
                   lastClosingPrice=closings[currentStep-1]
                   #print(new_model.predict(tradingDecisions).shape)
                  # print(list(model.signatures.keys()))  # ["serving_default"]
                #   print("NEW MODEL PREDICT:")
                  # print(new_model.predict(tradingDecisions))
                  # loss,acc = model.evaluate(tradingDecisions, closings, verbose=2)
                   #new_model.summary()
                   model=new_model
                print("PREDICTION: ")    
                print(model.predict([-1])[0][0])
                print(model.predict([0])[0][0])
                print(model.predict([1])[0][0])
                predictValue=float(model.predict([0])[0][0])
                print ("PREDICT VALUE: " + str(predictValue))
                print ("LAST CLOSING PRICE: " + str(lastClosingPrice))
                scale=round(predictValue/lastClosingPrice, 2) 
                print("SCALED: " + str(scale))
                lastClosingPrice = lastClosingPrice * scale
                sellOption=abs(lastClosingPrice-float(model.predict([-1])))
                holdOption=abs(lastClosingPrice-float(model.predict([0])))
                buyOption=abs(lastClosingPrice-float(model.predict([1])))
                tradeOptions={'SELL':sellOption,'HOLD':holdOption,'BUY':buyOption}
                sortOptions=sorted(tradeOptions.items(),key=lambda x: x[1])
               # mb.showinfo("TODAY'S TRADE OPTION FOR " + stockSymbolString, "For this stock today I say " + sortOptions[0][0])
                print(todaysDate)
                #print (dt.strftime("%m/%d/%Y"))
        except:
                print("CANNOT LOAD WEIGHTS")
        plt.plot(closeList,closeValues)  
        plt.grid(True)
        plt.show()
 #       lblDate.pack_forget()
 #       entClosingDate.delete(0,END)
 #       entClosingDate.pack_forget()
 #       lblAmount.pack_forget()
 #       entClosingAmount.pack_forget()
 #       entClosingAmount.delete(0,END)
       # gotStockDataFrom=stockDataSource.CHECKHISTORY    
        currentStep=0
        tradingDecisions=[]
        closings=[]
      #  print (qTable)
  
        root.withdraw()
        root.update()
        #tk.mainloop()
        return
    print(gotStockDataFrom.name)
    if (str(gotStockDataFrom.name) == 'CHECKHISTORY'):  
       # itsFrom=lastMonth
       itsFrom=lastYear
    else:
        print(str(currentPortfolioDate)[:10])
        try:
            itsFrom= datetime.datetime.strptime(str(currentPortfolioDate)[:10],"%m/%d/%Y")
        except:
             itsFrom= datetime.datetime.strptime(str(currentPortfolioDate)[:10],"%Y-%m-%d")
             
    print ("IT'S FROM " + str(itsFrom))
  #  try:
    print ("GETTING DATA...")
    data = bt.feeds.YahooFinanceData(
        #dataname=datapath,
        dataname=  stockSymbolString ,
        # Do not pass values before this date
        fromdate=itsFrom,
        # Do not pass values before this date
        todate=todaysDate + datetime.timedelta(days=1), # 
        # Do not pass values after this date
        reverse=False)
    print ("IT'S FROM " + str(itsFrom) + ", CURRENT PORTFOLIO DATE: " + str(currentPortfolioDate) + " TODAY'S DATE: " + str(todaysDate))
    if (itsFrom == todaysDate):
        txtStockInfo.insert(tk.END, "**YOU BOUGHT SHARES TODAY!")
        return
    # Add the Data Feed to Cerebro
    print('ADDING DATA...')
    cerebro.adddata(data)

    # Set our desired cash start
    print("SETTING CASH...")
    cerebro.broker.setcash(portfolioValue)
    balance=portfolioValue
    # Print out the starting conditions
    print("TO START PORTFOLIO...")
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    stockInfo += 'Starting Portfolio Value: %.2f' % cerebro.broker.getvalue() + "\n"
    # Run over everything
    closingCount=0
    cerebro.run()
    print (str(currentStep))
    # Print out the final result
    print('Final Portfolio Value: %.2f' % balance)    # Plot the result
    stockInfo += 'Final Portfolio Value: %.2f' % balance
    model=keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
    model.compile(optimizer='sgd', loss='mean_squared_error')
    new_model=None
    lastClosingPrice=closings[currentStep-1]
    if not path.exists('./saved_model_check_history/my_model'):
            # Train the model with the new callback
            model.fit(tradingDecisions, 
                      closings,  
                      epochs=100)  # Pass callback to training
            model.save('saved_model_check_history/my_model')   
    else:
           # model = keras.models.load_model('saved_model/my_model')
           # loss, acc = model.evaluate(tradingDecisions, closings, verbose=2)
         #  print("SAVED MODEL EXISTS --")
         #  model.save('saved_model_check_history/my_model')
          # model=keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
          # model.compile(optimizer='sgd', loss='mean_squared_error')                   
         #  new_model=keras.models.load_model('saved_model_check_history/my_model')
         #  new_model.summary()
          # new_model.evaluate(tradingDecisions,  closings, verbose=2)
          # print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
      #     print("NEW MODEL PREDICT:")
       #    print(new_model.predict(tradingDecisions))
          # loss,acc = model.evaluate(tradingDecisions, closings, verbose=2)
           #new_model.summary()
           print("SAVED MODEL EXISTS --")
          # model=keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
          # model.compile(optimizer='sgd', loss='mean_squared_error')                   
         #  new_model=keras.models.load_model('saved_model_external/my_model')
         #  new_model.summary()
         #  new_model.evaluate(tradingDecisions,  closings, verbose=2)
          # print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
          # model = tf.saved_model.load('./saved_model_external/my_model')
           print ("LOADING SAVED MODEL TO NEW MODEL:")
           new_model = keras.models.load_model('saved_model_check_history/my_model')
          # print (new_model)
           print("CALCULATING LOSS & ACCURACY:")
           acc=new_model.evaluate(tradingDecisions, closings, verbose=2)
           print('Restored model, accuracy: {:5.2f}%'.format(100*acc))
           lastClosingPrice=closings[currentStep-1]
           #print(new_model.predict(tradingDecisions).shape)
          # print(list(model.signatures.keys()))  # ["serving_default"]
        #   print("NEW MODEL PREDICT:")
          # print(new_model.predict(tradingDecisions))
          # loss,acc = model.evaluate(tradingDecisions, closings, verbose=2)
           #new_model.summary()
           model=new_model           
           
           
    print("PREDICTION: ")    
    print(model.predict([-1])[0][0])
    print(model.predict([0])[0][0])
    print(model.predict([1])[0][0])
    predictValue=float(model.predict([0])[0][0])
    print ("PREDICT VALUE: " + str(predictValue))
    print ("LAST CLOSING PRICE: " + str(lastClosingPrice))
    scale=round(predictValue/lastClosingPrice, 2) 
    print("SCALED: " + str(scale))
    lastClosingPrice = lastClosingPrice * scale
    sellOption=abs(lastClosingPrice-float(model.predict([-1])))
    holdOption=abs(lastClosingPrice-float(model.predict([0])))
    buyOption=abs(lastClosingPrice-float(model.predict([1])))
    tradeOptions={'SELL':sellOption,'HOLD':holdOption,'BUY':buyOption}
    sortOptions=sorted(tradeOptions.items(),key=lambda x: x[1])
  #  mb.showinfo("TODAY'S TRADE OPTION FOR " + stockSymbolString, "For this stock today I say " + sortOptions[0][0])
    txtStockInfo.insert(tk.END, stockInfo)
    btnSavePortfolioFile["state"]="normal"
    btnSavePortfolioFile["bg"]='yellow'
   #finalPortfolioValue=cerebro.broker.getvalue()
    print (str(balance))
    finalPortfolioValue=balance
    txtPortfolio.delete(0,tk.END)
    txtPortfolio.insert(tk.END,float(round(finalPortfolioValue,2)))
    #cerebro.plot(iplot= False)
    plt.suptitle("STOCK CLOSING DATA FOR " + stockSymbolString + " " + str(itsFrom.strftime("%b-%d-%y")) + " - " + str(todaysDate.strftime("%b-%d-%y"))) #
    print ("HERE ARE YOUR STATS DATA FOR THE CLOSINGS YOU REQUEST:")
    print (closeValues)
  #  dictStats={}
    print ("MEAN:")
    theMean=round(np.mean(closeValues),2)
    print(theMean)
    print ("MEDIAN:")
    theMedian=round(np.median(closeValues),2)
    print(theMedian)
    print ("MODE:")
    theMode=round(stats.mode(closeValues)[0][0],2)
    print(theMode)   
    theMin=min(closeValues)
    theMax=max(closeValues)
    theMaxIdx=closeValues.index(theMax)
    theMinIdx=closeValues.index(theMin)
    theMaxDate=qTable[theMaxIdx][0]
    theMinDate=qTable[theMinIdx][0]
    todaysDate=qTable[len(qTable)-1][0]
    theRange=theMax - theMin
   # sinceMax=todaysDate + datetime.timedelta(days=-365)
    print ("TODAY IS " + str(todaysDate))
    print(theMaxDate)
    
    dtMax=datetime.datetime.strptime(theMaxDate, '%m/%d/%Y')
    print(dtMax)
    print(todaysDate)
    dtToday=datetime.datetime.strptime(todaysDate, '%m/%d/%Y')
    print(dtToday)
    sinceMax=dtToday - dtMax
    print(sinceMax.days)
   # print (sinceMax)
    print ("HIGHEST CLOSING DATE: " + str(theMaxDate))
    stanDev=round(np.std(closeValues),2)
    theVar=round(np.var(closeValues),2)
    thePercentile=round(np.percentile(closeValues,80),2)
  #  dictStats["80%"]=thePercentile
    slope, intercept, r, p, std_err = stats.linregress(xList, closeValues)
    lastClosing=round(closeValues[len(closeValues)-1],2)
    def myfunc(x):
        return slope * x + intercept

    myModel = list(map(myfunc, xList))
    plt.scatter(xList, closeValues)  
    plt.plot(xList, myModel)
  #  if itsFrom == lastMonth:
  #      plt.plot(closeList, closeValues)  
  #  else:
  #      plt.plot(closeValues) 
  #  plt.grid(True)
  #  plt.show()
   
    myPolyModel=np.poly1d(np.polyfit(xList, closeValues, 3))
    myPolyLine=np.linspace(1,len(closeValues))
    r2=r2_score(closeValues, myPolyModel(xList))
    plt.scatter(xList, closeValues)
    plt.plot(myPolyLine, myPolyModel(myPolyLine))
    plt.plot()
   
    #randForst.suptitle('PREDICTION DATA WITH INVESTMENT $100000')
    #randForst.show()
  #  lblDate.pack_forget()
  #  entClosingDate.delete(0,END)
  #  entClosingDate.pack_forget()
  #  lblAmount.pack_forget()
  #  entClosingAmount.pack_forget()
  #  entClosingAmount.delete(0,END)
  #  root.update()
    #gotStockDataFrom=stockDataSource.CHECKHISTORY  
    print (qTable)
   # print (str(currentStep))
   
    currentStep=0
    tradingDecisions=[]
    closings=[]
    
 #  dictStats["count"]=len(xList)
    statFields=["count","mean","standard deviation","min","'80%","max"]
    statVals=[]
    statVals.append(len(xList))
    statsInfo=""
    statsInfo += "LATEST CLOSING: " + str(lastClosing) + "\nMAXIMUM: " + str(theMax) + "\nMINIMUM: " + str(theMin) + "\nMEAN: " + str(theMean) + "\nMEDIAN: " + str(theMedian) + "\n MODE:" + str(theMode) + "\nRANGE: " + str(theRange)
    statsInfo += "\nSTANDARD DEVIATION: " + str(stanDev) + "\nVARIANCE: " + str(theVar) + "\n80% PERCENTILE: " + str(thePercentile)
    statVals.append(theMean)
    statVals.append(stanDev)
    statVals.append(theMin)
    statVals.append(thePercentile)
    statVals.append(theMax)
   # statFileName=stockSymbolString + "_stats.csv"
   # with open(statFileName,'w') as csvfile:
   #     csvwriter=csv.writer(csvfile)
   #     csvwriter.writerow(statFields)
   #     csvwriter.writerow(statVals)
    #  dictStats["mean"]=theMean
  #  dictStats["standard deviation"]=stanDev
  #  dictStats["min"]=theMin
  #  dictStats["max"]=theMax
    lblCloseInfo['text']=statsInfo
    buyingDecision=0
    queryCount=0
    analyzeInfo = "(analysis goes here)"
    analyzeInfo="Stock symbol: " + stockSymbolString + "\n"
    analyzeInfo += "Stock bought: " + str(stockBought) + "\n"
    queryCount +=1
    if stockBought == False: 
        buyingDecision +=1
        
    analyzeInfo += "Date of most recent high this period: " + str(theMaxDate) + "\n"
    analyzeInfo += "Days since high: " + str(sinceMax.days) +"\n"
    queryCount +=1
    if sinceMax.days <= 30:
        buyingDecision += 1
        
    analyzeInfo += "Difference between highest and recent closing: " + str(round((theMax - lastClosing),2)) + "\n"
    queryCount +=1
    if lastClosing > theMean:
        analyzeInfo+="Recent closing greater than the mean." + "\n"
        buyingDecision +=1
    else:
      analyzeInfo += "Recent closing less than the mean." + "\n"
    queryCount +=1
    analyzeInfo+= "Difference between mode and mean: " + str(round((theMode - theMean),2)) + "\n"
    if theMode > theMean:
        buyingDecision +=1
    maxOccurredAfter=""
    queryCount +=1
    if theMaxIdx > theMinIdx:
        maxOccurredAfter="after"
        buyingDecision += 1
    else:
        maxOccurredAfter="before"
    analyzeInfo += "The high occurred " + maxOccurredAfter + " the low." + "\n"
    queryCount +=1
    if lastClosing > theMean + stanDev:
        analyzeInfo += "Recent closing greater than the mean plus standard deviation. " + "\n"
        buyingDecision +=1
    else: 
        analyzeInfo += "Recent closing less than the mean plus standard deviation. " + "\n"
    queryCount +=1
    if lastClosing > thePercentile:
        analyzeInfo += "Recent closing greater than 80% percentile. " + "\n"
        buyingDecision +=1
    else:
        analyzeInfo += "Recent closing less than 80% percentile. " + "\n"
    absR=abs(r)
    absR2=abs(r2)
    
    print ("R: " + str(r))
    print ("R2: " + str(r2))
    print ("ABSOLUTE VALUE R: " + str(absR))
    print("ABSOLUTE VALUE R2: " + str(absR2))
    queryCount +=1
    predictability = round(r * 100, 2)
    if absR2 > absR:
        predictability = round(r2 * 100, 2)
    if predictability > 50: 
        buyingDecision +=1
    analyzeInfo += "Predictablity: " + str(predictability) + "%.\n"
    
    
    recommendation=buyingDecision/queryCount
    buyHoldSell=""
    if recommendation > 0.66:
        if stockBought:
            buyHoldSell = "HOLD"
        else:
            buyHoldSell = "BUY"
    if recommendation > 0.33 and recommendation < 0.66:
        buyHoldSell="HOLD"
    if recommendation < 0.33:
        if stockBought:
            buyHoldSell="SELL"
        else:
            buyHoldSell="HOLD"
            
    analyzeInfo += "TRADING DECISION: "  + buyHoldSell + "."
 #   lblAnalysisInfo['text']=analyzeInfo
    print ('THE Xs:')
    print (xList)
    print ('THE Ys:')
    print (closeValues)
 #   closingsFileName=stockSymbolString + '.csv'
    closeField=["CLOSE"]

   # df = pd.read_csv(closingsFileName) 
    datFrame=[]
    theRows=[]
    theClosings=[]
    for i in range(len(xList)):
       # theRows.append(i)
        theRows.append(closeValues[i])
        theRows.append(myDailyBalances[i])
        theRows.append(myNetWorth[i])
        theRows.append(myProfits[i])
        datFrame.append(theRows)
        theRows=[]
   # datFrame=[xList,closeValues]
  # datFrame.append(closeValues)
    #print(datFrame)
    
    df=pd.DataFrame(datFrame, columns=[ 'Closing amount','Daily balances','Net worth','Profit'])
    orig_df=pd.DataFrame(datFrame, columns=[ 'Closing amount','Daily balances','Net worth','Profit'])
    print(orig_df['Daily balances'])
    print ('HERES DATAFRAME:')
    
    print(df)
    print ('DATAFRAME SHAPE:')
    print(df.shape)
    print( df.describe())
    origDataDescription=df.describe()
  #  dates_column=['Days in past year']
    closings_column=['Closing amount']
    balances_column=['Daily balances']
    netWorths_column=['Net worth']
    profits_column=['Profit']
 #   print ('TARGET COLUMN:')
   # print(target_column)



 
    print ('THE PREDICTORS:')
    predictors=list(set(list(df.columns)) - set(profits_column))
    df[predictors]=df[predictors]/df[predictors].max()
    print(df.describe())  
    analyzeInfo += "\n" + str(origDataDescription)
    lblAnalysisInfo['text']= analyzeInfo  
    X = df[predictors].values
    y = df[profits_column].values
   # print('X VALUES:')
   # print(X)
   # print('y VALUES:')
   # print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
    print("TRAINING:")
    print(X_train.shape);
    print("TESTING:")
    print(X_test.shape)
    
    closeData=np.array(closeValues)
    closeSeries=pd.Series(closeData)
    
 #   print("CLOSING DATA SERIES:")
 #   print(closeSeries)
 #   print (closeSeries.shape)
 #   print( closeSeries.describe() )
 #   dfpredictors=closeSeries/closeSeries.max()
 #   print( dfpredictors)
 #   print(dfpredictors.describe())
  #  print ('DF PREDICTORS:')
  #  print(dfpredictors)
  #  X=np.array(xList)
  #  Xseries=pd.Series(xList)
  #  Xvals=Xseries.values
  #  y=dfpredictors.values
  #  print(Xvals)
  #  print(y)
  #  Xtrain, Xtest, Ytrain,  Ytest=train_test_split(X, y, test_size=0.25, random_state=40)
  #  print(Xtrain.shape)
  #  print(Xtest.shape)
    dtree = DecisionTreeRegressor(max_depth=8, min_samples_leaf=0.13, random_state=3)
    print(dtree.fit(X_train, y_train))
    # Code lines 1 to 3
    print('TRAINED PREDICTION:')
    pred_train_tree= dtree.predict(X_train)
    print(np.sqrt(mean_squared_error(y_train,pred_train_tree)))
    print(r2_score(y_train, pred_train_tree))
    
    # Code lines 4 to 6
    print('TESTED PREDICTION:')
    pred_test_tree= dtree.predict(X_test)
    print(np.sqrt(mean_squared_error(y_test,pred_test_tree))) 
    print(r2_score(y_test, pred_test_tree))
    
    # Code Lines 1 to 4: Fit the regression tree 'dtree1' and 'dtree2' 
    print('FITTING REGRESSION TREES:')
    dtree1 = DecisionTreeRegressor(max_depth=2)
    dtree2 = DecisionTreeRegressor(max_depth=5)
    dtree1.fit(X_train, y_train)
    dtree2.fit(X_train, y_train)
    print(dtree1.fit(X_train, y_train))
    print(dtree2.fit(X_train, y_train))
    
    # Code Lines 5 to 6: Predict on training data
    print('TRAINED PREDICTION:')
    tr1 = dtree1.predict(X_train)
    tr2 = dtree2.predict(X_train) 
    print(tr1)
    print(tr2)
    #Code Lines 7 to 8: Predict on testing data
    print('TESTED PREDICTION:')
    y1 = dtree1.predict(X_test)
    y2 = dtree2.predict(X_test) 
    print(y1)
    print(y2)

    # Print RMSE and R-squared value for regression tree 'dtree1' on training data
    print("\n\r")
    print('R-square value for regression tree dtree1 training data:')
    print(np.sqrt(mean_squared_error(y_train,tr1))) 
    print(r2_score(y_train, tr1))
    print("\n\r")
    # Print RMSE and R-squared value for regression tree 'dtree1' on testing data
    print('R-square value for regression tree dtree1 testing data:')
    print(np.sqrt(mean_squared_error(y_test,y1))) 
    print(r2_score(y_test, y1)) 
    print("\n\r")
    
    # Print RMSE and R-squared value for regression tree 'dtree2' on training data
    print('R-square value for regression tree dtree2 training data:')
    print(np.sqrt(mean_squared_error(y_train,tr2))) 
    print(r2_score(y_train, tr2))
    
    # Print RMSE and R-squared value for regression tree 'dtree2' on testing data
    print('R-square value for regression tree dtree2 testing data:')
    print(np.sqrt(mean_squared_error(y_test,y2))) 
    print(r2_score(y_test, y2)) 
    
    #RF model
    print("NOW HERE'S THE RANDOM FOREST MODEL:")
    model_rf = RandomForestRegressor(n_estimators=500, oob_score=True, random_state=100)
    model_rf.fit(X_train, y_train.ravel()) 
    print('TRAINED PREDICTION:')
    pred_train_rf= model_rf.predict(X_train)
    print(np.sqrt(mean_squared_error(y_train,pred_train_rf)))
    print(r2_score(y_train, pred_train_rf))
    print('TESTED PREDICTION:')
    pred_test_rf = model_rf.predict(X_test)
    print(np.sqrt(mean_squared_error(y_test,pred_test_rf)))
    print(r2_score(y_test, pred_test_rf))
    analyzeInfo += "\n" + "RANDOM FOREST PREDICTABILITY: " + str((r2_score(y_test, pred_test_rf)) * 100) + "%"
    lblAnalysisInfo['text']= analyzeInfo  
    print("BALANCES:")
    print(myDailyBalances)
    print('PROFITS:')
    print(myProfits)
    print('NET WORTHS:')
    print(myNetWorth)
    #plt.plot(myDailyBalances)
    #plt.plot(myNetWorth)
    fig, axs = plt.subplots(figsize=(10,6)) 
   # axs[2].set_title('CLOSINGS')
    orig_df[closings_column].plot(kind='line', color='blue', ax=axs)
    orig_df[balances_column].plot(kind='bar', color='orange', ax=axs)
    orig_df[netWorths_column].plot(kind='bar', color='red', ax=axs)
    df[profits_column].plot(kind='bar', color='green', ax=axs)
    width=0.35
    #plt.xlim([-width,1000])
  #  axs[2].plot( xList,  closeValues)
  #  axs[2].set_title('Daily Closings')
   # axs[1].bar(xList,myDailyBalances, width=0.4, color='orange')
   # axs[1].set_title('Balances')
   # axs[0].bar(xList,myNetWorth, width=0.4, color='red')
   # axs[0].set_title('Net Worth & Profits')
   # axs[0].bar(xList,myProfits,width=0.5, color='green')
   # print (orig_df['Daily balances'])
    plt.show()
    xList.clear()
   # root.withdraw()
  #  root.update()
    
   # root.mainloop()

    
    return
   # except:
   #    if txtStockInfo.get("1.0",END) == "": txtStockInfo.insert(tk.END, "**NO STOCK SYMBOL FOR %s" % stockSymbolString)   

