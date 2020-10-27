
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path, time  # To manage paths
from os import path
import sys  # To find out the script name (in argv[0])
from decimal import Decimal
# Import the backtrader platform
import backtrader as bt    

import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog

from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
from enum import Enum
import csv
import pandas
import math
import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
currentStep=0
matplotlib.use('QT5Agg')


class stockDataSource(Enum):
    CHECKHISTORY = 1
    PORTFOLIOFILE = 2
    FROMEXTERNALFILE = 3

class thisStockBought(Enum):
    NO=0
    YES=1

class tradeOption(Enum):
    HOLD=0
    BUY=1
    SELL=2

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
        stockSymbolString=txtStockSymbol.get()
        currentPrice=self.dataclose[0]
        portFile='./portfolio/' + stockSymbolString + '.csv'
        profitValues=[]
        print ("PROFIT VALUES:")
        print (profitValues)
        #print(wasBought.name)
 
        txtPortfolio.delete(0,END)
        txtPortfolio.insert(END,float(round(balance,2)))
        stockSymbolString=txtStockSymbol.get().upper()
        todaysDate=datetime.datetime.now().strftime('%m/%d/%Y')
        finalPortfolioValue=float(txtPortfolio.get())
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
        entClosingDate.delete(0,END)
        entClosingDate.insert(END,dt.strftime("%m/%d/%Y"))
        root.update()
        entClosingAmount.delete(0,END)
        entClosingAmount.insert(END,str(lastClosingPrice))
        root.update()
    
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

        

def missing_portfolio_value():
    mb.showinfo("PORTFOLIO MISSING", "Please enter a numeric portfolio amount!")


