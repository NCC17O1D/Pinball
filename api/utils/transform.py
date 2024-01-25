from pygame import Vector2

from api.utils.event_value import EventValue
from constants import PADDLE_SPEED, PTPF
from options import Options

class Transform:
    def __init__(self, parent) -> None:
        self.parent = parent

        self.pos: Vector2 = Vector2()

        self.rotation_speed: float = PADDLE_SPEED
        self.do_smooth_rotation: bool = False
        self.target_smooth_rotation: float = float("inf")
        self.rot: EventValue[float] = EventValue(0)
    
    def rotate(self, angle: float) -> None:
        self.rot.set_value(self.rot.get_value() + angle)

    def update(self, scaled_delta_time: float) -> None:
        if self.do_smooth_rotation:
            self._rotate_towards(self.rotation_speed * scaled_delta_time)

    def init_smooth_rotation(self, target: float) -> None:
        if target == self.target_smooth_rotation:
            return
        self.do_smooth_rotation = True
        self.target_smooth_rotation = target

    def _rotate_towards(self, rotation_speed) -> None:
        rotation_difference = self.target_smooth_rotation - self.rot.get_value()
        if abs(rotation_difference) <= rotation_speed:
            self.do_smooth_rotation = False
            angle = rotation_difference
        else:
            angle = rotation_speed if rotation_difference > 0 else -rotation_speed
        self.rotate(angle)

    def serialize(self) -> dict:
        asf = Options().asf
        return {
            "pos": [self.pos.x/asf, self.pos.y/asf],
            "rot": self.rot.get_value()
        }
    
    def deserialize(self, data: dict) -> None:
        self.pos = Vector2(data["pos"]) * Options().asf
        print(self.pos)
        self.rot.set_value(data["rot"])