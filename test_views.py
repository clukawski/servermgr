from django.test import TestCase, RequestFactory
from mgr import views
from mgr.models import Server

class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_add(self):
        request = self.factory.post('/', {'ip': '192.168.1.100', 'action':'Add', 'username': 'username1', 'password': 'password1'})

        response = views.index(request)
        
        server = Server.objects.all()[0]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("192.168.1.100" in response.content.decode("utf-8"))
        self.assertTrue("192.168.1.100", server.ip)

