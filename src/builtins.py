class World:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.facing = 0
        self.hp = 100
        self.potions = 1

    def step_forward(self):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        dx, dy = directions[self.facing]
        self.x += dx
        self.y += dy
        return 1

    def turn_left(self):
        self.facing = (self.facing - 1) % 4
        return 1

    def turn_right(self):
        self.facing = (self.facing + 1) % 4
        return 1

    def use_potion(self):
        if self.potions > 0:
            self.potions -= 1
            self.hp = 100
            return 1
        return 0


def make_builtins():
    world = World()
    return {
        'step_forward': world.step_forward,
        'turn_left': world.turn_left,
        'turn_right': world.turn_right,
        'use_potion': world.use_potion,
    }