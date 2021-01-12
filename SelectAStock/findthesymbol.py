# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 10:17:55 2020

@author: 15406
"""
global tk
from tkinter import END

def find_stock_symbol(entFindSymbol, lstSymbols, dctSymbols):
    print("YOU CLICKED FIND BUTTON")
    print(entFindSymbol.get())
    if entFindSymbol.get() == "": return
    
    lstSymbols.delete(0,END)
    srchString=entFindSymbol.get()
    itemCount=0
    for key,value in dctSymbols.items():
        if srchString.upper() in value.upper() or srchString.upper() in key.upper():
            print(value)
            lstSymbols.insert(itemCount,key.ljust(9) + "|" + value)
            itemCount +=1 