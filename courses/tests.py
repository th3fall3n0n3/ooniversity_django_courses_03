from django.test import TestCase, Client
from courses.models import Course, Lesson
from courses.forms import CourseModelForm
from coaches.models import Coach
from coaches.tests import create_coaches
from pybursa.tests import process_cases

# Create your tests here.
def change_request(items, i):
    return {'name' : items[i].name + '_new',
                        'short_description' : items[i].short_description + '_new',
                        'description' : items[i].description + '_new'}

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

    def test_detail_response_on_nothing(self):
        client = Client()   
        response = client.get('/courses/1/')
        self.assertEqual(response.status_code, 404)

    def test_detail_response_on_created(self):
        client = Client()
        items = create_courses(lessons=True)
        response = client.get('/courses/1/')
        self.assertEqual(response.status_code, 200)

    def test_detail_present_items_title(self): 
        client = Client()
        items = create_courses(lessons=False)
        for i in items:
            response = client.get('/courses/%d/' % items[i].id)
            self.assertContains(response, '<title>%s Description</title>' % items[i].name )

    def test_detail_present_items_students_url(self):
        client = Client()
        items = create_courses(lessons=False)
        for i in items:
            response = client.get('/courses/%d/' % items[i].id)
            self.assertContains(response, '<a href="/students/?course_id=%d">' % items[i].id )
    
    def test_detail_present_items_name_header(self):
        client = Client()
        items = create_courses(lessons=False)
        for i in items:
            response = client.get('/courses/%d/' % items[i].id)
            self.assertContains(response, '<h1 class="org_name">%s</h1>' % items[i].name )

    def test_detail_present_items_description(self):
        client = Client()
        items = create_courses(lessons=False)
        for i in items:
            response = client.get('/courses/%d/' % items[i].id)
            self.assertContains(response, '<h3 class="org_name">%s</h3>' % items[i].description[:31] )
         
    def test_detail_present_items_description(self):
        client = Client()
        items = create_courses(lessons=False)
        for i in items:
            response = client.get('/courses/%d/' % items[i].id)
            self.assertContains(response, '<a href="/coaches/%d/">%s %s</a>' % (items[i].coach.id, 
                                                                   items[i].coach.user.first_name, 
                                                                   items[i].coach.user.last_name))
          
    def test_detail_add_lesson_button(self):
        client = Client()
        items = create_courses(lessons=True)
        for i in items[0]:
            response = client.get('/courses/%d/' % items[0][i].id)
            self.assertContains(response, '<p class="add_button"><a href="/courses/%d/add_lesson" class="glow_cyan">Add a new lesson</a></p>' % items[0][i].id)

    def test_detail_lessons(self):
        client = Client()
        items = create_courses(lessons=True)
        for i in items[0]:
            for lesson in items[1][i+"_lessons"]:
                response = client.get('/courses/%d/' % items[0][i].id)
                self.assertContains(response, '<td>%s</td><td>%s</td><td>%s</td>' % (lesson.order,
                                                                             lesson.subject,
                                                                             lesson.description))
        
