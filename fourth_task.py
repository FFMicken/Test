import heapq

def sort_k_sorted_array(arr, k):
    n = len(arr)
    if n == 0: return []
    
    # 1. Создаем кучу из первых k+1 элементов
    # Это "окно", в котором гарантированно находится минимальный элемент
    heap = arr[:k+1]
    heapq.heapify(heap)
    
    target_index = 0
    
    # 2. Проходим по оставшимся элементам
    for i in range(k + 1, n):
        # Извлекаем минимум из кучи и ставим на верное место
        arr[target_index] = heapq.heappop(heap)
        # Добавляем следующий элемент из массива в кучу
        heapq.heappush(heap, arr[i])
        target_index += 1
        
    # 3. Достаем остатки из кучи
    while heap:
        arr[target_index] = heapq.heappop(heap)
        target_index += 1
        
    return arr

# Пример
# Элемент 2 смещен на 2 позиции (был индексом 2, станет 0)
data = [6, 5, 3, 2, 8, 10, 9] 
k = 3
sorted_data = sort_k_sorted_array(data, k)
print(sorted_data) # [2, 3, 5, 6, 8, 9, 10]