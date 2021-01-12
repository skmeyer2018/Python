# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:51:03 2020

@author: 15406
"""

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
