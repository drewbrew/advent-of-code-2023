from dataclasses import dataclass
from itertools import batched
from pathlib import Path


REAL_INPUT = Path("day05.txt").read_text()

TEST_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class Mapping:
    def __init__(self, ranges: list[tuple[int, int, int]] | None = None):
        self.ranges = ranges or []

    def add_range(self, source_start: int, destination_start: int, range_: int):
        self.ranges.append((source_start, destination_start, range_))

    def __getitem__(self, obj: int) -> int:
        for source_start, dest_start, range_ in self.ranges:
            if obj in range(source_start, source_start + range_ + 1):
                offset = obj - source_start
                return dest_start + offset
        return obj

    def __repr__(self):
        return f"{self.__class__.__name__}({self.ranges})"


@dataclass
class Garden:
    seeds: list[int]
    seed_to_soil: Mapping
    soil_to_fertilizer: Mapping
    fertilizer_to_water: Mapping
    water_to_light: Mapping
    light_to_temperature: Mapping
    temperature_to_humidity: Mapping
    humidity_to_location: Mapping

    def next_seed(self, part2: bool = False):
        if not part2:
            iterator = iter(self.seeds)
            while True:
                try:
                    yield next(iterator)
                except StopIteration:
                    return
        else:
            for start, length in batched(self.seeds, n=2):
                for seed in range(start, start + length + 1):
                    yield seed


def parse_input(puzzle_input: str) -> Garden:
    seed_line, *groups = puzzle_input.split("\n\n")
    _, seed_list = seed_line.split(": ")
    seeds = [int(i) for i in seed_list.split()]
    kwargs = {"seeds": seeds}
    for group in groups:
        header, *lines = group.splitlines()
        map_name = header.split()[0].replace("-", "_")
        kwargs[map_name] = Mapping()
        for line in lines:
            destination_start, source_start, range_ = [int(i) for i in line.split()]
            kwargs[map_name].add_range(source_start, destination_start, range_)
    print(kwargs)
    garden = Garden(**kwargs)
    return garden


def part1(puzzle_input: str, part2: bool = False):
    garden = parse_input(puzzle_input)
    if puzzle_input == TEST_INPUT:
        expected = {79: 81, 14: 14, 55: 57, 13: 13}
        for seed, soil in expected.items():
            assert garden.seed_to_soil[seed] == soil, (
                seed,
                soil,
                garden.seed_to_soil[seed],
            )
    min_location = 10_000_000_000
    if part2:
        total = sum(garden.seeds[i] for i in range(1, len(garden.seeds), 2))
        print("processing " f"{total}" " seeds")
        seeds_processed = 0
    for seed in garden.next_seed(part2=part2):
        soil = garden.seed_to_soil[seed]
        fertilizer = garden.soil_to_fertilizer[soil]
        water = garden.fertilizer_to_water[fertilizer]
        light = garden.water_to_light[water]
        temperature = garden.light_to_temperature[light]
        humidity = garden.temperature_to_humidity[temperature]
        location = garden.humidity_to_location[humidity]
        if part2:
            seeds_processed += 1
            if not seeds_processed % 100_000:
                print(
                    f"processed {seeds_processed} "
                    f"({seeds_processed * 100 / total:.4f}%), {min_location=}",
                    end="\r",
                )
        min_location = min(min_location, location)
    print()
    return min_location


def main():
    part_1_test = part1(TEST_INPUT)
    assert part_1_test == 35, part_1_test
    print(part1(REAL_INPUT))
    part_2_test = part1(TEST_INPUT, True)
    assert part_2_test == 46, part_2_test
    print(part1(REAL_INPUT, True))


if __name__ == "__main__":
    main()
