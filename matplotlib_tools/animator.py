"""Classes for animation in matplotlib
Superclass of FuncAnimation, makes customisation easier in code"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# time delay between frames
INTERVAL = 20

class GroupAnimator(FuncAnimation):
	"""Class to store multiple Animator objects, and render them side-by-side
	Allows for multiple drawings to be saved in a single .gif"""
	def __init__(self, fig: plt.Figure, anims, T):
		"""
		:param fig: pyplot figure object to plot the animations on
		:param anims: list of Animator objects to plot
		:param T: total time (in seconds) of animation
		"""
		self.anims = anims
		total_frames = int(T * 1000 // INTERVAL)
		kwargs = {
			"init_func": self.init_func,
			"frames": total_frames,
			"interval": INTERVAL,
			"blit": True
		}

		super().__init__(fig, self.animate, **kwargs)

	def init_func(self):
		anim_data = []
		for anim in self.anims:
			anim_data += anim.init_func()
		return anim_data

	def animate(self, i):
		anim_data = []
		for anim in self.anims:
			anim_data += anim.animate(i)
		return anim_data


class Animator:
	"""Object stores all lines to be animated
	Main drawing stored in self.line
	init() is called at the beginning of each loop
	animate() is called at each frame"""
	def __init__(self, ax: plt.Axes, func):
		"""
		:param ax: pyplot Axes to plot onto
		:param func: function to evaluate at each frame, returns x and y data
		"""
		# init function for FuncAnimation
		self.line, = ax.plot([], [], lw=3)
		self.eval_func = func

	def init_func(self):
		self.line.set_data([], [])
		return [self.line,]

	def animate(self, i):
		t = i * (INTERVAL / 1000)

		x_data, y_data = self.eval_func(t)
		self.line.set_data(x_data, y_data)
		return [self.line,]