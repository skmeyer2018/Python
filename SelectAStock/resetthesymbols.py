# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:28:13 2020

@author: 15406
"""
import tkinter as tk
import csv
def reset_symbol_list(lstSymbols, dctSymbols):
  print("RESETTING SYMBOL LIST:")
  lstSymbols.delete(0,tk.END)
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