import explorerhat as exp
from pins import AsyncWorker

from time import sleep
from itertools import cycle, islice

##   Cycle all LEDs, back and forth, fading them out nicely. Does all of that in an async way
#    @param cycle_interruptor is called each time we move to another LED
#    @param start_of_cycle_interruptor is called each time we start a cycle
#    @param rate at which we move to the next LED in seconds
#    @param fade_out time in seconds
def startup(cycle_interruptor = lambda : None, start_of_cycle_interruptor = lambda : None, rate=0.1, fade_out=0.2):

    lights = [exp.light.blue, exp.light.yellow, exp.light.red, exp.light.green]

    passes = list(islice(cycle([lights, lights[::-1]]), None, 2))

    serie = [item for sublist in [passes[0]] + map(lambda p : p[1:], passes[1:]) for item in sublist]

    def _cycler():
        if start_of_cycle_interruptor():
            exp.light.off()
            return False
        for s in serie:
            s.fade(100,0,fade_out)
            sleep(rate)
            if cycle_interruptor():
                exp.light.off()
                return False

    exp.light.off()

    worker = AsyncWorker(_cycler)
    worker.start()
    return True
