from django.test import TestCase, Client
from courses.tests import create_courses
from students.models import Student
from courses.models import Course
from pybursa.tests import process_cases

# Create your tests here.
def create_form(addin=""):
    return {'name' : 'Student_test' + addin,
            'surname' : 'Surname' + addin,
            'email' : addin[::-1] + 'test@just.for.test.com',
            'phone' : '0800-500-500-2' + addin ,
            'address' : 'test_address' + addin,
            'skype' : 'skype.for_test' +addin,
            'date_of_birth' : '2015-01-01',
            'courses': 1 }    

def create_form_new(item, addin=""):
    return {'name' : item.name + addin,
            'surname' : item.surname + addin,
            'email' : addin[::-1] + item.email,
            'phone' : item.phone + addin ,
            'address' : item.address + addin,
            'skype' : item.skype +addin,
            'date_of_birth' : item.date_of_birth,
            'courses': 1 }    

def create_students():
    items = {}
    courses = create_courses()
    for i in courses:
        for id in range(1,4):
            items['student_' + i + str(id)] = Student.objects.create(
            name = 'student%d' % id,
            surname = '%dstudent' %id,
            date_of_birth = '2015-01-0%d' % id,
            email = 'student_%d@email.com' % id,
            phone = str(id) * 10,
            address = 'student %d address' % id,
            skype = 'student.skype %d' % id 
            )
            items['student_' + i + str(id)].courses.add(courses[i].id)
    return items
        
class StudentsListTest(TestCase):

    def test_student_lists_normal_response(self):
        client = Client()
        response = client.get('/students/?course_id=1')  
        self.assertEqual(response.status_code, 200)

    def test_student_lists_no_courses(self):
        client = Client()
        response = client.get('/students/?course_id=1') 
        self.assertContains(response, 'Unfortunately there is no students in this course or course not found')     

    def test_student_lists_pages(self):
        client = Client()
        response = client.get('/students/?course_id=1') 
        items = create_students()
        for i in items:
            if items[i].id % 2 == 0:
                page = items[i].id / 2
            else:
                page = items[i].id / 2 + 1
            response = client.get('/students/?page=%d' % page )  
            self.assertEqual(response.status_code, 200)

    def test_student_lists_urls(self):
        client = Client()
        response = client.get('/students/?course_id=1') 
        items = create_students()
        for i in items:
            if items[i].id % 2 == 0:
                page = items[i].id / 2
            else:
                page = items[i].id / 2 + 1
            response = client.get('/students/?page=%d' % page )
            self.assertContains(response, '<a href="/students/%d/">%s %s<a>' % ( 
                                items[i].id, items[i].surname, items[i].name ))

    def test_student_lists_course_pages(self):
        client = Client()
        response = client.get('/students/?course_id=1') 
        items = create_students()
        for z in items:
            for i in items[z].courses.all():
                students_count = len(Student.objects.filter(courses=i.id))
                if students_count % 2 == 0:
                    pages = students_count / 2
                else:
                    pages = students_count / 2 + 1
                response = client.get('/students/?course_id=%d&page=1' % 1 )  
                self.assertEqual(response.status_code, 200)

    def test_student_lists_pagination(self):
        client = Client()
        response = client.get('/students/?course_id=1') 
        items = create_students()
        for z in items:
            for i in items[z].courses.all():
                students_count = len(Student.objects.filter(courses=i.id))
                if students_count % 2 == 0:
                    pages = students_count / 2
                else:
                    pages = students_count / 2 + 1
                response = client.get('/students/?course_id=%d&page=1' % 1 )  
                self.assertContains(response, '<a>Page 1 of %d</a>' % pages)

