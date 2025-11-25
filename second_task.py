import random

class PerfectHashMap:
    def __init__(self, keys):
        self.p = 1000000007  # Большое простое число для хеширования
        self.keys = list(set(keys))  # Убираем дубликаты — в идеале ключи уникальные
        self.n = len(self.keys)

        # Память под хеш-таблицу первого уровня:
        #    buckets[i] — это либо None, либо таблица второго уровня
        self.buckets = [None] * self.n

        # Для каждого бакета нужно хранить параметры хеша второго уровня
        self.secondary_params = [None] * self.n
        
        # Параметры хеша первого уровня
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)
        
        self.build()

    # Универсальная хеш-функция: (a*x + b mod p) mod m
    def _hash(self, key, a, b, m):
        return ((a * key + b) % self.p) % m

    def build(self):
        # -----------------------------
        # ШАГ 1 — распределяем ключи по корзинам
        # -----------------------------
        temp_buckets = [[] for _ in range(self.n)]

        for key in self.keys:
            idx = self._hash(key, self.a, self.b, self.n)
            temp_buckets[idx].append(key)

        # -----------------------------
        # ШАГ 2 — для каждой корзины строим идеальную таблицу второго уровня
        # -----------------------------
        for i, bucket in enumerate(temp_buckets):
            if not bucket:
                continue  # корзина пустая — пропускаем

            k = len(bucket)
            # Размер таблицы второго уровня = k^2
            # Это гарантирует возможность найти хеш без коллизий
            m_sub = k * k

            found = False

            # Подбираем a_sub, b_sub ПОВТОРНО,
            # пока внутри корзины не исчезнут коллизии
            while not found:
                a_sub = random.randint(1, self.p - 1)
                b_sub = random.randint(0, self.p - 1)

                # Таблица второго уровня
                sub_table = [None] * m_sub
                collision = False

                # Пытаемся разложить ключи без коллизий
                for item in bucket:
                    h = self._hash(item, a_sub, b_sub, m_sub)

                    # Если уже занято — коллизия, пробуем заново
                    if sub_table[h] is not None:
                        collision = True
                        break

                    sub_table[h] = item

                # Если коллизий нет — успех
                if not collision:
                    self.buckets[i] = sub_table
                    self.secondary_params[i] = (a_sub, b_sub, m_sub)
                    found = True

    # Поиск ключа в идеальной хеш-таблице
    def get(self, key):
        # Первый уровень — ищем бакет
        idx = self._hash(key, self.a, self.b, self.n)

        if self.buckets[idx] is None:
            return None

        # Второй уровень — ищем позицию внутри таблицы бакета
        a_sub, b_sub, m_sub = self.secondary_params[idx]
        h = self._hash(key, a_sub, b_sub, m_sub)

        val = self.buckets[idx][h]

        # Проверяем, совпал ли ключ (идеальная таблица, но всё равно проверяем)
        return val if val == key else None


# Пример
phm = PerfectHashMap([10, 25, 30, 55, 105])
print(phm.get(55))  # 55
print(phm.get(99))  # None
