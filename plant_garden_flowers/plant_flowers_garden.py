# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:04:52 2024

@author: gaurav
"""
import os
import argparse


def read_garden_file(filename: str) -> list[list[str]]:
    """
    Read garden file and return map of garden
    as a list of list of 'X' and ' '

    throws FileNotFoundError if file not found
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Garden file {filename} not found")

    garden = []
    with open(filename, "r") as f:
        for line in f:
            garden.append(list(line.strip()))

    return garden


def read_flowers_file(filename: str) -> list[tuple[str, int, int]]:
    """
    Read flower file and return the tuple of
    each kind of flower and required number,
    along with minimum distance between them

    throws FileNotFoundError if file not found
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Flower file {filename} not found")

    flowers = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            assert len(parts) == 3, f"Invalid flower line: {line}"
            flower_type, count, distance = parts
            assert flower_type != "X", "Flower type X can't be same as the wall"
            flowers.append((flower_type, int(count), int(distance)))

    return flowers


def is_flower_allowed(
        garden: list[str],
        flower_type: str,
        distance: int,
        x: int,
        y: int,
) -> bool:
    """
    Is given (x, y) location allowed to have
    a flower type given the garden constraint
    """
    if garden[x][y] != " ":
        return False

    rows = len(garden)
    cols = len(garden[0])
    for i in range(rows):
        for j in range(cols):
            if garden[i][j] == flower_type and abs(x - i) + abs(y - j) < distance:
                return False
    return True


def plant_flowers(
        garden: list[str],
        flowers: list[tuple[str, int, int]],
) -> list[str]:
    """
    Plant flowers in the garden and return
    success True/False; i.e. goal.
    Side-effect: update garden with flowers
    """
    # Sort flowers by distance in descending order
    flowers = sorted(flowers, key=lambda x: x[2], reverse=True)
    rows = len(garden)
    cols = len(garden[0])

    def internal(index):
        if index == len(flowers):
            # No more flower types yay
            return True

        flower_type, count, distance = flowers[index]

        def backtrack():
            nonlocal count
            if count == 0:
                # All done for this type; now, try the next type
                # In case the next type is not planted correctly
                # return False and retry current one
                return internal(index + 1)

            for i in range(rows):
                for j in range(cols):
                    if is_flower_allowed(garden, flower_type, distance, i, j):
                        # Put type in current loc
                        garden[i][j] = flower_type
                        count -= 1

                        # print("---------", flower_type, count)
                        # for row in garden: print("".join(row))

                        if backtrack():
                            return True

                        # We are not able to place flowers
                        # So, undo this step and retry
                        count += 1
                        garden[i][j] = " "
            return False

        return backtrack()

    return internal(0)


def main(garden_file: str, flowers_file: str):
    garden = read_garden_file(garden_file)
    flowers = read_flowers_file(flowers_file)

    print(f"Garden: {garden_file}, Flowers: {flowers_file}")
    for flower in flowers:
        print(flower)

    if plant_flowers(garden, flowers):
        print("====Design for flowers in garden====")
    else:
        print("====No valid design====")

    for row in garden:
        print("".join(row))


# python plant_flowers_garden.py "instructions - python\garden0.txt" "instructions - python\flowers0.txt"
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Plant flowers in garden")
    parser.add_argument("garden_file", type=str, help="Garden layout file")
    parser.add_argument("flowers_file", type=str, help="Flower details file")

    args = parser.parse_args()

    main(args.garden_file, args.flowers_file)
