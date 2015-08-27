import explorerhat as exp
from pins import AsyncWorker
from time import sleep
from itertools import cycle, islice
import threading

def startup(should_end = lambda _ : None, rate=0.1, fade_out=0.2): 
	lights = [exp.light.blue, exp.light.yellow, exp.light.red, exp.light.green]

	passes = list(islice(cycle([lights, lights[::-1]]), None, 2))

	serie = [item for sublist in [passes[0]] + map(lambda p : p[1:], passes[1:]) for item in sublist]

	
	def _there_and_back():
		for s in serie:
			s.fade(100,0,fade_out)
			sleep(rate)
			if should_end(nbr):
				exp.light.off()
				return False

	exp.light.off()

	worker = AsyncWorker(_there_and_back)
	worker.start()
	return True


