import random
from mesa import Model
# Поддержка разных версий Mesa (3.x и 4.x)
try:
    from mesa.space import MultiGrid
except ImportError:
    from mesa.discrete_space import MultiGrid

from agent import PersonAgent

class SociologyModel(Model):
    """Главный класс мира симуляции"""

    def __init__(self, width, height, archetype_counts):
        super().__init__()
        # MultiGrid позволяет находиться нескольким агентам в одной клетке
        # torus=True "зацикливает" карту (ушел направо - вышел слева)
        self.grid = MultiGrid(width, height, torus=True)

        # Создаем агентов на основе переданных настроек UI
        for archetype, data in archetype_counts.items():
            for _ in range(data["count"]):
                agent = PersonAgent(self, archetype, data["color"])
                # Размещаем агента в случайной точке сетки
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

    def step(self):
        """Один глобальный такт времени в симуляции"""
        # Вызываем метод step() у всех агентов в случайном порядке
        self.agents.shuffle_do("step")
