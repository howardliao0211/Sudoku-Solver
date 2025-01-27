from dataclasses import dataclass

@dataclass
class BoardUpdateInfo:
    row: int
    col: int
    val: int
    isEnable: bool
