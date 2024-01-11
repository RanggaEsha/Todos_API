# buat schema todos kolom id, todo, is_done
from db import conn
from psycopg2.errors import DatabaseError

def get_all_todos():
    cur = conn.cursor()
    try:
        cur.execute("SELECT id,todo,is_done FROM todos")
        todos = cur.fetchall()
        new_todos = []
        for todo in todos:
            new_todo = {
                "id" : todo[0],
                "todo" : todo[1],
                "is_done" : todo[2]
            }
            new_todos.append(new_todo)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    return new_todos

def get_todo_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id,todo,is_done FROM todos WHERE id = %s",(id,))
        todo = cur.fetchone()
        conn.commit()
    except Exception as e:
        cur.rollback()
        raise e
    finally:
        cur.close()

    if todo is None:
        return None
    
    return {
        "id": todo[0],
        "todo": todo[1],
        "is_done": todo[2]
    }

def create_new_todo(new_todo: str,is_done):
    cur = conn.cursor()
    try:
        new_is_done = is_done
        cur.execute("INSERT INTO todos (todo,is_done) VALUES (%s,%s)",(new_todo,new_is_done))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def update_todo_by_id(id,new_todo: str):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE todos SET todo = %s WHERE id = %s",(new_todo,id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_todo_by_id(id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE from TODOS WHERE id = %s",(id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()



# create_new_todo('kamu baiik')
# for todo in get_all_todos():
#     print('id:',todo[0],'todo:',todo[1],'is_done:',todo[2])

    
# print(get_todo_by_id(1))
# print(get_all_todos())

print(update_todo_by_id(2,'nyuci'))
print(get_all_todos())

