# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:42:37 2020

@author: 15406
"""

global tk
from tkinter import END
import csv
import tkinter as tk
reader=None


def find_stock_symbol(entFindSymbol, lstSymbols, dctSymbols):
    if entFindSymbol.get() == "": return
    print("YOU CLICKED FIND BUTTON")
    lstSymbols.delete(0,END)
    srchString=entFindSymbol.get()
    itemCount=0
    for key,value in dctSymbols.items():
        if srchString.upper() in value.upper() or srchString.upper() in key.upper():
            print(value)
            lstSymbols.insert(itemCount,key.ljust(9) + "|" + value)
            itemCount +=1 
 
def reset_symbol_list(lstSymbols, dctSymbols):
  print("RESETTING SYMBOL LIST:")
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

def select_your_symbol(lstSymbols, txtStockSymbol):
    symbolItem=lstSymbols.get(lstSymbols.curselection())
    pipePos=symbolItem.find("|")
    symbolResult=symbolItem[0:pipePos].rstrip()
    txtStockSymbol.delete(0, END)
    txtStockSymbol.insert(END, symbolResult)
 