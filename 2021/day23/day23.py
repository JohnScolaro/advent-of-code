"""
Problem 23 of the Advent-of-Code 2021

I just put in the positions of the bugs manually. No reading of inputs here.
"""

from typing import Dict, List, Optional, Set, Tuple
import queue

YIELD_DISTANCE_FROM_ROOM_0_EXIT = {0: 2, 1: 1, 2: 1, 3: 3, 4: 5, 5: 7, 6: 8}
YIELD_DISTANCE_FROM_ROOM_1_EXIT = {0: 4, 1: 3, 2: 1, 3: 1, 4: 3, 5: 5, 6: 6}
YIELD_DISTANCE_FROM_ROOM_2_EXIT = {0: 6, 1: 5, 2: 3, 3: 1, 4: 1, 5: 3, 6: 4}
YIELD_DISTANCE_FROM_ROOM_3_EXIT = {0: 8, 1: 7, 2: 5, 3: 3, 4: 1, 5: 1, 6: 2}
YIELD_DISTANCES_FOR_ROOM = [
    YIELD_DISTANCE_FROM_ROOM_0_EXIT,
    YIELD_DISTANCE_FROM_ROOM_1_EXIT,
    YIELD_DISTANCE_FROM_ROOM_2_EXIT,
    YIELD_DISTANCE_FROM_ROOM_3_EXIT,
]

Space = Optional[int]
Room = Tuple[Space, ...]
Rooms = Tuple[Room, Room, Room, Room]
YieldPosition = Tuple[Space, Space, Space, Space, Space, Space, Space]
State = Tuple[Rooms, YieldPosition]
Cost = int


class CostState:
    def __init__(self, cost: Cost, state: State) -> None:
        self.cost = cost
        self.state = state

    def __hash__(self) -> int:
        return hash((self.cost, self.state))

    def __repr__(self) -> str:
        return f"CostState(cost={self.cost}, state={self.state}"

    def __eq__(self, __o: object) -> bool:
        if self.cost == __o.cost and self.state == __o.state:
            return True

    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost


def part_a() -> int:
    yield_positions = (None, None, None, None, None, None, None)
    rooms = ((1, 0), (2, 3), (1, 2), (3, 0))
    state = (rooms, yield_positions)

    from_states = {}
    minimum_cost_state = get_minimum_cost(state, from_states)

    path = reconstruct_states(from_states, state, minimum_cost_state.state)
    for p in path:
        print(p)

    return minimum_cost_state.cost


def part_b() -> int:
    yield_positions = (None, None, None, None, None, None, None)
    rooms = ((3, 3, 3, 2), (0, 2, 1, 0), (2, 1, 0, 1), (3, 0, 2, 1))
    state = (rooms, yield_positions)

    from_states = {}
    minimum_cost_state = get_minimum_cost(state, from_states)

    path = reconstruct_states(from_states, state, minimum_cost_state.state)
    for p in path:
        print(p)

    return minimum_cost_state.cost


def reconstruct_states(from_states, initial_state: State, final_state: State) -> List[State]:
    path = []
    cur_state = final_state
    while True:
        path.append(cur_state)
        if cur_state == initial_state:
            break
        cur_state = from_states[cur_state]
    return reversed(path)


def get_minimum_cost(state: State, from_states: Dict[State, State]) -> int:
    priority_queue = queue.PriorityQueue()
    priority_queue.put(CostState(cost=0, state=state))

    lowest_cost_to_achieve_state = {}

    highest_energy_explored = 0

    while True:
        cost_state = priority_queue.get()
        cost = cost_state.cost
        state = cost_state.state
        lowest_cost_to_achieve_state[state] = cost

        if cost > highest_energy_explored:
            highest_energy_explored = cost
            print(f"{highest_energy_explored}")

        if everyone_home(state):
            return cost_state

        next_states_via_yield: Set[CostState] = get_next_states_from_yield(cost_state)
        next_states_via_return_home: Set[CostState] = get_next_states_from_return_home(cost_state)

        for new_cost_state in next_states_via_yield.union(next_states_via_return_home):
            new_cost = new_cost_state.cost
            new_state = new_cost_state.state
            if (new_state not in lowest_cost_to_achieve_state) or (new_cost <= lowest_cost_to_achieve_state[new_state]):
                from_states[new_state] = state
                priority_queue.put(new_cost_state)


def everyone_home(state: State) -> bool:
    rooms = state[0]
    num_rooms = len(rooms)
    room_depth = len(rooms[0])
    return all(rooms[i][j] == i for i in range(num_rooms) for j in range(room_depth))


