import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
connection = psycopg2.connect(user="postgres",
                              password="46esehir", 
                              host="127.0.0.1", 
                              port="5432", 
                              database = "customers")
cursor = connection.cursor()

def create_data(connection):
    """создание базы данных"""
    try:
        connection = psycopg2.connect(user='postgres',  
                                      host="127.0.0.1", 
                                      port="5432")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection. cursor()
        sql_create_database = "create database customers"
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print("Ошибка при работе с Posgresql", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
        print("Соединение с Postgres закрыто") 
   

def join_db(connection):
    """подключение к базе данных"""
    try:
        connection = psycopg2.connect(user="postgres",
                              password="46esehir", 
                              host="127.0.0.1", 
                              port="5432", 
                              database = "customers")
        
        cursor = connection.cursor()
        print("Информация о сервере Postgres")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print(f"вы подключены к {record}, \n")
    except (Exception, Error) as error:
        print("Ошибка при работе с Posgresql", error)
    finally:
        if connection:
            cursor.close()
            connection. close()
        print("Соединение с postgresql закрыто")


def create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS client 
                      (id SERIAL PRIMARY KEY, 
                      firstname VARCHAR(30) NOT NULL, 
                      lastname VARCHAR(30) NOT NULL, 
                      email TEXT NOT NULL);
                   ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS phonenumber 
                      (client_id INT NOT NULL REFERENCES client(id),
                      client_phonenumber VARCHAR(30) UNIQUE);
                   ''')

connection.commit()

def add_client(cursor, firstname, lastname, email):
    '''добавление нового клиента'''
    cursor.execute('''INSERT INTO client (firstname, lastname, email) 
                      VALUES (%s, %s, %s);''', (firstname, lastname, email))

connection.commit()

def add_phonenumber(cursor, client_id, client_phonenumber):
    '''добавление нового номера'''
    cursor.execute('''INSERT INTO phonenumber (client_id, client_phonenumber)
                      VALUES (%s, %s);''', (client_id, client_phonenumber))


def change_client():
    '''изменения данных клиента'''
    print('Выберите команду для изменения инфо о клиенте: \n'
    '1 - изменить имя; 2 - изменить фамилию; 3 - изменить email; 4 - изменить номер.')
    while True:
        change_command = int(input('Введите команду для изменения: '))
        if change_command == 1:
            id_client = input('id клиента данные которого нужно изменить: ')
            change_name = input('Введите имя для изменения: ')
            cursor.execute('''UPDATE client SET firstname = %s WHERE id = %s;
                              ''', (change_name, id_client))
            print('Имя изменено')
            break
        elif change_command == 2:
            id_client = input('id клиента данные которого нужно изменить')
            change_lastname = input('Введите фамилию для изменения')
            cursor.execute('''UPDATE client SET lastname = %s WHERE id = %s;
                           ''', (change_lastname, id_client))
            print('фамилия заменена')
            break
        elif change_command == 3:
            id_client = input('id клиента данные которого нужно изменить')
            change_email = input('Введите email для изменения')
            cursor.execute('''UPDATE client SET email = %s WHERE id = %s;
                           ''', (change_email, id_client))
            print('email изменен')
            break
        elif change_command == 4:
            change_number = input('Введите номер который нужно изменить: ')
            on_change_number = input('Введите номер на который нужно изменить: ')
            cursor.execute('''UPDATE phonenumber SET client_phonenumber = %s WHERE client_phonenumber = %s;
            ''', (on_change_number, change_number))
            print('номер изменен')
            break
        else:
            print('неверная команда')

connection.commit()   


def delete_phone():
    '''удаление номера'''
    delete_client_id = input('Введите id клиента номер которого нужно удалить: ')
    delete_client_number = input('Введите номер который нужно ужалить: ')
    cursor.execute('''DELETE FROM phonenumber WHERE client_phonenumber = %s;
''', ( delete_client_number,))

connection.commit()



def delete_client():
    client_id_for_delete = input('Введите id клиента для удаления: ')
    client_lastname_for_delete = input('Введите фамилию для удаления: ')
    cursor.execute('''DELETE FROM phonenumber WHERE id = %s;
                   '''), (client_id_for_delete,)
                       
    cursor.execute('''DELETE FROM client WHERE id = %s AND lastname = %s;
                   '''), (client_id_for_delete, client_lastname_for_delete)

connection.commit()


def find_client():
    print('Для поиска клиента по информации,введите команду \n'
          '1 - поиск по имени; 2 - поиск по фамилии; 3 - поиск по email; 4 - поиск по номеру')
    while True:
        command = int(input('Введите команду: '))
        if command == 1:
            command_find_firstname = input('Введите имя для поиска: ')
            cursor.execute('''SELECT id, firstname, lastname, client_phonenumber
                              FROM client AS cl
                              LEFT JOIN phonenumber p ON cl.id = p.client_id
                              WHERE firstname = %s;''', (command_find_firstname,)) 
            print(cursor.fetchall())
            break
        elif command == 2:
            command_find_lastname = input('Введите фамилию для поиска: ')
            cursor.execute('''SELECT id, firstname, lastname, email, client_phonenumber 
                              FROM client AS cl
                              LEFT JOIN phonenumber p ON cl.id = p.client_id
                              WHERE lastname = %s;''', (command_find_lastname,))
            print(cursor.fetchall())
            break
        elif command == 3:
            command_find_email = input('Введите email для поиска: ')
            cursor.execute('''SELECT id, firstname, lastname, email, client_phonenumber 
                              FROM client AS cl
                              LEFT JOIN phonenumber p ON cl.id = p.client_id
                              WHERE email = %s;''', (command_find_email,))
            print(cursor.fetchall())
            break
        elif command == 4:
            command_find_phone = input('Введите номер для поиска: ')
            cursor.execute('''SELECT id, firstname, lastname, email, client_phonenumber 
                              FROM client AS cl
                              LEFT JOIN phonenumber p ON cl.id = p.client_id
                              WHERE client_phonenumber = %s;''', (command_find_phone,))
            print(cursor.fetchall())
            break
        else:
            print('Команды не существует')


def delete_db(cursor):
    cursor.execute("""
        DROP TABLE client, phonenumber CASCADE;
        """)

with psycopg2.connect(user="postgres",
                      password="46esehir", 
                      host="127.0.0.1", 
                      port="5432", 
                      database = "customers") as connection:
    
    #delete_db(cursor)
    #create_table(cursor)
    #add_client(cursor, 'Alex', 'zhiga', 'asd@.com',)
    #add_client(cursor, 'vika', 'kryga', 'qwe@.com')
    #add_client(cursor, 'sonya', 'drago', 'zxc@.com')
    #add_phonenumber(cursor, 1, 89125)
    #add_phonenumber(cursor, 2, 8916543)
    #add_phonenumber(cursor, 3, 8945325)
    #change_client()
    #delete_phone()
    #find_client()
    connection.commit()
connection.close() 