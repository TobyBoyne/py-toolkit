from collections import defaultdict
from time import perf_counter
# json used for pprint
from json import dumps

class Timer:
	"""Class to record the time taken as a dictionary
	Can record several different times at once
	Will add to total time if called multiple times for the same label"""
	def __init__(self):
		self.times = defaultdict(int)
		self.current_name = None
		self.start_time = None

	def start(self, name):
		t = perf_counter()
		if self.current_name is not None:
			self.times[self.current_name] += t - self.start_time

		self.start_time = t
		self.current_name = name

	def stop(self):
		# save current, stop recording
		self.start(None)

	def __repr__(self):
		return dumps(dict(self.times), indent=4)