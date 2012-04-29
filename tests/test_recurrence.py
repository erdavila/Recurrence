import unittest
from datetime import date
from itertools import izip
import recurrence


class TestDaysBasedRecurrence(unittest.TestCase):
	def setUp(self):
		self.dbr = recurrence.DaysBasedRecurrence(period=3, anchor=date(2012, 4, 7))

	def testAttributes(self):
		self.assertEquals(self.dbr.period, 3)
		self.assertEquals(self.dbr.anchor, date(2012, 4, 7))
	
	def testReadOnlyAttributes(self):
		def set_period():
			self.dbr.period = 10
		self.assertRaises(AttributeError, set_period)
		
		def set_anchor():
			self.dbr.anchor = date(2012, 12, 20)
		self.assertRaises(AttributeError, set_anchor)
		
		self.dbr.foo = 'bar'
	
	def testComparisons(self):
		# Equal period and anchor
		self.assertTrue( self.dbr == recurrence.DaysBasedRecurrence(period=3, anchor=date(2012, 4, 7)))
		self.assertFalse(self.dbr != recurrence.DaysBasedRecurrence(period=3, anchor=date(2012, 4, 7)))
		
		# Different period
		self.assertFalse(self.dbr == recurrence.DaysBasedRecurrence(period=4, anchor=date(2012, 4, 7)))
		self.assertTrue( self.dbr != recurrence.DaysBasedRecurrence(period=4, anchor=date(2012, 4, 7)))
		
		# Different anchor
		self.assertFalse(self.dbr == recurrence.DaysBasedRecurrence(period=3, anchor=date(2012, 4, 6)))
		self.assertTrue( self.dbr != recurrence.DaysBasedRecurrence(period=3, anchor=date(2012, 4, 6)))
		
	
	def testGetOccurrence(self):
		self.assertEquals(self.dbr.get_occurrence(-9), date(2012, 3, 11))
		self.assertEquals(self.dbr.get_occurrence(-8), date(2012, 3, 14))
		self.assertEquals(self.dbr.get_occurrence(-7), date(2012, 3, 17))
		self.assertEquals(self.dbr.get_occurrence(-6), date(2012, 3, 20))
		self.assertEquals(self.dbr.get_occurrence(-5), date(2012, 3, 23))
		self.assertEquals(self.dbr.get_occurrence(-4), date(2012, 3, 26))
		self.assertEquals(self.dbr.get_occurrence(-3), date(2012, 3, 29))
		self.assertEquals(self.dbr.get_occurrence(-2), date(2012, 4,  1))
		self.assertEquals(self.dbr.get_occurrence(-1), date(2012, 4,  4))
		
		self.assertEquals(self.dbr.get_occurrence( 0), date(2012, 4,  7))
		
		self.assertEquals(self.dbr.get_occurrence( 1), date(2012, 4, 10))
		self.assertEquals(self.dbr.get_occurrence( 2), date(2012, 4, 13))
		self.assertEquals(self.dbr.get_occurrence( 3), date(2012, 4, 16))
		self.assertEquals(self.dbr.get_occurrence( 4), date(2012, 4, 19))
		self.assertEquals(self.dbr.get_occurrence( 5), date(2012, 4, 22))
		self.assertEquals(self.dbr.get_occurrence( 6), date(2012, 4, 25))
		self.assertEquals(self.dbr.get_occurrence( 7), date(2012, 4, 28))
		self.assertEquals(self.dbr.get_occurrence( 8), date(2012, 5,  1))
		self.assertEquals(self.dbr.get_occurrence( 9), date(2012, 5,  4))
	
	
	def testIsOccurrence(self):
		self.assertTrue( self.dbr.is_occurrence(date(2012, 3, 29)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 3, 30)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 3, 31)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4,  1)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  2)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  3)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4,  4)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  5)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  6)))
		
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4,  7)))
		
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  8)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  9)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4, 10)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 11)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 12)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4, 13)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 14)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 15)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4, 16)))
	
	
	def testGetOccurrenceNumber(self):
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 3, 29)), -3)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 3, 30)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 3, 31)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4,  1)), -2)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  2)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  3)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4,  4)), -1)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  5)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  6)))
		
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4,  7)),  0)
		
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  8)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  9)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4, 10)),  1)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 11)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 12)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4, 13)),  2)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 14)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 15)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4, 16)),  3)
	
	
	def testGetGeneratorDefault(self):
		EXPECTED = [
			date(2012, 4,  7),
			date(2012, 4, 10),
			date(2012, 4, 13),
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
			date(2012, 4, 28),
			date(2012, 5,  1),
			date(2012, 5,  4),
		]
		for occurrence, expected in izip(self.dbr.get_generator(), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGetGeneratorWithFirstPositive(self):
		EXPECTED = [
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
			date(2012, 4, 28),
			date(2012, 5,  1),
			date(2012, 5,  4),
			date(2012, 5,  7),
			date(2012, 5, 10),
			date(2012, 5, 13),
		]
		for occurrence, expected in izip(self.dbr.get_generator(first_occurrence_number=3), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGetGeneratorWithFirstNegative(self):
		EXPECTED = [
			date(2012, 3, 29),
			date(2012, 4,  1),
			date(2012, 4,  4),
			date(2012, 4,  7),
			date(2012, 4, 10),
			date(2012, 4, 13),
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
		]
		for occurrence, expected in izip(self.dbr.get_generator(first_occurrence_number=-3), EXPECTED):
			self.assertEquals(occurrence, expected, 'occurence=%r, expected=%r' % (occurrence, expected))
	
	
	def testGetGeneratorWithDirection(self):
		EXPECTED = [
			date(2012, 4, 16),
			date(2012, 4, 13),
			date(2012, 4, 10),
			date(2012, 4,  7),
			date(2012, 4,  4),
			date(2012, 4,  1),
			date(2012, 3, 29),
			date(2012, 3, 26),
			date(2012, 3, 23),
			date(2012, 3, 20),
		]
		generator = self.dbr.get_generator(first_occurrence_number=3, direction=recurrence.PAST)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurence=%r, expected=%r' % (occurrence, expected)
				)



if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()