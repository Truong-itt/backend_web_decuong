from django.core.management.base import BaseCommand
from site1.models import Course, User, CurriculumCourse, Curriculum
import json
import os 
class Command(BaseCommand):
    help = 'Export Course data to a JSON file'

    def handle(self, *args, **kwargs):
        current_dir = os.path.dirname(__file__)
        grandparent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        data_dir = os.path.join(grandparent_dir, 'data_example')
        os.makedirs(data_dir, exist_ok=True)
         
        
        courses = Course.objects.all()
        courses_data = [course.to_dict() for course in courses]  
        with open('data_example/courses_data.json', 'w', encoding='utf-8') as f:
            json.dump(courses_data, f, ensure_ascii=False, indent=4)
            
        #  tiep tuc thuc hien voi user 
        user = User.objects.all()
        user_data = [user.to_dict() for user in user]
        
        with open('data_example/user_data.json', 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)
            
        #  thuc hien lay thong tin ra tu curr course 
        currcourse = CurriculumCourse.objects.all()
        currcourse_data = [currcourse.to_dict() for currcourse in currcourse]
        with open('data_example/currcourse_data.json', 'w', encoding='utf-8') as f:
            json.dump(currcourse_data, f, ensure_ascii=False, indent=4)
        
        #  tiep tuc thuc hien cho curr 
        curr = Curriculum.objects.all()
        curr_data = [curr.to_dict() for curr in curr]
        with open('data_example/curr_data.json', 'w', encoding='utf-8') as f:
            json.dump(curr_data, f, ensure_ascii=False, indent=4)
            

        self.stdout.write(self.style.SUCCESS('Successfully exported courses to courses_data.json'))