def button_click():
    global loadCSV
    global stockDataSource
    global gotStockDataFrom
    global qTable
    global currentStep
    global closingCount
    global tf
    currentStep=0
    qTable=[]
    txtStockInfo.delete('1.0',END)
    stockSymbolString=txtStockSymbol.get().upper()
    lblStockHistory['text']="Stock history for " + stockSymbolString
    print ("YOU CLICKED FOR SYMBOL " + stockSymbolString)
    numPort=round(float(txtPortfolio.get()),0)
    print(isinstance(numPort,float))
    txtPortfolioData.delete('1.0',END)
    if txtPortfolio.get().strip() == '' or txtPortfolio.get() == '0' or not isinstance(numPort,float):
        missing_portfolio_value()
        return
    try:
        portfolioValue=float(txtPortfolio.get())
    except:
        portfolioValue=0
    
    global stockInfo
    global balance
    stockInfo=""
    cerebro = bt.Cerebro()
    global plt
    global closeList
    global closeValues
    global btnSavePortfolioFile
    global gotStockDataFrom
    global currentPortfolioDate
    global numberOfShares
    global currentPrice
    global trading
    global netWorth
    global profit
    global tradingAmount
    global portfolioUpdated
    global fullPath
    global tradingDecisions
    global closings
    global model
    global tradeAction
    global externalRows

    lastClosingPrice=0
    lblDate.pack()
    entClosingDate.pack()
    lblAmount.pack()
    entClosingAmount.pack()
    root.update()
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
    if str(gotStockDataFrom.name) == 'FROMEXTERNALFILE': 
        print("FILENAME: " + str(fullPath))
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

        cerebro.run()

            
    # Print out the final result
        #finalPortfolioValue=cerebro.broker.getvalue()
        finalPortfolioValue=balance
        print('Final Portfolio Value: %.2f' % finalPortfolioValue)    # Plot the result
        stockInfo += 'Final Portfolio Value: %.2f' % finalPortfolioValue  
        txtPortfolio.delete(0,END)
        txtPortfolio.insert(END,float(round(finalPortfolioValue,2)))
        txtStockInfo.insert(tk.END, stockInfo)
        btnSavePortfolioFile["state"]="normal"
        btnSavePortfolioFile["bg"]='yellow'
        finalPortfolioValue=cerebro.broker.getvalue()
        #cerebro.plot(iplot= False)
        plt.suptitle("STOCK CLOSING DATA FOR " + stockSymbolString + " " + str(halfYearBack.strftime("%b-%d-%y")) + " - " + str(todaysDate.strftime("%b-%d-%y"))) #
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
                mb.showinfo("TODAY'S TRADE OPTION FOR " + stockSymbolString, "For this stock today I say " + sortOptions[0][0])
                print(todaysDate)
                #print (dt.strftime("%m/%d/%Y"))
        except:
                print("CANNOT LOAD WEIGHTS")
        plt.plot(closeList,closeValues)  
        plt.grid(True)
        plt.show()
        lblDate.pack_forget()
        entClosingDate.delete(0,END)
        entClosingDate.pack_forget()
        lblAmount.pack_forget()
        entClosingAmount.pack_forget()
        entClosingAmount.delete(0,END)
        gotStockDataFrom=stockDataSource.CHECKHISTORY    
        currentStep=0
        tradingDecisions=[]
        closings=[]
      #  print (qTable)
        return
    
    if (str(gotStockDataFrom.name) == 'CHECKHISTORY'):  
       # itsFrom=lastMonth
       itsFrom=halfYearBack
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
                      epochs=50)  # Pass callback to training
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
    mb.showinfo("TODAY'S TRADE OPTION FOR " + stockSymbolString, "For this stock today I say " + sortOptions[0][0])
    txtStockInfo.insert(tk.END, stockInfo)
    btnSavePortfolioFile["state"]="normal"
    btnSavePortfolioFile["bg"]='yellow'
   #finalPortfolioValue=cerebro.broker.getvalue()
    print (str(balance))
    finalPortfolioValue=balance
    txtPortfolio.delete(0,END)
    txtPortfolio.insert(END,float(round(finalPortfolioValue,2)))
    #cerebro.plot(iplot= False)
    plt.suptitle("STOCK CLOSING DATA FOR " + stockSymbolString + " " + str(itsFrom.strftime("%b-%d-%y")) + " - " + str(todaysDate.strftime("%b-%d-%y"))) #
    if itsFrom == lastMonth:
        plt.plot(closeList, closeValues)  
    else:
        plt.plot(closeValues) 
    plt.grid(True)
    plt.show()
    lblDate.pack_forget()
    entClosingDate.delete(0,END)
    entClosingDate.pack_forget()
    lblAmount.pack_forget()
    entClosingAmount.pack_forget()
    entClosingAmount.delete(0,END)
    root.update()
    gotStockDataFrom=stockDataSource.CHECKHISTORY  
    print (qTable)
   # print (str(currentStep))
    currentStep=0
    tradingDecisions=[]
    closings=[]
   # except:
   #    if txtStockInfo.get("1.0",END) == "": txtStockInfo.insert(tk.END, "**NO STOCK SYMBOL FOR %s" % stockSymbolString)       
        
def save_portfolio():
     global portfolioList
     global os
     global portfolioRecords
     portfolioStringData=""
     stockSymbolString=txtStockSymbol.get().upper()
     todaysDate=datetime.datetime.now().strftime('%Y-%m-%d')
     finalPortfolioValue=float(txtPortfolio.get())
     portfolioFileName=stockSymbolString + ".csv"
     fields=[]             

     if path.exists('./portfolio/' + portfolioFileName) == False:    
      fields=['Updated','Symbol','Transaction','CurrentPrice','Balance', 'Net Worth', 'Profit']
     csvRows=[todaysDate,stockSymbolString,  str(tradeAction.name), lastClosingPrice,balance,netWorth,finalPortfolioValue]      
     with open('./portfolio/' + portfolioFileName, 'a') as portfolioFileName:
         csvWriter=csv.writer(portfolioFileName)
         csvWriter.writerow(fields)
         csvWriter.writerow(csvRows)

     portfolioList.insert(END, stockSymbolString + '.csv')
     for i in range(len(fields)):
         portfolioStringData += fields[i] + "|"
     portfolioStringData += "\n\r" * 2
     for i in range(len(csvRows)):
         portfolioStringData += str(csvRows[i]) + "|"
     portfolioStringData += "\n\r" * 2
     txtPortfolioData.delete('1.0',END)
     txtPortfolioData.insert(END, portfolioStringData)   
    
