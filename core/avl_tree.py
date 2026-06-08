from core.node import AVLNode

class AVLTree:
    """
    Implementação didática de uma Árvore AVL.
    
    A Árvore AVL é uma árvore binária de busca auto-balanceável. 
    A diferença de altura entre a sub-árvore esquerda e direita de qualquer nó (Fator de Balanceamento)
    não pode ser maior que 1. Se for, a árvore realiza rotações para se rebalancear.
    """
    def __init__(self):
        self.root = None
        self.rotation_count = 0
        self.rotations_log = []

    def get_height(self, node):
        """Retorna a altura do nó. Retorna 0 se o nó for nulo."""
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """
        Calcula o Fator de Balanceamento do nó.
        Fórmula: Altura da Esquerda - Altura da Direita.
        > 1  : Desbalanceada para a esquerda
        < -1 : Desbalanceada para a direita
        """
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        """
        Realiza uma rotação simples à direita.
        O filho esquerdo (x) sobe e se torna o novo pai. O pai antigo (y) desce para a direita.
        """
        x = y.left
        T2 = x.right

        # Realiza a rotação
        x.right = y
        y.left = T2

        # Atualiza as alturas (primeiro do filho antigo, depois do novo pai)
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        self.rotation_count += 1
        return x

    def left_rotate(self, x):
        """
        Realiza uma rotação simples à esquerda.
        O filho direito (y) sobe e se torna o novo pai. O pai antigo (x) desce para a esquerda.
        """
        y = x.right
        T2 = y.left

        # Realiza a rotação
        y.left = x
        x.right = T2

        # Atualiza as alturas
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        self.rotation_count += 1
        return y

    def insert(self, value):
        """Interface pública para inserção. Inicia a recursão na raiz."""
        self.root, log = self._insert_node(self.root, value)
        if log:
            self.rotations_log.append(log)

    def _insert_node(self, root, value):
        """
        Método recursivo de inserção na AVL.
        Passo 1: Inserção padrão de Árvore Binária de Busca.
        Passo 2: Atualização de altura e rebalanceamento no retorno da recursão.
        """
        log = None
        
        # Passo 1: Inserção normal de BST
        if not root:
            return AVLNode(value), log
        elif value < root.value:
            root.left, log_left = self._insert_node(root.left, value)
            if log_left: log = log_left
        elif value > root.value:
            root.right, log_right = self._insert_node(root.right, value)
            if log_right: log = log_right
        else:
            # Valores duplicados não são permitidos nesta implementação
            return root, log 

        # Passo 2: Atualiza a altura do nó ancestral atual
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Passo 3: Obtém o fator de balanceamento para checar se ele se desbalanceou
        balance = self.get_balance(root)

        # Se o nó ficar desbalanceado, existem 4 casos:

        # Caso 1 - Esquerda Esquerda (LL)
        if balance > 1 and value < root.left.value:
            log = f"Rotação Simples à Direita (LL) em {root.value}"
            return self.right_rotate(root), log

        # Caso 2 - Direita Direita (RR)
        if balance < -1 and value > root.right.value:
            log = f"Rotação Simples à Esquerda (RR) em {root.value}"
            return self.left_rotate(root), log

        # Caso 3 - Esquerda Direita (LR)
        # Requer rotação dupla: primeiro à esquerda no filho, depois à direita na raiz
        if balance > 1 and value > root.left.value:
            log = f"Rotação Dupla (Esquerda-Direita) em {root.value}"
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root), log

        # Caso 4 - Direita Esquerda (RL)
        # Requer rotação dupla: primeiro à direita no filho, depois à esquerda na raiz
        if balance < -1 and value < root.right.value:
            log = f"Rotação Dupla (Direita-Esquerda) em {root.value}"
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root), log

        return root, log

    def min_value_node(self, root):
        """Encontra o nó de menor valor em uma dada árvore (o mais à esquerda possível)."""
        if root is None or root.left is None:
            return root
        return self.min_value_node(root.left)

    def delete(self, value):
        """Interface pública para remoção."""
        self.root, log = self._delete_node(self.root, value)
        if log:
            self.rotations_log.append(log)

    def _delete_node(self, root, value):
        """
        Método recursivo de remoção na AVL.
        Passo 1: Remoção padrão de Árvore Binária de Busca.
        Passo 2: Atualização de altura e rebalanceamento.
        """
        log = None
        
        # Passo 1: Remoção normal de BST
        if not root:
            return root, log

        elif value < root.value:
            root.left, log_left = self._delete_node(root.left, value)
            if log_left: log = log_left
        elif value > root.value:
            root.right, log_right = self._delete_node(root.right, value)
            if log_right: log = log_right
        else:
            # Nó com apenas um filho ou sem filhos
            if root.left is None:
                temp = root.right
                root = None
                return temp, log
            elif root.right is None:
                temp = root.left
                root = None
                return temp, log

            # Nó com dois filhos: Pega o sucessor in-order (menor da subárvore direita)
            temp = self.min_value_node(root.right)
            root.value = temp.value # Copia o valor
            # Deleta o sucessor
            root.right, log_right = self._delete_node(root.right, temp.value)
            if log_right: log = log_right

        if root is None:
            return root, log

        # Passo 2: Atualiza a altura do nó atual
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Passo 3: Obtém o balanço para rebalancear
        balance = self.get_balance(root)

        # Caso LL na remoção
        if balance > 1 and self.get_balance(root.left) >= 0:
            log = f"Rotação Direita (Delete LL) em {root.value}"
            return self.right_rotate(root), log

        # Caso LR na remoção
        if balance > 1 and self.get_balance(root.left) < 0:
            log = f"Rotação Dupla Esq-Dir (Delete LR) em {root.value}"
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root), log

        # Caso RR na remoção
        if balance < -1 and self.get_balance(root.right) <= 0:
            log = f"Rotação Esquerda (Delete RR) em {root.value}"
            return self.left_rotate(root), log

        # Caso RL na remoção
        if balance < -1 and self.get_balance(root.right) > 0:
            log = f"Rotação Dupla Dir-Esq (Delete RL) em {root.value}"
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root), log

        return root, log

    def get_node_count(self, node=None, is_root=True):
        """Conta quantos nós existem na árvore."""
        if is_root:
            node = self.root
        if not node:
            return 0
        return 1 + self.get_node_count(node.left, False) + self.get_node_count(node.right, False)

    def inorder(self, root=None, is_root=True):
        """Percurso Em Ordem: Esquerda -> Raiz -> Direita (Retorna valores ordenados)."""
        if is_root: root = self.root
        res = []
        if root:
            res = self.inorder(root.left, False)
            res.append(root.value)
            res = res + self.inorder(root.right, False)
        return res

    def preorder(self, root=None, is_root=True):
        """Percurso Pré-Ordem: Raiz -> Esquerda -> Direita."""
        if is_root: root = self.root
        res = []
        if root:
            res.append(root.value)
            res = res + self.preorder(root.left, False)
            res = res + self.preorder(root.right, False)
        return res

    def postorder(self, root=None, is_root=True):
        """Percurso Pós-Ordem: Esquerda -> Direita -> Raiz."""
        if is_root: root = self.root
        res = []
        if root:
            res = self.postorder(root.left, False)
            res = res + self.postorder(root.right, False)
            res.append(root.value)
        return res

    def search(self, value):
        """Busca O(log N) na árvore iterativamente."""
        current = self.root
        while current:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False
