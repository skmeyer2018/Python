# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:05:03 2020

@author: 15406
"""

def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))