def select_portfolio():
    global portfolioList
    global txtPortfolio
    global txtStockSymbol
    global currentPortfolioDate
    global gotStockDataFrom
    global balance
    global numberOfShares
    global currentPrice
    global tradingAmount
    global netWorth
    global profit
    global portfolioUpdated
    global buyingChoice
    global wasBought
    global currentStep
    global tradeAction
    closeList=[]
    closeValues=[]
    profitValues=[]
    todaysDate=datetime.datetime.now()
    portfolioRows=""
    currentPortfolioData={}
    stockSymbolString=portfolioList.get( portfolioList.curselection())
    buyingChoice=False
    print("CURRENT PORTFOLIO DATE: " + str(currentPortfolioDate))
    print ("you selected " + stockSymbolString )
    print (stockSymbolString[:-4])
    wasBought=thisStockBought.NO
    with open('./portfolio/' + stockSymbolString, 'r') as portfolioFile:
        reader=csv.reader(portfolioFile)
        rowCount=0
        for row in reader:
            portfolioSubrow=""
            for item in range(len(row)):
                print(row[item])
                if rowCount == 0:
                    portfolioSubrow += row[item].center(9) + " | "
                else:
                        if item == 4 or item == 6:
                            if row[item] != '':
                             txtPortfolio.delete(0,END)
                             txtPortfolio.insert(END, row[item])
                             balance=row[item]
                             balance=round(float(balance),2)
                        if item == 1:
                              if str(row[item]) != '': 
                                  currentPortfolioDate=str(row[item])
                              if rowCount > 2:
                                  if str(currentPortfolioDate) != '' and str(currentPortfolioDate) not in closeList:
                                   closeList.append(str(currentPortfolioDate))                            
                       # try:
                          #     currentPortfolioDate=datetime.datetime.strptime(row[item],'%m/%d/%Y')
                        #       print ("DATE: " + str(currentPortfolioDate))
                              
                        #except:
                          #     pass
                        if item == 3:
                            if row[item] == 'BUY':
                                wasBought=thisStockBought.YES
                            elif row[item] == 'SELL':
                                wasBought=thisStockBought.NO
                        
                        if item >= 5:
                            portfolioSubrow += row[item].center(22)
                            if item == 5: 
                                currentPrice=row[item]
                                if rowCount > 2:
                                 try:   
                                  closeValues.append(float(currentPrice))
                                  print("CLOSING PRICE: " + str(currentPrice))
                                 except:
                                     pass
                            if item == 6: tradingAmount=row[item]
                            if item == 7: netWorth=row[item]
                            if item == 8: 
                                if rowCount >2:
                                 try:
                                  profit=row[item] 
                                  profitValues.append(float(profit))
                                 except:
                                     pass
                            
                        elif item == 4:
                            try:
                             fl=round(float(row[item]),2)
                             portfolioSubrow += str(fl).center(22) 
                             numberOfShares= row[item]
                            except:
                                pass
                        else:
                            portfolioSubrow += row[item].center(10)
 

            if rowCount == 0:
                    portfolioSubrow += "\n"
                    portfolioSubrow+=90 * "="
            portfolioSubrow += "\n"
            rowCount+=1
            portfolioRows += portfolioSubrow
            
    #print(str(closeList[len(closeList)-1]))
    #currentPortfolioDate=closeList[len(closeList)-1]
    txtPortfolioData.delete('1.0',END)
    txtPortfolioData.insert(END, portfolioRows)   
    txtStockSymbol.delete(0,END)
    txtStockSymbol.insert(END,stockSymbolString[:-4]) 
    gotStockDataFrom=stockDataSource.PORTFOLIOFILE
    print ("TRADING AMOUNT: " + str(tradingAmount))
    print ("CURRENT PRICE: " + str(currentPrice))
    
    print ("CURENT PORTFOLIO DATE: " + str(currentPortfolioDate))
    portFile='./portfolio/' + stockSymbolString
    modTime=time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(portFile)))
    print (modTime)
    print (todaysDate.strftime('%m/%d/%Y'))
    print (closeList)
    print (closeValues)
    print (profitValues)
    print(modTime != todaysDate.strftime('%m/%d/%Y'))
 

    gotStockDataFrom=stockDataSource.CHECKHISTORY 

    
