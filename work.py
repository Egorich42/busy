import sqlite3

#https://ru.stackoverflow.com/questions/224243/Как-в-python-программно-создать-новую-базу-данных-и-выполнить-в-ней-скрипт

#https://habrahabr.ru/post/321510/

#https://habrahabr.ru/post/305926/

#https://www.site-do.ru/db/sql3.php

#https://habrahabr.ru/post/123636/

#https://www.site-do.ru/db/sql3.php

conn = sqlite3.connect('bas.sqlite')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cur = conn.cursor()




cur.execute("""
UPDATE users 
SET ostatok = '99999999'
WHERE id=1;
""")


cur.execute("""
UPDATE users 
SET ostatok = '1111111111'
WHERE id=2;
""")


cur.execute("""
UPDATE users 
SET ostatok = '678543121212'
WHERE id=3;
""")


cur.execute("""
UPDATE users 
SET ostatok = '333333333333333'
WHERE id=4;
""")

a = cur.execute("""
SELECT ostatok 
FROM users
""").fetchall()
print(a)



# ТУТ БУДЕТ НАШ КОД РАБОТЫ С БАЗОЙ ДАННЫХ


# Не забываем закрыть соединение с базой данных
conn.close()
