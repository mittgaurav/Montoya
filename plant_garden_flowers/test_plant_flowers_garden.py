# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 18:16:50 2024

@author: gaurav
"""
import pytest
from plant_flowers_garden import plant_flowers, read_garden_file, read_flowers_file


@pytest.mark.parametrize("garden_file, flowers_file, expected", [
    ("garden0.txt", "flowers0.txt", True),
    ("garden1.txt", "flowers1.txt", True),
    ("garden2.txt", "flowers2.txt", True),
    ("garden3.txt", "flowers3.txt", True),
    ("garden4.txt", "flowers4.txt", True),
    ("garden5.txt", "flowers5.txt", False),
    ("garden6.txt", "flowers6.txt", True),
    ("garden7.txt", "flowers7.txt", True),
])
def test_plant_flowers(garden_file, flowers_file, expected):
    folder = r"instructions - python"

    garden = read_garden_file(f"{folder}/{garden_file}")
    flowers = read_flowers_file(f"{folder}/{flowers_file}")

    garden_str = "\n".join(["".join(row) for row in garden])

    result = plant_flowers(garden, flowers)

    assert result == expected, f"{flowers}\n{garden_str}"


if __name__ == "__main__":
    pytest.main()
