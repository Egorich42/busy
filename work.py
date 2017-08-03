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

b = cur.execute("""

UPDATE bank
SET summ = '99999999'
""").fetchall()
conn.commit()


b = cur.execute("""
SELECT *
FROM tn;
""").fetchall()

print(b)

# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ


# Не забываем закрыть соединение с базой данных
conn.close()
