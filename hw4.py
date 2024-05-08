#1
def create_tables(connect):
    with connect.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS clients (
                        PRIMARY KEY(client_id),
                            client_id INT,
                            first_name VARCHAR(30) NOT NULL,
                            last_name VARCHAR(30) NOT NULL,
                            email VARCHAR(30) UNIQUE NOT NULL);
                        
                        CREATE TABLE IF NOT EXISTS phone_numbers (
                            client_id INT REFERENCES clients(client_id),
                            number VARCHAR(16) UNIQUE NOT NULL);   
                        ''')  #номер телефона вида: +7(NNN)NNN-NN-NN
        connect.commit()

#доп.функция для проверки наличия записи в таблице
def check_in_table(client_id, connect):
    with connect.cursor() as cur:
        cur.execute('SELECT EXISTS (SELECT * FROM clients WHERE client_id = %s);', (client_id,))
        return cur.fetchone()
    
#доп.функция для красивого вывода в 7-мом задании
def format_result(info, connect):   
    with connect.cursor() as cur:
        clients_info = []
        for v in info:
            client_info = {}
            client_info['ID'] = v[0]
            client_info['first_name'] = v[1]
            client_info['last_name'] = v[2]
            client_info['email'] = v[3]
            clients_info.append(client_info)
        for i in clients_info:
            cur.execute('''SELECT number FROM phone_numbers
                            WHERE client_id = %s;
                        ''', (i['ID'],))
            for n in cur.fetchall():
                n = ''.join(n)
                if 'phone_numbers' not in i:
                    i['phone_numbers'] = [n]
                else:
                    i['phone_numbers'].append(n)
            return clients_info

#2
def add_client(client_id, first_name, last_name, email, number=None, connect=None):
    if check_in_table(client_id=client_id, connect=connect) == (False,):
        with connect.cursor() as cur:
            cur.execute('''
                        INSERT INTO clients(client_id, first_name, last_name, email) 
                        VALUES (%s, %s, %s, %s);
                        ''', (client_id, first_name, last_name, email))
            connect.commit()
            if type(number) == list:
                for n in number:
                    cur.execute('''
                            INSERT INTO phone_numbers(client_id, number)
                            VALUES (%s, %s);    
                            ''', (client_id, n))
                connect.commit()
            elif type(number) == str:
                cur.execute('''
                        INSERT INTO phone_numbers(client_id, number)
                        VALUES (%s, %s);
                        ''', (client_id, number))
                connect.commit()
    else:
        print('Клиент с таким ID уже существует')

#3
def add_phone_number(client_id, number, connect=None):
    if check_in_table(client_id, connect) == (True,):
        with connect.cursor() as cur:
            if type(number) == list:
                for n in number:
                    cur.execute('''
                            INSERT INTO phone_numbers(client_id, number)
                            VALUES (%s, %s);    
                            ''', (client_id, n))
                connect.commit()
            elif type(number) == str:
                cur.execute('''
                        INSERT INTO phone_numbers(client_id, number)
                        VALUES (%s, %s);
                            ''', (client_id, number))
                connect.commit()
    else:
        print('Клиента с таким ID не существует')

#4
def update_client(client_id, first_name, last_name, email, number=None, connect=None):
    if check_in_table(client_id, connect) == (True,):
        with connect.cursor() as cur:
            cur.execute('''
                        UPDATE clients
                        SET first_name = %s,
                            last_name = %s,
                            email = %s
                        WHERE client_id = %s;
                        ''', (first_name, last_name, email, client_id))
            connect.commit()
            if type(number) == list:
                cur.execute('''
                        DELETE FROM phone_numbers
                            WHERE client_id = %s;
                        ''', (client_id,))
                for n in number:
                    cur.execute('''
                                INSERT INTO phone_numbers(client_id, number)
                                VALUES (%s, %s);
                                ''', (client_id, n))
                connect.commit()
            elif type(number) == str:
                cur.execute('''
                        DELETE FROM phone_numbers
                            WHERE client_id = %s;
                        ''', (client_id,))
                cur.execute('''
                            INSERT INTO phone_numbers(client_id, number)
                            VALUES (%s, %s);
                            ''', (client_id, number))
                connect.commit()
    else:
        print('Клиента с таким ID не существует')

#5 P.S Я понял это задание как удалить все номера для определенного клиента
def delete_number(client_id, connect=None):
    if check_in_table(client_id, connect) == (True,):
        with connect.cursor() as cur:
            cur.execute('''DELETE FROM phone_numbers
                                WHERE client_id = %s;
                            ''', (client_id,))
            connect.commit()
    else:
        print('Клиента с таким ID не существует')

#6
def delete_client(client_id, connect=None):
    if check_in_table(client_id, connect) == (True,):
        with connect.cursor() as cur:
            cur.execute('''DELETE FROM phone_numbers
                                WHERE client_id = %s;
                            DELETE FROM clients 
                                WHERE client_id = %s;
                            
                            ''', (client_id, client_id))
            connect.commit()
    else:
        print('Клиента с таким ID не существует')

#7
def find_client(info, connect=None):
    with connect.cursor() as cur:
        cur.execute('SELECT EXISTS (SELECT * FROM phone_numbers WHERE number = (%s));', (info, ))
        if cur.fetchone() == (False,):
            cur.execute('''SELECT * FROM clients
                        WHERE first_name LIKE (%s)
                        OR last_name LIKE (%s)
                        OR email LIKE (%s);
                    ''', (info, info, info))
            clients_info = format_result(cur.fetchall(), connect=connect)
            if bool(clients_info) == True:
                return clients_info
            else:
                return 'Клиента с таким параметром не существует'

        else:
            cur.execute('SELECT client_id FROM phone_numbers WHERE number LIKE (%s)', (info,))
            client_id = cur.fetchone()
            cur.execute('SELECT * FROM clients WHERE client_id = (%s)', (client_id,))
            clients_info = format_result(cur.fetchall(), connect=connect)
            if bool(clients_info) == True:
                return clients_info
            else:
                return 'Клиента с таким параметром не существует'