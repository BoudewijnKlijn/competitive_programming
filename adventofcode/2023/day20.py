import math
from queue import Queue


class Module:
    def __init__(self, name, output: list[str]):
        self.name = name
        self.output = output
        self.type_ = "special"

    def send_pulse(self, is_high_pulse: bool):
        return [(self.name, is_high_pulse, out_name) for out_name in self.output]

    def receive_pulse(self, input_name: str, is_high_pulse: bool):
        return self.send_pulse(is_high_pulse)

    def __repr__(self):
        return f"{self.name}({self.type_}) --> {self.output}"


class FlipFlop(Module):
    def __init__(self, name, output: list[str]):
        super().__init__(name, output)
        self.type_ = "Flip-flop"
        self.on = False

    def receive_pulse(self, input_name: str, is_high_pulse: bool):
        if not is_high_pulse:  # only act on low pulses
            self.on = not self.on  # flip state
            return self.send_pulse(is_high_pulse=self.on)
        return []

    def __repr__(self):
        return f"{self.name}({self.type_}) state={self.on} --> {self.output}"


class Conjunction(Module):
    def __init__(self, name, output: list[str]):
        super().__init__(name, output)
        self.type_ = "Conjunction"
        self.last_inputs = dict()

    def receive_pulse(self, input_name: str, is_high_pulse: bool):
        self.last_inputs[input_name] = is_high_pulse  # update before sending
        if all(self.last_inputs.values()):
            return self.send_pulse(is_high_pulse=False)
        else:
            return self.send_pulse(is_high_pulse=True)

    def __repr__(self):
        return f"{self.name}({self.type_}) inputs={self.last_inputs} --> outputs={self.output}"


def part1(content):
    n_button_pushes = 1000
    modules = init_modules(content)
    low, high = simulate(n_button_pushes, modules)
    return low * high


def init_modules(content):
    outputs = set()
    modules = dict()
    for line in content.strip().split("\n"):
        name, output = map(str.strip, line.split("->"))
        output = output.strip().split(", ")
        outputs.update(output)
        if name.startswith("%"):
            name = name[1:]
            modules[name] = FlipFlop(name, output)
        elif name.startswith("&"):
            name = name[1:]
            modules[name] = Conjunction(name, output)
        else:
            modules[name] = Module(name, output)

    # Create dead end modules: output and rx
    for output in outputs:
        if not modules.get(output):
            modules[output] = Module(output, [])

    # add inputs to conjunction modules
    for module_name in modules.keys():
        for o in modules[module_name].output:
            if o == "output":
                continue
            try:
                modules[o].last_inputs[module_name] = False
            except AttributeError:
                pass

    return modules


def simulate(n_button_pushes=1000, modules=None):
    n_low_pulses = 0
    n_high_pulses = 0

    needles = ["vm", "kb", "dn", "vk"]
    low_when = [[] for _ in needles]

    for i in range(n_button_pushes):
        if i % 1000 == 0:
            print(i)

        q = Queue()
        q.put(
            ("button", False, "broadcaster")
        )  # start with low pulse from button to broadcaster
        while not q.empty():
            pulse_from, is_high_pulse, module_name = q.get()
            n_low_pulses += 1 if not is_high_pulse else 0
            n_high_pulses += 1 if is_high_pulse else 0
            module = modules[module_name]

            # Let's assume that whenever it gets a low pulse, it's just a single low pulse.
            if module_name == "rx" and not is_high_pulse:
                print(f"Button pushed {i} times")
                exit()

            pulses_received = module.receive_pulse(pulse_from, is_high_pulse)
            for pulse in pulses_received:
                # print(pulse)
                q.put(pulse)

                if pulse_from in ["vm", "kb", "dn", "vk"] and not is_high_pulse:
                    print(i, pulse_from, is_high_pulse)
                    idx = needles.index(pulse_from)
                    if (
                        len(low_when[idx]) == 0
                        or len(low_when[idx]) > 0
                        and low_when[idx][-1] != i
                    ):
                        low_when[idx].append(i)
                    print(low_when)
                    for arr in low_when:
                        if len(arr) > 1:
                            print(delta(arr))

    return n_low_pulses, n_high_pulses


def delta(array):
    return [array[i + 1] - array[i] for i in range(len(array) - 1)]


def part2(content):
    """This may take many simulations, probably too many to simulate, so I have to analyze.
    After many (5.8m+) iterations, I got not a single low pulse to rx.
    Let's assume that whenever it gets a low pulse, it's just a single low pulse.
    rx has no outputs
    the only input to rx is sq.
    'sq': sq(Conjunction) inputs={'fv': False, 'kk': False, 'vt': False, 'xr': False} --> outputs=['rx']
    sq will only output a low pulse if all inputs are high, so fv, kk, vt, xr must all be high.
    'fv': fv(Conjunction) inputs={'vm': False} --> outputs=['sq']
    'kk': kk(Conjunction) inputs={'kb': False} --> outputs=['sq']
    'vt': vt(Conjunction) inputs={'dn': False} --> outputs=['sq']
    'xr': xr(Conjunction) inputs={'vk': False} --> outputs=['sq']
    So, all four inputs to sq, are all conjunctions with only one input, which means they are inverters.
    So, vm, kb, dn, vk, must all output a low signal. Each will be inverted, and then send a high pulse to sq.
    vm, kb, dn, vk, are all conjunctions with many inputs. becomes harder to analyze.
    Maybe we can already see cycles of low pulse outputs, with differing periods.
    Found the periods:
        [3863, 3863, 3863]
        [3931, 3931, 3931]
        [3797, 3797, 3797]
        [3769, 3769, 3769]
    One part is finding the least common multiple of these periods.
    Another part is that the cycles start at a different time: vm starts at 3862, kb at 3930, dn at 3796, vk at 3768
    So, now we just have to find a certain button presses (BP) such that:
        BP % 3863 = 3862
        BP % 3931 = 3930
        BP % 3797 = 3796
        BP % 3769 = 3768
    This is similar to day 8, except that these cycles are already all primes.
    We could multiply them all, but then they still don't align at the start.
    I know from previous years that the Chinese Remainder Theorem can be used to solve this.
    The first two match when the first cycle is multiplied by 3930.
    """
    n_button_pushes = 10**10
    modules = init_modules(content)
    simulate(n_button_pushes, modules)

    starts = [3862, 3930, 3796, 3768]
    periods = [3863, 3931, 3797, 3769]
    for p in range(4):
        for q in range(4):
            if p == q:
                continue
            array = []
            for i in range(50_000):
                if (starts[p] + periods[p] * i) % periods[q] == starts[q]:
                    array.append(i)
            print(p, q, delta(array))

    return math.prod(periods)


if __name__ == "__main__":
    SAMPLE = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

    SAMPLE2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

    assert part1(SAMPLE) == 32000000

    with open("day20.txt") as f:
        CONTENT = f.read()

    print(part1(CONTENT))  # 867118762

    print(part2(CONTENT))  # 217317393039529
