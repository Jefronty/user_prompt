
import os
import sys
import time
import getpass

if os.name == 'nt': #Windows
	import msvcrt
	platform = 'Windows'
else:
	import select
	import termios
	platform = 'Posix'

DEFAULT_TIMEOUT = 30.0


class TimeoutOccurred(Exception):
	pass


def user_prompt(prompt='', timeout=None, hide_input=False):
	if timeout is None:
		if hide_input:
			return getpass.getpass(prompt)
		if sys.version_info[0] < 3:
			return raw_input(prompt)
		else:
			return input(prompt)
	if platform == 'Windows':
		return win_timed_prompt(
			prompt=prompt,
			timeout=timeout,
			hide_input=hide_input
		)
	else:
		return posix_timed_prompt(
			prompt=prompt,
			timeout=timeout,
			hide_input=hide_input
		)


def posix_timed_prompt(prompt='', timeout=DEFAULT_TIMEOUT, hide_input=False):
	old_settings = None
	if hide_input:
		old_settings = termios.tcgetattr(sys.stdin.fileno())
		new_settings = old_settings[:]
		new_settings[3] &= ~(termios.ECHO | termios.ECHONL)
		termios.tcsetattr(
			sys.stdin.fileno(),
			termios.TCSADRAIN,
			new_settings
		)
	try:
		sys.stdout.write(prompt)
		sys.stdout.flush()
		(ready, _, _) = select.select([sys.stdin], [], [], timeout)
		if ready:
			return sys.stdin.readline().rstrip('\n')
		else:
			raise TimeoutOccurred
	finally:
		if old_settings is not None:
			termios.tcsetattr(
				sys.stdin.fileno(),
				termios.TCSADRAIN,
				old_settings
			)


def put_str(string):
	for c in string:
		msvcrt.putwch(c)


def win_timed_prompt(prompt='', timeout=DEFAULT_TIMEOUT, hide_input=False):
	clock = getattr(time, 'monotonic', time.time)
	begin = clock()
	end = begin + timeout
	put_str(prompt)
	line = ''
	while clock() < end:
		if msvcrt.kbhit():
			c = msvcrt.getwch()
			if c == '\r' or c == '\n':
				put_str('\r\n')
				return line
			if c == '\003':
				raise KeyboardInterrupt
			if c == '\b':
				line = line[:-1]
				if not hide_input:
					put_str('\r\n' + prompt + line)
			else:
				if not hide_input:
					msvcrt.putwch(c)
				line = line + c
		time.sleep(0.05)
	raise TimeoutOccurred