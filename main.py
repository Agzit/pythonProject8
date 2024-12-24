import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

TASKS_FILE = 'tasks.txt'

class Task:
    def __init__(self, id, title, priority, is_done=False):
        self.id = id
        self.title = title
        self.priority = priority
        self.is_done = is_done

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'isDone': self.is_done
        }


tasks = []
task_id_counter = 1

def load_tasks():
    global task_id_counter
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            try:
                data = json.load(file)
                for task_data in data:
                    task = Task(
                        id=task_data['id'],
                        title=task_data['title'],
                        priority=task_data['priority'],
                        is_done=task_data['isDone']
                    )
                    tasks.append(task)
                    task_id_counter = max(task_id_counter, task.id + 1)
            except json.JSONDecodeError:
                pass


def save_tasks():
    with open(TASKS_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)


# Загрузка задач при старте сервера
load_tasks()


# Обработчик запросов
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/tasks":
            self.handle_get_tasks()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/tasks":
            self.handle_create_task()
        elif self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            self.handle_complete_task()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_get_tasks(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Разрешаем все домены
        self.end_headers()
        # Отправляем список задач в формате JSON
        self.wfile.write(json.dumps([task.to_dict() for task in tasks]).encode())

    def handle_create_task(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        title = data.get('title')
        priority = data.get('priority')

        if not title or not priority:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Title and priority are required"}')
            return

        if priority not in ['low', 'normal', 'high']:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid priority"}')
            return

        global task_id_counter
        task = Task(
            id=task_id_counter,
            title=title,
            priority=priority
        )
        tasks.append(task)
        task_id_counter += 1
        save_tasks()

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(task.to_dict()).encode())

    def handle_complete_task(self):
        task_id = int(self.path.split('/')[-2])
        task = next((task for task in tasks if task.id == task_id), None)

        if task is None:
            self.send_response(404)
            self.end_headers()
            return

        task.is_done = True
        save_tasks()

        self.send_response(200)
        self.end_headers()


# Настройка и запуск сервера
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
