# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:23:56 2020

@author: 15406
"""

def open_stock_data(root,txtStockInfo,txtStockSymbol,tk,gotStockDataFrom,fullPath ):
    global fromExternal
    global stockDataSource 
    global loadCSV

    global externalRows

    from tkinter import filedialog
    import os.path
    from os import path
    import csv
    root.filename =  filedialog.askopenfilename(initialdir = "/", title = "Select a .CSV file", filetypes = (("csv files", "*.csv"),("all files","*.*")))
    loadCSV=os.path.basename(root.filename)
    print ("FILENAME: " + str(loadCSV))
    fullPath=root.filename
    print (fullPath)
    loadSymbol=os.path.splitext(loadCSV)[0][:-4]
    txtStockSymbol.insert(tk.END, loadSymbol )
    fromExternal=True
    print(gotStockDataFrom.name)
    txtStockInfo.delete('1.0',tk.END)
    
    try:
        with open(fullPath, 'r') as extFile:
            print("FULL PATH: " + str(fullPath))
            externalRows=len( list(csv.reader(extFile)))
    except:
        gotStockDataFrom=stockDataSource.CHECKHISTORY 
    return [fullPath, gotStockDataFrom.name]