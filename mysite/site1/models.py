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

class SubjectPre(models.Model):
    # id_subject = models.CharField(max_length=255, primary_key=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

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