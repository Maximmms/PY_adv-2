import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv

PHONE_INDEX = 5

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
#Задание 1
for contact in contacts_list[1:]:
    parts = " ".join(contact[:3]).split()
    contact[0] = parts[0].strip()
    contact[1] = parts[1].strip() if len(parts) > 1 else ""
    contact[2] = parts[2].strip() if len(parts) > 2 else ""

#Задание 2
pattern_list = [
    # Номера со скобками
    r"(\+7|8)\s*\((\d{3})\)\s*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})",
    # Номера без скобок
    r"(\+7|8)[\s\-]?(\d{3})[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})",
]

for contact in contacts_list[1:]:
    if contact[PHONE_INDEX]:
        # Обрабатываем основной номер
        for pattern in pattern_list:
            new_phone = re.sub(pattern, r"+7(\2)\3-\4-\5", contact[PHONE_INDEX])
            if new_phone != contact[PHONE_INDEX]:  # Если замена произошла
                contact[PHONE_INDEX] = new_phone
                break

        # Обрабатываем добавочный номер (убираем лишние пробелы и скобки)
        contact[PHONE_INDEX] = re.sub(
            r"\s*\(?\s*доб\.\s*(\d+)\s*\)?",  # Ищем "доб." с пробелами и скобками
            r" доб.\1",  # Заменяем на " доб.0792"
            contact[PHONE_INDEX]
        ).strip()  # Удаляем пробелы в начале/конце, если есть


#Задание 3

def is_same_person(person1, person2):
    """Проверяет, относятся ли две записи к одному человеку."""
    # Фамилия должна совпадать (если не пустая в обеих записях)
    if person1[0] and person2[0] and person1[0] != person2[0]:
        return False

    # Имя должно совпадать (если не пустое в обеих записях)
    if person1[1] and person2[1] and person1[1] != person2[1]:
        return False

    # Отчество должно совпадать (если не пустое в обеих записях)
    if person1[2] and person2[2] and person1[2] != person2[2]:
        return False

    return True


def merge_people(person1, person2):
    """Объединяет две записи о человеке, сохраняя непустые значения."""
    merged = []
    for i in range(len(person1)):
        if person1[i]:
            merged.append(person1[i])
        else:
            merged.append(person2[i])
    return merged


def merge_records(data):
    merged = []

    for current in data:
        found = False
        for i, existing in enumerate(merged):
            if is_same_person(current, existing):
                merged[i] = merge_people(existing, current)
                found = True
                break

        if not found:
            merged.append(current)

    return merged

contacts_list =  sorted(merge_records(contacts_list[1:]))

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(contacts_list)