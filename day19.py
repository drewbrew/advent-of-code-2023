"""day 19: aplenty"""
from itertools import combinations_with_replacement
from pathlib import Path
from dataclasses import dataclass

TEST_INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

REAL_INPUT = Path("day19.txt").read_text()

from celery import Celery

import day19_generated_test as day19_generated

app = Celery("day19", broker="redis://localhost", backend="redis://localhost")


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def score(self) -> int:
        return self.x + self.m + self.a + self.s

    def __str__(self) -> str:
        return f"x={self.x},m={self.m},a={self.a},s={self.s}"


@dataclass
class Workflow:
    name: str
    conditions: list[str]

    def to_python(self) -> str:
        """Convert the instructions into a python function"""
        func_name = self.name if self.name != "in" else "in_"
        output = [f"def {func_name}(part) -> str:"]
        for instruction in self.conditions:
            if ":" not in instruction:
                if instruction in "AR":
                    output.append(f'    return "{instruction}"')
                else:
                    output.append(f"    return {instruction}(part)")
                continue
            condition, destination = instruction.split(":")
            if "<" in condition:
                attr, amount = condition.split("<")
                amount = int(amount)
                output.append(
                    f"    if part.{attr} < {amount}:",
                )
            elif ">" in condition:
                attr, amount = condition.split(">")
                amount = int(amount)
                output.append(
                    f"    if part.{attr} < {amount}:",
                )
            else:
                raise ValueError(f"unknown instruction {instruction}")
            if destination in "AR":
                output.append(f'        return "{destination}"')
            else:
                output.append(f"        return {destination}(part)")
        return "\n".join(output)

    def run_through_workflow(self, part: Part) -> str:
        """Run the part through the workflow

        Returns A, R, or the name of a new workflow
        """
        # print('running part', part, 'through', self.name)
        for instruction in self.conditions:
            # print('instruction', instruction)
            if ":" not in instruction:
                # the end
                # print('end', instruction)
                return instruction
            condition, destination = instruction.split(":")
            if "<" in condition:
                attr, amount = condition.split("<")
                amount = int(amount)
                if getattr(part, attr) < amount:
                    # print('<', amount, True)
                    return destination
                # print('<', amount, False)
            elif ">" in condition:
                attr, amount = condition.split(">")
                amount = int(amount)
                if getattr(part, attr) > amount:
                    # print('>', amount, True)
                    return destination
                # print('>', amount, False)
            else:
                raise ValueError(f"unknown instruction {instruction}")


def parse_input(puzzle: str) -> tuple[list[Workflow], list[Part]]:
    raw_flows, raw_parts = puzzle.split("\n\n")
    parts = []
    for p in raw_parts.splitlines():
        # print(p)
        part_dict = {}
        for group in p[1:-1].split(","):
            try:
                attr, val = group.split("=")
            except ValueError:
                if not group:
                    continue
                print(group)
                raise
            part_dict[attr] = int(val)
        # print(part_dict)
        parts.append(Part(**part_dict))
    workflows = []
    for f in raw_flows.splitlines():
        name, instructions = f[:-1].split("{")
        workflows.append(Workflow(name=name, conditions=instructions.split(",")))
    return workflows, parts


def part1(puzzle: str) -> int:
    workflows, parts = parse_input(puzzle)
    score = 0
    flows = {flow.name: flow for flow in workflows}
    for part in parts:
        # print(part)
        flow = flows["in"]
        flow_name = flow.name
        while True:
            flow_name = flow.run_through_workflow(part)
            # print(flow_name)
            try:
                flow = flows[flow_name]
            except KeyError:
                break
        if flow_name == "A":
            # print('accepted', part)
            score += part.score
        # else:
        #     print('rejected', part)
    return score


def part2(puzzle: str) -> int:
    """How many possible workflows can be accepted?"""
    workflows, _ = parse_input(puzzle)
    if puzzle == TEST_INPUT:
        Path("day19_generated_test.py").write_text(
            "\n\n".join(flow.to_python() for flow in workflows)
        )
    else:
        Path("day19_generated.py").write_text(
            "\n\n".join(flow.to_python() for flow in workflows)
        )
    task = do_part_2.chunks(
        combinations_with_replacement(range(1, 4001), 3),
        100,
    ).apply_async()
    print("waiting")
    result = task.get()
    accepted = 0
    for line in result:
        accepted += sum(line)
    return accepted


@app.task
def do_part_2(x: int, m: int, a: int, test: bool = False) -> int:
    """do part 2 for a batch of 1000"""
    # print(f'{x=},{m=},{a=}')
    return sum(day19_generated.in_(Part(x, m, a, s)) == "A" for s in range(1, 4001))


def main():
    part_1_score = part1(TEST_INPUT)
    assert part_1_score == 19114, part_1_score
    print(part1(REAL_INPUT))
    # part_2_score = part2(TEST_INPUT)
    # assert part_2_score == 167409079868000, part_2_score
    print("part 2: go")
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
