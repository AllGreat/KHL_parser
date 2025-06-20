

import pandas as pd

Season = int(input('Выберите сезон:\n1 - 2008-2009\n2 - 2009-2010\n3 - 2010-2011\n4 - 2011-2012\n5 - 2012-2013\nВведите соответствующую цифру: '))
SEason = Season
if Season == 1:                                     # |
    Season = 'khl_2008_09.csv'                       # |
elif Season == 2:                                   # |
    Season = 'khl_2009_10.csv'                      # |
elif Season == 3:                                   # |  В зависимости от введенной пользователем цифры записываем в переменную название файла с нужным сезоном
    Season = 'khl_2010_11.csv'                      # |
elif Season == 4:                                   # |
    Season = 'khl_2011_12.csv'                      # |
elif Season == 5:                                   # |
    Season = 'khl_2012_13.csv'                      # |
else:
     print('Ошибка! Введены неверные данные!')   # Сообщаем пользователю об ошибке, в случае, если данные введены неверно)  

df = pd.read_csv(Season, sep=',') # Считываем данные с соответствующего файла

def get_score_left(score): # Функция необходимая для обработки забитых шайб где команда слева
    temp = score.split(":")
    if temp[0] != "": return int(temp[0]) - int(temp[1]) # Проверка на то, что счёт не является " : " 
    return 0



def get_score(score): # Функция необходимая для обработки забитых шайб
    temp = score.split(":")
    if temp[0] != "": return [int(i) for i in temp] # Проверка на то, что счёт не является " : " 
    return [0,0]

goals_left = pd.DataFrame({"команда": df['Команда_1']}) 
# Формируем таблицу забитых шайб для левых команд (столбцы со словом "лев" - забитые командой)

goals_left["основа лев"] = df["Период_1"].apply(lambda x: get_score(x)[0]) + df["Период_2"].apply(lambda x: get_score(x)[0]) + df["Период_3"].apply(lambda x: get_score(x)[0])
goals_left["основа прав"] = df["Период_1"].apply(lambda x: get_score(x)[1]) + df["Период_2"].apply(lambda x: get_score(x)[1]) + df["Период_3"].apply(lambda x: get_score(x)[1])
# Получаем голы за основное время складывая 3 периода
goals_left["овертайм лев"] = df["Овертайм"].apply(lambda x: get_score(x)[0])  # | Т.к. функция возвращает массив двух элементов
goals_left["овертайм прав"] = df["Овертайм"].apply(lambda x: get_score(x)[1]) # | для забитых шайб берём первое значение
goals_left["буллиты лев"] = df["Буллиты"].apply(lambda x: get_score(x)[0])    # | для пропущеных второе
goals_left["буллиты прав"] = df["Буллиты"].apply(lambda x: get_score(x)[1])

goals_right = pd.DataFrame({"команда": df['Команда_2']})
# Формируем таблицу забитых шайб для правых команд (столбцы со словом "лев" - забитые командой)

goals_right["основа прав"] = df["Период_1"].apply(lambda x: get_score(x)[0]) + df["Период_2"].apply(lambda x: get_score(x)[0]) + df["Период_3"].apply(lambda x: get_score(x)[0])
goals_right["основа лев"] = df["Период_1"].apply(lambda x: get_score(x)[1]) + df["Период_2"].apply(lambda x: get_score(x)[1]) + df["Период_3"].apply(lambda x: get_score(x)[1])
# Получаем голы за основное время складывая 3 периода
goals_right["овертайм прав"] = df["Овертайм"].apply(lambda x: get_score(x)[0]) # | Из-за зеркального расположения счёта
goals_right["овертайм лев"] = df["Овертайм"].apply(lambda x: get_score(x)[1])  # | из функции для забитых шайб берём второе значение
goals_right["буллиты прав"] = df["Буллиты"].apply(lambda x: get_score(x)[0])   # | для пропущеных первое
goals_right["буллиты лев"] = df["Буллиты"].apply(lambda x: get_score(x)[1])

goals = pd.concat([goals_left, goals_right]) # Получаем единую таблицу голов для каждой команды в каждой игре
print(goals)
goals["разница"] = sum([goals.iloc[:,i] for i in range(1,7,2)]) - sum([goals.iloc[:,i] for i in range(2,7,2)]) 
goals["забитые"] = sum([goals.iloc[:,i] for i in range(1,7,2)])


result = pd.DataFrame({"команда": goals["команда"]}) # Создаём новую таблицу для подсчёта количества побед и поражений

result['основа В'] = goals[["основа лев","основа прав"]].apply(lambda x: int(x[0] > x[1]), axis=1) # | Сравнивая счёт получаем 1 или 0 в зависимости
result['основа П'] = goals[["основа лев","основа прав"]].apply(lambda x: int(x[0] < x[1]), axis=1) # | победила команда или проиграла соответственно