def buy_shares():
    global currentPortfolioDate
    global txtStockSymbol
    global balance
    global lastClosingPrice
    global buyAmount
    global buying
    global lblBuy
    global entBuyAmount
    global btnBuy
    global numberOfShares
    fields=[]
    csvRows=[]
    activityContents=""

    buyAmount=entBuyAmount.get()
    if float(buyAmount)==0:
        lblBuy.destroy()
        entBuyAmount.destroy()
        btnBuy.destroy() 
        return
    
    print ("AMOUNT OF PURCHASE: " + buyAmount)
    numberOfShares=float(buyAmount)/float(lastClosingPrice)
   # numberOfShare="%.2f" % numberOfShares
   # print (numberOfShares)
    print ("YOU BOUGHT " + str(numberOfShares))
    balance -= float(buyAmount)
    print ("YOUR BALANCE: " + str(balance))
    netWorth=balance + numberOfShares * lastClosingPrice
    profit=netWorth-balance
    txtPortfolio.delete(0,END)
    txtPortfolio.insert(END,float(balance))
    stockSymbolString=txtStockSymbol.get().upper()
    todaysDate=datetime.datetime.now().strftime('%m/%d/%Y')
    finalPortfolioValue=float(txtPortfolio.get())
    portfolioFileName=stockSymbolString + ".csv"
    if path.exists('./portfolio/' + portfolioFileName) == False:    
      fields=['Symbol','Updated','Balance', 'Transaction', 'NumberOfShares', 'CurrentPrice', 'TradingAmount', 'Net Worth', 'Profit']
    csvRows=[stockSymbolString, todaysDate, finalPortfolioValue,'BUY',numberOfShares,lastClosingPrice,buyAmount,netWorth,profit]      
    with open('./portfolio/' + portfolioFileName, 'a') as portfolioFile:
         csvWriter=csv.writer(portfolioFile)
         csvWriter.writerow(csvRows)    

    
    txtPortfolioData.delete('1.0',END)
    portfolioText=""

    gotStockDataFrom=stockDataSource.PORTFOLIOFILE
    txtStockSymbol.delete(0,END)
    txtStockSymbol.insert(END,stockSymbolString[:-4])
    txtPortfolio.delete(0,END)
    txtPortfolio.insert(END,balance) 

    lblBuy.destroy()
    entBuyAmount.destroy()
    btnBuy.destroy()

    
    
def sell_Stock():
    global balance
    global netWorth
    global profit
    global currentPrice
    global numberOfShares
    global portfolioFileName
    global stockSymbolString
    global todaysDate
    global var
    todaysDate=datetime.datetime.now()
    todaysDate=str(todaysDate.strftime('%m/%d/%Y'))
    if var.get() == 1:
        balance += float(numberOfShares) * float(currentPrice)
        balance=round(balance,2)
        numberOfShares=0
        portfolioFileName=stockSymbolString + '.csv'
        csvRows=[stockSymbolString, todaysDate, balance,'SELL',numberOfShares,lastClosingPrice,buyAmount,netWorth,profit]      
        with open('./portfolio/' + portfolioFileName, 'a') as portfolioFile:
             csvWriter=csv.writer(portfolioFile)
             csvWriter.writerow(csvRows)
    lblSell.destroy()
    entSellAmount.destroy()
    rbYesSell.destroy()
    rbNoSell.destroy()
    txtStockInfo.delete('1.0',END)
             
    
def find_stock_symbol():
    global dctSymbols
    if entFindSymbol.get() == "": return
    lstSymbols.delete(0,END)
    srchString=entFindSymbol.get()
    itemCount=0
    for key,value in dctSymbols.items():
        if srchString.upper() in value.upper() or srchString.upper() in key.upper():
            print(value)
            lstSymbols.insert(itemCount,key.ljust(9) + "|" + value)
            itemCount +=1
            
