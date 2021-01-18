from time import perf_counter
# json used for pprint
from json import dumps

class Timer:
	"""Class to record the time taken as a dictionary
	Can record several different times at once
	Will add to total time if called multiple times for the same label"""
	def __init__(self):
		self.times = {}
		self.current_name = None
		self.start_time = None

	def start(self, name):
		t = perf_counter()
		if self.current_name is not None:
			if not self.current_name in self.times:
				self.times[self.current_name] = {'total time': 0., 'num times': 0, 'avg time': 0.}

			current_dict = self.times[self.current_name]
			current_dict['total time'] += t - self.start_time
			current_dict['num times'] += 1
			current_dict['avg time'] = current_dict['total time'] / current_dict['num times']

		self.start_time = t
		self.current_name = name

	def stop(self):
		# save current, stop recording
		self.start(None)

	def __repr__(self):
		return dumps(dict(self.times), indent=4)


if __name__ == '__main__':
	timer = Timer()
	for i in range(10):
		if i < 5:
			timer.start('loop1')
			for _ in range(100000):
				pass

		timer.start('loop2')
		for _ in range(1000):
			pass

	timer.stop()
	print(timer)