class StudentsDetailTest(TestCase):
        
    def test_student_detail_not_found(self):
        client = Client()
        response = client.get('/students/1/')  
        self.assertEqual(response.status_code, 404)
    
    def test_student_detail_normal_response(self):
        client = Client()
        items = create_students()
        response = client.get('/students/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_detail_title(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<title>%s %s Details</title>' % ( items[i].name,
                                                                             items[i].surname ))

    def test_student_detail_header(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<h1 class="glow_cyan_t">%s %s</h1>' % ( items[i].name,
                                                                                    items[i].surname ))

    def test_student_detail_surname(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<td>Surname</td><td>%s</td>' % items[i].surname)

    def test_student_detail_name(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<td>Name</td><td>%s</td>' % items[i].name)

    def test_student_detail_email(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<td>E-mail</td><td>%s</td>' % items[i].email)

    def test_student_detail_phone(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<td>Phone</td><td>%s</td>' % items[i].phone)

    def test_student_detail_address(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<td>Address</td><td>%s</td>' % items[i].address)

    def test_student_detail_skype(self):
        client = Client()
        items = create_students()       
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertContains(response, '<td>Skype</td><td>%s</td>' % items[i].skype )

    def test_student_add_button(self):
        client = Client()
        response = client.get('/students/')
        self.assertContains(response, '<a href="/students/add/')

class StudentAddTest(TestCase):

    def test_student_add_normal_response(self):
        client = Client()
        response = client.get('/students/add/')
        self.assertEqual(response.status_code, 200)
        
    def test_student_add_title(self):
        client = Client()
        response = client.get('/students/add/')
        self.assertContains(response, '<title>Student registration</title>')

    def test_student_add_header(self):
        client = Client()
        response = client.get('/students/add/')
        self.assertContains(response, '<h1 class="glow_cyan_t">Student registration</h1>')
    
    def test_student_form_post(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_student_form_title(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertContains(response, '<title>Pybursa Students</title>')

    def test_student_form_message(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertContains(response, 'Student Student_test Surname has been successfully added.')

    def test_student_form_name_url(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertContains(response, '<a href="/students/1/">Surname Student_test<a>')

    def test_student_form_courses_link(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertContains(response,  '<a href="/courses/1/">PyBursa</a><br>')

    def test_student_form_edit_button(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertContains(response, '<a href="/students/edit/1/"')

    def test_student_form_remove_button(self):
        client = Client()
        create_courses()
        response = client.post('/students/add/', create_form(), follow=True)
        self.assertContains(response, '<a href="/students/remove/1/"')

class StudentEditTest(TestCase):

    def test_edit_student_no_data(self):
        client = Client()
        response = client.get('/students/edit/1/')
        self.assertEqual(response.status_code, 404)

    def test_edit_student_normal_response(self):
        client = Client()
        items = create_students()
        response = client.get('/students/edit/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_edit_student_title(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<title>Student info update</title>')
        
    def test_edit_student_name(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<input id="id_name" maxlength="100" name="name" type="text" value="%s" />' % items[i].name)

    def test_edit_student_surname(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<input id="id_surname" maxlength="100" name="surname" type="text" value="%s" />' % items[i].surname)

    def test_edit_student_b_date(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<input id="id_date_of_birth" name="date_of_birth" type="text" value="%s"' % items[i].date_of_birth)

    def test_edit_student_email(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<input id="id_email" maxlength="75" name="email" type="email" value="%s" />' % items[i].email)

    def test_edit_student_phone(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<input id="id_phone" maxlength="30" name="phone" type="text" value="%s" />' % items[i].phone)

    def test_edit_student_skype(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id) 
            self.assertContains(response, '<input id="id_skype" maxlength="255" name="skype" type="text" value="%s" />' % items[i].skype)

    def test_edit_form_submit(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form("_new"), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_edit_form_submit_message(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form_new(items[i], "_new"), follow=True)
            self.assertContains(response, 'Info on the student has been sucessfully changed.')
        
    def test_edit_student_name_new(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form_new(items[i], "_new"), follow=True) 
            response = client.get('/students/edit/%d/' % items[i].id)
            self.assertContains(response, '<input id="id_name" maxlength="100" name="name" type="text" value="%s" />' % (items[i].name + "_new"))

    def test_edit_student_surname_new(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form_new(items[i], "_new"), follow=True)
            response = client.get('/students/edit/%d/' % items[i].id)
            self.assertContains(response, '<input id="id_surname" maxlength="100" name="surname" type="text" value="%s" />' % (items[i].surname + "_new"))

    def test_edit_student_email_new(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form_new(items[i], "_new"), follow=True)
            response = client.get('/students/edit/%d/' % items[i].id)
            self.assertContains(response, '<input id="id_email" maxlength="75" name="email" type="email" value="%s" />' % ("wen_" + items[i].email))

    def test_edit_student_phone_new(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form_new(items[i], "_new"), follow=True)
            response = client.get('/students/edit/%d/' % items[i].id)
            self.assertContains(response, '<input id="id_phone" maxlength="30" name="phone" type="text" value="%s" />' % (items[i].phone + "_new"))

    def test_edit_student_skype_new(self):
        client = Client()
        items = create_students()
        for i in items:
            response = client.post('/students/edit/%d/' % items[i].id, 
                                   create_form_new(items[i], "_new"), follow=True)
            response = client.get('/students/edit/%d/' % items[i].id)
            self.assertContains(response, '<input id="id_skype" maxlength="255" name="skype" type="text" value="%s" />' % (items[i].skype + "_new"))

class StudentDeleteTest(TestCase):

    def test_student_delete_no_data(self):
        client = Client()
        response = client.get('/students/remove/1/')
        self.assertEqual(response.status_code, 404)
        
    def test_student_delete_normal_response(self):
        client = Client()
        items = create_students()
        response = client.get('/students/remove/1/')
        self.assertEqual(response.status_code, 200)

    def test_student_delete_form_submit(self):
        client = Client()
        items = create_students()
        response = client.post('/students/remove/1/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_student_delete_message(self):
        client = Client()
        items = create_students()
        response = client.post('/students/remove/1/', follow=True)
        self.assertContains(response, 'Info on student1 1student has been sucessfully deleted.')

