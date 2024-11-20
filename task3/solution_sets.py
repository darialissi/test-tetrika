def normalize(groups: list[tuple]) -> list[tuple]:
    """
    Нормализует интервалы, исключая субинтервалы.
    Вспомогательная (необязательная) функция, сокращает расходы по памяти.
    """
    result = []

    current = [groups[0][0], groups[0][1]]

    for group in groups:
        if group[0] < current[1]:
            if group[0] < current[0]:
                current[0] = group[0]
            if group[1] > current[1]:
                current[1] = group[1]
        else:
            result.append(current)
            current = [group[0], group[1]]

    result.append(current)

    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals.get("lesson")
    pupil = intervals.get("pupil")
    tutor = intervals.get("tutor")

    if not pupil or not tutor:
        return 0

    # Интервалы в кортежах
    pupil_groups = normalize(list(zip(pupil[::2], pupil[1::2])))
    tutor_groups = normalize(list(zip(tutor[::2], tutor[1::2])))

    # Множества интервалов
    pupil_set = set()
    tutor_set = set()
    lesson_set = set(range(lesson[0], lesson[1]))

    for group in pupil_groups:
        pupil_set.update(range(group[0], group[1]))

    for group in tutor_groups:
        tutor_set.update(range(group[0], group[1]))

    # Пересечение всех множеств
    common_time = pupil_set.intersection(tutor_set).intersection(lesson_set)
    
    return len(common_time)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'