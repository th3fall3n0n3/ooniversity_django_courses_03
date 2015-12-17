from django.test import TestCase, Client
from django.contrib.auth.models import User
from coaches.models import Coach
from pybursa.tests import process_cases


# Create your tests here.
def create_coaches():
    items = {}
    items['coach1'] = Coach.objects.create(
        user = User.objects.create_user('coach1', 'coach1@test.com', 'coach1', 
                                        first_name="Coach", last_name="One"),
        date_of_birth = '2015-10-10',
        gender = 'M',
        phone = '0123456789',
        address = 'address 2345 test case',
        skype = 'coach1.skype',
        description = 'super coach can teach everything')
    items['coach2'] = Coach.objects.create(
        user = User.objects.create_user('coach2', 'coach2@test.com', 'coach2',
                                        first_name="Coach", last_name="Two"),
        date_of_birth = '2010-10-10',
        gender = 'M',
        phone = '987654321',
        address = 'address 1234 test case',
        skype = 'coach2.skype',
        description = 'super coach can teach nothing')
    return items

class CoachDetailsTest(TestCase):
    
    def test_coach_details(self):
        client = Client() 
        response = client.get('/coaches/1/')
        self.assertEqual(response.status_code, 404)
        items = create_coaches()

        for i in items:
            response = client.get('/coaches/%d/' % items[i].id)
            self.assertEqual(response.status_code, 200)
            process_cases(self, response, {
                'title' : '<title>%s %s Details</title>' % (items[i].user.first_name,
                                                            items[i].user.last_name),
                'header' : '<h1 class="glow_cyan_t">%s %s</h1>' % (items[i].user.first_name,
                                                                   items[i].user.last_name),
                'surname' : '<td>Surname</td><td>%s</td>' % items[i].user.last_name,
                'name' : '<td>Name</td><td>%s</td>' % items[i].user.first_name,
                'email': '<td>E-mail</td><td>%s</td>' % items[i].user.email,
                'phone' : '<td>Phone</td><td>%s</td>' % items[i].phone,
                'address': '<td>Address</td><td>%s</td>' % items[i].address})
            
