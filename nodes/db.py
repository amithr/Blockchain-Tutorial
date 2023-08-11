import sqlite3

def create_database():
    conn = sqlite3.connect('blockchain_tutorial.db')
    users_table_query = ('''
    CREATE TABLE USERS (
        EMAIL               TEXT    NOT NULL,
        COMMAND_NODE_PORT   INT     NOT NULL,
        ACTIVE              BOOL    NOT NULL
    );
    ''')

    node_table_query = ('''
    CREATE TABLE NODES (
        EMAIL          TEXT    NOT NULL,
        NODE_PORT      INT     NOT NULL,
        ACTIVE         BOOL    NOT NULL,
        FOREIGN KEY (COMMAND_NODE) REFERENCES USERS(EMAIL)
    );
''')
     
    conn.execute(users_table_query)
    conn.execute(node_table_query)
    conn.close()

def add_user(email, command_node_port, active):
    conn = sqlite3.connect('blockchain_tutorial.db')  # Replace 'your_database.db' with the actual database name

    conn.execute("INSERT INTO USERS (EMAIL, COMMAND_NODE_PORT, ACTIVE) VALUES (?,?,?)", (email, command_node_port, active))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('blockchain_tutorial.db')  # Replace 'your_database.db' with the actual database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE EMAIL = ?", (email,))
    user = cursor.fetchone() 
    conn.close()

    return user

def insert_node_record(email, node_port, active):
    conn = sqlite3.connect('blockchain_tutorial.db')  # Replace 'your_database.db' with the actual database name
    conn.execute("INSERT INTO NODES (EMAIL, NODE_PORT, ACTIVE) VALUES (?,?,?)", (email, node_port, active))
    conn.commit()
    conn.close()


def delete_node_record(email=None, node_port=None):
    conn = sqlite3.connect('blockchain_tutorial.db')  # Replace 'your_database.db' with the actual database name

    if email is not None:
        conn.execute("DELETE FROM NODES WHERE EMAIL = ?", (email,))
    elif node_port is not None:
        conn.execute("DELETE FROM NODES WHERE NODE_PORT = ?", (node_port,))
    
    conn.commit()
    conn.close()

def get_nodes_by_email(email):
    conn = sqlite3.connect('blockchain_tutorial.db')  # Replace 'your_database.db' with the actual database name

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NODES WHERE EMAIL = ?", (email,))
    nodes = cursor.fetchall()
    
    conn.close()

    return nodes