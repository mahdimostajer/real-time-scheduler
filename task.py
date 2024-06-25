from itertools import count


class Task:
    id_counter = count(start=1)

    def __init__(self, period: int, util: float, execution_time: float):
        self.id: int = next(self.id_counter)
        self.period: int = period
        self.util: float = util
        self.execution_time: float = execution_time

    def __str__(self) -> str:
        return f"TASK=> id={self.id}: period={self.period} util={self.util} execution_time={self.execution_time}"

