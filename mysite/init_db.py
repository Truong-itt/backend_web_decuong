import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# from django.contrib.auth.models import User 
# as AuthUser

        
from site1.models import Course, SubjectPre, CLOs1, CLOs2, CLOs3, CLOs4, Content, User, CurriculumCourse, Curriculum

    
print(os.environ.get("DJANGO_SETTINGS_MODULE"))

# def create_superuser():
#     if not AuthUser.objects.filter(username='admin').exists():
#         AuthUser.objects.create_superuser('admin', 'admin@example.com', 'admin')
#         print('Superuser created successfully.')
#     else:
#         print('Superuser already exists.')

def create_superuser():
    id_user = 'admin_id'
    email = 'admin@gmail.com'
    first_name = 'Admin'
    last_name = 'User'
    role = 99  # Ví dụ cho role của superuser
    department = 'CNTT'
    password = '123456'

    # Kiểm tra xem superuser đã tồn tại chưa
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(id_user=id_user, email=email, first_name=first_name, last_name=last_name, role=role, department=department,password=password)
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')
        
        
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Lấy đường dẫn tới thư mục 'data'
    data_dir = os.path.join(current_dir, 'data_example')
    
    
    print('Loading data...')
    with open('data_example/courses_data.json', 'r', encoding='utf-8') as file:
        courses_data  = json.load(file)
        
    for course_data in courses_data:
        # print(course_data)
        primary_teachers = []
        for teacher_data in course_data['primary_teacher']:
            '''
            print(teacher_data.get('id_user', ''))
            print(teacher_data.get('role', ''))
            print(teacher_data.get('first_name', ''))
            print(teacher_data.get('last_name', ''))
            print(teacher_data.get('gmail', ''))
            '''
            try:
                user, created = User.objects.get_or_create(
                    id_user = teacher_data['id_user'],
                    defaults={
                        'role': teacher_data['role'],
                        'first_name': teacher_data['first_name'],
                        'last_name': teacher_data['last_name'],
                        'email': teacher_data['email'],
                        'department': teacher_data['department'],
                        'password': teacher_data['password']
                    }
                )
                if created:
                    user.set_password(teacher_data['password'])
                    user.save()
                primary_teachers.append(user)
            except Exception as e:
                print(e)
        
      
                
        head_departments = []
        for teacher_data in course_data['head_department']:
            user, created = User.objects.get_or_create(
                id_user = teacher_data['id_user'],
                defaults={
                    'role': teacher_data['role'],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'department': teacher_data['department'],
                    'password': teacher_data['password']
                }
            )
            if created:
                user.set_password(teacher_data['password'])
                user.save()
            head_departments.append(user)
        
        teachers = []
        for teacher_data in course_data['teacher']:
            user, created = User.objects.get_or_create(
                id_user = teacher_data['id_user'],
                defaults={
                    'role': teacher_data['role'],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'department': teacher_data['department'],
                    'password': teacher_data['password']
                }
            )
            if created:
                user.set_password(teacher_data['password'])
                user.save()
            teachers.append(user)
            
        subject_pres = []
        for sub_item in course_data.get('subject_pre', []):
            sub, created = SubjectPre.objects.get_or_create(
                name = sub_item['name'],
            )
            subject_pres.append(sub)
            
        CLOs1s = []
        for CLOs1_item in course_data.get('CLOs1', []):
            CLOs1_data, created = CLOs1.objects.get_or_create(
                order = CLOs1_item['order'],
                content = CLOs1_item['content'],
                PLO = CLOs1_item['PLO'],
            )
            CLOs1s.append(CLOs1_data)
        
        CLOs2s = []
        for CLOs2_item in course_data.get('CLOs2', []):
            CLOs2_data, created = CLOs2.objects.get_or_create(
                order = CLOs2_item['order'],
                a = CLOs2_item['a'],
                b = CLOs2_item['b'],
                c = CLOs2_item['c'],
                d = CLOs2_item['d'],
                e = CLOs2_item['e'],
                f = CLOs2_item['f'],
                g = CLOs2_item['g'],
                h = CLOs2_item['h']
            )
            CLOs2s.append(CLOs2_data)
   
        CLOs3s = []
        for CLOs3_item in course_data.get('CLOs3', []):
            CLOs3_data, created = CLOs3.objects.get_or_create(
                order = CLOs3_item['order'],
                exam = CLOs3_item['exam'],
                method = CLOs3_item['method'],
                point = CLOs3_item['point'],
                criteria = CLOs3_item['criteria'],
            )
            CLOs3s.append(CLOs3_data)
            
        CLOs4s = []
        for CLos4_item in course_data.get('CLOs4', []):
            CLOs4_data, created = CLOs4.objects.get_or_create(
                order = CLos4_item['order'],
                exam = CLos4_item['exam'],
                method = CLos4_item['method'],
                criteria = CLos4_item['criteria'],
            )
            
        contents = []
        for content_item in course_data.get('content', []):
            content, created = Content.objects.get_or_create(
                order = content_item['order'],
                content = content_item['content'],
                number_session = content_item['number_session'],
                CLOs = content_item['CLOs'],
                method = content_item['method'],
                self_study = content_item['self_study'],
            )
            contents.append(content)
                
        subject_similars = []
        for subject_similar_item in course_data.get('subject_similar', []):
            subject_similar, created = SubjectPre.objects.get_or_create(
                name = subject_similar_item['name'],
            )
            subject_similars.append(subject_similar)
        course, created = Course.objects.get_or_create(
            id_course_main = course_data['id_course_main'],
            defaults={
                'name': course_data.get('name', ''),
                'title': course_data.get('title', '') ,
                'number_credit': course_data.get('number_credit', ''),
                'document': course_data.get('document',''),
                'target': course_data.get('target', ''),
                'description': course_data.get('description',''),
                # 'subject_similar': course_data.get('subject_similar', ''),
                'time_update': course_data.get('time_update', ''),
            }
        )
        course.subject_similar.set(subject_similars)
        course.primary_teacher.set(primary_teachers)
        course.head_department.set(head_departments)
        course.teacher.set(teachers)
        course.subject_pre.set(subject_pres)
        course.CLOs1.set(CLOs1s)
        course.CLOs2.set(CLOs2s)
        course.CLOs3.set(CLOs3s)
        course.CLOs4.set(CLOs4s)
        course.content.set(contents)        
        course.save()


        
    with open('data_example/currcourse_data.json', 'r', encoding='utf-8') as file:
        currcourse_data = json.load(file)
    # noi dung xu li cho cac truong thong thuong va manytomany cho bang currcourse nhieu nhieu gom co teacher va course
    for currcourse_item in currcourse_data:
        teachers = []
        for teacher_data in currcourse_item['teacher']:
            #  chua co thi tao co roi thi lay 
            user, created = User.objects.get_or_create(
                id_user = teacher_data['id_user'],
                defaults={
                    'role': teacher_data['role'],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'department': teacher_data['department'],
                    'password': teacher_data['password']
                }
            )
            if created:
                user.set_password(teacher_data['password'])
                user.save()
            teachers.append(user)
            
        courses = []
        for course_id in currcourse_item['id_course']:
            course = Course.objects.get(id_course_main=course_id)
            courses.append(course)
        
        currcourse, created = CurriculumCourse.objects.get_or_create(
            id_curriculumCourse = currcourse_item['id_curriculumCourse'],
            defaults={
                #  xu li cho cac truong thong thuong
                'mandatory': currcourse_item['mandatory'],
                'is_confirm': currcourse_item['is_confirm'],
                'semester': currcourse_item['semester'],
            }
        )
        #  set lại moi quan he manytomany
        currcourse.teacher.set(teachers)
        currcourse.id_course.set(courses)
        currcourse.save()
        
    #  xu li cho curriculum
    
    with open('data_example/curr_data.json', 'r', encoding='utf-8') as file:
        curr_data = json.load(file)
        
    for curr_item in curr_data:
        currcourses = []
        for currcourse_item in curr_item['curriculum_course']:
            currcourse = CurriculumCourse.objects.get(id_curriculumCourse=currcourse_item['id_curriculumCourse'])
            currcourses.append(currcourse)
        
        curriculum, created = Curriculum.objects.get_or_create(
            id_curriculum = curr_item['id_curriculum'],
            defaults={
                'name': curr_item['name'],
                'year': curr_item['year'],
                'department': curr_item.get('department', ''),
                'note': curr_item.get('note', '')                
            }
        )
        curriculum.curriculum_course.set(currcourses)
        curriculum.save()
        
    #  xu li cho user bo xun moi quan he nhieu nhieu giua user va curriculum va moi quan he nhieu nhieu giua user va course
    #  example data user    
    # [
    # {
    #     "id_user": "id_gv_hung",
    #     "role": 1,
    #     "first_name": "Hung",
    #     "last_name": "Hoang",
    #     "gmail": "hoanghung@gmail.com",
    #     "courses": [
    #         "id_course_dl",
    #         "id_course_ml"
    #     ],
    #     "Curriculum": [
    #         "id_curriculums_nm"
    #     ]
    # }
    # ]
    
    # with open('data_example/user_data.json', 'r', encoding='utf-8') as file:
    #     user_data = json.load(file)
    
    # for user_item in user_data:
    #     user = User.objects.get(id_user=user_item['id_user'])
    #     courses_to_add = []
    #     for course_id in user_item.get('courses', []):
    #         course = Course.objects.get(id_course_main=course_id)
    #         courses_to_add.append(course)
    #     user.courses.add(*courses_to_add)
        
    #     curriculums_to_add = []
    #     for curriculum_id in user_item.get('Curriculum', []):
    #         curriculum = Curriculum.objects.get(id_curriculum=curriculum_id)
    #         curriculums_to_add.append(curriculum)
    #     user.Curriculum.add(*curriculums_to_add)
    #     user.save()
        
    with open('data_example/user_data.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)

    for user_item in user_data:
        user, created = User.objects.get_or_create(
            id_user=user_item['id_user'],
            defaults={
                'email': user_item['email'],
                'first_name': user_item['first_name'],
                'last_name': user_item['last_name'],
                'department': user_item['department'],
                'role': user_item['role'],
                'password': user_item['password']
            }
        )
        
        
        '''
                   'role': teacher_data['role'],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'department': teacher_data['department'],
                    'password': teacher_data['password']
        '''
        if created:
            user.set_password(user_item['password'])
            user.save()
        
        courses_to_add = []
        for course_id in user_item.get('courses', []):
            try:
                course = Course.objects.get(id_course_main=course_id)
                courses_to_add.append(course)
            except Course.DoesNotExist:
                print(f"Course with ID {course_id} not found.")

        user.courses.add(*courses_to_add)
        
        curriculums_to_add = []
        for curriculum_id in user_item.get('Curriculum', []):
            try:
                curriculum = Curriculum.objects.get(id_curriculum=curriculum_id)
                curriculums_to_add.append(curriculum)
            except Curriculum.DoesNotExist:
                print(f"Curriculum with ID {curriculum_id} not found.")

        user.Curriculum.add(*curriculums_to_add)
        user.save()

if __name__ == '__main__':
    create_superuser()
    load_data()
    print('Data loaded successfully')
        
        