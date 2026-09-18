import random
from mesa import Agent

class PersonAgent(Agent):
    """Базовый класс агента симуляции"""

    def __init__(self, model, archetype, color):
        super().__init__(model)
        self.archetype = archetype
        self.color = color
        self.agent_type = "Person"

    # Метод получения информации о соседях на клетке(возвращает предложение о соседях)
    def get_neighbors_message(self):
        message = " Неподалёку от вас находятся: "
        neighbors = [a for a in self.model.grid.get_neighbors(self.pos, moore =True, radius = 0, include_center=True) if a.agent_type == "Person"]
        if len(neighbors) == 1:
            message = " Вы одни в окрестности."
            return message
        for neighbor in neighbors:
            if neighbor.unique_id != self.unique_id:
                message += f"{str(neighbor.archetype)} ID-{str(neighbor.unique_id)}, "
        message = message.removesuffix(", ")
        message += "."
        return message

    # Метод получения информации о биоме(возвращает предложение о биоме)
    def get_biome_message(self):
        local_biome = self.model.biome_map.get_biome(self.pos[0],self.pos[1])["name"]
        match local_biome:
            case "Поле":
                return " Вы находитесь в полях."
            case "Лес":
                return " Вы находитесь в лесу."
            case "Город":
                return " Вы находитесь в руинах города."
            case _:
                return ""

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
