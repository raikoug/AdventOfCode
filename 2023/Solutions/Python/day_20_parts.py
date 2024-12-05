

from typing import Any
from icecream import ic
from numpy import prod
from functools import reduce

class Pulse:
    low: bool
    high: bool

    def __init__(self, low: bool, high: bool):
        self.low = low
        self.high = high
    
    def __str__(self) -> str:
        return f'{"LowPulse" if self.low else "HighPulse"}'
    
    def __repr__(self) -> str:
        return self.__str__()
    

class Flip_Flop: # modules starting with % are flip flops
    state: bool
    destinations: list
    conjunction: bool = False
    flip_flop: bool = True
    broadcaster: bool = False
    label: str

    def __init__(self, destinations: list, label: str):
        self.state = False
        self.destinations = destinations
        self.flip_flop = True
        self.conjunction = False
        self.broadcaster = False
        self.label = label
    
    def __str__(self) -> str:
        return f'Flip_Flop -{self.label:^3} - {"ON" if self.state else "OFF":^3} -> {self.destinations}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def process_pulse(self, pulse:Pulse, source: Any):
        if pulse.low: # flip flops acts only when pulse is low
            self.state = not self.state
            for destination in self.destinations:
                yield destination, Pulse(low=not self.state, high=self.state)
        else:
            return list()

class Conjuction: # modules starting with & are conjuctions
    destinations: list
    label: str
    conjunction: bool = True
    flip_flop: bool = False
    broadcaster: bool = False
    
    def __init__(self, destinations: list, label: str):
        self.label = label
        self.inputs = dict()
        self.destinations = destinations
        self.conjunction = True
        self.flip_flop = False

    def __str__(self) -> str:
        res = ''
        res += f'Conjuction {self.label} -> {self.destinations}\n'
        res += f'     └─ Inputs: {self.inputs}\n'
        return res
    
    def __repr__(self) -> str:
        return self.__str__()

    def init_label(self, label: str):
        if label not in self.inputs.keys(): # init the label if not already present
            self.inputs[label] = Pulse(low=True, high=False) # set source to low
    
    def process_pulse(self, pulse:Pulse, source: str): # remember the pulses received
        self.inputs[source] = Pulse(low=pulse.low, high=pulse.high)
        #ic(self.inputs)
        all_high = all([pulse.high for pulse in self.inputs.values()])
        for destination in self.destinations:
            yield destination, Pulse(low=all_high, high= not all_high)

class Broadcaster: # send same pulse he receive to all the destinations
    destinations: list
    conjunction: bool = False
    flip_flop: bool = False
    broadcaster: bool = True

    def __init__(self, destinations: list):
        self.destinations = destinations
        self.conjunction = False
        self.flip_flop = False
        self.broadcaster = True

    def __str__(self) -> str:
        return f'Broadcaster -> {self.destinations}'
    
    def __repr__(self) -> str:
        return self.__str__()

    def process_pulse(self, pulse:Pulse, source: Any):
        for destination in self.destinations:
            yield destination, pulse

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors 

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)

    modules = dict()


    for line in tf:
        if line.startswith('broadcaster'):
            label, dest_str = line.split(' -> ')
            destinations = dest_str.split(', ')
            modules['broadcaster'] = Broadcaster(destinations)

        else:
            # '&|%zq -> fd, gk, pp, ph, ss, dr, pl'
            #  label -> destinations
            type = line[0]
            label, dest_str = line[1:].split(' -> ')
            destinations = dest_str.split(', ')
            if type == '%':
                # add a flip_flop
                modules[label] = Flip_Flop(destinations, label)
            elif type == '&':
                # add a conjuction
                modules[label] = Conjuction(destinations, label)
            else:
                # we should never be here
                ic("PANIC!")
    #loop through modules and if they have a broadcaster as destination, add init its label
    for label, module in modules.items():
        for destination in module.destinations: # destinations here are labels!
            if destination in modules and modules[destination].conjunction:
                modules[destination].init_label(label)
    #ic(modules)
    #import sys;sys.exit(0)
    1            
    # for part 2 some fixies:
        # destination module is rx
        # for him to receive e low pulse &ls have to receive high pulses from all his inputs
        # his inputs are tx, dd, nz, ph
        #  could have taken them programmatically but stikazzi...
        #  I get how many cicle each of them need to send HIGH, and LCM them
      
    modules_mod = {'tx': 0, 'dd': 0, 'nz': 0, 'ph': 0}

    # button is a manual module that send low pulse to the broadcast and start the cycle
    part_1_low_beams = 0
    part_1_high_beams = 0
    part_2_res = 0
    part_1_end = False
    part_2_end = False
    i = 0
    while 1:
        # Button is pressed!
        i += 1
        if i % 10000 == 0: print(i, end = '\r')
        beams_to_process = list()
        beams_to_process.append(['button', 'broadcaster', Pulse(low=True, high=False)])
                                #  src         dst                pulse
        if i == 1000: part_1_end = True
        if not part_1_end: part_1_low_beams += 1
        if part_2_end and part_1_end:
            break
    
        while beams_to_process:
            #print('-------------------------------------------------')
            src, dst, pulse = beams_to_process.pop(0)
            if dst == 'ls':
                if pulse.high:
                    #ic(i, src, pulse)
                    if modules_mod[src] == 0:  modules_mod[src] = i

                    if all([modules_mod[mod] != 0 for mod in modules_mod.keys()]):
                        #ic(modules_mod)
                        #ic(i)
                        part_2_end = True

            #ic(src, dst, pulse)
            if dst not in modules:
                continue
            dst_module = modules[dst]
            for new_beam in dst_module.process_pulse(pulse, src):
                    beams_to_process.append([dst, new_beam[0], new_beam[1]])
                    if not part_1_end and new_beam[1].low: part_1_low_beams += 1
                    if not part_1_end and new_beam[1].high: part_1_high_beams += 1
            
            #ic(beams_to_process)
            #print('-------------------------------------------------')
        
    # for each modules_mod value find the factors
    factors = list()
    for val in modules_mod.values():
        factors += prime_factors(val)
    
    part_2_res = reduce(lambda x, y: x*y, factors)
    ic(part_1_low_beams * part_1_high_beams)

    ic(part_2_res)