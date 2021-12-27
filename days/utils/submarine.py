import csv
import numpy as np
from typing import Optional, Dict, List, Union, Tuple
from tqdm import tqdm


class Submarine:
    def __init__(self, file_path: str = None, debug: bool = False) -> None:
        self.file_path = file_path
        self.debug = debug


class MoveSub(Submarine):
    def __init__(
        self,
        file_path: str,
        initial_position: Optional[Dict[str, int]] = None,
    ) -> None:
        self.position = initial_position or self._get_new_position()
        super().__init__(file_path=file_path)

    @staticmethod
    def _get_new_position() -> Dict[str, int]:
        return {"horizontal": 0, "vertical": 0, "aim": 0}

    def _move(self, direction: str, magnitude: int) -> None:
        if direction == "down":
            self.position["aim"] += magnitude
        elif direction == "up":
            self.position["aim"] -= magnitude
        else:
            self.position["horizontal"] += magnitude
            self.position["vertical"] += magnitude * self.position["aim"]

    def _move_no_aim(self, direction: str, magnitude: int) -> None:
        if direction == "down":
            self.position["vertical"] += magnitude
        elif direction == "up":
            self.position["vertical"] -= magnitude
        else:
            self.position["horizontal"] += magnitude

    def run_movement_no_aim(self):
        with open(self.file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                direction = row[0].split(" ")[0]
                magnitude = int(row[0].split(" ")[1])
                self._move_no_aim(direction, magnitude)
        print(f"position = {self.position}")
        print(
            f'horizontal * vertical = {self.position["horizontal"] * self.position["vertical"]}'
        )

    def run_movement(self):
        with open(self.file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                direction = row[0].split(" ")[0]
                magnitude = int(row[0].split(" ")[1])
                self._move(direction, magnitude)
        print(f"position = {self.position}")
        print(
            f'horizontal * vertical = {self.position["horizontal"] * self.position["vertical"]}'
        )


class DiagnosticSub(Submarine):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path=file_path)

    def _get_power_consumption(self, data: list) -> Dict[str, Union[str, int]]:
        values = self._calculate_gamma_and_epsilon(data)
        gamma = values[0]
        epsilon = values[1]
        return {
            "gamma_bin": gamma,
            "gamma_dec": int(gamma, 2),
            "epsilon_bin": epsilon,
            "epsilon_dec": int(epsilon, 2),
            "power_consumption": int(gamma, 2) * int(epsilon, 2),
        }

    def _calculate_gamma_and_epsilon(self, data, tie_value=None) -> Tuple[str, str]:
        gamma = ""
        epsilon = ""
        for digit_row in data:
            if sum(digit_row) > len(digit_row) / 2:
                gamma += "1"
                epsilon += "0"
            elif sum(digit_row) < len(digit_row) / 2:
                gamma += "0"
                epsilon += "1"
            else:
                gamma += tie_value
                epsilon += "1" if tie_value == 0 else "0"
        return gamma, epsilon

    def _get_oxygen_generator(
        self, oxygen_generator_list, transposed_data, starting_value=0
    ):
        if len(oxygen_generator_list) == 1:
            oxygen_generator = "".join(
                list(map(lambda x: str(x), oxygen_generator_list[0]))
            )
            return oxygen_generator
        gamma_relevant = int(
            self._calculate_gamma_and_epsilon(transposed_data, tie_value="1")[0][
                starting_value
            ]
        )
        oxygen_generator_list = [
            i for i in oxygen_generator_list if i[starting_value] == gamma_relevant
        ]
        transposed_data = np.transpose(oxygen_generator_list)
        return self._get_oxygen_generator(
            oxygen_generator_list, transposed_data, starting_value + 1
        )

    def _get_co2_scrubber(self, co2_scrubber_list, transposed_data, starting_value=0):
        if len(co2_scrubber_list) == 1:
            co2_scrubber = "".join(list(map(lambda x: str(x), co2_scrubber_list[0])))
            return co2_scrubber
        epsilon_relevant = int(
            self._calculate_gamma_and_epsilon(transposed_data, tie_value="1")[1][
                starting_value
            ]
        )
        co2_scrubber_list = [
            i for i in co2_scrubber_list if i[starting_value] == epsilon_relevant
        ]
        transposed_data = np.transpose(co2_scrubber_list)
        return self._get_co2_scrubber(
            co2_scrubber_list, transposed_data, starting_value + 1
        )

    def run_diagnostic(self, operation: str) -> None:
        with open(self.file_path, "r") as f:
            reader = csv.reader(f)
            data = [[int(i) for i in row[0]] for row in reader]
        transposed_data = np.transpose(data)
        if operation == "power_consumption":
            power_consumption = self._get_power_consumption(transposed_data)
            self.gamma_binary = power_consumption["gamma_bin"]
            self.epsilon_binary = power_consumption["epsilon_bin"]
            print(power_consumption)
        elif operation == "life_support_rating":
            oxygen_generator = self._get_oxygen_generator(
                oxygen_generator_list=data, transposed_data=transposed_data
            )
            co2_scrubber = self._get_co2_scrubber(
                co2_scrubber_list=data, transposed_data=transposed_data
            )
            oxygen_generator_dec = int(oxygen_generator, 2)
            co2_scrubber_dec = int(co2_scrubber, 2)
            life_support_rating = oxygen_generator_dec * co2_scrubber_dec
            print(life_support_rating)


class VentSub(Submarine):
    def __init__(self, file_path) -> None:
        super().__init__(file_path=file_path)

    def check_vents(self, diagonal: bool):
        with open(self.file_path, "r") as f:
            reader = csv.reader(f, delimiter=" ")
            moves = []
            x_list = []
            y_list = []
            for row in reader:
                x_from = row[0].split(",")[0]
                x_to = row[2].split(",")[0]
                y_from = row[0].split(",")[1]
                y_to = row[2].split(",")[1]
                if not diagonal:
                    if not (x_from == x_to or y_from == y_to):
                        continue
                moves.append(
                    {
                        "from": {"x": int(x_from), "y": int(y_from)},
                        "to": {"x": int(x_to), "y": int(y_to)},
                    }
                )
                x_list += [int(x_from), int(x_to)]
                y_list += [int(y_from), int(y_to)]
            max_x = max(x_list) + 1
            max_y = max(y_list) + 1

        map = [[0] * max_x for _ in range(max_y)]
        for move in moves:
            map = self._process_vent_move(move, map)
            # print(move)
            # self._print_vent_map(row, map)
            # print('')

        # self._print_vent_map(row, map)
        score = self._get_vent_score(map)
        print(score)

    def _get_vent_score(self, map):
        score = sum([sum([1 for number in row if number >= 2]) for row in map])
        return score

    def _print_vent_map(self, row, map):
        for i, row in enumerate(map):
            print(f'{i if len(str(i)) >1 else " "+str(i)}: {row}')

    def _process_vent_move(self, move: Dict, map: List[List[int]]):
        y_from = move["from"]["y"]
        y_to = move["to"]["y"]
        x_from = move["from"]["x"]
        x_to = move["to"]["x"]
        # straight row
        if y_from == y_to:
            line = (
                range(x_from, x_to + 1) if x_from <= x_to else range(x_to, x_from + 1)
            )
            for x in line:
                map[y_from][x] += 1
        # straight column
        elif x_from == x_to:
            line = (
                range(y_from, y_to + 1) if y_from <= y_to else range(y_to, y_from + 1)
            )
            for y in line:
                map[y][x_from] += 1
        # diagonal
        else:
            x_offset = 1 if x_from < x_to else -1
            y_offset = 1 if y_from < y_to else -1
            x = x_from
            y = y_from
            while abs(y - y_to) > 0 and abs(x - x_to) > 0:
                map[y][x] += 1
                x += x_offset
                y += y_offset
            map[y_to][x_to] += 1

        return map


class SegmentSub(Submarine):
    def __init__(self, file_path: str = None, debug: bool = False) -> None:
        super().__init__(file_path=file_path, debug=debug)

        self.segment_count_map = {
            2: [1],
            3: [7],
            4: [4],
            5: [2, 3, 5, 6],
            6: [0, 6, 9],
            7: [8],
        }

        self.default_segment_map = {
            "abcefg": 0,
            "cf": 1,
            "acdeg": 2,
            "acdfg": 3,
            "bcdf": 4,
            "abdfg": 5,
            "abdefg": 6,
            "acf": 7,
            "abcdefg": 8,
            "abcdfg": 9,
        }

        self.enigma_map = {}

        self.easy_digits = [1, 4, 7, 8]

    def _load_segment_data(self):
        data = []
        with open(self.file_path, "r") as f:
            for line in f:
                segment_data = line.split("|")
                data.append(
                    {
                        "input": segment_data[0].strip().split(" "),
                        "output": segment_data[1].strip().split(" "),
                    }
                )
        return data

    def count_easy_digits(self):
        data = self._load_segment_data()
        count = 0
        for row in data:
            output = row["output"]
            for digit in output:
                if self.debug:
                    print(digit, len(digit))
                if any([self.segment_count_map[len(digit)][0] in self.easy_digits]):
                    count += 1
        print(count)

    def run_segments(self):
        data = self._load_segment_data()
        total = 0
        for row in tqdm(data):
            enigma_map = {}
            # build scramble map {digit: int : segment: set} for 1,4,7,8
            scrambled_map = {}
            for digit in row["input"]:
                if len(digit) == 2:
                    scrambled_map[1] = set(digit)
                elif len(digit) == 3:
                    scrambled_map[7] = set(digit)
                elif len(digit) == 4:
                    scrambled_map[4] = set(digit)
                elif len(digit) == 7:
                    scrambled_map[8] = set(digit)

            # build scramble map for remaining numbers (req. 1,4,7,8)
            for digit in row["input"]:
                # 6 segment digit with 3 segments not in '4' is 0
                digit_set = set(digit)
                if len(digit) == 6:
                    if len(digit_set - scrambled_map[7]) == 3:
                        if len(digit_set - scrambled_map[4]) == 3:
                            scrambled_map[0] = digit_set
                        else:
                            scrambled_map[9] = digit_set
                    else:
                        scrambled_map[6] = digit_set
                elif len(digit) == 5:
                    if len(digit_set - scrambled_map[7]) == 3:
                        if len(digit_set - scrambled_map[4]) == 3:
                            scrambled_map[2] = digit_set
                        else:
                            scrambled_map[5] = digit_set
                    else:
                        scrambled_map[3] = digit_set

            for numeral, segments in scrambled_map.items():
                enigma_map["".join(sorted(segments))] = numeral

            output_digit = ""
            for digit in row["output"]:
                sorted_digit = "".join(sorted(digit))
                output_digit += str(enigma_map[sorted_digit])
            total += int(output_digit)
            if self.debug:
                print(f"{' '.join(row['output'])}: {output_digit} -> {total=}")
        print(total)

    def convert_to_valid_segment(self, scrambled_str):
        return "".join([self.enigma_map[char] for char in scrambled_str])
