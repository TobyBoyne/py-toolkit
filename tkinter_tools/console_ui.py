"""
Tools for logging to a UI
https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/
Threading should be used to allow for output while a function is running
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import logging
from logging.handlers import QueueHandler
import queue

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

input_queue = queue.Queue()
def console_input(prompt):
	"""Wait for an entry to the console"""
	logger.info(prompt)
	with input_queue.mutex:
		input_queue.queue.clear()
	return input_queue.get(block=True, timeout=None)


class ConsoleUi:
	"""Poll messages from a logging queue and display them in a scrolled text widget"""
	def __init__(self, frame):
		self.frame = frame
		self.input_start_idx = tk.END
		# Create a ScrolledText wdiget
		self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
		self.scrolled_text.pack(expand=True, fill=tk.BOTH)
		self.scrolled_text.configure(font='TkFixedFont')
		self.scrolled_text.tag_config('INFO',     foreground='black')
		self.scrolled_text.tag_config('DEBUG',    foreground='gray')
		self.scrolled_text.tag_config('WARNING',  foreground='dark orange')
		self.scrolled_text.tag_config('ERROR',    foreground='red')
		self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)

		self.scrolled_text.bind('<Key>', self.key_press)

		# Create a logging handler using a queue
		self.log_queue = queue.Queue()
		self.queue_handler = QueueHandler(self.log_queue)
		formatter = logging.Formatter('%(asctime)s:\t%(message)s', datefmt='%H:%M:%S')
		self.queue_handler.setFormatter(formatter)
		logger.addHandler(self.queue_handler)
		# Start polling messages from the queue
		self.frame.after(100, self.poll_log_queue)

	def display(self, record):
		msg = record.getMessage()
		self.scrolled_text.configure(state='normal')
		self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
		# self.scrolled_text.configure(state='disabled')
		# Autoscroll to the bottom
		self.scrolled_text.yview(tk.END)

		self.scrolled_text.mark_set('input_start', 'end-1c')
		self.scrolled_text.mark_gravity('input_start', tk.LEFT)

	def poll_log_queue(self):
		while True:
			try:
				record = self.log_queue.get(block=False)
			except queue.Empty:
				break
			else:
				self.display(record)

		# Check every 100ms if there is a new message in the queue to display
		self.frame.after(100, self.poll_log_queue)

	def key_press(self, event):
		"""Function used to send any inputs to the input_queue when the return key is pressed"""
		if event.char == '\r':
			user_input = self.scrolled_text.get('input_start', 'end-1c').strip()
			input_queue.put(user_input)
			self.scrolled_text.mark_set('input_start', 'end-1c')