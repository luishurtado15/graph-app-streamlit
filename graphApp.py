import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Demostración de Aplicaciones con Grafos", layout="wide")
st.title("🧠 Aplicaciones Reales con Teoría de Grafos")

st.write("Sistemas Autoadaptables, Universidad EAFIT, 2025")
st.write("Magda Rodriguez, Camilo Echavarría, Luis Miguel Hurtado")

aplicacion = st.sidebar.selectbox("Selecciona una aplicación para visualizar:", [
    "1. Planificación de rutas (Dijkstra)",
    "2. Red Social (Grado de Conexión)",
    "3. Recomendador de productos (Grafo bipartito)"
])

if aplicacion == "1. Planificación de rutas (Dijkstra)":
    st.subheader("📍 Ruta más corta entre ciudades")

    G = nx.DiGraph()
    G.add_weighted_edges_from([
        ("A", "B", 5),
        ("A", "C", 3),
        ("B", "D", 2),
        ("C", "D", 7),
        ("C", "E", 4),
        ("D", "E", 1)
    ])

    inicio = st.selectbox("Ciudad de origen", list(G.nodes), key="inicio1")
    fin = st.selectbox("Ciudad de destino", list(G.nodes), key="fin1")

    if nx.has_path(G, inicio, fin):
        path = nx.dijkstra_path(G, inicio, fin)
        dist = nx.dijkstra_path_length(G, inicio, fin)
        st.success(f"Ruta más corta: {' → '.join(path)} (Distancia: {dist})")

        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(20, 5))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_weight='bold', ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=list(zip(path, path[1:])), edge_color='red', width=3, ax=ax)
        st.pyplot(fig)
    else:
        st.error("No hay camino entre las ciudades seleccionadas.")

elif aplicacion == "2. Red Social (Grado de Conexión)":
    st.subheader("👥 Red Social: Grado de conexión entre personas")

    G = nx.Graph()
    G.add_edges_from([
        ("Ana", "Luis"),
        ("Luis", "Carlos"),
        ("Ana", "Marta"),
        ("Marta", "Carlos"),
        ("Carlos", "Jorge"),
        ("Luis", "Elena"),
        ("Elena", "Jorge")
    ])

    persona = st.selectbox("Selecciona una persona", list(G.nodes), key="persona")
    grado = nx.single_source_shortest_path_length(G, persona)

    st.info(f"Conexiones desde {persona}:")
    for destino, pasos in grado.items():
        st.write(f"{destino}: {pasos} {'paso' if pasos == 1 else 'pasos'}")

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(20, 5))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_weight='bold', ax=ax)
    st.pyplot(fig)

elif aplicacion == "3. Recomendador de productos (Grafo bipartito)":
    st.subheader("🛒 Recomendador sencillo basado en usuarios-productos")

    B = nx.Graph()
    usuarios = ["Luis", "Ana"]
    productos = ["Libro", "Auriculares", "Laptop"]

    B.add_nodes_from(usuarios, bipartite=0)
    B.add_nodes_from(productos, bipartite=1)
    B.add_edges_from([
        ("Luis", "Laptop"),
        ("Luis", "Libro"),
        ("Ana", "Auriculares"),
        ("Ana", "Libro")
    ])

    st.write("Usuarios y productos conectados si hubo una interacción (compra, interés, etc.)")
    pos = nx.bipartite_layout(B, usuarios)
    fig, ax = plt.subplots(figsize=(20, 5))
    nx.draw(B, pos, with_labels=True, node_color=['lightblue' if n in usuarios else 'salmon' for n in B.nodes],
            node_size=2000, font_weight='bold', ax=ax)
    st.pyplot(fig)

    st.markdown("**Sugerencia (básica)**: recomendar al usuario un producto que esté conectado a usuarios similares.")
