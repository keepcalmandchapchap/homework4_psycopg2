import psycopg2
import hw4




db = ''
user = ''
password = ''
conn = psycopg2.connect(database=db, user=user, password=password)

#1
hw4.create_tables(connect=conn)

#2
hw4.add_client(1, 'Максим', 'Деревцов', 'study@netology.ru', '+7(999)000-00-00', connect=conn)
hw4.add_client(2, 'Мирон', 'Оксимиронович', 'inoagent@bublik.com', ['+7(123)123-12-12', '+7(333)333-33-33'], connect=conn)
hw4.add_client(3, 'Валентин', 'Шпилька', 'OhIAh@rumbler.ru', '+7(929)929-29-29', connect=conn)
hw4.add_client(4, 'Джейсон', 'Стэтхэм', 'underground@pulya.com', connect=conn)
#3
hw4.add_phone_number(1, '+7(800)555-35-35', connect=conn)

#4
hw4.update_client(2, 'Иосиф', 'Джугашвили', 'USSRthebest@zhukov.com', '+7(555)555-55-55', connect=conn)

#5 
hw4.delete_number(2, connect=conn)

#6
hw4.delete_client(4, connect=conn)

#7
print(hw4.find_client('Максим', connect=conn))
print(hw4.find_client('+7(929)929-29-29', connect=conn))
print(hw4.find_client('OhIAh@rumbler.ru', connect=conn))
