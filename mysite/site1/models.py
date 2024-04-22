from django.db import models

class User(models.Model):
    id_user =  models.CharField(max_length=255, primary_key=True)
    role = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gmail = models.EmailField(blank=True)
    courses = models.ManyToManyField('Course', related_name='Course_user', blank=True)
    Curriculum = models.ManyToManyField('Curriculum', related_name='Curriculum_users', blank=True)

    class Meta:
        ordering = ['first_name']    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            "id_user": self.id_user,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gmail": self.gmail,
            "courses": [course.id_course_main for course in self.courses.all()],
            "Curriculum": [curriculum.id_curriculum for curriculum in self.Curriculum.all()]
        }

class SubjectPre(models.Model):
    # id_subject = models.CharField(max_length=255, primary_key=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            # "id": self.id,
            "name": self.name
        }
class CLOs1(models.Model):
    # id_clos1 = models.CharField(max_length=255, primary_key=True)
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(blank=True)
    content = models.CharField(max_length=255,blank=True)
    PLO = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"CLOs1 Order {self.order}: {self.content}"
    
    def to_dict(self):
        return {
            "order": self.order,
            "content": self.content,
            "PLO": self.PLO
        }

class CLOs2(models.Model):
    # id_clos2 = models.CharField(max_length=255, primary_key=True)
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()
    a = models.CharField(max_length=1, blank=True)
    b = models.CharField(max_length=1, blank=True)
    c = models.CharField(max_length=1, blank=True)
    d = models.CharField(max_length=1, blank=True)
    e = models.CharField(max_length=1, blank=True)
    f = models.CharField(max_length=1, blank=True)
    g = models.CharField(max_length=1, blank=True)
    h = models.CharField(max_length=1, blank=True)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"CLOs2 Order {self.order}"

    def to_dict(self):
        return {
            "order": self.order,
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d,
            "e": self.e,
            "f": self.f,
            "g": self.g,
            "h": self.h
        }
class CLOs3(models.Model):
    # id_clos3 = models.CharField(max_length=255, primary_key=True)
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(blank=True)
    exam = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=255, blank=True)
    point = models.CharField(max_length=255, blank=True)
    criteria = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"CLOs3 Order {self.order}: {self.exam}"
    
    def to_dict(self):
        return {
            "order": self.order,
            "exam": self.exam,
            "method": self.method,
            "point": self.point,
            "criteria": self.criteria
        }

class Content(models.Model):
    # id_content = models.CharField(max_length=255, primary_key=True)
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()
    content = models.TextField()
    number_session = models.CharField(max_length=255)
    CLOs = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    self_study = models.CharField(max_length=255)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Content Order {self.order}: {self.content}"
    
    def to_dict(self):
        return {
            "order": self.order,
            "content": self.content,
            "number_session": self.number_session,
            "CLOs": self.CLOs,
            "method": self.method,
            "self_study": self.self_study
        }


class Course(models.Model):
    # id_curriculum = models.CharField(max_length=255, primary_key=True)
    id_course_main = models.CharField(max_length=255, primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curriculums')
    name = models.CharField(max_length=255, blank=True)    # ten curriculum
    title = models.CharField(max_length=255, blank=True)   #     title curriculum
    number_credit = models.CharField(max_length=255, blank= True)   # so tin chi
    # teacher = models.CharField(max_length=255) 
    document = models.TextField(blank=True)  
    target = models.TextField(blank=True)
    description = models.TextField(blank=True)
    subject_similar = models.IntegerField(blank=True)
    
    subject_pre = models.ManyToManyField(SubjectPre, blank=True)
    CLOs1 = models.ManyToManyField(CLOs1, blank=True)
    CLOs2 = models.ManyToManyField(CLOs2, blank=True)
    CLOs3 = models.ManyToManyField(CLOs3, blank=True)
    content = models.ManyToManyField(Content, blank=True)
    primary_teacher = models.ManyToManyField(User, related_name='courses_as_primary_teacher', blank=True)  # Giáo viên chính
    head_department = models.ManyToManyField(User, related_name='courses_as_head_department', blank=True)  # Trưởng bộ môn
    teacher = models.ManyToManyField(User, related_name='courses_as_teacher', blank=True)  # Giáo viên

    time_update = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.title
    
    def to_dict(self):
        # Tạo dictionary cho các trường cơ bản
        course_dict = {
            "id_course_main": self.id_course_main,
            "name": self.name,
            "title": self.title,
            "number_credit": self.number_credit,
            "document": self.document,
            "target": self.target,
            "description": self.description,
            "subject_similar": self.subject_similar,
            "time_update": self.time_update
        }

        # Thêm các trường ManyToMany bằng cách sử dụng list comprehension
        course_dict['subject_pre'] = [subject_pre.to_dict() for subject_pre in self.subject_pre.all()]
        course_dict['CLOs1'] = [clos1.to_dict() for clos1 in self.CLOs1.all()]
        course_dict['CLOs2'] = [clos2.to_dict() for clos2 in self.CLOs2.all()]
        course_dict['CLOs3'] = [clos3.to_dict() for clos3 in self.CLOs3.all()]
        course_dict['content'] = [content.to_dict() for content in self.content.all()]
        course_dict['primary_teacher'] = [teacher.to_dict() for teacher in self.primary_teacher.all()]
        course_dict['head_department'] = [head.to_dict() for head in self.head_department.all()]
        course_dict['teacher'] = [teacher.to_dict() for teacher in self.teacher.all()]

        return course_dict
# update db 14/04/2024
    
class CurriculumCourse(models.Model):
    id_curriculumCourse = models.CharField(max_length=200, primary_key=True)
    mandatory = models.BooleanField(default=False)
    is_confirm = models.BooleanField(default=False)
    semester = models.IntegerField(default=1)
    teacher = models.ManyToManyField(User, blank=True)
    id_course = models.ManyToManyField(Course, blank=True)
    
    class Meta:
        ordering = ['id_curriculumCourse']
    
    def __str__(self):
        return self.id_curriculumCourse
    
    def to_dict(self):
        return {
            "id_curriculumCourse": self.id_curriculumCourse,
            "mandatory": self.mandatory,
            "is_confirm": self.is_confirm,
            "semester": self.semester,
            "teacher": [teacher.to_dict() for teacher in self.teacher.all()],
            "id_course": [course.id_course_main for course in self.id_course.all()]
        }
class Curriculum(models.Model):
    id_curriculum = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    curriculum_course = models.ManyToManyField(CurriculumCourse, blank=True, related_name='curriculum_course_ids')
    # user = models.ManyToManyField(User, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "id_curriculum": self.id_curriculum,
            "name": self.name,
            "year": self.year,
            "curriculum_course": [curriculum_course.to_dict() for curriculum_course in self.curriculum_course.all()]
        }