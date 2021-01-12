# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:48:45 2020

@author: 15406
"""
import datetime
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
