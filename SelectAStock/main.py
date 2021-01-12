# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:33:23 2020

@author: 15406
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from enum import Enum


 

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

import sys
 
sys.path.append(".")


from selectportfolio import select_portfolio
from saveportfolio import save_portfolio
from buttonclick import button_click



import datetime  # For datetime objects
import os.path, time  # To manage paths
from os import path
import sys  # To find out the script name (in argv[0])
from decimal import Decimal
# Import the backtrader platform


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
from symbols import  find_stock_symbol, reset_symbol_list, select_your_symbol
#from findthesymbol import find_stock_symbol
import numpy as np
import random
import backtrader as bt   
from selectportfolio import select_portfolio 
#from resetthesymbols import reset_symbol_list
from openstockdata import open_stock_data
fullPath=""
thePath=[]
btnSavePortfolioFile=None

def missing_portfolio_value():
    mb.showinfo("PORTFOLIO MISSING", "Please enter a numeric portfolio amount!")
    
def close_app():
 root.destroy()
 sys.exit(0)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy() 
        sys.exit(0)
 
def open_stock():
    if txtPortfolio.get() == '':
        missing_portfolio_value()
        return
    gotStockDataFrom=stockDataSource.FROMEXTERNALFILE
   # thePath=open_stock_data(root, txtStockInfo, txtStockSymbol, tk, gotStockDataFrom, fullPath)
    root.filename =  filedialog.askopenfilename(initialdir = "/", title = "Select a .CSV file", filetypes = (("csv files", "*.csv"),("all files","*.*")))
    loadCSV=os.path.basename(root.filename)
    print ("FILENAME: " + str(loadCSV))
    fullPath=root.filename
    print (fullPath)
    loadSymbol=os.path.splitext(loadCSV)[0][:-4]
    txtStockSymbol.insert(tk.END, loadSymbol )
    print ('FULLPATH: ' + str(fullPath))
    print('SOURCE:' + str(gotStockDataFrom.name)) 
    root.update()
    get_stock_history(fullPath, gotStockDataFrom)
    

def find():
    print ("finding...")
    find_stock_symbol(entFindSymbol, lstSymbols, dctSymbols)

def reset():
    reset_symbol_list(lstSymbols, dctSymbols)

def get_stock_history(fullPath=None, gotStockDataFrom=None):
   # try:
    btnStockSymbol['state']='disabled'
    root.update()
    if not gotStockDataFrom: gotStockDataFrom=stockDataSource.CHECKHISTORY
    print ("NOW GETTING HISTORY, SOURCE: " + str(gotStockDataFrom.name))
    print ("FULL PATH: " + str(fullPath))
   # except:
   # gotStockDataFrom=stockDataSource.CHECKHISTORY
   # fullPath=None
    button_click(bt, tk,txtStockInfo,txtStockSymbol, lblStockHistory, txtPortfolio, txtPortfolioData, currentPortfolioDate,stockDataSource, gotStockDataFrom, closingCount, tradeAction, btnSavePortfolioFile, fullPath)
    btnStockSymbol['state']='normal'
    root.update()
    print ("THE MEAN: "  + str(theMean))
           
currentStep=0
matplotlib.use('QT5Agg')

stockInfo=""
root = tk.Tk()
root.title("Stock Trading")
root.geometry("1000x900")  
root.configure(bg='#55bb22')
root.protocol("WM_DELETE_WINDOW", on_closing)
root.update()


lblSearchSymbol=tk.Label(root,text="Search a symbol",font='Arial 10 bold',bg='#55bb22')
entFindSymbol=tk.Entry(root, width="10", font='Arial 20 bold')
lstSymbols=Listbox(root, height=20, width="22",font='Arial 10 bold', bg="#aaeeff")
txtStockSymbol=tk.Entry(root, font='Arial 20 bold')
lstSymbols.bind("<<ListboxSelect>>", lambda x:select_your_symbol(lstSymbols, txtStockSymbol))
dctSymbols={}
reset()
       
lblSearchSymbol.place(x=40,y=10)
entFindSymbol.place(x=40, y=32)
btnFindSymbol=tk.Button(root,  text="FIND", width=22, command=find ) 

btnFindSymbol.place(x=40,y=88 )

lstSymbols.place(x=40, y=130)
btnResetSymbols=tk.Button(root, text="RESET", width=22, bg="dark green", fg="white", command=reset)
btnResetSymbols.place(x=40,y=650)
lblEnterPortfolio=tk.Label(root, text="ENTER YOUR PORTFOLIO AMOUNT:", font='Arial 10 bold', bg='#55bb22')
lblEnterPortfolio.pack()
txtPortfolio=tk.Entry(root, font='Arial 20 bold')
txtPortfolio.pack()
txtPortfolio.focus_set()
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
gotStockDataFrom=stockDataSource.CHECKHISTORY
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
theMean=0
tradeAction=tradeOption.HOLD
lblEnterSymbol.pack()

txtStockSymbol.pack()
#dataSource=str(gotStockDataFrom.name)
wasBought=thisStockBought.NO
qTable=[]
tradingDecisions=[]
closings=[]
model = None
currentBalance=0
txtStockInfo=tk.Text(root, height=10, width=50, font='Arial 11 bold' )
lblStockHistory=tk.Label(root, text="Stock history" , bg='#55bb22', font='Arial 11 bold')
txtPortfolioData=tk.Text(root, height=8, width=100, font='Times 10 bold',bg='beige', foreground='#885511')
lblSource=tk.Label(root, text="",bg='#55bb22', font='Arial 12' )
btnStockSymbol=tk.Button(root, text="GET STOCK HISTORY INFORMATION", bg="dark gray", command=get_stock_history)
print(theMean)
btnStockSymbol.pack()

lblStockHistory.pack()

lblSource.pack()
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
#btnBuy=tk.Button(root, text="BUY CURRENT STOCK", bg="dark green", foreground="white", command=buy_shares)
#btnBuy.pack_forget()
#lblSell=tk.Label(root, text="Ready to sell for this amount?", bg='#55bb22', font='Arial 11 bold')
#lblSell.pack_forget()
#entSellAmount=tk.Entry(root, font='Arial 20 bold', width=10 )
#entSellAmount.pack_forget()
#var = IntVar()
#rbYesSell=Radiobutton(root, text="Yes",variable=var, value=1, command=sell_Stock, bg='#55bb22', font='Arial 11 bold')
#rbYesSell.pack_forget()
#rbNoSell=Radiobutton(root,text="No", variable=var, value=2, command=sell_Stock, bg='#55bb22', font='Arial 11 bold')
#rbNoSell.pack_forget()
menubar=Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_stock)
filemenu.add_command(label="Exit", command=close_app)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
btnFindSymbol['state']="normal"

root.update()
tk.mainloop()

