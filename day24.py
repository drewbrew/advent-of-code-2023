"""Day 24: hailstones coming crashing"""
import decimal
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Self

import numpy as np

TEST_INPUT = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

REAL_INPUT = Path("day24.txt").read_text()
decimal.getcontext().prec = 50


@dataclass
class Hailstone:
    px: decimal.Decimal
    py: decimal.Decimal
    pz: decimal.Decimal
    vx: decimal.Decimal
    vy: decimal.Decimal
    vz: decimal.Decimal
    adjusted_x: decimal.Decimal = decimal.Decimal(0)
    adjusted_y: decimal.Decimal = decimal.Decimal(0)
    adjusted_z: decimal.Decimal = decimal.Decimal(0)

    def __str__(self) -> str:
        return f"{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}"

    def __eq__(self, __value: object) -> bool:
        return (
            self.px == __value.px
            and self.py == __value.py
            and self.pz == __value.pz
            and self.vz == __value.vz
            and self.vy == __value.vy
            and self.vx == __value.vx
        )

    def adjust(
        self,
        x: int | decimal.Decimal,
        y: int | decimal.Decimal,
        z: int | decimal.Decimal,
    ) -> Self:
        return self.__class__(
            px=self.px,
            py=self.py,
            pz=self.pz,
            vx=self.vx - (x - self.adjusted_x),
            vy=self.vy - (y - self.adjusted_y),
            vz=self.vz - (z - self.adjusted_z),
            adjusted_x=x,
            adjusted_y=y,
            adjusted_z=z,
        )

    def get_time(
        self, point: tuple[decimal.Decimal, decimal.Decimal]
    ) -> decimal.Decimal:
        if not self.vx:
            return (point[1] - self.py) / self.vy
        return (point[0] - self.px) / self.vx

    def get_z_at_intersection(
        self, other: Self, intersection: tuple[decimal.Decimal, decimal.Decimal]
    ) -> decimal.Decimal | None:
        """given an intersection and another hailstone, find where they'll meet"""
        # now we KNOW: z = pz_i + t_i*(vz_i-aZ)   [t = (inter[0]-px_i)/(vx_i)]
        #              z = pz_j + t_j*(vz_j-aZ)
        # (pz_i - pz_j + t_i*vz_i - t_j*vz_j)/(t_i - t_j) =  aZ
        my_time = self.get_time(intersection)
        other_time = other.get_time(intersection)
        if my_time == other_time:
            assert self.pz + my_time * self.vz == other.pz + other_time * other.vz
            return None
        return (self.pz - other.pz + my_time * self.vz - other_time * other.vz) / (
            my_time - other_time
        )

    @property
    def slope_xy(self):
        if self.vx == 0:
            return decimal.Decimal("inf")
        return self.vy / self.vx

    def intersection_on_xy(
        self, other: Self
    ) -> tuple[decimal.Decimal, decimal.Decimal] | None:
        # returns None, if parallel / intersect in a past
        if self.slope_xy == other.slope_xy:
            return None
        if self.slope_xy == float("inf"):  # self is vertical
            x1 = self.px
            y1 = other.slope_xy * (x1 - other.px) + other.py
        elif other.slope_xy == float("inf"):  # other is vertical
            x1 = other.px
            y1 = self.slope_xy * (x1 - self.px) + self.py
        else:
            # y - y1 = m1 * ( x - x1 ) reduced to solve for x
            x1 = (
                self.py - other.py - self.px * self.slope_xy + other.px * other.slope_xy
            ) / (other.slope_xy - self.slope_xy)
            y1 = self.py + self.slope_xy * (x1 - self.px)
        x1, y1 = x1.quantize(decimal.Decimal(".1")), y1.quantize(decimal.Decimal(".1"))
        # intY = round(intY)

        self_intersection_in_future = np.sign(x1 - self.px) == np.sign(self.vx)
        other_intersection_in_future = np.sign(x1 - other.px) == np.sign(other.vx)
        if not (self_intersection_in_future and other_intersection_in_future):
            return None
        return (x1, y1)

    def __hash__(self) -> int:
        return hash((self.px, self.py, self.pz, self.vx, self.vy, self.vz))


def parse_input(puzzle: str) -> list[Hailstone]:
    return [
        Hailstone(*(decimal.Decimal(i) for i in line.replace(" @", ",").split(", ")))
        for line in puzzle.splitlines()
    ]


def part1(puzzle: str, min_xy: int, max_xy: int) -> int:
    """Find all intersections of nodes in the area"""
    stones = parse_input(puzzle=puzzle)
    intersections = 0
    for stone1, stone2 in combinations(stones, r=2):
        if (stone1.vx == stone2.vx and stone1.vy == stone2.vy) or (
            stone1.vx / stone1.vy == stone2.vx / stone2.vy
        ):
            # parallel lines
            print(f"{stone1} and {stone2} are parallel")
            continue

        if intersection := stone1.intersection_on_xy(stone2):
            x1, y1 = intersection
        else:
            # no intersection
            continue
        # is it within range?
        if x1 < min_xy or x1 > max_xy or y1 < min_xy or y1 > max_xy:
            print(f"{stone1} and {stone2} collide but out of range {x1, y1}")
            continue

        print(stone1, stone2, "collide at", x1, y1)
        intersections += 1
    return intersections


def part2(puzzle: str) -> int:
    stones = parse_input(puzzle=puzzle)
    n = 0
    while True:
        print(".", end="")
        for x in range(n + 1):
            y = n - x
            for negate_x in (-1, 1):
                for negate_y in (-1, 1):
                    adjusted_x = x * negate_x
                    adjusted_y = y * negate_y
                    stone1 = stones[0]
                    stones[0] = stone1.adjust(adjusted_x, adjusted_y, 0)
                    stone1 = stones[0]
                    intersection = None
                    for index, stone2 in enumerate(stones[1:], start=1):
                        stone2 = stone2.adjust(adjusted_x, adjusted_y, 0)
                        stones[index] = stone2
                        intersection_candidate = stone1.intersection_on_xy(stone2)
                        if intersection_candidate is None:
                            break
                        if intersection is None:
                            intersection = intersection_candidate
                            continue
                        if intersection_candidate != intersection:
                            break
                    if (
                        intersection_candidate is None
                        or intersection_candidate != intersection
                    ):
                        continue
                    # print(
                    #     f"maybe a winner? v=<{adjusted_x},{adjusted_y},?>"
                    #     + f", p=<{intersection[0]},{intersection[1]},?>"
                    # )
                    adjusted_z = None
                    stone1 = stones[0]
                    for stone2 in stones[1:]:
                        new_z = stone1.get_z_at_intersection(stone2, intersection)
                        if adjusted_z is None:
                            # print(f'first aZ is {aZ} from {H2}')
                            adjusted_z = new_z
                            continue
                        elif new_z != adjusted_z:
                            # print(f"invalidated by {new_z} from {stone1}")
                            break
                    if adjusted_z == new_z:
                        stone1 = stones[0]
                        z = stone1.pz + stone1.get_time(intersection) * (
                            stone1.vz - adjusted_z
                        )
                        # print(
                        #     f"yay victory v=<{adjusted_x},{adjusted_y},{adjusted_z}>, p=<{intersection[0]},{intersection[1]},{z}>, s={z+intersection[0]+intersection[1]}"
                        # )
                        print("")
                        return int(z + intersection[0] + intersection[1])

        n += 1


def main():
    part_1_result = part1(TEST_INPUT, 7, 27)
    assert part_1_result == 2, part_1_result
    print(part1(REAL_INPUT, 200000000000000, 400000000000000))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 47, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
