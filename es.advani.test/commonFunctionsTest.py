# -*- coding: utf-8 -*-

#roberto bolaño debe dar
#roberto+bola%C3%B1o
import unittest
import sys
sys.path.append('C:\Users\Javier\Documents\SPYDER\wallabot\es.advani.src')
import commonFunctions as common

class TestStringMethods(unittest.TestCase):

    def testInputBolanio(self):
        self.assertEqual(common.translateSingleWord('bolaño'), 'bola%C3%B1o')

    def testInputRobertoBolanoTest(self):
        self.assertEqual(common.translateWords('roberto bolaño'), 'roberto+bola%C3%B1o')
 
    def testInputJulioCortazar(self):
        self.assertEqual(common.translateWords('julio cortázar'), 'julio+cort%C3%A1zar')
        
if __name__ == '__main__':
    unittest.main()