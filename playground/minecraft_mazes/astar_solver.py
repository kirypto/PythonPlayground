import heapq
from dataclasses import dataclass
from functools import total_ordering
from typing import List, Optional, Tuple, Set, Dict

Coord = Tuple[int, int]


@total_ordering
@dataclass
class _State:
    precursor: "Optional[_State]"
    pos: Coord
    cost_so_far: int
    estimated_remaining: float

    def __eq__(self, other) -> bool:
        if not isinstance(other, _State):
            raise ValueError(f"'other' was not a {_State.__name__}, instead was {type(other).__name__}")
        return self.cost_so_far + self.estimated_remaining == other.cost_so_far + other.estimated_remaining

    def __hash__(self) -> int:
        return hash((self.precursor, self.pos, self.cost_so_far, self.estimated_remaining))

    def __lt__(self, other) -> bool:
        if not isinstance(other, _State):
            raise ValueError(f"'other' was not a {_State.__name__}, instead was {type(other).__name__}")
        return self.cost_so_far + self.estimated_remaining < other.cost_so_far + other.estimated_remaining


def _main():
    is_traversable_map, start_position, target = _read_problem_input()

    path = _solve_with_a_star(is_traversable_map, start_position, target)

    _print_problem_output(path)


def _solve_with_a_star(is_traversable_map: List[List[bool]], start_position: Coord, target: Coord) -> List[Coord]:
    initial_state = _State(None, start_position, 0, _estimate_remaining(start_position, target))

    state_min_heap = [initial_state]
    heapq.heapify(state_min_heap)
    visited: Set[Coord] = set()
    finishing_state = None

    while state_min_heap:
        curr_state = heapq.heappop(state_min_heap)
        if curr_state.pos == target:
            finishing_state = curr_state
            break

        visited.add(curr_state.pos)
        for successor in _generate_successors(is_traversable_map, curr_state, visited, target):
            heapq.heappush(state_min_heap, successor)

    if finishing_state is None:
        raise ValueError("Could not find path")

    path: List[Coord] = []
    curr_state = finishing_state
    while curr_state is not None:
        path.insert(0, curr_state.pos)
        curr_state = curr_state.precursor

    return path


def _print_problem_output(path: List[Coord]) -> None:
    _direction_name_by_coord_delta: Dict[Coord, str] = {
        (1, 0): "south",
        (-1, 0): "north",
        (0, 1): "east",
        (0, -1): "west",
    }

    for index in range(len(path) - 1):
        curr_pos_row, curr_pos_col = path[index]
        next_pos_row, next_pos_col = path[index + 1]
        position_delta = next_pos_row - curr_pos_row, next_pos_col - curr_pos_col
        print(_direction_name_by_coord_delta[position_delta])
    print("fin")


def _read_problem_input() -> Tuple[List[List[bool]], Coord, Coord]:
    num_rows = int(input())
    num_cols = int(input())
    is_traversable_map: List[List[bool]] = []
    for _ in range(num_rows):
        map_line = input()
        if len(map_line) != num_cols:
            raise ValueError(f"Map line did not have expected length. Expected {num_cols}, was {len(map_line)}")
        is_traversable_map.append([char == "0" for char in map_line])
    start_input = input().split()
    start_position = (int(start_input[0]), int(start_input[1]))
    target_input = input().split()
    target = (int(target_input[0]), int(target_input[1]))
    return is_traversable_map, start_position, target


def _estimate_remaining(position: Coord, target: Coord) -> float:
    target_row, target_col = target
    position_row, position_col = position
    return abs(target_row - position_row) + abs(target_col - position_col)


def _generate_successors(
        is_traversable_map: List[List[bool]], state: _State, visited: Set[Coord], target: Coord
) -> Set[_State]:
    pos_row, pos_col = state.pos
    successor_positions = {
        (row, col)
        for row, col in [
            (pos_row + 1, pos_col),
            (pos_row - 1, pos_col),
            (pos_row, pos_col + 1),
            (pos_row, pos_col - 1),
        ]
        if (0 <= row <= len(is_traversable_map)
            and 0 <= col <= len(is_traversable_map[0])
            and is_traversable_map[row][col]
            and (row, col) not in visited)
    }
    return {
        _State(state, successor_position, state.cost_so_far + 1, _estimate_remaining(successor_position, target))
        for successor_position in successor_positions
    }


if __name__ == "__main__":
    _main()
