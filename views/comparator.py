import streamlit as st
import random
from core.avl_tree import AVLTree
from core.rb_tree import RedBlackTree
from visualizer.renderer import render_avl, render_rbt

def comparator_view():
    st.markdown("<h2 style='text-align: center;'>Comparador: AVL vs Rubro-Negra</h2>", unsafe_allow_html=True)

    if 'avl' not in st.session_state:
        st.session_state.avl = AVLTree()
    if 'rbt' not in st.session_state:
        st.session_state.rbt = RedBlackTree()

    # Controles Superiores
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        val_insert = st.number_input("Valor", value=0, step=1, format="%d", key="val_insert")
    with col2:
        if st.button("Inserir Nó", use_container_width=True, type="primary"):
            st.session_state.avl.insert(val_insert)
            st.session_state.rbt.insert(val_insert)
            st.rerun()
    with col3:
        if st.button("Remover Nó", use_container_width=True):
            st.session_state.avl.delete(val_insert)
            st.session_state.rbt.delete(val_insert)
            st.rerun()
    with col4:
        if st.button("Buscar", use_container_width=True):
            found_avl = st.session_state.avl.search(val_insert)
            found_rbt = st.session_state.rbt.search(val_insert)
            if found_avl and found_rbt:
                st.success(f"Valor {val_insert} encontrado em ambas!")
            else:
                st.error(f"Valor {val_insert} não encontrado.")

    # Ações Extras
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("Gerar 10 Nós Aleatórios", use_container_width=True):
            for _ in range(10):
                v = random.randint(1, 100)
                st.session_state.avl.insert(v)
                st.session_state.rbt.insert(v)
    with col_b:
        if st.button("Limpar Árvores", use_container_width=True):
            st.session_state.avl = AVLTree()
            st.session_state.rbt = RedBlackTree()
    with col_c:
         view_mode = st.selectbox("Modo de Exibição", ["Lado a Lado", "Apenas AVL", "Apenas Rubro-Negra"])

    st.divider()

    # Métricas
    st.markdown("### 📊 Comparativo de Métricas")
    m1, m2, m3, m4 = st.columns(4)
    avl_h = st.session_state.avl.get_height(st.session_state.avl.root)
    rbt_h = st.session_state.rbt.get_height(st.session_state.rbt.root)
    avl_nodes = st.session_state.avl.get_node_count()
    rbt_nodes = st.session_state.rbt.get_node_count()

    m1.metric("Altura AVL", avl_h)
    m2.metric("Rotações AVL", st.session_state.avl.rotation_count)
    m3.metric("Altura RBT", rbt_h)
    m4.metric("Rotações RBT", st.session_state.rbt.rotation_count)

    if avl_nodes > 0:
        if avl_h < rbt_h:
            st.info("💡 A Árvore AVL está mais baixa (melhor balanceamento estrito).")
        elif rbt_h < avl_h:
            st.info("💡 A Árvore Rubro-Negra está mais baixa.")
        else:
            st.info("💡 Ambas possuem a mesma altura.")

    st.divider()

    # Visualização
    if view_mode == "Lado a Lado":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h4 style='text-align:center;'>Árvore AVL</h4>", unsafe_allow_html=True)
            st.plotly_chart(render_avl(st.session_state.avl), use_container_width=True, key="comp_avl_side")
        with c2:
            st.markdown("<h4 style='text-align:center;'>Árvore Rubro-Negra</h4>", unsafe_allow_html=True)
            st.plotly_chart(render_rbt(st.session_state.rbt), use_container_width=True, key="comp_rbt_side")
    elif view_mode == "Apenas AVL":
        st.markdown("<h4 style='text-align:center;'>Árvore AVL</h4>", unsafe_allow_html=True)
        st.plotly_chart(render_avl(st.session_state.avl), use_container_width=True, key="comp_avl_only")
    else:
        st.markdown("<h4 style='text-align:center;'>Árvore Rubro-Negra</h4>", unsafe_allow_html=True)
        st.plotly_chart(render_rbt(st.session_state.rbt), use_container_width=True, key="comp_rbt_only")

    st.divider()

    # Percursos
    st.markdown("### 🛤️ Percursos")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("**Pré-ordem AVL**")
        st.write(st.session_state.avl.preorder())
    with p2:
        st.markdown("**Em-ordem**")
        st.write(st.session_state.avl.inorder())
    with p3:
        st.markdown("**Pós-ordem AVL**")
        st.write(st.session_state.avl.postorder())