class CoursesListTest(TestCase):

    def test_list_without_courses(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_list_with_courses(self):
        client = Client()
        items = create_courses()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_list_url_details(self):
        client = Client()
        items = create_courses()
        response = client.get('/')      
        for i in items:
            self.assertContains(response, '<a href="/courses/%d/">%s</a>' % (items[i].id,
                                                            items[i].name.upper()))
    def test_list_url_short_description(self):
        client = Client()
        items = create_courses()
        response = client.get('/')      
        for i in items:
            self.assertContains(response, items[i].short_description.title())

    def test_list_url_edit_button(self):
        client = Client()
        items = create_courses()
        response = client.get('/')      
        for i in items:
            self.assertContains(response, '<a href="/courses/edit/%d/" class="btn btn-info"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> Edit</a>' % items[i].id )
    
    def test_list_url_delete_buttton(self):
        client = Client()
        items = create_courses()
        response = client.get('/')      
        for i in items:
            self.assertContains(response, '<a href="/courses/remove/%d/" class="btn btn-info"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>' % items[i].id )

class CoursesEditTest(TestCase):

    def test_edit_no_course(self):
        client = Client()
        response = client.get('/courses/edit/1/')
        self.assertEqual(response.status_code, 404)

    def test_edit_normal_response(self):
        client = Client()
        items = create_courses()
        response = client.get('/courses/edit/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_edit_name_display(self):
        client = Client()
        items = create_courses()
        for i in items: 
            response = client.get('/courses/edit/%d/' % (items[i].id))
            self.assertContains(response, '<input id="id_name" maxlength="100" name="name" type="text" value="%s" />' % (items[i].name))

    def test_edit_short_description_display(self):
        client = Client()
        items = create_courses()
        for i in items: 
            response = client.get('/courses/edit/%d/' % (items[i].id))
            self.assertContains(response, '<input id="id_short_description" maxlength="255" name="short_description" type="text" value="%s" />' % (items[i].short_description))

    def test_edit_description_area(self):
        client = Client()
        items = create_courses()
        for i in items: 
            response = client.get('/courses/edit/%d/' % (items[i].id))
            self.assertContains(response, '<input id="id_short_description" maxlength="255" name="short_description" type="text" value="%s" />' % (items[i].short_description ))

    def test_edit_description_text(self):
        client = Client()
        items = create_courses()
        for i in items: 
            response = client.get('/courses/edit/%d/' % (items[i].id))
            self.assertContains(response, items[i].description)

    def test_edit_post(self):
        client = Client()
        items = create_courses()
        for i in items:
            response = client.post('/courses/edit/%d/' % items[i].id,
                       change_request(items, i), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_edit_post_message(self):
        client = Client()
        items = create_courses()
        for i in items:
            response = client.post('/courses/edit/%d/' % items[i].id,
                       change_request(items, i), follow=True)
            self.assertContains(response, 'The changes have been saved.')

    def test_edit_name_changed(self):
        client = Client()
        items = create_courses()
        for i in items:
            response = client.post('/courses/edit/%d/' % items[i].id,
                       change_request(items, i),
                        follow=True)
            self.assertContains(response, items[i].name + '_new')

    def test_edit_short_description_changed(self):
        client = Client()
        items = create_courses()
        for i in items:
            response = client.post('/courses/edit/%d/' % items[i].id,
                       change_request(items, i),
                        follow=True)
            self.assertContains(response, items[i].short_description + '_new')

    def test_edit_description_changed(self):
        client = Client()
        items = create_courses()
        for i in items:
            response = client.post('/courses/edit/%d/' % items[i].id,
                       change_request(items, i),
                        follow=True)
            self.assertContains(response, items[i].description + '_new')

class CoursesCreateTest(TestCase):

    def test_create_normal_response(self):
        client = Client()
        response = client.get('/courses/add/')
        self.assertEqual(response.status_code, 200)

    def test_create_button(self):
        client = Client()
        response = client.get('/')
        self.assertContains(response, '<a href="/courses/add/" class="glow_cyan">Add a new course</a>')

    def test_create_name(self):
        client = Client()
        response = client.get('/courses/add/')
        self.assertContains(response, '<input id="id_name" maxlength="100" name="name" type="text" />')

    def test_create_short_description(self):
        client = Client()
        response = client.get('/courses/add/')
        self.assertContains(response, '<input id="id_short_description" maxlength="255" name="short_description" type="text" />')

    def test_create_description_area(self):
        client = Client()
        response = client.get('/courses/add/')
        self.assertContains(response, '<textarea cols="40" id="id_description" name="description" rows="10">')
        
    def test_create_form_submit(self):
        client = Client()
        response = client.get('.courses/add/')

        name = 'Light saber course'
        short_description = 'Course about lightsaber usage'
        description = 'Lightsaber usage description'

        response = client.post('/courses/add/', {'name' : name , 'short_description' : short_description, 'description' : description}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create_created_message(self):
        client = Client()
        response = client.get('/courses/add/')

        name = 'Light saber course'
        short_description = 'Course about lightsaber usage'
        description = 'Lightsaber usage description'

        response = client.post('/courses/add/', {'name' : name , 'short_description' : short_description, 'description' : description}, follow=True)
        self.assertContains(response, 'Course %s has been successfully added.' % name)
        
    def test_create_created_url(self):
        client = Client()
        response = client.get('/courses/add/')

        name = 'Light saber course'
        short_description = 'Course about lightsaber usage'
        description = 'Lightsaber usage description'

        response = client.post('/courses/add/', {'name' : name , 'short_description' : short_description, 'description' : description}, follow=True)
        self.assertContains(response, '<a href="/courses/%d/">%s</a>' % (1, name.upper()))

    def test_create_created_short_description(self):
        client = Client()
        response = client.get('/courses/add/')

        name = 'Light saber course'
        short_description = 'Course about lightsaber usage'
        description = 'Lightsaber usage description'

        response = client.post('/courses/add/', {'name' : name , 'short_description' : short_description, 'description' : description}, follow=True)
        self.assertContains(response, short_description.title())

class LessonCreateTest(TestCase):

    def test_create_lesson_response(self):
        client = Client()
        items = create_courses(lessons=True)
        response = client.get('/courses/1/add_lesson')
        self.assertEqual(response.status_code, 200)

    def test_create_lesson_post_form(self):
        client = Client()    
        items = create_courses(lessons=True)
        for i in items[0]:
            response = client.post('/courses/%d/add_lesson' % items[0][i].id, 
                                   { 'subject' : 'lesson for %s' % items[0][i].name,
                                     'description' : 'Test description for %s course' % items[0][i].name,
                                     'course' : items[0][i].id,
                                     'order' : 66 },
                                   follow=True)
            self.assertEqual(response.status_code, 200)

    def test_create_lesson_post_message(self):
        client = Client()    
        items = create_courses(lessons=True)
        for i in items[0]:
            response = client.post('/courses/%d/add_lesson' % items[0][i].id, 
                                   { 'subject' : 'lesson for %s' % items[0][i].name,
                                     'description' : 'Test description for %s course' % items[0][i].name,
                                     'course' : items[0][i].id,
                                     'order' : 66 },
                                   follow=True)
            self.assertContains(response, 'Lesson lesson for %s has been successfully added.' % items[0][i].name)

    def test_create_lesson_post_created(self):
        client = Client()    
        items = create_courses(lessons=True)
        for i in items[0]:
            response = client.post('/courses/%d/add_lesson' % items[0][i].id, 
                                   { 'subject' : 'lesson for %s' % items[0][i].name,
                                     'description' : 'Test description for %s course' % items[0][i].name,
                                     'course' : items[0][i].id,
                                     'order' : 66 },
                                   follow=True)
            self.assertContains(response, '<td>66</td><td>lesson for %s</td><td>Test description for %s course</td>' % (items[0][i].name, items[0][i].name))

class CoursesDeleteTest(TestCase):

    def test_delete_no_data(self):
        client = Client()
        response = client.get('/courses/remove/1/')
        self.assertEqual(response.status_code, 404)
        
    def test_delete_normal_response(self):
        client = Client()
        items = create_courses()        
        response = client.get('/courses/remove/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_deleted_message(self):
        client = Client()
        items = create_courses()
        response = client.post('/courses/remove/1/', follow=True)
        self.assertContains(response, 'Course %s has been deleted.' % (items['course1'].name))

    def test_delete_item_removed(self):
        client = Client()
        items = create_courses()
        response = client.post('/courses/remove/1/', follow=True)
        self.assertNotContains(response, '<a href="/courses/1/">%s</a>' % (items['course1'].name.upper()))

    def test_delete_only_one_deleted(self):
        client = Client()
        items = create_courses()
        response = client.post('/courses/remove/1/', follow=True)
        self.assertContains(response, '<a href="/courses/2/">%s</a>' % (items['course2'].name.upper()))
