from django.test import TestCase, Client

# Create your tests here.

class FeedbackTest(TestCase):
    
    def test_feedback(self):
        client = Client()
        response = client.get('/feedback/')
        self.assertEqual(response.status_code, 200)
        response = client.post('/feedback/', {
            'name' : 'TestName',
            'subject' : 'Test Subject',
            'message' : 'Hello! this is a Test!',
            'from_email' : 'test@email.com' },
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for your feedback! We will keep in touch with you very soon!')

