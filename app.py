import streamlit as st
from views.comparator import comparator_view
from views.challenge import challenge_view

st.set_page_config(
    page_title="Tree Compare: AVL vs RBT",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Minimalist and Elegant Design
st.markdown("""
<style>
    .reportview-container {
        background: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌳 Tree System")
st.sidebar.markdown("Escolha o modo de operação:")

mode = st.sidebar.radio("Navegação", ["Comparador Livre", "Modo Desafio"])

st.sidebar.divider()
st.sidebar.markdown("""
**Sobre:**
Sistema educativo MVP para comparar Árvores AVL e Rubro-Negras, desenvolvido em Python.
""")

if mode == "Comparador Livre":
    comparator_view()
else:
    challenge_view()
