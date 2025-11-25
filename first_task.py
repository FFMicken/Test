class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None      # Левый ребёнок
        self.right = None     # Правый ребёнок
        self.height = 1       # Высота поддерева
        self.size = 1         # Количество элементов в поддереве (для индексов)


class AVLArray:
    # Получить размер поддерева
    def get_size(self, node):
        return node.size if node else 0

    # Получить высоту поддерева
    def get_height(self, node):
        return node.height if node else 0

    # Пересчитать height и size узла
    def update(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left),
                                   self.get_height(node.right))
            node.size = 1 + self.get_size(node.left) + self.get_size(node.right)

    # Правый поворот вокруг y
    #      y            x
    #     / \    →     / \
    #    x   C        A   y
    #   / \              / \
    #  A   B            B   C
    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self.update(y)
        self.update(x)
        return x

    # Левый поворот вокруг x
    #    x               y
    #   / \     →       / \
    #  A   y           x   C
    #     / \         / \
    #    B   C       A   B
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self.update(x)
        self.update(y)
        return y

    # Балансировка узла (AVL property)
    def balance(self, node):
        self.update(node)
        balance = self.get_height(node.left) - self.get_height(node.right)

        # Левое поддерево тяжелее
        if balance > 1:
            # LL-случай
            if self.get_height(node.left.left) >= self.get_height(node.left.right):
                return self.rotate_right(node)
            # LR-случай
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        # Правое поддерево тяжелее
        if balance < -1:
            # RR-случай
            if self.get_height(node.right.right) >= self.get_height(node.right.left):
                return self.rotate_left(node)
            # RL-случай
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    # Вставка value в позицию index (как в массив)
    def insert_at_index(self, node, index, value):
        # Если пришли в пустую позицию — создаём узел
        if not node:
            return AVLNode(value)

        left_size = self.get_size(node.left)

        # Идём влево, если индекс попадает в левое поддерево
        if index <= left_size:
            node.left = self.insert_at_index(node.left, index, value)
        # Иначе в правое поддерево (учитываем текущий узел)
        else:
            node.right = self.insert_at_index(node.right,
                                              index - left_size - 1,
                                              value)

        return self.balance(node)

    # Удаление элемента по индексу
    def delete_at_index(self, node, index):
        if not node:
            return None

        left_size = self.get_size(node.left)

        # Идём влево
        if index < left_size:
            node.left = self.delete_at_index(node.left, index)

        # Идём вправо
        elif index > left_size:
            node.right = self.delete_at_index(node.right,
                                              index - left_size - 1)

        # Нашли нужный узел
        else:
            # Один ребёнок → возвращаем его
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            # Два ребёнка → ищем минимальный в правом поддереве
            temp = node.right
            while temp.left:
                temp = temp.left

            # Меняем значения
            node.value = temp.value

            # Удаляем преемника
            node.right = self.delete_at_index(node.right, 0)

        return self.balance(node)

    # Получение значения по индексу (как array[index])
    def get_value_at_index(self, node, index):
        if not node:
            return None

        left_size = self.get_size(node.left)

        if index == left_size:
            return node.value
        elif index < left_size:
            return self.get_value_at_index(node.left, index)
        else:
            return self.get_value_at_index(node.right,
                                           index - left_size - 1)


# Пример
root = None
avl = AVLArray()

# Добавляем как push_back
for val in [10, 20, 30]:
    root = avl.insert_at_index(root, avl.get_size(root), val)

# Вставка в середину
root = avl.insert_at_index(root, 1, 15)

print(avl.get_value_at_index(root, 1))  # 15

# Удаление элемента по индексу
root = avl.delete_at_index(root, 1)
print(avl.get_value_at_index(root, 1)) 
