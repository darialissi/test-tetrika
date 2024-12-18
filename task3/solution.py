def normalize(groups: list[tuple[int]]) -> list[tuple[int]]:
    """
    Нормализует интервалы, исключая субинтервалы
    """
    result = []

    current = [groups[0][0], groups[0][1]]

    for group in groups[1:]:
        if group[0] <= current[1]:
            current[0] = min(group[0], current[0])
            current[1] = max(group[1], current[1])
        else:
            result.append(current)
            current = [group[0], group[1]]

    result.append(current)

    return result


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals.get("lesson")
    pupil = intervals.get("pupil")
    tutor = intervals.get("tutor")

    result = 0

    if not pupil or not tutor:
        return result

    # Интервалы в кортежах
    p_groups = normalize(list(zip(pupil[::2], pupil[1::2])))
    t_groups = normalize(list(zip(tutor[::2], tutor[1::2])))

    # Указатели на кортежи
    i1, i2 = 0, 0

    # Текущий общий интервал
    current = [0, 0]

    while i1 < len(p_groups) and i2 < len(t_groups):

        # Начало общего интервала
        current[0] = max(p_groups[i1][0], t_groups[i2][0])

        # Конец общего интервала
        if p_groups[i1][1] < t_groups[i2][1]:
            current[1] = p_groups[i1][1]
            i1 += 1
        elif p_groups[i1][1] > t_groups[i2][1]:
            current[1] = t_groups[i2][1]
            i2 += 1
        else:
            current[1] = t_groups[i2][1]
            i1 += 1
            i2 += 1

        # Краевые значения
        if current[0] < lesson[0]:
            current[0] = lesson[0]
        if current[1] > lesson[1]:
            current[1] = lesson[1]

        # Проверка валидности интервала
        if current[0] < current[1]:
            result += current[1] - current[0]

    return result