def get_next_states_from_yield(cost_state: CostState) -> Set[CostState]:
    """
    Returns a set of CostStates from all the valid moves where a bug moves from
    a room to a yield state.
    """
    cost_states: Set[CostState] = set()
    active_set = get_active_set(cost_state.state)
    for room_num, room_position in active_set:
        positions_to_yield_to = get_positions_we_can_yield_to(room_num, cost_state.state[1])
        for position_to_yield_to in positions_to_yield_to:
            cost_states.add(move_active_bug_to_yield(cost_state, (room_num, room_position), position_to_yield_to))
    return cost_states


def get_next_states_from_return_home(cost_state: CostState) -> Set[CostState]:
    cost_states: Set[CostState] = set()
    for i in range(7):
        if can_yielder_go_home(cost_state.state, i):
            cost_states.add(move_yielder_home(cost_state, i))
    return cost_states


def get_active_set(state: State) -> Set[Tuple[int, int]]:
    """
    Returns a set of (room, location in room) tuples of the bugs that are
    'active'.

    An active bug is one that can possibly move. IE: One that isn't blocked,
    and isn't in it's final position (IE: Everything behind it is in it's final
    position).
    """
    active_positions = set()
    rooms = state[0]
    num_rooms = len(rooms)
    room_depth = len(rooms[0])
    for i in range(num_rooms):
        if not room_is_complete(rooms, i):
            for position in range(room_depth):
                if rooms[i][position] is not None:
                    # Check if it's in it's final position
                    if not all(bug == i for bug in rooms[i][position:room_depth]):
                        active_positions.add((i, position))
                        break
    return active_positions


def can_yielder_go_home(state: State, current_yield_position: int) -> bool:
    # Is the destination room free? IE: Is the room empty, or contains only
    # bugs into their final position
    rooms = state[0]
    yield_positions = state[1]
    destination_room = yield_positions[current_yield_position]
    if destination_room is None:
        return False

    if not room_is_complete(rooms, destination_room):
        return False

    if am_blocked_from_room(yield_positions, current_yield_position):
        return False
    return True


def am_blocked_from_room(yield_positions: YieldPosition, current_yield_position: int) -> bool:
    dest_room_num = yield_positions[current_yield_position]
    dest_room_num += 1.5
    possible_blockers = {
        i
        for i in range(7)
        if (i < max(current_yield_position, dest_room_num)) and i > min(current_yield_position, dest_room_num)
    }
    return any(yield_positions[possible_blocker] is not None for possible_blocker in possible_blockers)


def room_is_complete(rooms: Rooms, room_num: int) -> bool:
    return all((bug_value is None) or (bug_value == room_num) for bug_value in rooms[room_num])


def move_yielder_home(cost_state: CostState, yield_index_to_move: int) -> CostState:
    """
    Returns the CostState after executing a move.
    """
    rooms = list(map(list, cost_state.state[0]))
    yield_positions = list(cost_state.state[1])

    bug = yield_positions[yield_index_to_move]
    yield_positions[yield_index_to_move] = None
    deepest_room_pos = max(i for i, room in enumerate(rooms[bug]) if room is None)
    rooms[bug][deepest_room_pos] = bug
    distance = YIELD_DISTANCES_FOR_ROOM[bug][yield_index_to_move] + 1 + deepest_room_pos
    additional_cost = distance * (10 ** bug)
    return CostState(cost=cost_state.cost + additional_cost, state=(tuple(map(tuple, rooms)), tuple(yield_positions)))


def move_active_bug_to_yield(
    cost_state: CostState,
    room_position: Tuple[int, int],
    position_to_yield_to: int,
) -> CostState:
    """
    Returns the new CostState after executing a move.
    """
    rooms = list(map(list, cost_state.state[0]))
    yield_positions = list(cost_state.state[1])

    bug = rooms[room_position[0]][room_position[1]]
    yield_positions[position_to_yield_to] = bug
    rooms[room_position[0]][room_position[1]] = None
    distance = YIELD_DISTANCES_FOR_ROOM[room_position[0]][position_to_yield_to] + 1 + room_position[1]
    additional_cost = distance * (10 ** bug)
    return CostState(cost=cost_state.cost + additional_cost, state=(tuple(map(tuple, rooms)), tuple(yield_positions)))


def get_positions_we_can_yield_to(room_num: int, yield_positions: YieldPosition) -> Set[int]:
    mod_room_pos = room_num + 1.5
    max_full_yield_below = list(i for i in range(7) if yield_positions[i] is not None and i < mod_room_pos)
    max_full_yield_below = max(max_full_yield_below or [-1])
    min_full_yield_above = list(i for i in range(7) if yield_positions[i] is not None and i > mod_room_pos)
    min_full_yield_above = min(min_full_yield_above or [7])

    return set(i for i in range(7) if (i < min_full_yield_above) and (i > max_full_yield_below))


if __name__ == "__main__":
    print(f"Part A: {part_a()}")
    print(f"Part B: {part_b()}")