def reset_symbol_list():
 global dctSymbols
 lstSymbols.delete(0,END)
 with open('StockSymbols.csv', 'r') as symbolsFile:
  reader=csv.reader(symbolsFile)
  rowCount=0
  for row in reader:
      symbolItem=''
      if rowCount == 0:
          rowCount +=1
          continue
      for symbolColumn in range(2):
          symbolItem += row[symbolColumn].ljust(9) + "|"
      dctSymbols[row[0]]=row[1]
      lstSymbols.insert(rowCount,symbolItem)
      rowCount+=1   
      
def select_your_symbol():
    symbolItem=lstSymbols.get(lstSymbols.curselection())
    pipePos=symbolItem.find("|")
    symbolResult=symbolItem[0:pipePos].rstrip()
    txtStockSymbol.delete(0, END)
    txtStockSymbol.insert(END, symbolResult)
    
def open_stock_data():
    global fromExternal
    global stockDataSource
    global gotStockDataFrom
    global loadCSV
    global fullPath
    global externalRows
    root.filename =  filedialog.askopenfilename(initialdir = "/", title = "Select a .CSV file", filetypes = (("csv files", "*.csv"),("all files","*.*")))
    loadCSV=os.path.basename(root.filename)
    print ("FILENAME: " + str(loadCSV))
    fullPath=root.filename
    print (fullPath)
    loadSymbol=os.path.splitext(loadCSV)[0][:-4]
    txtStockSymbol.insert(END, loadSymbol )
    fromExternal=True
    gotStockDataFrom=stockDataSource.FROMEXTERNALFILE
    txtStockInfo.delete('1.0',END)
    try:
        with open(fullPath, 'r') as extFile:
            externalRows=len( list(csv.reader(extFile)))
    except:
        gotStockDataFrom=stockDataSource.CHECKHISTORY 
    
   
def close_app():
 root.destroy()
    
stockInfo=""
root = tk.Tk()
root.title("Stock Trading")
root.geometry("1200x1300")  
root.configure(bg='#55bb22')
lblSearchSymbol=tk.Label(root,text="Search a symbol",font='Arial 10 bold',bg='#55bb22')
entFindSymbol=tk.Entry(root, width="10", font='Arial 20 bold')
lstSymbols=Listbox(root, height=20, width="22",font='Arial 10 bold', bg="#aaeeff")
lstSymbols.bind("<<ListboxSelect>>", lambda x:select_your_symbol())
dctSymbols={}
reset_symbol_list()
       
lblSearchSymbol.place(x=40,y=10)
entFindSymbol.place(x=40, y=32)
btnFindSymbol=tk.Button(root, text="FIND", width=22, command=find_stock_symbol)
btnFindSymbol.place(x=40,y=88 )
lstSymbols.place(x=40, y=130)
btnResetSymbols=tk.Button(root, text="RESET", width=22, bg="dark green", fg="white", command=reset_symbol_list)
btnResetSymbols.place(x=40,y=650)
lblEnterPortfolio=tk.Label(root, text="ENTER YOUR PORTFOLIO AMOUNT:", font='Arial 10 bold', bg='#55bb22')
lblEnterPortfolio.pack()
txtPortfolio=tk.Entry(root, font='Arial 20 bold')
txtPortfolio.pack()
lblEnterSymbol=tk.Label(root, text="ENTER A STOCK SYMBOL:", font='Arial 10 bold', bg='#55bb22')
#currentStep=0
baseline=0
gamma=0.999
Gt=0
oldReward=0
epsilon=0.4
Return=0
reweighting=0
rClip=0
gotStockDataFrom=0
currentPortfolioDate=None
balance=0
portfolioRecords=[]
purchaseAmount=0
lastClosingPrice=0
buyAmount=0
buyingChoice=False
numberOfShares=0
netWorth=0
profit=0
buyAmount=0
portfolioUpdated=False
dropCount=0
fromExternal=False
loadCSV=""
fullPath=""
closingCount=0
tradeAction=tradeOption.HOLD
lblEnterSymbol.pack()
txtStockSymbol=tk.Entry(root, font='Arial 20 bold')
txtStockSymbol.pack()
gotStockDataFrom=stockDataSource.CHECKHISTORY
wasBought=thisStockBought.NO
qTable=[]
tradingDecisions=[]
closings=[]
model = None
currentBalance=0
btnStockSymbol=tk.Button(root, text="GET STOCK HISTORY INFORMATION", bg="dark gray", command=button_click)
btnStockSymbol.pack()
lblStockHistory=tk.Label(root, text="Stock history" , bg='#55bb22', font='Arial 11 bold')
lblStockHistory.pack()
txtStockInfo=tk.Text(root, height=10, width=50, font='Arial 11 bold' )
txtStockInfo.pack()
btnSavePortfolioFile=tk.Button(root, text="SAVE CURRENT STOCK", bg="gray", state="disabled", command=save_portfolio)

