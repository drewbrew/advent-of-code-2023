from pathlib import Path
from enum import Enum
from collections import deque
from math import lcm

REAL_INPUT = Path("day20.txt").read_text()

TEST_INPUT = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


class ModuleType(Enum):
    button = "button"
    flip_flop = "flip-flop"
    conjunction = "conjunction"
    broadcaster = "broadcaster"
    machine = "machine"


class Module:
    module_type = ModuleType.broadcaster
    power_state = False

    def __init__(self, name: str, outputs: list[str]):
        self.name = name
        self.outputs = outputs

    def receive_pulse(self, value: bool, source: str = "") -> bool | None:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"


class Button(Module):
    module_type = ModuleType.button

    def receive_pulse(self, value: bool, source: str = "") -> bool | None:
        return False


class FlipFlop(Module):
    module_type = ModuleType.flip_flop

    def receive_pulse(self, value: bool, source: str = "") -> bool:
        # print("received", value, self.power_state)
        if not value:
            # print("received low!, sending", not self.power_state)
            self.power_state = not self.power_state
            return self.power_state


class Conjunction(Module):
    module_type = ModuleType.conjunction

    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.inputs: dict[bool] = {}

    def receive_pulse(self, value: bool, source: str) -> bool:
        self.inputs[source] = value
        # print(self.inputs)
        return not all(val for val in self.inputs.values())


class Broadcaster(Module):
    module_type = ModuleType.broadcaster
    last_received = False

    def receive_pulse(self, value: bool, source: str = "") -> bool:
        self.last_received = value
        return self.last_received


class Machine(Module):
    module_type = ModuleType.machine

    def receive_pulse(self, value: bool, source: str = "") -> bool | None:
        if not value:
            raise EndOfTheSim()


def parse_input(puzzle: str) -> list[Module]:
    mods = [Button("button", ["broadcaster"])]
    for line in puzzle.splitlines():
        sender, recipients = line.split(" -> ")
        outputs = [output.strip() for output in recipients.split(",")]
        if line.startswith("%"):
            mods.append(FlipFlop(name=sender[1:].strip(), outputs=outputs))
        elif line.startswith("&"):
            mods.append(Conjunction(name=sender[1:].strip(), outputs=outputs))
        else:
            mods.append(Broadcaster(name=sender, outputs=outputs))
    return mods


def part1(puzzle: str) -> int:
    low_pulses = 0
    high_pulses = 0
    modules = {mod.name: mod for mod in parse_input(puzzle)}
    sources = {name: [] for name in modules} | {"output": [], "rx": []}
    for module in modules.values():
        for output in module.outputs:
            sources[output].append(module.name)
    for module in modules.values():
        if isinstance(module, Conjunction):
            module.inputs = {source: False for source in sources[module.name]}
    for _ in range(1000):
        # print("---", low_pulses, high_pulses)
        # time to blast off 1000 pulses
        queue = deque([(modules["button"], False, "hand")])
        while queue:
            # print(queue, high_pulses, low_pulses)
            mod, incoming, source = queue.popleft()
            output = mod.receive_pulse(value=incoming, source=source)
            # print(mod, incoming, source, mod.outputs)
            if output is not None:
                for dest in mod.outputs:
                    if output is True:
                        high_pulses += 1
                    else:
                        low_pulses += 1
                    # print(
                    #     mod.name,
                    #     f'-{"low" if not output else "high"}->',
                    #     dest,
                    #     (low_pulses, high_pulses),
                    # )
                    try:
                        queue.append((modules[dest], output, mod.name))
                    except KeyError:
                        if dest in ["output", "rx"]:
                            # I'm sure this will come up in part 2
                            pass
                        else:
                            raise

    return low_pulses * high_pulses


def part2(puzzle: str) -> int:
    modules = {mod.name: mod for mod in parse_input(puzzle)}
    modules["rx"] = Machine(name="rx", outputs=[])
    sources = {name: [] for name in modules} | {"output": []}
    for module in modules.values():
        for output in module.outputs:
            sources[output].append(module.name)
    assert len(sources["rx"]) == 1
    # we want to track when we get a high pulse from any of the inputs to
    # the sole input that feeds rx
    watched = {source: 0 for source in sources[sources["rx"][0]]}
    for module in modules.values():
        if isinstance(module, Conjunction):
            module.inputs = {source: False for source in sources[module.name]}
    turns = 0
    try:
        while True:
            if not turns % 10000:
                print("---", turns, watched, end="\r")
            # if we've seen a high pulse from all our inputs, the answer
            # is the LCM of all the turns on which the input has been triggered
            if all(watched.values()):
                print(watched)
                return lcm(*watched.values())
            # time to blast off until rx turns on
            queue = deque([(modules["button"], False, "hand")])
            turns += 1
            while queue:
                # print(queue, high_pulses, low_pulses)
                mod, incoming, source = queue.popleft()
                output = mod.receive_pulse(value=incoming, source=source)
                # print(mod, incoming, source, mod.outputs)
                if output is not None:
                    if output and mod.name in watched and not watched[mod.name]:
                        # this is one of our key inputs
                        watched[mod.name] = turns
                    for dest in mod.outputs:
                        # print(
                        #     mod.name,
                        #     f'-{"low" if not output else "high"}->',
                        #     dest,
                        # )
                        try:
                            queue.append((modules[dest], output, mod.name))
                        except KeyError:
                            if dest == "output":
                                # surprisingly this didn't turn up in part 2
                                pass
                            else:
                                raise
    except EndOfTheSim:
        print()
        return turns


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 4250 * 2750, part_1_result
    # this helped me see what was going on
    # output = ["digraph {"]
    # for line in REAL_INPUT.splitlines():
    #     output.append(
    #         " " * 4
    #         + (
    #             line
    #             if not line.startswith(
    #                 (
    #                     "%",
    #                     "&",
    #                 )
    #             )
    #             else line[1:]
    #         )
    #     )
    # output.append("}")
    # Path("day20-viz.txt").write_text("\n".join(output))
    print(part1(REAL_INPUT))
    print(part2(REAL_INPUT))


class EndOfTheSim(Exception):
    pass


if __name__ == "__main__":
    main()
