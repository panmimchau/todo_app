#python todo.py --add "grocery shopping"
#python todo.py --list
#python todo.py --toggle 1
import sqlite3
from argparse import ArgumentParser

parser = ArgumentParser(description='Small TODO application')
parser.add_argument('--install', help='Installing new db! CAUTION: This will clear the current db!', action='store_true')
parser.add_argument('--add', help='Add new task')
parser.add_argument('--list', help='Show list of tasks', action='store_true')
parser.add_argument('--toggle', help='Change task status')
args = parser.parse_args()
width = '\t'

connection = sqlite3.connect('todo.db')
cursor = connection.cursor()

if args.install:
    print('Installing app')
    cursor.execute('DROP TABLE todos')
    cursor.execute('CREATE TABLE todos(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, is_done BOOLEAN)')
    connection.commit()

if args.add is not None:
    print('Adding...')
    title = args.add
    cursor.execute('INSERT INTO todos(title, is_done) VALUES(?, false)', (title,))
    connection.commit()
    
if args.toggle is not None:
    print('Changing status...')
    query = cursor.execute('SELECT is_done FROM todos WHERE id=?', (args.toggle,))
    is_done = query.fetchone()
    if is_done is None:
        print('No such position on list.')
        quit()
    elif is_done[0] == 1:
        print('Changing status to "TO DO"')
        new_is_done = 0
    elif is_done[0] == 0:
        print('Changing status to "DONE')
        new_is_done = 1
        
    cursor.execute('UPDATE todos SET is_done=? WHERE id=?', (new_is_done, args.toggle))
    connection.commit()
    
if args.list:
    print('Current list of tasks:')
    for todo_id, title, is_done in cursor.execute('SELECT id, title, is_done FROM todos'):
        print(f'{todo_id} \t {title:30s}  {"[v]" if is_done else "[ ]"}')
        