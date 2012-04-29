import unittest
from yearmonth import YearMonth
from datetime import date


class TestYearMonth(unittest.TestCase):


	def setUp(self):
		self.ym201112  = YearMonth(2011, 12)
		self.ym201201  = YearMonth(2012, 01)
		self.ym201206a = YearMonth(2012,  6)
		self.ym201206b = YearMonth(2012,  6)

	def testConstructor(self):
		self.assertEquals(self.ym201112.year , 2011)
		self.assertEquals(self.ym201112.month,   12)
		
		self.assertEquals(self.ym201201.year , 2012)
		self.assertEquals(self.ym201201.month,    1)
		
		self.assertEquals(self.ym201206a.year , 2012)
		self.assertEquals(self.ym201206a.month,    6)
		
		self.assertEquals(self.ym201206b.year , 2012)
		self.assertEquals(self.ym201206b.month,    6)
	
	def testValidateConstructorArguments(self):
		self.assertRaises(ValueError, lambda: YearMonth(2012, 0))
		self.assertRaises(ValueError, lambda: YearMonth(2012, -1))
		self.assertRaises(ValueError, lambda: YearMonth(2012, -5))
		self.assertRaises(ValueError, lambda: YearMonth(2012, 13))
		self.assertRaises(ValueError, lambda: YearMonth(2012, 15))
		
	def testReadOnlyAttributes(self):
		def change_year():
			self.ym201112.year = 2000
		self.assertRaises(AttributeError, change_year)

		def change_month():
			self.ym201112.month = 10
		self.assertRaises(AttributeError, change_month)
		
		ym = YearMonth(2012, 1)
		ym.day = 7  # Should not raise any exception 
	
	def testFromString(self):
		ym = YearMonth.from_string('2011-12')
		self.assertEquals(ym, self.ym201112)
		
		ym = YearMonth.from_string('2012-01')
		self.assertEquals(ym, self.ym201201)
		
		ym = YearMonth.from_string('2012-06')
		self.assertEquals(ym, self.ym201206a)

		def from_invalid_string1():
			YearMonth.from_string('2012-01-')
		self.assertRaises(ValueError, from_invalid_string1)

		def from_invalid_string2():
			YearMonth.from_string('2012-1')
		self.assertRaises(ValueError, from_invalid_string2)

		def from_invalid_string3():
			YearMonth.from_string('xyz')
		self.assertRaises(ValueError, from_invalid_string3)

	def testToString(self):
		self.assertEquals(str(self.ym201112) , '2011-12')
		self.assertEquals(str(self.ym201201) , '2012-01')
		self.assertEquals(str(self.ym201206a), '2012-06')

	def testFromDate(self):
		ym = YearMonth.from_date(date(2011, 12, 15))
		self.assertEquals(ym, self.ym201112)
		
		ym = YearMonth.from_date(date(2012, 1, 20))
		self.assertEquals(ym, self.ym201201)
		
		ym = YearMonth.from_date(date(2012, 6, 21))
		self.assertEquals(ym, self.ym201206a)

	def testFromToOrdinal(self):
		for ym in (self.ym201112, self.ym201201, self.ym201206a):
			ordinal = ym.to_ordinal()
			new_ym = YearMonth.from_ordinal(ordinal)
			self.assertEquals(new_ym, ym)
	
	def testFirstDay(self):
		dt = self.ym201112.get_first_day()
		self.assertEquals(dt, date(2011, 12, 1))
	
		dt = self.ym201201.get_first_day()
		self.assertEquals(dt, date(2012, 1, 1))
		
		dt = self.ym201206a.get_first_day()
		self.assertEquals(dt, date(2012, 6, 1))
	
	def testLastDay(self):
		dt = self.ym201112.get_last_day()
		self.assertEquals(dt, date(2011, 12, 31))
	
		dt = self.ym201201.get_last_day()
		self.assertEquals(dt, date(2012, 1, 31))
		
		dt = YearMonth(2012, 2).get_last_day()
		self.assertEquals(dt, date(2012, 2, 29))
		
		dt = self.ym201206a.get_last_day()
		self.assertEquals(dt, date(2012, 6, 30))
	
	def testGetDate(self):
		dt = self.ym201112.get_date(7)
		self.assertEquals(dt, date(2011, 12, 7))
	
		dt = self.ym201201.get_date(15)
		self.assertEquals(dt, date(2012, 1, 15))
	
		dt = self.ym201206a.get_date(21)
		self.assertEquals(dt, date(2012, 6, 21))
	
	def testRepr(self):
		self.assertEquals(repr(self.ym201112) , 'YearMonth(2011,12)')
		self.assertEquals(repr(self.ym201201) , 'YearMonth(2012,1)')
		self.assertEquals(repr(self.ym201206a), 'YearMonth(2012,6)')
	
	
	def testEqAndNeComparisons(self):
		def assertEqual(ym1, ym2):
			self.assertTrue( ym1 == ym2)
			self.assertFalse(ym1 != ym2)
		
		def assertNotEqual(ym1, ym2):
			self.assertFalse(ym1 == ym2)
			self.assertTrue( ym1 != ym2)
		
		assertEqual(   self.ym201112, self.ym201112)
		assertNotEqual(self.ym201112, self.ym201201)
		assertNotEqual(self.ym201112, self.ym201206a)
		assertNotEqual(self.ym201112, self.ym201206b)
	
		assertNotEqual(self.ym201201, self.ym201112)
		assertEqual(   self.ym201201, self.ym201201)
		assertNotEqual(self.ym201201, self.ym201206a)
		assertNotEqual(self.ym201201, self.ym201206b)
	
		assertNotEqual(self.ym201206a, self.ym201112)
		assertNotEqual(self.ym201206a, self.ym201201)
		assertEqual(   self.ym201206a, self.ym201206a)
		assertEqual(   self.ym201206a, self.ym201206b)
	
		assertNotEqual(self.ym201206b, self.ym201112)
		assertNotEqual(self.ym201206b, self.ym201201)
		assertEqual(   self.ym201206b, self.ym201206a)
		assertEqual(   self.ym201206b, self.ym201206b)
	
	
	def testLtAndGeComparisons(self):
		def assertLessThan(ym1, ym2):
			self.assertTrue( ym1 <  ym2)
			self.assertFalse(ym1 >= ym2)
		
		def assertNotLessThan(ym1, ym2):
			self.assertFalse(ym1 <  ym2)
			self.assertTrue( ym1 >= ym2)
		
		assertNotLessThan(self.ym201112, self.ym201112)
		assertLessThan(   self.ym201112, self.ym201201)
		assertLessThan(   self.ym201112, self.ym201206a)
		assertLessThan(   self.ym201112, self.ym201206b)
	
		assertNotLessThan(self.ym201201, self.ym201112)
		assertNotLessThan(self.ym201201, self.ym201201)
		assertLessThan(   self.ym201201, self.ym201206a)
		assertLessThan(   self.ym201201, self.ym201206b)
	
		assertNotLessThan(self.ym201206a, self.ym201112)
		assertNotLessThan(self.ym201206a, self.ym201201)
		assertNotLessThan(self.ym201206a, self.ym201206a)
		assertNotLessThan(self.ym201206a, self.ym201206b)
	
		assertNotLessThan(self.ym201206b, self.ym201112)
		assertNotLessThan(self.ym201206b, self.ym201201)
		assertNotLessThan(self.ym201206b, self.ym201206a)
		assertNotLessThan(self.ym201206b, self.ym201206b)
	

	def testGtAndLeComparisons(self):
		def assertGreaterThan(ym1, ym2):
			self.assertTrue( ym1 >  ym2)
			self.assertFalse(ym1 <= ym2)
		
		def assertNotGreaterThan(ym1, ym2):
			self.assertFalse(ym1 >  ym2)
			self.assertTrue( ym1 <= ym2)
			
		assertNotGreaterThan(self.ym201112, self.ym201112)
		assertNotGreaterThan(self.ym201112, self.ym201201)
		assertNotGreaterThan(self.ym201112, self.ym201206a)
		assertNotGreaterThan(self.ym201112, self.ym201206b)
	
		assertGreaterThan(   self.ym201201, self.ym201112)
		assertNotGreaterThan(self.ym201201, self.ym201201)
		assertNotGreaterThan(self.ym201201, self.ym201206a)
		assertNotGreaterThan(self.ym201201, self.ym201206b)
	
		assertGreaterThan(   self.ym201206a, self.ym201112)
		assertGreaterThan(   self.ym201206a, self.ym201201)
		assertNotGreaterThan(self.ym201206a, self.ym201206a)
		assertNotGreaterThan(self.ym201206a, self.ym201206b)
	
		assertGreaterThan(   self.ym201206b, self.ym201112)
		assertGreaterThan(   self.ym201206b, self.ym201201)
		assertNotGreaterThan(self.ym201206b, self.ym201206a)
		assertNotGreaterThan(self.ym201206b, self.ym201206b)
	
	
	def testAddAndSubtract(self):
		def assertSum(ym1, n, ym2):
			self.assertEquals(ym1 +    n, ym2)
			self.assertEquals(n   +  ym1, ym2)
			self.assertEquals(-n  +  ym2, ym1)
			self.assertEquals(ym2 + (-n), ym1)
			self.assertEquals(ym1 - (-n), ym2)
			self.assertEquals(ym1 -  ym2,  -n)
			self.assertEquals(ym2 -  ym1,   n)
			self.assertEquals(ym2 -    n, ym1)
			
			aux = ym1 ; aux += n  ; self.assertEquals(aux, ym2)
			aux = ym1 ; aux -= -n ; self.assertEquals(aux, ym2)
			aux = ym2 ; aux -= n  ; self.assertEquals(aux, ym1)
			aux = ym2 ; aux += -n ; self.assertEquals(aux, ym1)
		
		assertSum(self.ym201112, 0, self.ym201112)
		assertSum(self.ym201112, 1, self.ym201201)
		assertSum(self.ym201112, 6, self.ym201206a)

		assertSum(self.ym201201, -1, self.ym201112)
		assertSum(self.ym201201,  0, self.ym201201)
		assertSum(self.ym201201,  5, self.ym201206a)

		assertSum(self.ym201206a, -6, self.ym201112)
		assertSum(self.ym201206a, -5, self.ym201201)
		assertSum(self.ym201206a,  0, self.ym201206a)

		

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
