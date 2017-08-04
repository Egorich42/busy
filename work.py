import sqlite3

#https://ru.stackoverflow.com/questions/224243/Как-в-python-программно-создать-новую-базу-данных-и-выполнить-в-ней-скрипт

#https://habrahabr.ru/post/321510/

#https://habrahabr.ru/post/305926/

#https://www.site-do.ru/db/sql3.php

#https://habrahabr.ru/post/123636/

#https://www.site-do.ru/db/sql3.php

conn = sqlite3.connect('1.sqlite')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cur = conn.cursor()


kontr2= cur.execute("""
SELECT *
FROM tn;
""").fetchall()


conn.close()
kontr = [list(elem) for elem in kontr2]


cols = [column[0] for column in cur.description]


res = []
for row in kontr:
    res += [{col.lower():value for col,value in zip(cols,row)}] 





print(res)


# Не забываем закрыть соединение с базой данных
conn.close()
