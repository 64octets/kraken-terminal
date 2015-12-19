#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import helpers as h

# Set default encoding to allow currency symbols
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class TestStringMethods(unittest.TestCase):

  def test_currencyStr(self):

      # Currency with symbol and rounded to 2 decimal places
      self.assertEqual(h._currencyStr("300.123"), "€300.12")

      # Accepts float
      self.assertEqual(h._currencyStr(300.123), "€300.12")

  def test_getTicker(self):

       ticker = h.getTicker()

       # High, last and low prices.
       assert "High" in ticker['txt']
       assert "Last" in ticker['txt']
       assert "Low"  in ticker['txt']

if __name__ == '__main__':
    unittest.main()
