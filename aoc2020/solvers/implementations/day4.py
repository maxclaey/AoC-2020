import logging
import re
from pathlib import Path
from typing import Dict, List, Optional

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay4")


@SolverFactory.register(day=4)
class SolverDay4(PuzzleSolver):

    @property
    def demo_result_1(self) -> Optional[int]:
        return 2

    @property
    def demo_result_2(self) -> Optional[int]:
        return None

    def _read_file(self) -> List[Dict[str, str]]:
        passwords: List[Dict[str, str]] = []
        cur_password: Dict[str, str] = {}
        with self._input_file.open(mode="r") as f:
            for line in f:
                line = line.strip().lower()
                if len(line) == 0:
                    if len(cur_password) > 0:
                        passwords.append(cur_password)
                        cur_password = {}
                    continue
                parts = line.split(" ")
                for part in parts:
                    kv = part.strip().split(":")
                    if len(kv) != 2:
                        logger.error(f"Invalid key-value pair on line {line}")
                        continue
                    cur_password[kv[0].strip()] = kv[1].strip()
            if len(cur_password) > 0:
                passwords.append(cur_password)
        return passwords

    def solve_1(self) -> int:
        # Set of required keys
        all_fields = {
            "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"
        }
        optional_fields = ["cid"]
        valid_pwds = 0
        # Check each passwords
        for pwd in self._input_data:
            found_keys = set(pwd.keys())
            missing_keys = all_fields - found_keys
            logger.debug(f"Missing keys are {missing_keys}")
            valid = True
            for key in missing_keys:
                if key not in optional_fields:
                    valid = False
                    break
            if valid:
                valid_pwds += 1
        return valid_pwds

    def solve_2(self) -> int:
        valid_pwds = 0
        # Check all passwords
        for pwd in self._input_data:
            byr = self._check_year(pwd.get("byr", ""), 1920, 2002)
            iyr = self._check_year(pwd.get("iyr", ""), 2010, 2020)
            eyr = self._check_year(pwd.get("eyr", ""), 2020, 2030)
            hgt = self._check_height(pwd.get("hgt", ""))
            hcl = self._check_hair(pwd.get("hcl", ""))
            ecl = self._check_eye(pwd.get("ecl", ""))
            pid = self._check_pid(pwd.get("pid", ""))
            if byr and iyr and eyr and hgt and hcl and ecl and pid:
                valid_pwds += 1
        return valid_pwds

    @staticmethod
    def _check_year(year: str, min_val: int, max_val: int) -> bool:
        try:
            val = int(year)
            if min_val <= val <= max_val and len(year) == 4:
                return True
        except ValueError:
            pass
        return False

    @staticmethod
    def _check_height(height: str) -> bool:
        min_vals = {"cm": 150, "in": 59}
        max_vals = {"cm": 193, "in": 76}
        if len(height) < 4:
            return False
        unit = height[-2:]
        if unit not in min_vals:
            return False
        try:
            val = int(height[:-2])
        except ValueError:
            return False
        return min_vals[unit] <= val <= max_vals[unit]

    @staticmethod
    def _check_hair(color: str) -> bool:
        pattern = "^\#([0-9|a-f]){6}$"
        return re.fullmatch(pattern, color) is not None

    @staticmethod
    def _check_eye(color: str) -> bool:
        valid_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        return color in valid_colors

    @staticmethod
    def _check_pid(pid: str) -> bool:
        pattern = "^[0-9]{9}$"
        return re.fullmatch(pattern, pid) is not None

    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
