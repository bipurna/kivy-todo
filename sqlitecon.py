import sqlite3
from sqlite3 import Error

conn = None

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tb_tasks
               (id INTEGER PRIMARY KEY, tasks text NOT NULL, status text NOT NULL, insert_time text NOT NULL, complete_time text)''')
        
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def display(db_file,id=None):
    rows_list = []
    if id == None:
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM tb_tasks")
            rows = c.fetchall()
            for row in rows:
                rows_list.append(row)
                
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    else:
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM tb_tasks WHERE id=?",(id,))
            rows = c.fetchone()
            rows_list.append(rows)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    return rows_list

def insert_data_db(db_file,n,add,em,ph):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        params = (n,add,em,ph)
        c.execute("INSERT INTO tb_tasks(tasks, status, insert_time, complete_time) VALUES (?,?,?,?)",params)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def delete_entry(db_file,id):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("DELETE FROM tb_tasks WHERE id = ?",(id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def update_data(db_file,id,status,complete_time):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("UPDATE tb_tasks SET status = ?,complete_time=? WHERE id = ?",(status,complete_time,id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    
