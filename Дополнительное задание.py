#Подключаем библиотеки
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def selector():
    #Считываем варианты
    year=asker(5)
    #Для удобства заводим список
    lst=['khl_2008_09.csv','khl_2009_10.csv','khl_2010_11.csv','khl_2011_12.csv','khl_2012_13.csv']
    #
    #Считываем файл .csv , задаем кодировку UTF-8, обозначаем что 0я строка - заголовки, индексация по дате, разделитель в файле .csv это","
    dtframe=pd.read_csv(lst[year],encoding="UTF-8",header=0,index_col="Дата",parse_dates=True,sep=',')
    return [dtframe,year]

#функция запроса и проверки года
def asker(n):
    #Выводится предложение ввести год
    #Год запрашивается
    for i in range(5):
        try:
            year=input()
            if (year=="exit"):sys.exit()
            else: year=int(year)
            #Перебор
            for i in range(n):
                #Проверяем отсутствие в списке
                if (year not in range(5)):
                    #Зададим попытки
                    if (i!=5):
                        #Выведем сообщение о кол-ве попыток
                        print("Неверный формат!\nВведите число от 0 до ",5,"\nПопыток осталось ",5-i)
                        #Повторный запрос
                        year=int(input())
                        print(year)
                        #Если попытки закончились
                    else:
                        #Выходим
                        sys.exit()
                #Если в списке
                else:
                    #Возвращает год
                    return year
        except ValueError:
            print("Вы не ввели число!")
        sys.exit()



def washer_counter(team,number):
    win = np.array([0,0,0])
    lose = np.array([0,0,0])
    if (number == 2):
        for index,row in team.iterrows():
            win[0]+=int(row["Период_1"][0])
            win[1]+=int(row["Период_2"][0])
            win[2]+=int(row["Период_3"][0])
            lose[0]+=int(row["Период_1"][2])    
            lose[1]+=int(row["Период_2"][2])
            lose[2]+=int(row["Период_3"][2])
    else:
        for index,row in team.iterrows():
            win[0]+=int(row["Период_1"][2])
            win[1]+=int(row["Период_2"][2])
            win[2]+=int(row["Период_3"][2])
            lose[0]+=int(row["Период_1"][0])    
            lose[1]+=int(row["Период_2"][0])
            lose[2]+=int(row["Период_3"][0])
    return[win,lose]

def print_graph(sha_in,sha_out,team): 
    fig_1=plt.figure(figsize=(6,4)) #задание области фигуры
    fig_2=plt.figure(figsize=(6,4)) #задание области фигуры
    ax_1 = fig_1.add_subplot() #добавление области отображения диаграммы
    ax_2 = fig_2.add_subplot() #добавление области отображения диаграммы
    vals_1=[sha_in[0],sha_in[1],sha_in[2]] #список ошибок и кол-ва файлов
    labels_1=['Период 1','Период 2','Период 3'] #заголовки
    vals_2=[sha_out[0],sha_out[1],sha_out[2]] #список ошибок и кол-ва файлов
    labels_2=['Период 1','Период 2','Период 3'] #заголовки

    ax_1.pie(vals_1,labels=labels_1, autopct='%1.1f%%') #входные данные в диограмму, значения отображаются в виде %
    ax_1.grid() #не особо влияет, но занимает мин пространство для диаграммы
    ax_1.set_title("Шайбы,забитые командой "+team)
    ax_2.pie(vals_2,labels=labels_2, autopct='%1.1f%%') #входные данные в диограмму, значения отображаются в виде %
    ax_2.grid() #не особо влияет, но занимает мин пространство для диаграммы
    ax_2.set_title("Шайбы, пропущенные командой "+team)
    plt.show() #вывод дограммы           

print("Выбираем сезон:\n\t 0:2008-2009года \n\t 1:2009-2010года \n\t 2:2010-2011года \n\t 3:2011-2012года \n\t 4:2012-2013года")
select = selector()
df = select[0]
year = select[1]
print("\nВведите название команды:")
team = input()
df_team_first = df[df['Команда_1']==team]
df_team_second = df[df['Команда_2']==team]

win = washer_counter(df_team_first,1)
lose = washer_counter(df_team_second,2)

total_win = win[0]+lose[0]
total_lose = win[1]+lose[1]
print_graph(total_win,total_lose,team)





        
