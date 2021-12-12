import csv
import numpy as np
from typing import Optional, Dict, List, Union, Tuple

class Submarine:
    def __init__(
        self,
        move_file_path: str = None, 
        initial_position: Optional[Dict[str, int]] = None,
        diagnostic_file_path: str = None,
    ) -> None:
        self.move_file_path = move_file_path
        self.position = initial_position or self._get_new_position()
        self.diagnostic_file_path = diagnostic_file_path

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
            self.position["vertical"] += (magnitude * self.position["aim"])

    def _move_no_aim(self, direction: str, magnitude: int) -> None:
        if direction == "down":
            self.position["vertical"] += magnitude
        elif direction == "up":
            self.position["vertical"] -= magnitude
        else:
            self.position["horizontal"] += magnitude
        
    def run_movement_no_aim(self):
        with open(self.move_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                direction = row[0].split(' ')[0]
                magnitude = int(row[0].split(' ')[1])
                self._move_no_aim(direction, magnitude)
        print(f'position = {self.position}')
        print(f'horizontal * vertical = {self.position["horizontal"] * self.position["vertical"]}')

    def run_movement(self):
        with open(self.move_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                direction = row[0].split(' ')[0]
                magnitude = int(row[0].split(' ')[1])
                self._move(direction, magnitude)
        print(f'position = {self.position}')
        print(f'horizontal * vertical = {self.position["horizontal"] * self.position["vertical"]}')

    def _get_power_consumption(self, data: list) -> Dict[str, Union[str, int]]:
        values = self._calculate_gamma_and_epsilon(data)
        gamma = values[0]
        epsilon = values[1]
        return {
            'gamma_bin': gamma,
            'gamma_dec': int(gamma, 2),
            'epsilon_bin': epsilon,
            'epsilon_dec': int(epsilon, 2),
            'power_consumption': int(gamma, 2) * int(epsilon, 2)
        }

    def _calculate_gamma_and_epsilon(self, data, tie_value = None) -> Tuple[str, str]:
        gamma = ''
        epsilon = ''
        for digit_row in data:
            if sum(digit_row) > len(digit_row) / 2:
                gamma += '1'
                epsilon += '0'
            elif sum(digit_row) < len(digit_row) / 2:
                gamma += '0'
                epsilon += '1'
            else:
                 gamma += tie_value
                 epsilon += '1' if tie_value == 0 else '0'
        return gamma, epsilon

    def _get_oxygen_generator(self, oxygen_generator_list, transposed_data, starting_value=0):
        if len(oxygen_generator_list) == 1:
            oxygen_generator = ''.join(list(map(lambda x: str(x), oxygen_generator_list[0])))
            return oxygen_generator
        gamma_relevant = int(self._calculate_gamma_and_epsilon(transposed_data, tie_value='1')[0][starting_value])
        oxygen_generator_list = [i for i in oxygen_generator_list if i[starting_value] == gamma_relevant]
        transposed_data = np.transpose(oxygen_generator_list)
        return self._get_oxygen_generator(oxygen_generator_list, transposed_data, starting_value+1)

    def _get_co2_scrubber(self, co2_scrubber_list, transposed_data, starting_value=0):
        if len(co2_scrubber_list) == 1:
            co2_scrubber = ''.join(list(map(lambda x: str(x), co2_scrubber_list[0])))
            return co2_scrubber
        epsilon_relevant = int(self._calculate_gamma_and_epsilon(transposed_data, tie_value='1')[1][starting_value])
        co2_scrubber_list = [i for i in co2_scrubber_list if i[starting_value] == epsilon_relevant]
        transposed_data = np.transpose(co2_scrubber_list)
        return self._get_co2_scrubber(co2_scrubber_list, transposed_data, starting_value+1)

    def run_diagnostic(self, operation: str) -> None:
        with open (self.diagnostic_file_path, 'r') as f:
            reader = csv.reader(f)
            data = [[int(i) for i in row[0]] for row in reader]
        transposed_data = np.transpose(data)
        if operation == 'power_consumption':
            power_consumption = self._get_power_consumption(transposed_data)
            self.gamma_binary = power_consumption["gamma_bin"]
            self.epsilon_binary = power_consumption["epsilon_bin"]
            print(power_consumption)
        elif operation == 'life_support_rating':
            oxygen_generator = self._get_oxygen_generator(
                oxygen_generator_list=data,
                transposed_data=transposed_data
            )
            co2_scrubber = self._get_co2_scrubber(
                co2_scrubber_list=data,
                transposed_data=transposed_data
            )
            oxygen_generator_dec = int(oxygen_generator, 2)
            co2_scrubber_dec = int(co2_scrubber, 2)
            life_support_rating = oxygen_generator_dec * co2_scrubber_dec
            print(life_support_rating)