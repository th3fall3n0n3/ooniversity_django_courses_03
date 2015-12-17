from django.test import TestCase, Client
from courses.models import Course, Lesson
from courses.forms import CourseModelForm
from coaches.models import Coach
from coaches.tests import create_coaches
from pybursa.tests import process_cases

# Create your tests here.
def create_courses(lessons=False):
        items = {}
        create_coaches()
        items['course1'] = Course.objects.create(
            name = 'PyBursa',
            short_description = "Test web development",
            description = "Test description 1",
            coach = Coach.objects.get(user__username='coach1'),
            assistant = Coach.objects.get(user__username='coach2'))

        items['course2'] = Course.objects.create(
            name = 'usruByP',
            short_description = 'wow so much testing',
            description = "Test description 2",
            coach = Coach.objects.get(user__username='coach2'),
            assistant = Coach.objects.get(user__username='coach1'))

        if lessons == True:
            lessons = {}        
            for course in items:
                
                lessons[course+'_lessons']=[]
                for i in range(1,4):
                    lessons[course+'_lessons'].append(Lesson.objects.create(
                        subject = 'Test lesson %d for %s' % (i, items[course].name),
                        description = 'Course %s lesson %s description' % (items[course].name, i),
                        course = Course.objects.get(id=items[course].id),
                        order = i ))

            return items, lessons
        else:
            return items

class CoursesDetailTest(TestCase):

    def test_detail(self):
        client = Client() 
        
        response = client.get('/courses/1/')
        self.assertEqual(response.status_code, 404)

        items = create_courses(lessons=True)

        response = client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)

        for i in items[0]:
            cases = {}
            cases['title'] = '<title>%s Description</title>' % items[0][i].name
            cases['students_url'] = '<a href="/students/?course_id=%d">' % items[0][i].id
            cases['name_header'] = '<h1 class="org_name">%s</h1>' % items[0][i].name
            cases['description'] = '<h3 class="org_name">%s</h3>' % items[0][i].description[:31]
            cases['coach'] = '<a href="/coaches/%d/">%s %s</a>' % (items[0][i].coach.id, 
                                                                   items[0][i].coach.user.first_name, 
                                                                   items[0][i].coach.user.last_name)
            cases['button'] = '<p class="add_button"><a href="/courses/%d/add_lesson" class="glow_cyan">Add a new lesson</a></p>' % items[0][i].id
            for lesson in items[1][i+"_lessons"]:
                cases[lesson.order] = '<td>%s</td><td>%s</td><td>%s</td>' % (lesson.order,
                                                                             lesson.subject,
                                                                             lesson.description)

            response = client.get('/courses/%d/' % items[0][i].id)
            process_cases(self, response, cases)
        
class CoursesListTest(TestCase):

    def test_list(self):
        client = Client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)

        items = create_courses()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)

        for i in items:
            cases={}
            cases['url_detail'] = '<a href="/courses/%d/">%s</a>' % (items[i].id,
                                                            items[i].name.upper())
            cases['course_name'] = items[i].short_description.title()
            cases['edit_button'] = '<a href="/courses/edit/%d/" class="btn btn-info"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> Edit</a>' % items[i].id
            cases['delete_button'] = '<a href="/courses/remove/%d/" class="btn btn-info"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>' % items[i].id

            process_cases(self, response, cases)

class CoursesEditTest(TestCase):

    def test_edit(self):
        client = Client()

        response = client.get('courses/edit/1/')
        self.assertEqual(response.status_code, 404)

        items = create_courses()

        for i in items: 
            url = '/courses/edit/%d/' % (items[i].id)

            def create_cases(item, addin=""):
                cases = {}
                cases['name'] = '<input id="id_name" maxlength="100" name="name" type="text" value="%s" />' % (items[i].name + addin)
                cases['short_description'] = '<input id="id_short_description" maxlength="255" name="short_description" type="text" value="%s" />' % (items[i].short_description + addin)
                cases['description_area'] = '<label for="id_description">Description:</label></th><td><textarea cols="40" id="id_description" name="description" rows="10">'
                cases['description_text'] = items[i].description + addin
                return cases

            cases = create_cases(i)
            response = client.get(url)

            process_cases(self, response, cases)
            
            response = client.post('/courses/edit/%d/' % items[i].id,
                       {'name' : items[i].name + '_new',
                        'short_description' : items[i].short_description + '_new',
                        'description' : items[i].description + '_new'},
                        follow=True)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'The changes have been saved.')
            
            process_cases(self, response, create_cases(i, '_new'))

class CoursesCreateTest(TestCase):

    def test_create(self):
        client = Client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="/courses/add/" class="glow_cyan">Add a new course</a>')

        response = client.get('/courses/1/')
        self.assertEqual(response.status_code, 404)
        
        response = client.get('/courses/add/')
        self.assertEqual(response.status_code, 200)
        
        process_cases(self, response, {
                'name' : '<input id="id_name" maxlength="100" name="name" type="text" />',
                'short_description' : '<input id="id_short_description" maxlength="255" name="short_description" type="text" />',
                'description_area' : '<textarea cols="40" id="id_description" name="description" rows="10">' })

        name = 'Light saber course'
        short_description = 'Course about lightsaber usage'
        description = 'Lightsaber usage description'

        response = client.post('/courses/add/', {'name' : name , 'short_description' : short_description, 'description' : description}, follow=True)
        self.assertEqual(response.status_code, 200)
       
        process_cases(self, response, { 
                'message' : 'Course %s has been successfully added.' % name,
                'url' : '<a href="/courses/%d/">%s</a>' % (1, name.upper()),
                'short_description' : short_description.title()})

class LessonCreateTest(TestCase):

    def test_create_lesson(self):
        client = Client()
    
        items = create_courses(lessons=True)
        for i in items[0]:
            response = client.get('/courses/%d/add_lesson' % items[0][i].id)
            self.assertEqual(response.status_code, 200)
            response = client.post('/courses/%d/add_lesson' % items[0][i].id, 
                                   { 'subject' : 'lesson for %s' % items[0][i].name,
                                     'description' : 'Test description for %s course' % items[0][i].name,
                                     'course' : items[0][i].id,
                                     'order' : 66 },
                                   follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Lesson lesson for %s has been successfully added.' % items[0][i].name)
            self.assertContains(response, '<td>66</td><td>lesson for %s</td><td>Test description for %s course</td>' % (items[0][i].name, items[0][i].name))

class CoursesDeleteTest(TestCase):

    def test_delete(self):
        client = Client()
        response = client.get('/courses/remove/1/')
        self.assertEqual(response.status_code, 404)
        
        items = create_courses()
        
        response = client.get('/courses/remove/1/')
        self.assertEqual(response.status_code, 200)
        
        response = client.post('/courses/remove/1/', follow=True)
        self.assertContains(response, 'Course %s has been deleted.' % (items['course1'].name))
        self.assertNotContains(response, '<a href="/courses/1/">%s</a>' % (items['course1'].name.upper()))
        self.assertContains(response, '<a href="/courses/2/">%s</a>' % (items['course2'].name.upper()))
