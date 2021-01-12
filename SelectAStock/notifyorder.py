# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:10:08 2020

@author: 15406
"""

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