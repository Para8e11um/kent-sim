import random
from mesa import Agent

class PersonAgent(Agent):
    """Базовый класс агента симуляции"""

    def __init__(self, model, archetype, color):
        # В Mesa 3.0+ уникальный ID генерируется автоматически при передаче model
        super().__init__(model)
        self.archetype = archetype
        self.color = color

    def step(self):
        """Действие агента на каждом шаге (пока только случайное движение)"""
        # Получаем соседние клетки (moore=True значит 8 направлений по диагонали)
        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        if neighbors:
            # Выбираем случайную соседнюю клетку и перемещаемся туда
            new_pos = random.choice(neighbors)
            self.model.grid.move_agent(self, new_pos)
