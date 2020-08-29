
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from decimal import Decimal
# Import the backtrader platform
import backtrader as bt    

import tkinter as tk
from tkinter import *
from tkinter import ttk
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QT5Agg')


class TestStrategy(bt.Strategy):
    
    import matplotlib
   # import matplotlib.pyplot as plt
    global closeList
    
    
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        global stockInfo
       # global closeList
        stockInfo+='%s, %s' % (dt.isoformat(), txt) + "\n"
        shortDate=dt.strftime("%b-%d-%y")
        if not shortDate in closeList:
         closeList.append(shortDate)

        
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
       
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
        self.log('Close, %.2f' % self.dataclose[0])
        global currentStep
        global baseline
        global gamma
        global Gt
        global oldReward
        global epsilon
        global rClip
        global Return
        global reweighting
        global balance
        global closeValues
       # global closeValues
       # global closeList
        global plt
        currentStep += 1
        delayModifier=currentStep/30
        reward=balance * delayModifier
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
                if currentStep < 6:
                    Return += reward * (gamma ** currentStep) #DISCOUNTED SUM
                    Gt=Return
                    advantageEst=Return/(currentStep + 1) 
                    if currentStep==5: #DEFINE THE BASELINE
                        baseline=Return/6
                        #print ("BASELINE: %.2f" % baseline)
                else:
                    Return += reward
                   # print ("RETURN:" + str(Return))
                    Gt=Return
                    advantageEst= Return/(currentStep + 1) - baseline
                    if oldReward == 0:
                        oldReward=reward                
                    else: #CALCULATE THE REWEIGHTING FACTOR
                        #if reward < oldReward:
                           # self.stockWarning="COULD WARN OF DROP IN STOCK"
                        reweighting=reward/oldReward
                    oldReward=reward #SAVE THE CURRENT VALUE OF REWARDS
                    r=reweighting * advantageEst
                    if reweighting  <= 1 -  epsilon and  advantageEst < 0:
                        rClip= (1 -  epsilon) * advantageEst
                    elif reweighting >= 1 +  epsilon and advantageEst > 0:
                        rClip= (1 +  epsilon) * advantageEst
                    else:
                        rClip= reweighting * advantageEst               
                    r = min(r, rClip )
                   # self.log("VALUE OF r: %.2f" % r)
            except:
                print ("**ERROR IN ALGORITHM", sys.exc_info()[0])
                
                
           # self.log("REWARD: %.2f" % reward)
        
        #self.log('REWARD: ' + str(reward))
        # self.log('REWARD: %.2f' % str(reward))
        # self.log('High, %.2f' % self.datahigh[0])
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()       

 


def button_click():
    txtStockInfo.delete('1.0',END)
    stockSymbolString=txtStockSymbol.get().upper()
    print ("YOU CLICKED FOR SYMBOL " + stockSymbolString )
    portfolioValue=float(txtPortfolio.get())
    global stockInfo
    global balance
    stockInfo=""
    cerebro = bt.Cerebro()
   # import matplotlib
    #import matplotlib.pyplot as plt
    global plt
    global closeList
    global closeValues
    #global portfolioValue
    print ('YOUR CURRENT PORTFOLIO: %.2f' % portfolioValue )
    closeList=[]
    closeValues=[]
    

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
   #datapath = os.path.join(modpath, './datas/orcl-1995-2014.csv')

    # Create a Data Feed
    todaysDate=datetime.datetime.now()
    lastMonth=todaysDate + datetime.timedelta(days=-30)
    
    try:
        print ("GETTING DATA...")
        data = bt.feeds.YahooFinanceData(
            #dataname=datapath,
            dataname=  stockSymbolString ,
            # Do not pass values before this date
            fromdate=lastMonth,
            # Do not pass values before this date
            todate=todaysDate  + datetime.timedelta(days=1),
            # Do not pass values after this date
            reverse=False)
    
        # Add the Data Feed to Cerebro
        print('ADDING DATA...')
        cerebro.adddata(data)
    
        # Set our desired cash start
        print("SETTING CASH...")
        cerebro.broker.setcash(portfolioValue)
        balance=portfolioValue
        # Print out the starting conditions
        print("TO START PORFOLIO...")
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        stockInfo += 'Starting Portfolio Value: %.2f' % cerebro.broker.getvalue() + "\n"
        # Run over everything
        cerebro.run()
    
        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())    # Plot the result
        stockInfo += 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()
        txtStockInfo.insert(tk.END, stockInfo)
        finalPortfolioValue=cerebro.broker.getvalue()
        fPortfolio=open('./portfolio/' + stockSymbolString + '.txt', 'w')
        fPortfolio.write( str(finalPortfolioValue))
        fPortfolio.close()
       # cerebro.plot(iplot=False)

        plt.plot(closeList, closeValues)
        plt.grid(True)
        plt.show()       
    except:
        txtStockInfo.insert(tk.END, "**NO STOCK SYMBOL FOR %s" % stockSymbolString)       
        

stockInfo=""
root = tk.Tk()
root.title="Stock Trading"
root.geometry("1200x1300")  
root.configure(bg='#55bb22')
lblEnterPortfolio=tk.Label(root, text="ENTER YOUR PORTFOLIO AMOUNT:", font='Arial 10 bold', bg='#55bb22')
lblEnterPortfolio.pack()
txtPortfolio=tk.Entry(root, font='Arial 20 bold')
txtPortfolio.pack()
lblEnterSymbol=tk.Label(root, text="ENTER A STOCK SYMBOL:", font='Arial 10 bold', bg='#55bb22')
currentStep=0
baseline=0
gamma=0.999
Gt=0
oldReward=0
epsilon=0.4
Return=0
reweighting=0
rClip=0
lblEnterSymbol.pack()
txtStockSymbol=tk.Entry(root, font='Arial 20 bold')
txtStockSymbol.pack()

btnStockSymbol=tk.Button(root, text="GET STOCK INFORMATION", bg="dark gray", command=button_click)
btnStockSymbol.pack()
txtStockInfo=tk.Text(root, height=20, width=60, font='Arial 11 bold' )

txtStockInfo.pack()
portfolioList=Listbox(root)
portfolioFile1=os.listdir('./portfolio')[0]
for i in range(len(os.listdir('./portfolio'))):
    portfolioList.insert(i,os.listdir('./portfolio')[i])
portfolioList.pack()
root.update()
tk.mainloop()

