from django.db import models

class User(models.Model):
    id_user =  models.CharField(max_length=255, primary_key=True)
    role = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gmail = models.EmailField()

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
    order = models.IntegerField()
    content = models.CharField(max_length=255)
    PLO = models.CharField(max_length=255)

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
    order = models.IntegerField()
    exam = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    point = models.CharField(max_length=255)
    criteria = models.CharField(max_length=255)

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


class Curriculum(models.Model):
    id_curriculum = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curriculums')
    name = models.CharField(max_length=255)    # ten curriculum
    title = models.CharField(max_length=255)   # title curriculum
    number_credit = models.CharField(max_length=255)   # so tin chi
    # teacher = models.CharField(max_length=255) 
    document = models.TextField()  
    target = models.TextField()
    description = models.TextField()
    subject_similar = models.IntegerField()
    # subject_pre = models.ForeignKey(SubjectPre, on_delete=models.CASCADE)
    # CLOs1 = models.ForeignKey(CLOs1, on_delete=models.CASCADE)
    # CLOs2 = models.ForeignKey(CLOs2, on_delete=models.CASCADE)
    # CLOs3 = models.ForeignKey(CLOs3, on_delete=models.CASCADE)
    # content = models.ForeignKey(Content, on_delete=models.CASCADE)
    
    subject_pre = models.ManyToManyField(SubjectPre)
    CLOs1 = models.ManyToManyField(CLOs1)
    CLOs2 = models.ManyToManyField(CLOs2)
    CLOs3 = models.ManyToManyField(CLOs3)
    content = models.ManyToManyField(Content)
    
    time_update = models.CharField(max_length=255)
    primary_teacher = models.CharField(max_length=255)  # Giáo viên chính
    head_department = models.CharField(max_length=255)  # Trưởng bộ môn

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.title




