import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from model import SociologyModel

st.set_page_config(page_title="LLM Society Base", layout="wide")

# --- КОНФИГУРАЦИЯ АРХЕТИПОВ ---
ARCHETYPES_CONFIG = {
    "Илья": "#EF553B",  # Красный
    "Дима": "#00CC96",  # Зеленый
    "Вадим": "#AB63FA", # Фиолетовый
}

def hex_to_rgb(hex_color):
    """Преобразует HEX строку ('#1E88E5') в список RGB ([30, 136, 229])"""
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

# --- БОКОВАЯ ПАНЕЛЬ (НАСТРОЙКИ) ---
st.sidebar.header("Настройки мира")
grid_size = st.sidebar.slider("Размер сетки", 10, 30, 15)

# Единый ползунок для количества агентов каждого типа
count_per_archetype = st.sidebar.slider("Агентов каждого типа", 0, 50, 10)

# Применяем выбранное значение ко всем архетипам
archetype_counts = {}
for arch, color in ARCHETYPES_CONFIG.items():
    archetype_counts[arch] = {"count": count_per_archetype, "color": color}

# Инициализация модели в памяти Streamlit
if st.sidebar.button("🔄 Создать мир", use_container_width=True) or "model" not in st.session_state:
    st.session_state.model = SociologyModel(grid_size, archetype_counts)
    st.session_state.step = 0

model = st.session_state.model

# --- ИНТЕРФЕЙС УПРАВЛЕНИЯ И КАРТА ---
col_map, col_ctrl = st.columns([3, 1])

with col_ctrl:
    st.subheader("Управление")
    if st.button("▶ 1 Шаг", use_container_width=True):
        model.step()
        st.session_state.step += 1

    st.info(f"**Глобальный шаг:** {st.session_state.step}")

with col_map:
    st.subheader("Карта общества")

    data = []
    for agent in model.agents:
        data.append({
            "ID": agent.unique_id,
            "Архетип": agent.archetype,
            "X": agent.pos[0],
            "Y": agent.pos[1],
            "Color": agent.color
        })

    if data:
        color_grid = np.array([[hex_to_rgb(model.biome_map.get_biome(x, y)["color"]) for x in range(grid_size)] for y in range(grid_size)],dtype=np.uint8)
        print(color_grid[0][0])
        print(color_grid[5][5])
        fig = px.imshow(color_grid,origin='lower')
        df = pd.DataFrame(data)

        fig_agents = px.scatter(
            df, x="X", y="Y",
            hover_name="Архетип", hover_data=["ID"],
            color="Архетип", color_discrete_map=ARCHETYPES_CONFIG
        )

        fig_agents.update_traces(marker=dict(size=14, line=dict(width=1, color="#1e1e1e")))

        for trace in fig_agents.data:
            fig.add_trace(trace)

        fig.update_layout(
            showlegend=False,
            template="plotly_dark",
            # uirevision сохраняет масштаб и позицию камеры между перезагрузками Streamlit
            uirevision="constant",
            xaxis=dict(
                range=[-0.5, grid_size - 0.5],
                dtick=1,
                showgrid=True,
                showticklabels=False,
                autorange=False,   # Запрещаем Plotly автоподстраивать оси
                fixedrange=True    # Запрещаем зум/скролл мышкой, если хотите жесткую карту
            ),
            yaxis=dict(
                range=[-0.5, grid_size - 0.5],
                dtick=1,
                showgrid=True,
                showticklabels=False,
                autorange=False,   # Запрещаем автоподстройку
                fixedrange=True,
                scaleanchor="x",   # Делает ячейки строго квадратными (1:1)
                scaleratio=1
            ),
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=False)
    else:
        st.warning("В мире нет агентов. Добавьте их в настройках.")
