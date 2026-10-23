import math
from typing import List,Optional
class FeedForwardLearning:
    def __init__(self, max_sp:float, num_ranges:int=5, learning_rate:float=0.2):
        """
        Инициализация системы упреждения (Feed-Forward Learning).
        
        :param num_ranges: Количество геометрических диапазонов для уставки
        :param learning_rate: Коэффициент скорости обучения (альфа: от 0.0 до 1.0)
        """
        self.max_sp = float(max_sp)
        self.num_ranges = int(num_ranges)
        self.learning_rate = float(learning_rate)
        
        # Нам больше не нужен жесткий max_target для генерации границ.
        # Мы можем привязать границы диапазонов к физике нарастания дозы относительно макс. упреждения.
        # Для универсальности будем считать, что уставки масштабируются динамически,
        # а диапазоны мы определим как нормированные коэффициенты от 0.0 до 1.0.
        self.range_factors = self._generate_geometric_factors()
        
        # Хранилище обученных значений упреждения для каждого диапазона.
        # Изначально они заполнены None. Это маркер того, что диапазон еще НЕ ИСПЫТАН (нужен пробный замес).
        self.trained_ff:List[Optional[float]] = [None] * self.num_ranges

    def _generate_geometric_factors(self):
        """Генерирует геометрическую (экспоненциальную) шкалу распределения диапазонов от 0.0 до 1.0"""
        factors = []
        for i in range(1, self.num_ranges):
            fraction = i / self.num_ranges
            # Экспоненциальное сгущение сетки
            val = (1.0 - math.exp(-2 * fraction)) / (1 - math.exp(-2))
            factors.append(1.0-round(val, 3))
        factors.reverse( )
        return factors

    def _get_range_index(self, target_weight):
        """
        Определяет индекс диапазона для текущей уставки.
        Масштабирует уставку относительно условного ориентира, 
        мы используем отношение max_sp к дозе.
        Чем больше доза относительно max_sp, тем выше индекс диапазона.
        """
        normalized_target = min(target_weight / self.max_sp, 1.0)
        
        for index, factor in enumerate(self.range_factors):
            if normalized_target <= factor:
                return index
        return self.num_ranges - 1

    def ff_for(self, target_weight,min_ff:float,max_ff:float):
        """
        Запрос значения упреждения перед началом дозирования.
        
        Возвращает значение_упреждения
        Если для этого диапазона еще нет данных (None), включается режим сверх осторожного недосыпа (20%).
        """
        idx = self._get_range_index(target_weight)
        trained_val = self.trained_ff[idx]
        
        if trained_val is None:
            return (min_ff + max_ff)/2
        
        # ДИАПАЗОН ОБУЧЕН: Выдаем точное боевое значение
        return trained_val

    def update_learning(self, target_weight, actual_weight, min_ff:float, max_ff:float, last_cutoff_weight=None):
        """
        Алгоритм фиксации данных и самообучения. Вызывается строго ПОСЛЕ стабилизации веса.
        
        :param min_ff: минимальное упреждение
        :param max_ff: максимальное упреждение
        :param target_weight: Целевой вес (уставка)
        :param actual_weight: Фактический вес, зафиксированный весами в конце
        :param last_cutoff_weight: На каком фактическом весе ПЛК реально закрыл заслонку (опционально)
        """
        idx = self._get_range_index(target_weight)
        trained_val = self.trained_ff[idx]
        
        # Если это был первый пробный замес (у нас не было данных в trained_advances)
        if trained_val is None:
            if last_cutoff_weight is not None:
                # Идеальный вариант: мы точно знаем, на каком весе закрылись.
                # Летящий столб = Фактический финальный вес минус вес в момент отсечки.
                measured_column = actual_weight - last_cutoff_weight
            else:
                # Если ПЛК не передал точку отсечки, вычисляем её через выданное ранее упреждение
                predicted_advance = self.ff_for(target_weight,min_ff,max_ff)
                measured_column = actual_weight - (target_weight - predicted_advance)
            
            # Валидируем полученный столб физическими границами класса
            measured_column = max(min(min_ff,max_ff), min(measured_column, max(max_ff,min_ff)))
            
            # Сохраняем как базовую "нулевую точку" диапазона. Первый замес успешно обучен!
            self.trained_ff[idx] = round(measured_column, 2)
            return self.trained_ff[idx]

        # Если это ОЧЕРЕДНОЙ (рабочий) замес — применяем экспоненциальное сглаживание
        error = actual_weight - target_weight  # Пересып > 0, недосып < 0
        
        # Корректируем упреждение: при пересыпе увеличиваем его, чтобы закрываться раньше
        new_advance = trained_val + (self.learning_rate * error)
        
        # Строго удерживаем самообучение в физических границах железа
        new_advance = max(min(min_ff,max_ff), min(new_advance, max(max_ff,min_ff)))
        
        self.trained_ff[idx] = round(new_advance, 2)
        return self.trained_ff[idx]
    
if __name__=='__main__':
    """эксперименты по использованию"""
    learn = FeedForwardLearning(1500)
    print([round(1500*x,2) for x in learn.range_factors])

    learn.update_learning(760,765,0,500)
    learn.update_learning(760,770,0,500)
    sp = 0
    while sp<2000:
        sp+=100
        print(sp,learn._get_range_index(sp),learn.ff_for(sp,0,500))
