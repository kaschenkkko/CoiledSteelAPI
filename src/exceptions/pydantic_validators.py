def validate_range_pairs(values):
    """Валидация параметров диапазона.

    - Проверяем, что передаются пары только одного параметра.
    - Проверяем пары на целостность, чтобы не допускать только значения min,
      или только значения max.
    - Проверяем что передано одинаковое количество параметров (num min = num max).
    - Проверяем, что min не больше max в каждой паре значений.
    """
    filters = {
        'id': ('min_id', 'max_id'),
        'length': ('min_length', 'max_length'),
        'weight': ('min_weight', 'max_weight'),
        'created_at': ('min_created_at', 'max_created_at'),
        'deleted_at': ('min_deleted_at', 'max_deleted_at'),
    }
    used_filters = [key for key, (min_f, max_f) in filters.items() if
                    values.get(min_f) or values.get(max_f)]

    if not used_filters:
        return values

    if len(used_filters) > 1:
        raise ValueError('Фильтрация возможна только по одному параметру')

    selected_filter = used_filters[0]
    min_f, max_f = filters[selected_filter]
    min_vals = values.get(min_f)
    max_vals = values.get(max_f)

    if (min_vals and not max_vals) or (max_vals and not min_vals):
        raise ValueError(f'Необходимо передавать оба параметра {min_f} и {max_f}')

    if len(min_vals) != len(max_vals):
        raise ValueError(f'Разное количество пар min-max для {min_f}')

    for min_v, max_v in zip(min_vals, max_vals, strict=False):
        if min_v > max_v:
            raise ValueError(f'Значение {min_f} не может быть больше {max_f}')

    return values
