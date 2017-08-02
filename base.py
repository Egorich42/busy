# Импортируем библиотеку, соответствующую типу нашей базы данных 
import sqlite3

#https://ru.stackoverflow.com/questions/224243/Как-в-python-программно-создать-новую-базу-данных-и-выполнить-в-ней-скрипт

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = sqlite3.connect('bas.sqlite')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cur = conn.cursor()
cur.executescript("""
create table users (
	id int(10),
	ostatok int(10),
	name varchar(100) NOT NULL,
	PRIMARY KEY (id)
);


INSERT INTO users VALUES ('1','20','orbite');	
INSERT INTO users  VALUES ('2','50','clondike');
INSERT INTO users  VALUES ('3','444','craft');
INSERT INTO users  VALUES ('4','8736','flotdotlot');

""")


# Не забываем закрыть соединение с базой данных
conn.close()
