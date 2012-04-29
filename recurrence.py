import itertools
import datetime


MONTH_DAY = 'MONTH_DAY'

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
	
	def __init__(self, period, anchor):
		self.period = period
		self.anchor = anchor
	
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
			return delta_days / self.period
		else:
			raise ValueError('The date %r is not a valid occurrence' % occurrence)
	
	def get_generator(self, first_occurrence_number=0, direction=FUTURE):
		for number in itertools.count(start=first_occurrence_number, step=(-1 if direction < 0 else +1)):
			occurrence = self.get_occurrence(number)
			yield occurrence
	
	def __setattr__(self, attr, value):
		if attr in ('period', 'anchor') and hasattr(self, attr):
			raise AttributeError('Attribute ' + attr + ' cannot be set')
		return super(DaysBasedRecurrence, self).__setattr__(attr, value)
	
	def __eq__(self, other):
		return self.period == other.period and self.anchor == other.anchor
	
	def __ne__(self, other):
		return not (self == other)
	
	def __hash__(self):
		return hash(self.anchor) ^ hash(self.period) 