result['овертайм В'] = goals[["овертайм лев","овертайм прав"]].apply(lambda x: int(x[0] > x[1]), axis=1)
result['овертайм П'] = goals[["овертайм лев","овертайм прав"]].apply(lambda x: int(x[0] < x[1]), axis=1)

result['буллиты В'] = goals[["буллиты лев","буллиты прав"]].apply(lambda x: int(x[0] > x[1]), axis=1)
result['буллиты П'] = goals[["буллиты лев","буллиты прав"]].apply(lambda x: int(x[0] < x[1]), axis=1)

result = result.groupby(["команда"]).sum() # Получим сумму побед и поражений на каждом этапе игры для каждой команды
result["очки"] = result.apply(lambda x: x[0]*3 + x[1]*0 + x[2]*2 + x[3]*1 + x[4]*2 + x[5]*1, axis=1) # Добавим в таблицу подсчёт очков
result["игр"] = goals.groupby(["команда"]).count().iloc[:,0] # Подсчитаем общее количество игр сыгранных каждой командой

goals = goals.groupby(["команда"]).sum() # Получим общее число голов сделанное каждой командой на каждом этапе игры


output = pd.DataFrame({ # Создадим новую таблицу для правильного представления на выходе
    "И": result["игр"],
    "В": result["основа В"],
    "ВО": result["овертайм В"],
    "ВБ": result["буллиты В"],
    "ПБ": result["буллиты П"],
    "ПО": result["овертайм П"],
    "П": result["основа П"],
    "Ш": goals.apply(lambda x: f"{sum(x[0::2])}:{sum(x[1::2])}", axis=1),
    "О": result["очки"],
    "разница": goals["разница"],
    "забитые": goals["забитые"]
})  
# забитые
output = output.sort_values(['О', "В", "разница", "забитые"], ascending=[False, False, False, False]) # Отсортируем таблицу по итоговым очкам в убывающем порядке
print(output.iloc[:,0:-2])

SEason = int(SEason)

# Выписан список западной конференции
if SEason == 1:
    konf_zapad  = ["Витязь", "СКА", "Сочи", "Спартак", "Торпедо НН", "Динамо Мн", "Динамо Р", "Динамо М", "Торпедо", "Кунльлунь", "Локомотив", "Северсталь", "ЦСКА", "ХК МВД", "Атлант"]
elif SEason == 2:
    konf_zapad  = ["Витязь", "СКА", "Спартак", "Торпедо НН", "Динамо Мн", "Динамо Р", "Динамо М", "Торпедо", "Кунльлунь", "Локомотив", "Северсталь", "ЦСКА", "Атлант"]    
elif SEason == 3:
    konf_zapad  = ["Лев ПП", "Витязь", "СКА", "Спартак", "Торпедо НН", "Динамо Мн", "Динамо Р", "Динамо М", "Торпедо", "Северсталь", "ЦСКА", "Атлант"]
elif SEason == 4:
    konf_zapad = ["Лев ПП", "Витязь", "СКА", "Спартак", "Локомотив", "Торпедо НН", "Динамо Мн", "Динамо Р", "Динамо М", "Торпедо", "Северсталь", "ЦСКА", "Атлант"]
elif SEason == 5:
    konf_zapad = ["Донбасс", "Лев Пр", "Слован", "Локомотив" "Витязь", "СКА", "Спартак", "Торпедо НН", "Динамо Мн", "Динамо Р", "Динамо М", "Торпедо", "Северсталь", "ЦСКА", "Атлант"]

# | Создаём отдельные таблицы для каждой конференции. В квадратных скобках получаем список из пересекающихся элементов в
# | списке конференции запад и текущей таблицы. Для востока снова берём список индексов и исключаем пересечение (западные команды).
# | Т.к. элементы неодинаковы - использован класс set только по причине возможности использовать булевы операторы.
#
# После получения списка команд получаем таблицу с помощью функции loc.

output_vostok = output.loc[list(set(konf_zapad) & set(output.index) ^ set(output.index))]
output_zapad = output.loc[list(set(konf_zapad) & set(output.index))]

output_vostok = output_vostok.sort_values(['О', "В", "разница", "забитые"], ascending=[False, False, False, False]) # Снова сортируем от большего к меньшему
output_zapad = output_zapad.sort_values(['О', "В", "разница", "забитые"], ascending=[False, False, False, False])

print(f"\n\nВосточная конференция\n\n{output_vostok.iloc[:,0:-2]}")
print(f"\n\nЗападная конференция\n\n{output_zapad.iloc[:,0:-2]}")
