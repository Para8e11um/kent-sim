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
        color_grid = np.array([[hex_to_rgb(model.biome_map.get_biome(x, y).get("Color", model.biome_map.get_biome(x, y).get("color"))) for x in range(grid_size)] for y in range(grid_size)], dtype=np.uint8)
        fig = px.imshow(color_grid, origin='lower')
        df = pd.DataFrame(data)

        # 1. Настраиваем график агентов (добавляем их в группу легенды "Агенты")
        fig_agents = px.scatter(
            df, x="X", y="Y",
            hover_name="Архетип", hover_data=["ID"],
            color="Архетип", color_discrete_map=ARCHETYPES_CONFIG
        )

        fig_agents.update_traces(
            marker=dict(size=14, line=dict(width=1, color="#1e1e1e")),
            legendgroup="Агенты",               # Группировка в легенде
            legendgrouptitle_text="Агенты"      # Заголовок группы
        )

        for trace in fig_agents.data:
            fig.add_trace(trace)

        for biome in model.biome_map.biomes:
            biome_color = biome.get("color", "#000000")

            fig.add_scatter(
                x=[None], y=[None],
                mode="markers",
                name=biome["name"],
                marker=dict(
                    size=14,
                    color=biome_color,
                    symbol="square",
                    line=dict(width=1, color="#1e1e1e")
                ),
                legendgroup="Биомы",
                legendgrouptitle_text="Биомы"
            )

        # 3. Настройка макета
        fig.update_layout(
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor="rgba(0,0,0,0)"
            ),
            template="plotly_dark",
            uirevision="constant",
            xaxis=dict(
                range=[-0.5, grid_size - 0.5],
                dtick=1,
                showgrid=True,
                showticklabels=False,
                autorange=False,
                fixedrange=True
            ),
            yaxis=dict(
                range=[-0.5, grid_size - 0.5],
                dtick=1,
                showgrid=True,
                showticklabels=False,
                autorange=False,
                fixedrange=True,
                scaleanchor="x",
                scaleratio=1
            ),
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=False)
    else:
        st.warning("В мире нет агентов. Добавьте их в настройках.")
