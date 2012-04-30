import itertools
import datetime
import yearmonth


DAY_OF_MONTH = 'DAY_OF_MONTH'

SUN = SUNDAY = 'SUNDAY'
MON = MONDAY = 'MONDAY'
TUE = TUESDAY = 'TUESDAY'
WED = WEDNESDAY = 'WEDNESDAY'
THU = THURSDAY = 'THURSDAY'
FRI = FRIDAY = 'FRIDAY'
SAT = SATURDAY = 'SATURDAY'

FUTURE = +1
PAST   = -1


class DaysBasedRecurrence(object):
	
	def __init__(self, anchor, period):
		if not isinstance(anchor, datetime.date):
			raise ValueError('Invalid anchor instance: ' + repr(anchor))
		
		self.anchor = anchor
		self.period = period
	
	def get_occurrence(self, number):
		delta_days = number * self.period
		delta = datetime.timedelta(days=delta_days)
		return self.anchor + delta
	
	def is_occurrence(self, candidate):
		delta = candidate - self.anchor
		delta_days = delta.days
		return delta_days % self.period == 0
	
	def get_occurrence_number(self, occurrence):
		delta = occurrence - self.anchor
		delta_days = delta.days
		if delta_days % self.period == 0:
			return delta_days // self.period
		else:
			raise ValueError('The date %r is not a valid occurrence' % occurrence)
	
	def get_occurrence_after(self, date):
		delta = date - self.anchor
		delta_days = delta.days
		remainder = delta_days % self.period
		delta_days += self.period - remainder
		delta = datetime.timedelta(days=delta_days)
		occurrence = self.anchor + delta
		return occurrence
		
	def get_generator(self, first_occurrence_number=0, direction=FUTURE):
		for number in itertools.count(start=first_occurrence_number, step=(-1 if direction < 0 else +1)):
			occurrence = self.get_occurrence(number)
			yield occurrence
	
	def __setattr__(self, attr, value):
		if attr in ('anchor', 'period') and hasattr(self, attr):
			raise AttributeError('Attribute ' + attr + ' cannot be set')
		return super(DaysBasedRecurrence, self).__setattr__(attr, value)
	
	def __eq__(self, other):
		return (isinstance(other, DaysBasedRecurrence)
				and self.anchor == other.anchor
				and self.period == other.period
			)
	
	def __ne__(self, other):
		return not (self == other)
	
	def __hash__(self):
		return hash(self.anchor) ^ hash(self.period) 


class MonthsBasedRecurrence(object):
	def __init__(self, anchor, period, ordinal, day=DAY_OF_MONTH):
		if not isinstance(anchor, yearmonth.YearMonth):
			raise ValueError('Invalid anchor instance: ' + repr(anchor))
		
		self.anchor = anchor
		self.period = period
		self.ordinal = ordinal
		self.day = day
	
	def get_occurrence(self, number):
		if self.ordinal < 1: raise NotImplementedError()
		if self.day != DAY_OF_MONTH: raise NotImplementedError()
		ym = self.anchor + number * self.period
		return ym.get_date(self.ordinal)
	
	def is_occurrence(self, candidate_occurrence):
		if self.ordinal < 1: raise NotImplementedError()
		if self.day != DAY_OF_MONTH: raise NotImplementedError()
		if candidate_occurrence.day != self.ordinal:
			return False
		ym = yearmonth.YearMonth.from_date(candidate_occurrence)
		delta = ym - self.anchor
		return delta % self.period == 0
	
	def get_occurrence_number(self, occurrence):
		if self.ordinal < 1: raise NotImplementedError()
		if self.day != DAY_OF_MONTH: raise NotImplementedError()
		if occurrence.day != self.ordinal:
			raise ValueError('The date %r is not a valid occurrence' % occurrence)
		ym = yearmonth.YearMonth.from_date(occurrence)
		delta = ym - self.anchor
		if delta % self.period == 0:
			return delta // self.period
		else:
			raise ValueError('The date %r is not a valid occurrence' % occurrence)
	
	def get_occurrence_after(self, date):
		if self.ordinal < 1: raise NotImplementedError()
		if self.day != DAY_OF_MONTH: raise NotImplementedError()
		ym = yearmonth.YearMonth.from_date(date)
		delta = ym - self.anchor
		remainder = delta % self.period
		if remainder == 0:
			if date.day >= self.ordinal:
				ym += self.period
		else:
			ym += self.period - remainder
		return ym.get_date(self.ordinal)
	
	def get_generator(self, first_occurrence_number=0, direction=FUTURE):
		for number in itertools.count(start=first_occurrence_number, step=(-1 if direction < 0 else +1)):
			occurrence = self.get_occurrence(number)
			yield occurrence
	
	def __setattr__(self, attr, value):
		if attr in ('anchor', 'period', 'ordinal', 'day') and hasattr(self, attr):
			raise AttributeError('Attribute ' + attr + ' cannot be set')
		return super(MonthsBasedRecurrence, self).__setattr__(attr, value)
	
	def __eq__(self, other):
		return (isinstance(other, MonthsBasedRecurrence)
			and self.anchor == other.anchor
			and self.period == other.period
			and self.ordinal == other.ordinal
			and self.day == other.day
		)
	
	def __ne__(self, other):
		return not (self == other)
	
	def __hash__(self):
		return hash(self.anchor) ^ hash(self.period) ^ hash(self.ordinal) ^ hash(self.day)  
