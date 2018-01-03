from django.test import TestCase, RequestFactory
from mgr import views
from mgr.models import Server

class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_add(self):
        request = self.factory.post('/', {'ip': '192.168.1.100', 'action':'Add', 'username': 'username1', 'password': 'password1'})

        response = views.index(request)
        
        print(response)
        server = Server.objects.all()[0]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("192.168.1.100" in response.content.decode("utf-8"))
        self.assertTrue("192.168.1.100", server.ip)

    def test_add_invalid_ip(self):
        request = self.factory.post('/', {'ip': 'not an ip', 'action':'Add', 'username': 'username1', 'password': 'password1'})

        response = views.index(request)

        servers = Server.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertFalse("192.168.1.100" in response.content.decode("utf-8"))
        self.assertFalse(servers)

    def test_add_invalid_username(self):
        request = self.factory.post('/', {'ip': '192.168.1.100', 'action':'Add', 'username': 'username1$$$$$', 'password': 'password1'})

        response = views.index(request)

        servers = Server.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertFalse("192.168.1.100" in response.content.decode("utf-8"))
        self.assertFalse(servers)

    def test_add_invalid_password(self):
        request = self.factory.post('/', {'ip': '192.168.1.100', 'action':'Add', 'username': 'username1', 'password': 'password1----$$$$$'})

        response = views.index(request)

        servers = Server.objects.all()
        print(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse("192.168.1.100" in response.content.decode("utf-8"))
        self.assertFalse(servers)

    def test_delete_success(self):
        # Create Server object
        server = Server(ip='192.168.1.100', username='username', password='password')
        self.assertTrue("192.168.1.100", server.ip)

        request = self.factory.post('/delete/1')

        response = views.delete(request, 1)

        self.assertTrue("192.168.1.100" not in response.content.decode("utf-8"))
        self.assertFalse(Server.objects.all())
