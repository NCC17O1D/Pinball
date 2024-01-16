from pygame import Vector2, Color
from api.objects.game_object import GameObject
from api.components.mesh import CircleMesh
from api.components.collider import CircleCollider
from api.components.rigidbody import Rigidbody
from api.components.renderer import Renderer
from options import Options

class Ball(GameObject):
    def __init__(self, pos: Vector2, color: Color = Color(255, 255, 255)):
        self.color = color
        self.radius = 25 * Options().asf
        super().__init__(pos, 5)

    def on_awake(self):
        # Add the necessary components
        self.add_components(
            CircleMesh(self.color, self.radius),
            CircleCollider(),
            Rigidbody(),
            Renderer()
        )
        return super().on_awake()

    def on_destroy(self) -> None:
        self.scene.active_ball_count -= 1
        return super().on_destroy()
    
    def on_update(self, delta_time: float):
        if self.transform.pos.y > self.scene.screen.get_height() + self.radius/2:
            self.on_destroy()
        return super().on_update(delta_time)