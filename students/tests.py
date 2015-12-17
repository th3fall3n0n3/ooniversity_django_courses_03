from django.test import TestCase, Client
from courses.tests import create_courses
from students.models import Student
from courses.models import Course
from pybursa.tests import process_cases

# Create your tests here.
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

    def test_student_lists(self):
        client = Client()
        response = client.get('/students/?course_id=1')  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unfortunately there is no students in this course or course not found')     
        items = create_students()
        for i in items:
            if items[i].id % 2 == 0:
                page = items[i].id / 2
            else:
                page = items[i].id / 2 + 1
            
            response = client.get('/students/?page=%d' % page )  
            self.assertEqual(response.status_code, 200)
            process_cases(self, response, {
                          'student' : '<a href="/students/%d/">%s %s<a>' % ( 
                                      items[i].id, items[i].surname, items[i].name )})
        for i in items[i].courses.all():
            students_count = len(Student.objects.filter(courses=i.id))
            if students_count % 2 == 0:
                pages = students_count / 2
            else:
                pages = students_count / 2 + 1
            response = client.get('/students/?course_id=%d&page=1' % 1 )  
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<a>Page 1 of %d</a>' % pages)

class StudentsDetailTest(TestCase):
        
    def test_student_detail(self):
        client = Client()
        response = client.get('/students/1/')  
        self.assertEqual(response.status_code, 404)
        items = create_students()
        
        for i in items:
            response = client.get('/students/%d/' % items[i].id)  
            self.assertEqual(response.status_code, 200)
            process_cases(self, response, { 
                                'title' : '<title>%s %s Details</title>' % ( items[i].name,
                                                                             items[i].surname ),
                                'header' : '<h1 class="glow_cyan_t">%s %s</h1>' % ( items[i].name,
                                                                                    items[i].surname ),
                                'surname' : '<td>Surname</td><td>%s</td>' % items[i].surname,
                                'name' : '<td>Name</td><td>%s</td>' % items[i].name,
                                'email' : '<td>E-mail</td><td>%s</td>' % items[i].email,
                                'phone' : '<td>Phone</td><td>%s</td>' % items[i].phone,
                                'address' : '<td>Address</td><td>%s</td>' % items[i].address,
                                'skype' : '<td>Skype</td><td>%s</td>' % items[i].skype })

class StudentAddButtonTest(TestCase):

    def test_student_add_button(self):
        client = Client()
        response = client.get('/students/')
        self.assertContains(response, '<a href="/students/add/')

class StudentAddTest(TestCase):

    def test_student_add(self):
        client = Client()
        response = client.get('/students/add/')
        self.assertEqual(response.status_code, 200)
        
        process_cases(self, response, {
                      'title' : '<title>Student registration</title>',
                      'header' : '<h1 class="glow_cyan_t">Student registration</h1>'})
        
        create_courses()
        response = client.post('/students/add/', {
                      'name' : 'Student_test',
                      'surname' : 'Surname',
                      'email' : 'test@just.for.test.com',
                      'phone' : '0800-500-500-2',
                      'address' : 'test_address' ,
                      'skype' : 'skype.for_test',
                      'date_of_birth' : '2015-01-01',
                      'courses': 1 },
                      follow=True )
        self.assertEqual(response.status_code, 200)
        process_cases(self, response, {
                      'title' : '<title>Pybursa Students</title>',
                      'message' : 'Student Student_test Surname has been successfully added.',
                      'name_url' : '<a href="/students/1/">Surname Student_test<a>',
                      'courses_link' : '<a href="/courses/1/">PyBursa</a><br>',
                      'edit_button' : '<a href="/students/edit/1/"',
                      'remove_button' : '<a href="/students/remove/1/"' })

class StudentEditTest(TestCase):

    def test_edit_student(self):
        
        def create_cases(item, addin=""):
                cases = {}
                cases['title'] = '<title>Student info update</title>'
                cases['name'] = '<input id="id_name" maxlength="100" name="name" type="text" value="%s" />' % (item.name + addin)
                cases['surname'] = '<input id="id_surname" maxlength="100" name="surname" type="text" value="%s" />' % (item.surname + addin)
                cases['b_date'] = '<input id="id_date_of_birth" name="date_of_birth" type="text" value="%s"' % item.date_of_birth
                cases['email'] = '<input id="id_email" maxlength="75" name="email" type="email" value="%s" />' % (addin[::-1] + item.email)
                cases['phone'] = '<input id="id_phone" maxlength="30" name="phone" type="text" value="%s" />' % (item.phone + addin)
                cases['address'] = '<input id="id_address" maxlength="255" name="address" type="text" value="%s" />' % (item.address + addin)
                cases['skype'] = '<input id="id_skype" maxlength="255" name="skype" type="text" value="%s" />' % (item.skype + addin)
                return cases        

        client = Client()
        response = client.get('/students/edit/1/')
        self.assertEqual(response.status_code, 404)

        items = create_students()
        
        for i in items:
            response = client.get('/students/edit/%d/' % items[i].id)  
            self.assertEqual(response.status_code, 200)
            
            cases = create_cases(items[i])
            process_cases(self, response, cases)

            response = client.post('/students/edit/%d/' % items[i].id, {
                                   'name' : items[i].name + "_new",
                                   'surname' : items[i].surname + "_new",
                                   'date_of_birth' : items[i].date_of_birth,
                                   'email' : "wen_" + items[i].email,
                                   'phone' : items[i].phone + "_new",
                                   'address' : items[i].address + "_new",
                                   'skype' : items[i].skype + "_new",
                                   'courses' : items[i].courses.all()[0].id },
                                   follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Info on the student has been sucessfully changed.')
            response = client.get('/students/edit/%d/' % items[i].id)  
            self.assertEqual(response.status_code, 200)

            cases = create_cases(items[i], "_new")
            process_cases(self, response, cases)

class StudentDeleteTest(TestCase):

    def test_student_delete(self):
        client = Client()
        response = client.get('/students/remove/1/')
        self.assertEqual(response.status_code, 404)
        
        items = create_students()
        
        response = client.get('/students/remove/1/')
        self.assertEqual(response.status_code, 200)

        response = client.post('/students/remove/1/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Info on student1 1student has been sucessfully deleted.')

    
