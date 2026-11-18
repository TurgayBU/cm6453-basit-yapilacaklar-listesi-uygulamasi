import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

DB = "app.db"
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);
"""

ENDPOINTS = [
    {"method": "GET", "path": "/api/tasks", "description": "List all tasks"},
    {"method": "POST", "path": "/api/tasks", "description": "Create a new task"},
    {"method": "GET", "path": "/api/tasks/<int:task_id>", "description": "Get a task by ID"},
    {"method": "PUT", "path": "/api/tasks/<int:task_id>", "description": "Update a task"},
    {"method": "DELETE", "path": "/api/tasks/<int:task_id>", "description": "Delete a task"}
]


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        if self.path == "/api/tasks":
            conn = db()
            rows = conn.execute("SELECT * FROM tasks").fetchall()
            tasks = [dict(r) for r in rows]
            self.send_json(200, tasks)
        elif self.path.startswith("/api/tasks/"):
            task_id = int(self.path.split('/')[-1])
            conn = db()
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row:
                self.send_json(200, dict(row))
            else:
                self.send_json(404, {"message": "Task not found"})
        else:
            self.send_json(404, {"message": "Not found"})

    def do_POST(self):
        data = self.read_json()
        title = data.get("title")
        if not title:
            self.send_json(400, {"message": "Title is required"})
            return

        conn = db()
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        self.send_json(201, {"message": "Task created", "id": conn.execute("SELECT last_insert_rowid()").fetchone()[0]})

    def do_PUT(self):
        task_id = int(self.path.split('/')[-1])
        data = self.read_json()
        title = data.get("title")
        completed = data.get("completed")

        conn = db()
        conn.execute("UPDATE tasks SET title = ?, completed = ? WHERE id = ?", (title, completed, task_id))
        conn.commit()

        if conn.rowcount > 0:
            self.send_json(200, {"message": "Task updated"})
        else:
            self.send_json(404, {"message": "Task not found"})

    def do_DELETE(self):
        task_id = int(self.path.split('/')[-1])
        conn = db()
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

        if conn.rowcount > 0:
            self.send_json(200, {"message": "Task deleted"})
        else:
            self.send_json(404, {"message": "Task not found"})

if __name__ == "__main__":
    db().executescript(SCHEMA)
    HTTPServer(("0.0.0.0", 9000), Handler).serve_forever()