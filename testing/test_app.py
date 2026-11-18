import json
import unittest
from urllib.request import urlopen
from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
from app import Handler, ENDPOINTS, SCHEMA, db

class TestBackendEndpoints(unittest.TestCase):

    def setUp(self):
        Handler.db = db
        Handler.send_json = Handler.send_json
        Handler.read_json = Handler.read_json
        Handler.do_GET = Handler.do_GET
        Handler.do_POST = Handler.do_POST
        Handler.do_PUT = Handler.do_PUT
        Handler.do_DELETE = Handler.do_DELETE
        Handler.ENDPOINTS = ENDPOINTS
        Handler.SCHEMA = SCHEMA
        Handler.db().executescript(SCHEMA)
        Handler.db().row_factory = sqlite3.Row
        self.server_address = ('0.0.0.0', 9000)
        self.server = HTTPServer(self.server_address, Handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server_thread.join()

    def test_get_all_tasks(self):
        url = "http://localhost:9000/api/tasks"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertEqual(len(data), 0)
        response.close()

        url = "http://localhost:9000/api/tasks"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Task')
        response.close()

    def test_create_task(self):
        url = "http://localhost:9000/api/tasks"
        data = {"title": "New Task"}
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        response = urlopen(req)
        data = json.loads(response.read.decode())
        self.assertEqual(response.status, 201)
        self.assertEqual(data['message'], 'Task created')
        self.assertTrue('id' in data)
        response.close()

        url = "http://localhost:9000/api/tasks"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertTrue('Test Task' in data)
        response.close()

    def test_get_task_by_id(self):
        url = "http://localhost:9000/api/tasks/0"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertEqual(response.status, 200)
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['completed'], False)
        response.close()

    def test_update_task(self):
        url = "http://localhost:9000/api/tasks/0"
        data = {"title": "Updated Task", "completed": True}
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        response = urlopen(req)
        data = json.loads(response.read.decode())
        self.assertEqual(response.status, 200)
        self.assertEqual(data['message'], 'Task updated')

        url = "http://localhost:9000/api/tasks/0"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertEqual(data['title'], 'Updated Task')
        self.assertEqual(data['completed'], True)
        response.close()

    def test_delete_task(self):
        url = "http://localhost:9000/api/tasks/0"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertEqual(response.status, 200)
        response.close()

        url = "http://localhost:9000/api/tasks/0"
        response = urlopen(url)
        data = json.loads(response.read.decode())
        self.assertEqual(response.status, 404)
        response.close()
import threading
if __name__ == '__main__':
    unittest.main()