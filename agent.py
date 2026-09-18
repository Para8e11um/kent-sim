import random
from mesa import Agent

class PersonAgent(Agent):
    """Базовый класс агента симуляции"""

    def __init__(self, model, archetype, color):
        super().__init__(model)
        self.archetype = archetype
        self.color = color

    # Метод получения информации о клетке для агента
    def get_neighbors_message(self):
        message = "Неподалёку от вас находятся: "
        neighbors = self.model.grid.get_neighbors(self.pos, moore =True, radius = 0, include_center=True)
        if len(neighbors) == 1:
            message = "Вы одни в окрестности."
            return message
        for neighbor in neighbors:
            if neighbor.unique_id != self.unique_id:
                message += f"{str(neighbor.archetype)} ID-{str(neighbor.unique_id)}, "
        message = message.removesuffix(", ")
        message += "."
        return message

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
