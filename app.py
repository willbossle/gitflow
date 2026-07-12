from flask import Flask, request, jsonify, render_template, abort
import sqlite3
import os

app = Flask(__name__)

# Diretório onde o banco de dados será salvo
db_directory = '/dados'
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

db_path = os.path.join(db_directory, 'database.db')


# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Função para inicializar o banco de dados com uma tabela de tarefas
def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()


# Inicializar o banco de dados se não existir
init_db()


# Página para criar uma nova tarefa
@app.route('/')
def index():
    return render_template('index.html')


# Página para listar todas as tarefas
@app.route('/view_tasks')
def view_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    tasks_list = [dict(task) for task in tasks]
    return render_template('tasks.html', tasks=tasks_list)


# Rota para listar todas as tarefas (API)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    tasks_list = [dict(task) for task in tasks]
    return jsonify({'tasks': tasks_list})


# Rota para criar uma nova tarefa
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'title': request.json['title'],
        'done': False
    }
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, done) VALUES (?, ?)',
                 (task['title'], task['done']))
    conn.commit()
    new_task = conn.execute('SELECT * FROM tasks WHERE id ='
                            'last_insert_rowid()').fetchone()
    conn.close()
    return jsonify({'task': dict(new_task)}), 201


# Rota para atualizar uma tarefa existente
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = request.json
    if 'title' in task and not isinstance(task['title'], str):
        abort(400)
    if 'done' in task and not isinstance(task['done'], bool):
        abort(400)

    conn = get_db_connection()
    existing_task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                                 (task_id,)).fetchone()
    if existing_task is None:
        abort(404)

    conn.execute('UPDATE tasks SET title = ?, done = ? WHERE id = ?',
                 (task.get('title', existing_task['title']),
                  task.get('done', existing_task['done']), task_id))
    conn.commit()
    updated_task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                                (task_id,)).fetchone()
    conn.close()
    return jsonify({'task': dict(updated_task)})


# Rota para deletar uma tarefa
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'result': True})


# Rota para tratar erro 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")