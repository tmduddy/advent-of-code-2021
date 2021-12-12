import csv
from typing import Optional, Dict

class Submarine:
    def __init__(self, file_path: str, position: Optional[Dict[str, int]] = None) -> None:
        self.file_path = file_path
        self.position = position or self._get_new_position()

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
        

    def run_no_aim(self):
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                direction = row[0].split(' ')[0]
                magnitude = int(row[0].split(' ')[1])
                self._move_no_aim(direction, magnitude)
        print(f'position = {self.position}')
        print(f'horizontal * vertical = {self.position["horizontal"] * self.position["vertical"]}')

    def run(self):
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                direction = row[0].split(' ')[0]
                magnitude = int(row[0].split(' ')[1])
                self._move(direction, magnitude)
        print(f'position = {self.position}')
        print(f'horizontal * vertical = {self.position["horizontal"] * self.position["vertical"]}')