from core.node import RBNode

class RedBlackTree:
    """
    Implementação didática de uma Árvore Rubro-Negra (Red-Black Tree).
    
    A árvore Rubro-Negra garante o balanceamento mantendo propriedades de cores:
    1. Todo nó é VERMELHO ou PRETO.
    2. A raiz é sempre PRETA.
    3. As folhas nulas (TNULL) são sempre PRETAS.
    4. Um nó VERMELHO não pode ter filhos VERMELHOS (propriedade do vermelho).
    5. Todo caminho de um nó até as folhas tem a mesma quantidade de nós PRETOS.
    """
    def __init__(self):
        # TNULL é o nó sentinela que representa o "None" nas folhas
        # É essencial que o TNULL seja PRETO para respeitar a propriedade 3.
        self.TNULL = RBNode(0, color="BLACK")
        self.root = self.TNULL
        self.rotation_count = 0
        self.rotations_log = []

    def get_node_count(self, node=None, is_root=True):
        """Conta quantos nós existem na árvore (ignora TNULL)."""
        if is_root:
            node = self.root
        if node == self.TNULL:
            return 0
        return 1 + self.get_node_count(node.left, False) + self.get_node_count(node.right, False)

    def get_height(self, node=None, is_root=True):
        """Calcula a altura física da árvore (não a altura preta)."""
        if is_root:
            node = self.root
        if node == self.TNULL:
            return 0
        return 1 + max(self.get_height(node.left, False), self.get_height(node.right, False))

    # --- Funções de Percurso (Pre, In, Post) ---
    def pre_order_helper(self, node):
        if node != self.TNULL:
            res = [node.value]
            res = res + self.pre_order_helper(node.left)
            res = res + self.pre_order_helper(node.right)
            return res
        return []

    def inorder_helper(self, node):
        if node != self.TNULL:
            res = self.inorder_helper(node.left)
            res.append(node.value)
            res = res + self.inorder_helper(node.right)
            return res
        return []

    def post_order_helper(self, node):
        if node != self.TNULL:
            res = self.post_order_helper(node.left)
            res = res + self.post_order_helper(node.right)
            res.append(node.value)
            return res
        return []

    def preorder(self):
        return self.pre_order_helper(self.root)

    def inorder(self):
        return self.inorder_helper(self.root)

    def postorder(self):
        return self.post_order_helper(self.root)

    # --- Funções de Busca ---
    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.value:
            return node
        if key < node.value:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def search(self, k):
        res = self.search_tree_helper(self.root, k)
        return res != self.TNULL

    # --- Rotações ---
    def left_rotate(self, x):
        """
        Rotação à Esquerda no nó X.
        Puxa o filho direito de X para cima, empurrando X para a esquerda.
        """
        self.rotation_count += 1
        self.rotations_log.append(f"Rotação à Esquerda em {x.value}")
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """
        Rotação à Direita no nó X.
        Puxa o filho esquerdo de X para cima, empurrando X para a direita.
        """
        self.rotation_count += 1
        self.rotations_log.append(f"Rotação à Direita em {x.value}")
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # --- Inserção ---
    def insert(self, key):
        """
        Insere uma nova chave na Árvore.
        Sempre insere o nó como VERMELHO primeiro e depois corrige possíveis 
        violações das propriedades da árvore Rubro-Negra chamando fix_insert.
        """
        node = RBNode(key)
        node.parent = None
        node.value = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "RED" # Nós novos entram sempre como vermelhos

        y = None
        x = self.root

        # Desce na árvore para achar a posição de inserção (como em BST)
        while x != self.TNULL:
            y = x
            if node.value < x.value:
                x = x.left
            elif node.value > x.value:
                x = x.right
            else:
                return # Sem duplicatas

        # Liga o nó no seu pai
        node.parent = y
        if y == None:
            self.root = node
        elif node.value < y.value:
            y.left = node
        else:
            y.right = node

        # Se for raiz, apenas pinta de preto
        if node.parent == None:
            node.color = "BLACK"
            return

        # Se o pai for a raiz, não há regra violada
        if node.parent.parent == None:
            return

        # Corrige a árvore
        self.fix_insert(node)

    def fix_insert(self, k):
        """
        Resolve violações após a inserção iterativamente.
        Ocorre quando um nó vermelho (k) é inserido num pai também vermelho.
        (Viola a regra 4: Nó vermelho não tem filho vermelho).
        A correção envolve Recoloração ou Rotações baseadas na cor do TIO de 'k'.
        """
        while k.parent.color == "RED":
            # Pai de k é filho direito do avô de k
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left # u é o tio
                # Caso 1: Tio é vermelho (Apenas recolore)
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    # Caso 2: Tio é preto, e k é filho esquerdo (Rotação Direita no pai, depois Caso 3)
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    # Caso 3: Tio é preto, k é filho direito (Rotação Esquerda no avô)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            # Pai de k é filho esquerdo do avô de k (Casos simétricos aos acima)
            else:
                u = k.parent.parent.right # u é o tio
                # Caso 1
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    # Caso 2
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    # Caso 3
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def minimum(self, node):
        """Busca o menor nó de uma sub-árvore (útil para deleção)."""
        while node.left != self.TNULL:
            node = node.left
        return node

    def rb_transplant(self, u, v):
        """Função auxiliar de deleção que 'transplanta' (sobrescreve) a posição do nó u com o nó v."""
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # --- Remoção ---
    def delete(self, key):
        """Remove a chave da árvore e corrige violações de cores."""
        self.delete_node_helper(self.root, key)

    def delete_node_helper(self, node, key):
        z = self.TNULL
        # Busca o nó para deletar
        while node != self.TNULL:
            if node.value == key:
                z = node
            if node.value <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            return # Nó não existe

        y = z
        y_original_color = y.color
        
        # Casos simples: remoção com 1 filho nulo ou sem filhos
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            # Caso complexo: nó possui dois filhos
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        # Se um nó PRETO foi removido, a contagem de pretos na árvore foi alterada.
        # Precisamos chamar o corretor.
        if y_original_color == "BLACK":
            self.fix_delete(x)

    def fix_delete(self, x):
        """
        Corrige os desbalanceamentos e contagens de nós pretos causados por uma deleção de nó preto.
        A lógica lida com 4 casos simétricos baseados na cor do 'irmão' de x.
        """
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right # s é o irmão
                
                # Caso 1: O irmão s é vermelho
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                # Caso 2: O irmão s é preto e seus dois filhos são pretos
                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    # Caso 3: Irmão s preto, filho esquerdo vermelho, direito preto
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.right_rotate(s)
                        s = x.parent.right

                    # Caso 4: Irmão s preto, filho direito vermelho
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                # Casos simétricos
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"
