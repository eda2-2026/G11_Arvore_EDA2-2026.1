import streamlit as st
import random
from core.avl_tree import AVLTree
from visualizer.renderer import render_avl

def generate_challenge():
    tree = AVLTree()
    vals = random.sample(range(1, 50), 5)
    for v in vals:
         tree.insert(v)
    return tree, vals

def challenge_view():
    st.markdown("<h2 style='text-align: center;'>Modo Desafio: Especialista em AVL</h2>", unsafe_allow_html=True)

    if 'ch_tree' not in st.session_state:
        st.session_state.ch_tree, st.session_state.ch_vals = generate_challenge()
        st.session_state.ch_next_val = random.randint(1, 50)
        st.session_state.ch_answered = False

    st.info("Neste modo, você praticará a identificação de desbalanceamentos em uma Árvore AVL.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Árvore Atual")
        st.plotly_chart(render_avl(st.session_state.ch_tree), use_container_width=True, key="chal_avl")

    with col2:
        st.markdown("### O Desafio")
        st.markdown(f"**Qual será o comportamento ao inserir o valor {st.session_state.ch_next_val}?**")

        if not st.session_state.ch_answered:
            with st.form("challenge_form"):
                node_unbal = st.number_input("1. Qual nó ficará desbalanceado? (Digite o valor, ou 0 se nenhum)", step=1, value=0)
                case_type = st.selectbox("2. Qual será o Caso AVL?", ["Nenhum (Permanece Balanceada)", "LL (Esquerda-Esquerda)", "RR (Direita-Direita)", "LR (Esquerda-Direita)", "RL (Direita-Esquerda)"])
                rot_type = st.selectbox("3. Qual rotação aplicar?", ["Nenhuma", "Simples à Direita", "Simples à Esquerda", "Dupla: Esquerda, depois Direita", "Dupla: Direita, depois Esquerda"])

                submitted = st.form_submit_button("Enviar Resposta", type="primary")
                
                if submitted:
                    # Simular inserção para obter a resposta real
                    sim_tree = AVLTree()
                    for v in st.session_state.ch_vals:
                        sim_tree.insert(v)
                    
                    logs_before = len(sim_tree.rotations_log)
                    sim_tree.insert(st.session_state.ch_next_val)
                    logs_after = len(sim_tree.rotations_log)
    
                    st.session_state.ch_sim_tree = sim_tree
                    
                    expected_unbal = 0
                    expected_case = "Nenhum (Permanece Balanceada)"
                    expected_rot = "Nenhuma"
    
                    if logs_after > logs_before:
                        last_log = sim_tree.rotations_log[-1]
                        # Avaliar as respostas baseadas no log exato do AVLTree
                        if "(LL)" in last_log:
                            expected_case = "LL (Esquerda-Esquerda)"
                            expected_rot = "Simples à Direita"
                        elif "(RR)" in last_log:
                            expected_case = "RR (Direita-Direita)"
                            expected_rot = "Simples à Esquerda"
                        elif "(Esquerda-Direita)" in last_log:
                            expected_case = "LR (Esquerda-Direita)"
                            expected_rot = "Dupla: Esquerda, depois Direita"
                        elif "(Direita-Esquerda)" in last_log:
                            expected_case = "RL (Direita-Esquerda)"
                            expected_rot = "Dupla: Direita, depois Esquerda"
                        
                        # Extrair o nó que sofreu a rotação (fica no fim da string após "em ")
                        val_str = last_log.split("em ")[-1]
                        expected_unbal = int(val_str)
                    
                    # Avaliar Acertos
                    score = 0
                    if node_unbal == expected_unbal: score += 1
                    if case_type == expected_case: score += 1
                    if rot_type == expected_rot: score += 1
    
                    st.session_state.ch_user_unbal = node_unbal
                    st.session_state.ch_user_case = case_type
                    st.session_state.ch_user_rot = rot_type
                    
                    st.session_state.ch_score = score
                    st.session_state.ch_expected_unbal = expected_unbal
                    st.session_state.ch_expected_case = expected_case
                    st.session_state.ch_expected_rot = expected_rot
                    
                    st.session_state.ch_answered = True
                    st.rerun()
        else:
            if st.session_state.ch_score == 3:
                st.success("🎉 Parabéns! Você acertou tudo! Análise perfeita do desbalanceamento.")
            elif st.session_state.ch_score > 0:
                st.warning(f"⚠️ Quase lá! Você acertou {st.session_state.ch_score} de 3 perguntas. Veja o que errou.")
            else:
                st.error("❌ Errou tudo! Mas errar faz parte do aprendizado. Veja o gabarito abaixo.")

            st.markdown("#### Gabarito e Correção")
            st.markdown(f"- **Nó desbalanceado:** Você respondeu '{st.session_state.ch_user_unbal}' | Esperado **{st.session_state.ch_expected_unbal}**")
            st.markdown(f"- **Caso AVL:** Você respondeu '{st.session_state.ch_user_case}' | Esperado **{st.session_state.ch_expected_case}**")
            st.markdown(f"- **Rotação Aplicada:** Você respondeu '{st.session_state.ch_user_rot}' | Esperado **{st.session_state.ch_expected_rot}**")
            
            st.markdown("### Árvore Após Inserção")
            st.plotly_chart(render_avl(st.session_state.ch_sim_tree), use_container_width=True, key="chal_sim_avl")
            
            if st.button("Próximo Desafio"):
                del st.session_state.ch_tree
                st.rerun()
