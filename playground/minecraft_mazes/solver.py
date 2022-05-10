from typing import List


def _main():
    num_rows = int(input())
    num_cols = int(input())
    traversable_map: List[List[bool]] = []
    for _ in range(num_rows):
        map_line = input()
        if len(map_line) != num_cols:
            raise ValueError("Map line did not have expected length")
        traversable_map.append([char == "0" for char in map_line])

    start_pos_row, start_pos_col = [int(char) for char in input().split()]
    end_pos_row, end_pos_col = [int(char) for char in input().split()]
    print("fin")


if __name__ == "__main__":
    _main()
