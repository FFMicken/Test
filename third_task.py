class BrokenHeap:
    def __init__(self):
        self.heap = []
        self.k = 3  # каждый узел имеет 3 детей: left, mid, right

    # Поменять элементы местами
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Вставка: кладём в конец и поднимаем
    def insert(self, value):
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    # Извлечение корня: ставим последний элемент в корень и опускаем его
    def extract_root(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return root

    # Подъём элемента вверх по твоим нестандартным правилам
    def _sift_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // self.k   # формула родителя в k-куче

            # Тип ребёнка:
            # 0 = левый, 1 = средний, 2 = правый
            child_type = (idx - 1) % self.k

            p_val = self.heap[parent]
            c_val = self.heap[idx]
            should_swap = False

            # Левый ребёнок → он должен быть БОЛЬШЕ родителя
            # (если нет → меняем местами)
            if child_type == 0:
                if p_val > c_val:
                    should_swap = True

            # Средний и правый → должны быть МЕНЬШЕ родителя
            # (если нет → меняем местами)
            else:
                if p_val < c_val:
                    should_swap = True

            if should_swap:
                self._swap(parent, idx)
                idx = parent
            else:
                break

    # Опускание вниз: проверяем все три подчинённых
    def _sift_down(self, idx):
        n = len(self.heap)
        while True:
            # Индексы детей
            left  = 3 * idx + 1
            mid   = 3 * idx + 2
            right = 3 * idx + 3

            target = idx

            # Проверяем нарушения правил:

            # 1. Левый ребёнок должен быть БОЛЬШЕ родителя
            # если родитель > левый → нарушение, надо поменять
            if left < n and self.heap[target] > self.heap[left]:
                target = left

            # 2. Средний должен быть МЕНЬШЕ родителя
            # если родитель < средний → нарушение
            if mid < n:
                if self.heap[idx] < self.heap[mid]:
                    target = mid

            # 3. Правый также должен быть МЕНЬШЕ родителя
            if right < n:
                if self.heap[idx] < self.heap[right]:
                    target = right

            # Если нашли нарушение — меняем и продолжаем
            if target != idx:
                self._swap(idx, target)
                idx = target
            else:
                break


# Пример
bh = BrokenHeap()
for x in [10, 5, 20, 15, 30]:
    bh.insert(x)

print(bh.heap)
