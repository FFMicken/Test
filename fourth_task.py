class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        # Переносим последний элемент в корень и просеиваем вниз
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _sift_up(self, idx):
        # Пока элемент меньше родителя, меняем их местами
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        n = len(self.heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            # Ищем меньшего среди детей
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != idx:
                self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
                idx = smallest
            else:
                break
    
    def __len__(self):
        return len(self.heap)

def sort_k_sorted_array(arr, k):
    n = len(arr)
    heap = MinHeap()
    
    # Результирующий индекс, куда будем класть отсортированные элементы
    target_idx = 0
    
    # 1. Заполняем кучу первыми k+1 элементами
    # В "почти отсортированном" массиве минимальный элемент 
    # гарантированно находится в диапазоне [0, k]
    for i in range(min(n, k + 1)):
        heap.push(arr[i])
        
    # 2. Скользящее окно: достаем минимум, добавляем следующий элемент массива
    for i in range(k + 1, n):
        arr[target_idx] = heap.pop()
        target_idx += 1
        heap.push(arr[i])
        
    # 3. Достаем всё, что осталось в куче
    while len(heap) > 0:
        arr[target_idx] = heap.pop()
        target_idx += 1
        
    return arr

# --- Тестирование ---
# Элементы смещены не более чем на 3 позиции
data = [6, 5, 3, 2, 8, 10, 9]
k = 3

print(f"Исходный массив: {data}")
sort_k_sorted_array(data, k)
print(f"Отсортированный: {data}") 
# Ожидается: [2, 3, 5, 6, 8, 9, 10]