btnSavePortfolioFile.pack()
lblPortfolioFiles=tk.Label(root,text="Your portfolio files:", bg='#55bb22', font='Arial 11 bold')
lblPortfolioFiles.pack()
portfolioList=Listbox(root, height="5")
portfolioList.bind("<<ListboxSelect>>", lambda x: select_portfolio())
externalRows=0
for i in range(len(os.listdir('./portfolio'))):
    portfolioList.insert(i,os.listdir('./portfolio')[i])
portfolioList.pack()
#lblActivityData=tk.Label(root,text="Activity data:",bg='#55bb22', font='Arial 11 bold' )
#lblActivityData.place(x=80, y=850)
lblPortfolioData=tk.Label(root,text="Current portfolio data:" , bg='#55bb22', font='Arial 11 bold')
lblPortfolioData.pack()
#txtActivityData=tk.Text(root,height=8, width=60, font='Times 8 bold',bg='beige', foreground='#885511')
#txtActivityData.place(x=80,y=890)
txtPortfolioData=tk.Text(root, height=8, width=100, font='Times 10 bold',bg='beige', foreground='#885511')
txtPortfolioData.pack()
lblDate=tk.Label(root, text="Closing date:", height=2,  width=50, font="Arial 20 bold", bg='#55bb22', foreground='black')
lblDate.pack_forget()
entClosingDate=tk.Entry(root, width=50, font="Arial 20 bold", bg='white', foreground='black')
entClosingDate.pack_forget()
lblAmount=tk.Label(root, text="Closing amount:", height=2,  width=50,   font="Arial 20 bold", bg='#55bb22', foreground='black')
lblAmount.pack_forget()
entClosingAmount=tk.Entry(root, width=50, font="Arial 20 bold", bg='white', foreground='black')
entClosingAmount.pack_forget()
lblBuy=tk.Label(root, text="Buy shares? (enter a dollar figure, 0='no')", bg='#55bb22', font='Arial 11 bold')
lblBuy.destroy()
entBuyAmount=tk.Entry(root, font='Arial 20 bold', width=10)
entBuyAmount.pack_forget()
btnBuy=tk.Button(root, text="BUY CURRENT STOCK", bg="dark green", foreground="white", command=buy_shares)
btnBuy.pack_forget()
lblSell=tk.Label(root, text="Ready to sell for this amount?", bg='#55bb22', font='Arial 11 bold')
lblSell.pack_forget()
entSellAmount=tk.Entry(root, font='Arial 20 bold', width=10 )
entSellAmount.pack_forget()
var = IntVar()
rbYesSell=Radiobutton(root, text="Yes",variable=var, value=1, command=sell_Stock, bg='#55bb22', font='Arial 11 bold')
rbYesSell.pack_forget()
rbNoSell=Radiobutton(root,text="No", variable=var, value=2, command=sell_Stock, bg='#55bb22', font='Arial 11 bold')
rbNoSell.pack_forget()
menubar=Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_stock_data)
filemenu.add_command(label="Exit", command=close_app)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
root.update()
tk.mainloop()

