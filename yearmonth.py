from datetime import date, timedelta
from functools import total_ordering
import re


@total_ordering
class YearMonth(object):
	def __init__(self, year, month):
		if month < 1 or month > 12:
			raise ValueError('Invalid month: ' + str(month))
		
		self.year = year
		self.month = month
	
	@staticmethod
	def from_string(string):
		m = re.match(r'^(\d{4})-(\d{2})$', string)
		if m is None:
			raise ValueError('Invalid YearMonth string initialization: ' + repr(string))
		else:
			year  = int(m.group(1))
			month = int(m.group(2))
			return YearMonth(year, month)
	
	@staticmethod
	def from_date(date):
		return YearMonth(date.year, date.month)
	
	@staticmethod
	def from_ordinal(ordinal):
		year = ordinal // 12
		month = (ordinal % 12) + 1
		return YearMonth(year, month)
	
	def __setattr__(self, attr, value):
		if attr in ('year', 'month') and hasattr(self, attr):
			raise AttributeError('Attribute ' + attr + ' cannot be set')
		return super(YearMonth, self).__setattr__(attr, value)
	
	def to_ordinal(self):
		return self.year * 12 + (self.month - 1)
	
	def get_first_day(self):
		return self.get_date(1)
	
	def get_last_day(self):
		return (self + 1).get_first_day() - timedelta(days=1)
	
	def get_date(self, day):
		return date(self.year, self.month, day)
	
	def __hash__(self):
		return self.to_ordinal()
	
	def __eq__(self, other):
		return self.year == other.year and self.month == other.month
	
	def __ne__(self, other):
		return self.year != other.year or self.month != other.month
	
	def __lt__(self, other):
		return self.to_ordinal() < other.to_ordinal()
	
	def __add__(self, other):
		return YearMonth.from_ordinal(self.to_ordinal() + other)
	
	def __radd__(self, other):
		return self + other
	
	def __sub__(self, other):
		if isinstance(other, YearMonth):
			return self.to_ordinal() - other.to_ordinal()
		else:
			return self + (-other)
	
	def __str__(self):
		return '%04d-%02d' % (self.year, self.month)

	def __unicode__(self):
		return unicode(str(self))

	def __repr__(self):
		return '%s(%d,%d)' % (self.__class__.__name__, self.year, self.month)
