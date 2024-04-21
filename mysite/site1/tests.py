from django.test import TestCase

# Create your tests here.


class CurriculumSerializer(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Curriculum
        fields = ['id_curriculum', 'user_id', 'user', 'name', 'title', 'number_credit', 'document', 'target', 'description', 'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2', 'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department']
    
    def create(self, validated_data):
        # Bỏ qua pop user ở đây vì đã handle ở PrimaryKeyRelatedField
        subject_pre_data_list = validated_data.pop('subject_pre', [])
        CLOs1_data_list = validated_data.pop('CLOs1', [])
        CLOs2_data_list = validated_data.pop('CLOs2', [])
        CLOs3_data_list = validated_data.pop('CLOs3', [])
        content_data_list = validated_data.pop('content', [])
        
        curriculum = Curriculum.objects.create(**validated_data)
        
        # Xử lý cho các mối quan hệ ManyToMany...
        
        return curriculum



class CurriculumSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required = True)
    subject_pre = SubjectPreSerializer(many=True, required= False)
    CLOs1 = CLOs1Serializer(many=True, required= False)
    CLOs2 = CLOs2Serializer(many=True, required= False)
    CLOs3 = CLOs3Serializer(many=True, required= False)
    content = ContentSerializer(many=True, required= False)
    # chi tienh gan user vào cho user_id
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),   #chi tinh rang userd id nen tuong utng voi mot id trong model user
        source='user'  # chi dinh truong nay tham chieu den truong user trong curriculum 
        , write_only=True   # chi cho phep ghi
    )
    user =  UserSerializer(read_only=True) # de thien thi thon tin user khi serilize
    class Meta:
        model = Curriculum
        fields = ['id_curriculum', 'user_id', 'user','name', 'title',
                  'number_credit', 'document', 'target', 'description', 
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2', 
                  'CLOs3', 'content', 'time_update','primary_teacher', 
                  'head_department']


        
    def create(self, validated_data):
        user = validated_data.pop('user')
        print(user)
        subject_pre_data_list = validated_data.pop('subject_pre')
        CLOs1_data_list = validated_data.pop('CLOs1')
        CLOs2_data_list = validated_data.pop('CLOs2')
        CLOs3_data_list = validated_data.pop('CLOs3')
        content_data_list = validated_data.pop('content')
        
        # xu li user có ton tai chua 
        # user_id = user_id['user']
        # user = User.objects.filter(id_user = user_id).first()
        # if not user:
        #     raise NotFound('User not found so do not updated')
        
        # xu li cho ac du lieu lien quan
        curriculum = Curriculum.objects.create(user = user,**validated_data)
        
        for subject_pre_data in subject_pre_data_list:
            subject_pre, created = SubjectPre.objects.get_or_create(**subject_pre_data)
            curriculum.subject_pre.add(subject_pre)    
        
        for CLOs1_data in CLOs1_data_list:
            CLOs1, created = CLOs1.objects.get_or_create(**CLOs1_data)
            curriculum.CLOs1.add(CLOs1)
            
        for CLOs2_data in CLOs2_data_list:
            CLOs2, created = CLOs2.objects.get_or_create(**CLOs2_data)
            curriculum.CLOs2.add(CLOs2)
            
        for CLOs3_data in CLOs3_data_list:
            CLOs3, created = CLOs3.objects.get_or_create(**CLOs3_data)
            curriculum.CLOs3.add(CLOs3)
        
        for content_data in content_data_list:
            content, created = Content.objects.get_or_create(**content_data)
            curriculum.content.add(content)
        
        return curriculum    
















from django.db import models

class User(models.Model):
    role = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gmail = models.EmailField()

class Teacher(models.Model):
    name = models.CharField(max_length=255)

class SubjectPre(models.Model):
    name = models.CharField(max_length=255)

class CLOs1(models.Model):
    order = models.IntegerField()
    content = models.TextField()
    PLO = models.CharField(max_length=255)

class CLOs2(models.Model):
    order = models.IntegerField()
    a = models.CharField(max_length=1, blank=True)
    b = models.CharField(max_length=1, blank=True)
    c = models.CharField(max_length=1, blank=True)
    # ... continue for d, e, f, g, h

class CLOs3(models.Model):
    order = models.IntegerField()
    exam = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    point = models.CharField(max_length=255)
    criteria = models.CharField(max_length=255)

class Content(models.Model):
    order = models.IntegerField()
    content = models.TextField()
    number_session = models.CharField(max_length=255)
    CLOs = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    self_study = models.CharField(max_length=255)

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    course_id = models.IntegerField()
    title = models.CharField(max_length=255)
    number_credit = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_teacher')
    document = models.TextField()
    target = models.TextField()
    description = models.TextField()
    subject_pre = models.ForeignKey(SubjectPre, on_delete=models.CASCADE, related_name='subject_pre')
    subject_similar = models.ForeignKey(SubjectPre, on_delete=models.CASCADE, related_name='subject_similar')
    CLOs1 = models.ForeignKey(CLOs1, on_delete=models.CASCADE)
    CLOs2 = models.ForeignKey(CLOs2, on_delete=models.CASCADE)
    CLOs3 = models.ForeignKey(CLOs3, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    time_update = models.CharField(max_length=255)
    primary_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='primary_teacher')
    head_department = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='head_department')

class Curriculum(models.Model):
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum_course = models.ForeignKey('CurriculumCourse', on_delete=models.CASCADE)

class CurriculumCourse(models.Model):
    mandatory = models.BooleanField()
    is_confirm = models.BooleanField()
    semester = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='curriculum_teacher')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

















from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gmail = models.EmailField()
    role = models.IntegerField()

class SubjectPre(models.Model):
    name = models.CharField(max_length=255)

class CLOs1(models.Model):
    order = models.IntegerField()
    content = models.TextField()
    PLO = models.CharField(max_length=255)

class CLOs2(models.Model):
    order = models.IntegerField()
    a = models.CharField(max_length=1, blank=True)
    b = models.CharField(max_length=1, blank=True)
    c = models.CharField(max_length=1, blank=True)
    d = models.CharField(max_length=1, blank=True)
    e = models.CharField(max_length=1, blank=True)
    f = models.CharField(max_length=1, blank=True)
    g = models.CharField(max_length=1, blank=True)
    h = models.CharField(max_length=1, blank=True)

class CLOs3(models.Model):
    order = models.IntegerField()
    exam = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    point = models.CharField(max_length=255)
    criteria = models.CharField(max_length=255)

class Content(models.Model):
    order = models.IntegerField()
    content = models.TextField()
    number_session = models.CharField(max_length=255)
    CLOs = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    self_study = models.CharField(max_length=255)

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_courses')
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    number_credit = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, related_name='teacher_courses', on_delete=models.CASCADE)
    document = models.TextField()
    target = models.TextField()
    description = models.TextField()
    subject_pre = models.ForeignKey(SubjectPre, related_name='pre_courses', on_delete=models.CASCADE)
    subject_similar = models.ForeignKey(SubjectPre, related_name='similar_courses', on_delete=models.CASCADE)
    CLOs1 = models.ForeignKey(CLOs1, on_delete=models.CASCADE)
    CLOs2 = models.ForeignKey(CLOs2, on_delete=models.CASCADE)
    CLOs3 = models.ForeignKey(CLOs3, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    time_update = models.CharField(max_length=255)
    primary_teacher = models.ForeignKey(User, related_name='primary_teachers', on_delete=models.CASCADE)
    head_department = models.ForeignKey(User, related_name='head_departments', on_delete=models.CASCADE)

class Curriculum(models.Model):
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum_course = models.ForeignKey('CurriculumCourse', on_delete=models.CASCADE)

class CurriculumCourse(models.Model):
    mandatory = models.BooleanField()
    is_confirm = models.BooleanField()
    semester = models.IntegerField()
    teacher = models.ForeignKey(User, related_name='course_teachers', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    
    
    
class CourseSerializer_DeleteChild(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                                                 source='user',
                                                 write_only=True)
    user = UserSerializer(read_only=True)
    
    subject_pre_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    CLOs1_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs2_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs3_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    content_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    class Meta:
        model = Course
        fields = ['id_curriculum', 'user_id', 'user', 'name', 
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department',
                  'subject_pre_removal_request', 'CLOs1_removal_request', 'CLOs2_removal_request',
                  'CLOs3_removal_request', 'content_removal_request']
    
    def update(self, instance, validated_data):
        subject_pre_names_to_remove = validated_data.pop('subject_pre_removal_request', [])
        CLOs1_orders_to_remove = validated_data.pop('CLOs1_removal_request', [])
        CLOs2_orders_to_remove = validated_data.pop('CLOs2_removal_request', [])
        CLOs3_orders_to_remove = validated_data.pop('CLOs3_removal_request', [])
        content_orders_to_remove = validated_data.pop('content_removal_request', [])
        
        # Ensure user exists before proceeding
        user_id = validated_data.get('user')
        if user_id is not None:
        # Removing SubjectPre by name
            for name_to_remove in subject_pre_names_to_remove:
                try:
                    instance.subject_pre.filter(name=name_to_remove).delete()
                except SubjectPre.DoesNotExist:
                    pass
            # Removing CLOs1 by order
            for order in CLOs1_orders_to_remove:
                try:
                    instance.CLOs1.filter(order=order).delete()
                except CLOs1.DoesNotExist:
                    pass
            # Removing CLOs2 by order
            for order in CLOs2_orders_to_remove:
                try:
                    instance.CLOs2.filter(order=order).delete()
                except CLOs2.DoesNotExist:
                    pass
            # Removing CLOs3 by order
            for order in CLOs3_orders_to_remove:
                try:
                    instance.CLOs3.filter(order=order).delete()
                except CLOs3.DoesNotExist:
                    pass
            # Removing Content by order
            for order in content_orders_to_remove:
                try:
                    instance.content.filter(order=order).delete()
                except Content.DoesNotExist:
                    pass
        else:
            raise NotFound('User not found so do not updated')

        return super().update(instance, validated_data)
    
    
    
    
    
    
    
    
    
    
    
    
    
   
class CourseSerializer_DeleteChild(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserSerializer(read_only=True)
    
    subject_pre_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    CLOs1_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs2_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs3_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    content_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    class Meta:
        model = Course
        fields = ['id_curriculum', 'user_id', 'user', 'name', 
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department',
                  'subject_pre_removal_request', 'CLOs1_removal_request', 'CLOs2_removal_request',
                  'CLOs3_removal_request', 'content_removal_request']
    
    def update(self, instance, validated_data):
        subject_pre_names_to_remove = validated_data.pop('subject_pre_removal_request', [])
        CLOs1_orders_to_remove = validated_data.pop('CLOs1_removal_request', [])
        CLOs2_orders_to_remove = validated_data.pop('CLOs2_removal_request', [])
        CLOs3_orders_to_remove = validated_data.pop('CLOs3_removal_request', [])
        content_orders_to_remove = validated_data.pop('content_removal_request', [])
        
        # Ensure user exists before proceeding
        user_id = validated_data.get('user')
        if user_id is not None:
        # Removing SubjectPre by name
            for name_to_remove in subject_pre_names_to_remove:
                try:
                    instance.subject_pre.filter(name=name_to_remove).delete()
                except SubjectPre.DoesNotExist:
                    pass
            # Removing CLOs1 by order
            for order in CLOs1_orders_to_remove:
                try:
                    instance.CLOs1.filter(order=order).delete()
                except CLOs1.DoesNotExist:
                    pass
            # Removing CLOs2 by order
            for order in CLOs2_orders_to_remove:
                try:
                    instance.CLOs2.filter(order=order).delete()
                except CLOs2.DoesNotExist:
                    pass
            # Removing CLOs3 by order
            for order in CLOs3_orders_to_remove:
                try:
                    instance.CLOs3.filter(order=order).delete()
                except CLOs3.DoesNotExist:
                    pass
            # Removing Content by order
            for order in content_orders_to_remove:
                try:
                    instance.content.filter(order=order).delete()
                except Content.DoesNotExist:
                    pass
        else:
            raise NotFound('User not found so do not updated')

        return super().update(instance, validated_data)
    











     
class CourseSerializer(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id_curriculum', 'user_id', 'user', 'name', 
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department']
    
    def create(self, validated_data):
        # Bỏ qua pop user ở đây vì đã handle ở PrimaryKeyRelatedField
        if validated_data.get('user'):
            subject_pre_data_list = validated_data.pop('subject_pre', [])
            CLOs1_data_list = validated_data.pop('CLOs1', [])
            CLOs2_data_list = validated_data.pop('CLOs2', [])
            CLOs3_data_list = validated_data.pop('CLOs3', [])
            content_data_list = validated_data.pop('content', [])
            
            curriculum = Curriculum.objects.create(**validated_data)
            
            # Xử lý cho các mối quan hệ ManyToMany...
            for subject_pre_data in subject_pre_data_list:
                subject_pre, created = SubjectPre.objects.get_or_create(**subject_pre_data)
                curriculum.subject_pre.add(subject_pre)    
            
            # for CLOs1_data in CLOs1_data_list:
            #     print(CLOs1_data)
            #     CLOs1, created = CLOs1.objects.get_or_create(**CLOs1_data)
            #     curriculum.CLOs1.add(CLOs1)
            for clos1_data in CLOs1_data_list:
                # Thay đổi biến CLOs1 thành clos1_obj để tránh xung đột tên
                clos1_obj, created = CLOs1.objects.get_or_create(**clos1_data)
                curriculum.CLOs1.add(clos1_obj)
            for CLOs2_data in CLOs2_data_list:
                clos2_obj, created = CLOs2.objects.get_or_create(**CLOs2_data)
                curriculum.CLOs2.add(clos2_obj)
                
            for CLOs3_data in CLOs3_data_list:
                clos3_obj, created = CLOs3.objects.get_or_create(**CLOs3_data)
                curriculum.CLOs3.add(clos3_obj)
            
            for content_data in content_data_list:
                content_obj, created = Content.objects.get_or_create(**content_data)
                curriculum.content.add(content_obj)
            return curriculum
        else:
            raise NotFound('User not found so do not created')

    def update(self, instance, validated_data):
        # instance.id_curriculum = validated_data.get('id_curriculum', instance.id_curriculum)
        if validated_data.get('user'):
            # nhũng dữ liệu cơ bản chỉ get và lưu lại
            instance.name = validated_data.get('name', instance.name)
            instance.title = validated_data.get('title', instance.title)
            instance.number_credit = validated_data.get('number_credit', instance.number_credit)
            instance.document = validated_data.get('document', instance.document)
            instance.target = validated_data.get('target', instance.target)
            instance.description = validated_data.get('description', instance.description)
            instance.subject_similar = validated_data.get('subject_similar', instance.subject_similar)
            instance.time_update = validated_data.get('time_update', instance.time_update)
            instance.primary_teacher = validated_data.get('primary_teacher', instance.primary_teacher)
            instance.head_department = validated_data.get('head_department', instance.head_department)
            instance.save()
            
            if 'subject_pre' in validated_data:
                subject_pre_data_list = validated_data.pop('subject_pre', [])
                existing_subject_pre_items = {item.name: item for item in instance.subject_pre.all()}

                for item_data in subject_pre_data_list:
                    name = item_data['name']
                    subject_pre_item = existing_subject_pre_items.get(name)

                    if subject_pre_item:
                        # Nếu tồn tại, cập nhật thông tin cho subject_pre_item
                        for key, value in item_data.items():
                            setattr(subject_pre_item, key, value)
                        subject_pre_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.subject_pre
                        new_subject_pre_item = SubjectPre.objects.create(**item_data)
                        instance.subject_pre.add(new_subject_pre_item)
                        
            if 'CLOs1' in validated_data:
                CLOs1_data_list = validated_data.pop('CLOs1', [])
                existing_CLOs1_items = {item.order: item for item in instance.CLOs1.all()}

                for item_data in CLOs1_data_list:
                    order = item_data['order']
                    CLOs1_item = existing_CLOs1_items.get(order)

                    if CLOs1_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs1_item
                        for key, value in item_data.items():
                            setattr(CLOs1_item, key, value)
                        CLOs1_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs1
                        new_CLOs1_item = CLOs1.objects.create(**item_data)
                        instance.CLOs1.add(new_CLOs1_item)
                        
            if 'CLOs2' in validated_data:
                CLOs2_data_list = validated_data.pop('CLOs2', [])
                existing_CLOs2_items = {item.order: item for item in instance.CLOs2.all()}

                for item_data in CLOs2_data_list:
                    order = item_data['order']
                    CLOs2_item = existing_CLOs2_items.get(order)

                    if CLOs2_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs2_item
                        for key, value in item_data.items():
                            setattr(CLOs2_item, key, value)
                        CLOs2_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs2
                        new_CLOs2_item = CLOs2.objects.create(**item_data)
                        instance.CLOs2.add(new_CLOs2_item)
            
            if 'CLOs3' in validated_data:
                CLOs3_data_list = validated_data.pop('CLOs3', [])
                existing_CLOs3_items = {item.order: item for item in instance.CLOs3.all()}

                for item_data in CLOs3_data_list:
                    order = item_data['order']
                    CLOs3_item = existing_CLOs3_items.get(order)

                    if CLOs3_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs3_item
                        for key, value in item_data.items():
                            setattr(CLOs3_item, key, value)
                        CLOs3_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào    instance.CLOs3
                        new_CLOs3_item = CLOs3.objects.create(**item_data)
                        instance.CLOs3.add(new_CLOs3_item)
            
            if 'content' in validated_data:
                content_data_list = validated_data.pop('content', [])
                existing_content_items = {item.order: item for item in instance.content.all()}
                
                for item_data in content_data_list:
                    order = item_data['order']
                    content_item = existing_content_items.get(order)
                    
                    if content_item:
                        # Nếu tồn tại, cập nhật thông tin cho content_item
                        for key, value in item_data.items():
                            setattr(content_item, key, value)
                        content_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.content
                        new_content_item = Content.objects.create(**item_data)
                        instance.content.add(new_content_item)
            return instance
        else:
            raise NotFound('User not found so do not updated')
        
        
        
        
        
        
        
        
        
        
    def delete(self, request, pk):
        curriculum = self.get_object(pk)
        curriculum.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class CourseSerializer_DeleteChild(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                                                 source='user',
                                                 write_only=True)
    user = UserSerializer(read_only=True)
    
    subject_pre_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    CLOs1_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs2_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs3_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    content_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    class Meta:
        model = Course
        fields = ['id_curriculum', 'user_id', 'user', 'name', 
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department',
                  'subject_pre_removal_request', 'CLOs1_removal_request', 'CLOs2_removal_request',
                  'CLOs3_removal_request', 'content_removal_request']
    
    def update(self, instance, validated_data):
        subject_pre_names_to_remove = validated_data.pop('subject_pre_removal_request', [])
        CLOs1_orders_to_remove = validated_data.pop('CLOs1_removal_request', [])
        CLOs2_orders_to_remove = validated_data.pop('CLOs2_removal_request', [])
        CLOs3_orders_to_remove = validated_data.pop('CLOs3_removal_request', [])
        content_orders_to_remove = validated_data.pop('content_removal_request', [])
        
        # Ensure user exists before proceeding
        user_id = validated_data.get('user')
        if user_id is not None:
        # Removing SubjectPre by name
            for name_to_remove in subject_pre_names_to_remove:
                try:
                    instance.subject_pre.filter(name=name_to_remove).delete()
                except SubjectPre.DoesNotExist:
                    pass
            # Removing CLOs1 by order
            for order in CLOs1_orders_to_remove:
                try:
                    instance.CLOs1.filter(order=order).delete()
                except CLOs1.DoesNotExist:
                    pass
            # Removing CLOs2 by order
            for order in CLOs2_orders_to_remove:
                try:
                    instance.CLOs2.filter(order=order).delete()
                except CLOs2.DoesNotExist:
                    pass
            # Removing CLOs3 by order
            for order in CLOs3_orders_to_remove:
                try:
                    instance.CLOs3.filter(order=order).delete()
                except CLOs3.DoesNotExist:
                    pass
            # Removing Content by order
            for order in content_orders_to_remove:
                try:
                    instance.content.filter(order=order).delete()
                except Content.DoesNotExist:
                    pass
        else:
            raise NotFound('User not found so do not updated')

        return super().update(instance, validated_data)
    
       
class CourseSerializer(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id_curriculum', 'user_id', 'user', 'name', 
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department']
    
    def create(self, validated_data):
        # Bỏ qua pop user ở đây vì đã handle ở PrimaryKeyRelatedField
        if validated_data.get('user'):
            subject_pre_data_list = validated_data.pop('subject_pre', [])
            CLOs1_data_list = validated_data.pop('CLOs1', [])
            CLOs2_data_list = validated_data.pop('CLOs2', [])
            CLOs3_data_list = validated_data.pop('CLOs3', [])
            content_data_list = validated_data.pop('content', [])
            
            curriculum = Curriculum.objects.create(**validated_data)
            
            # Xử lý cho các mối quan hệ ManyToMany...
            for subject_pre_data in subject_pre_data_list:
                subject_pre, created = SubjectPre.objects.get_or_create(**subject_pre_data)
                curriculum.subject_pre.add(subject_pre)    
            
            # for CLOs1_data in CLOs1_data_list:
            #     print(CLOs1_data)
            #     CLOs1, created = CLOs1.objects.get_or_create(**CLOs1_data)
            #     curriculum.CLOs1.add(CLOs1)
            for clos1_data in CLOs1_data_list:
                # Thay đổi biến CLOs1 thành clos1_obj để tránh xung đột tên
                clos1_obj, created = CLOs1.objects.get_or_create(**clos1_data)
                curriculum.CLOs1.add(clos1_obj)
            for CLOs2_data in CLOs2_data_list:
                clos2_obj, created = CLOs2.objects.get_or_create(**CLOs2_data)
                curriculum.CLOs2.add(clos2_obj)
                
            for CLOs3_data in CLOs3_data_list:
                clos3_obj, created = CLOs3.objects.get_or_create(**CLOs3_data)
                curriculum.CLOs3.add(clos3_obj)
            
            for content_data in content_data_list:
                content_obj, created = Content.objects.get_or_create(**content_data)
                curriculum.content.add(content_obj)
            return curriculum
        else:
            raise NotFound('User not found so do not created')

    def update(self, instance, validated_data):
        # instance.id_curriculum = validated_data.get('id_curriculum', instance.id_curriculum)
        if validated_data.get('user'):
            # nhũng dữ liệu cơ bản chỉ get và lưu lại
            instance.name = validated_data.get('name', instance.name)
            instance.title = validated_data.get('title', instance.title)
            instance.number_credit = validated_data.get('number_credit', instance.number_credit)
            instance.document = validated_data.get('document', instance.document)
            instance.target = validated_data.get('target', instance.target)
            instance.description = validated_data.get('description', instance.description)
            instance.subject_similar = validated_data.get('subject_similar', instance.subject_similar)
            instance.time_update = validated_data.get('time_update', instance.time_update)
            instance.primary_teacher = validated_data.get('primary_teacher', instance.primary_teacher)
            instance.head_department = validated_data.get('head_department', instance.head_department)
            instance.save()
            
            if 'subject_pre' in validated_data:
                subject_pre_data_list = validated_data.pop('subject_pre', [])
                existing_subject_pre_items = {item.name: item for item in instance.subject_pre.all()}

                for item_data in subject_pre_data_list:
                    name = item_data['name']
                    subject_pre_item = existing_subject_pre_items.get(name)

                    if subject_pre_item:
                        # Nếu tồn tại, cập nhật thông tin cho subject_pre_item
                        for key, value in item_data.items():
                            setattr(subject_pre_item, key, value)
                        subject_pre_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.subject_pre
                        new_subject_pre_item = SubjectPre.objects.create(**item_data)
                        instance.subject_pre.add(new_subject_pre_item)
                        
            if 'CLOs1' in validated_data:
                CLOs1_data_list = validated_data.pop('CLOs1', [])
                existing_CLOs1_items = {item.order: item for item in instance.CLOs1.all()}

                for item_data in CLOs1_data_list:
                    order = item_data['order']
                    CLOs1_item = existing_CLOs1_items.get(order)

                    if CLOs1_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs1_item
                        for key, value in item_data.items():
                            setattr(CLOs1_item, key, value)
                        CLOs1_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs1
                        new_CLOs1_item = CLOs1.objects.create(**item_data)
                        instance.CLOs1.add(new_CLOs1_item)
                        
            if 'CLOs2' in validated_data:
                CLOs2_data_list = validated_data.pop('CLOs2', [])
                existing_CLOs2_items = {item.order: item for item in instance.CLOs2.all()}

                for item_data in CLOs2_data_list:
                    order = item_data['order']
                    CLOs2_item = existing_CLOs2_items.get(order)

                    if CLOs2_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs2_item
                        for key, value in item_data.items():
                            setattr(CLOs2_item, key, value)
                        CLOs2_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs2
                        new_CLOs2_item = CLOs2.objects.create(**item_data)
                        instance.CLOs2.add(new_CLOs2_item)
            
            if 'CLOs3' in validated_data:
                CLOs3_data_list = validated_data.pop('CLOs3', [])
                existing_CLOs3_items = {item.order: item for item in instance.CLOs3.all()}

                for item_data in CLOs3_data_list:
                    order = item_data['order']
                    CLOs3_item = existing_CLOs3_items.get(order)

                    if CLOs3_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs3_item
                        for key, value in item_data.items():
                            setattr(CLOs3_item, key, value)
                        CLOs3_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào    instance.CLOs3
                        new_CLOs3_item = CLOs3.objects.create(**item_data)
                        instance.CLOs3.add(new_CLOs3_item)
            
            if 'content' in validated_data:
                content_data_list = validated_data.pop('content', [])
                existing_content_items = {item.order: item for item in instance.content.all()}
                
                for item_data in content_data_list:
                    order = item_data['order']
                    content_item = existing_content_items.get(order)
                    
                    if content_item:
                        # Nếu tồn tại, cập nhật thông tin cho content_item
                        for key, value in item_data.items():
                            setattr(content_item, key, value)
                        content_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.content
                        new_content_item = Content.objects.create(**item_data)
                        instance.content.add(new_content_item)
            return instance
        else:
            raise NotFound('User not found so do not updated')
    
class CurriculumSerializer_DeleteChild(serializers.ModelSerializer):
    curriculum_course = CurriculumCourseSerializer(many=True, required=False)
    curriculum_course_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    class Meta:
        model = Curriculum
        fields = ['id_curriculum', 'name', 'year', 'curriculum_course', 'curriculum_course_removal_request']    
        
    def update(self, instance, validated_data):
        curriculum_course_ids_to_remove = validated_data.pop('curriculum_course_removal_request', [])
        
        for id_to_remove in curriculum_course_ids_to_remove:
            try:
                instance.curriculum_course.filter(id_curriculumCourse=id_to_remove).delete()
            except CurriculumCourse.DoesNotExist:
                pass

        return super().update(instance, validated_data)
    
    
    
    
    
    
    
    
    
    
class CourseSerializer(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id_curriculum', 'user_id', 'user', 'name', 
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department']
    
    def create(self, validated_data):
        # Bỏ qua pop user ở đây vì đã handle ở PrimaryKeyRelatedField
        if validated_data.get('user'):
            subject_pre_data_list = validated_data.pop('subject_pre', [])
            CLOs1_data_list = validated_data.pop('CLOs1', [])
            CLOs2_data_list = validated_data.pop('CLOs2', [])
            CLOs3_data_list = validated_data.pop('CLOs3', [])
            content_data_list = validated_data.pop('content', [])
            
            curriculum = Curriculum.objects.create(**validated_data)
            
            # Xử lý cho các mối quan hệ ManyToMany...
            for subject_pre_data in subject_pre_data_list:
                subject_pre, created = SubjectPre.objects.get_or_create(**subject_pre_data)
                curriculum.subject_pre.add(subject_pre)    
            
            # for CLOs1_data in CLOs1_data_list:
            #     print(CLOs1_data)
            #     CLOs1, created = CLOs1.objects.get_or_create(**CLOs1_data)
            #     curriculum.CLOs1.add(CLOs1)
            for clos1_data in CLOs1_data_list:
                # Thay đổi biến CLOs1 thành clos1_obj để tránh xung đột tên
                clos1_obj, created = CLOs1.objects.get_or_create(**clos1_data)
                curriculum.CLOs1.add(clos1_obj)
            for CLOs2_data in CLOs2_data_list:
                clos2_obj, created = CLOs2.objects.get_or_create(**CLOs2_data)
                curriculum.CLOs2.add(clos2_obj)
                
            for CLOs3_data in CLOs3_data_list:
                clos3_obj, created = CLOs3.objects.get_or_create(**CLOs3_data)
                curriculum.CLOs3.add(clos3_obj)
            
            for content_data in content_data_list:
                content_obj, created = Content.objects.get_or_create(**content_data)
                curriculum.content.add(content_obj)
            return curriculum
        else:
            raise NotFound('User not found so do not created')

    def update(self, instance, validated_data):
        # instance.id_curriculum = validated_data.get('id_curriculum', instance.id_curriculum)
        if validated_data.get('user'):
            # nhũng dữ liệu cơ bản chỉ get và lưu lại
            instance.name = validated_data.get('name', instance.name)
            instance.title = validated_data.get('title', instance.title)
            instance.number_credit = validated_data.get('number_credit', instance.number_credit)
            instance.document = validated_data.get('document', instance.document)
            instance.target = validated_data.get('target', instance.target)
            instance.description = validated_data.get('description', instance.description)
            instance.subject_similar = validated_data.get('subject_similar', instance.subject_similar)
            instance.time_update = validated_data.get('time_update', instance.time_update)
            instance.primary_teacher = validated_data.get('primary_teacher', instance.primary_teacher)
            instance.head_department = validated_data.get('head_department', instance.head_department)
            instance.save()
            
            if 'subject_pre' in validated_data:
                subject_pre_data_list = validated_data.pop('subject_pre', [])
                existing_subject_pre_items = {item.name: item for item in instance.subject_pre.all()}

                for item_data in subject_pre_data_list:
                    name = item_data['name']
                    subject_pre_item = existing_subject_pre_items.get(name)

                    if subject_pre_item:
                        # Nếu tồn tại, cập nhật thông tin cho subject_pre_item
                        for key, value in item_data.items():
                            setattr(subject_pre_item, key, value)
                        subject_pre_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.subject_pre
                        new_subject_pre_item = SubjectPre.objects.create(**item_data)
                        instance.subject_pre.add(new_subject_pre_item)
                        
            if 'CLOs1' in validated_data:
                CLOs1_data_list = validated_data.pop('CLOs1', [])
                existing_CLOs1_items = {item.order: item for item in instance.CLOs1.all()}

                for item_data in CLOs1_data_list:
                    order = item_data['order']
                    CLOs1_item = existing_CLOs1_items.get(order)

                    if CLOs1_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs1_item
                        for key, value in item_data.items():
                            setattr(CLOs1_item, key, value)
                        CLOs1_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs1
                        new_CLOs1_item = CLOs1.objects.create(**item_data)
                        instance.CLOs1.add(new_CLOs1_item)
                        
            if 'CLOs2' in validated_data:
                CLOs2_data_list = validated_data.pop('CLOs2', [])
                existing_CLOs2_items = {item.order: item for item in instance.CLOs2.all()}

                for item_data in CLOs2_data_list:
                    order = item_data['order']
                    CLOs2_item = existing_CLOs2_items.get(order)

                    if CLOs2_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs2_item
                        for key, value in item_data.items():
                            setattr(CLOs2_item, key, value)
                        CLOs2_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs2
                        new_CLOs2_item = CLOs2.objects.create(**item_data)
                        instance.CLOs2.add(new_CLOs2_item)
            
            if 'CLOs3' in validated_data:
                CLOs3_data_list = validated_data.pop('CLOs3', [])
                existing_CLOs3_items = {item.order: item for item in instance.CLOs3.all()}

                for item_data in CLOs3_data_list:
                    order = item_data['order']
                    CLOs3_item = existing_CLOs3_items.get(order)

                    if CLOs3_item:
                        # Nếu tồn tại, cập nhật thông tin cho CLOs3_item
                        for key, value in item_data.items():
                            setattr(CLOs3_item, key, value)
                        CLOs3_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào    instance.CLOs3
                        new_CLOs3_item = CLOs3.objects.create(**item_data)
                        instance.CLOs3.add(new_CLOs3_item)
            
            if 'content' in validated_data:
                content_data_list = validated_data.pop('content', [])
                existing_content_items = {item.order: item for item in instance.content.all()}
                
                for item_data in content_data_list:
                    order = item_data['order']
                    content_item = existing_content_items.get(order)
                    
                    if content_item:
                        # Nếu tồn tại, cập nhật thông tin cho content_item
                        for key, value in item_data.items():
                            setattr(content_item, key, value)
                        content_item.save()  # Lưu thay đổi
                    else:
                        # Nếu không tồn tại, tạo mới và thêm vào instance.content
                        new_content_item = Content.objects.create(**item_data)
                        instance.content.add(new_content_item)
            return instance
        else:
            raise NotFound('User not found so do not updated')
   
   
   
        for teacher_id in teacher_ids:
            teacher = User.objects.filter(id_user=teacher_id).first()
            if teacher:
                curriculum_course.teacher.add(teacher)
   
   
   
class CurriculumDetailView(APIView):
    def get_object(self, pk):
        try:
            return Curriculum.objects.get(pk=pk)
        except Curriculum.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer(curriculum)
        return Response(serializer.data)
   
   
class CurriculumCourseView(APIView):
    def get(self, request):
        curriculumCourse = CurriculumCourse.objects.all()
        serializer = CurriculumCourseSerializer(curriculumCourse, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CurriculumCourseSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class CurriculumCourseSerializer(serializers.ModelSerializer):
    id_course = CourseSerializer(many=True, required=False)
    teacher_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)  # Thêm trường này để nhận ID
    course_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)  # Thêm trường này để nhận ID
    teacher = UserSerializer(many=True, required = False)

    class Meta:
        model = CurriculumCourse
        fields = ['id_curriculumCourse', 'mandatory', 'is_confirm', 'semester', 'teacher', 'id_course', 'teacher_ids','course_ids']
        
    def create(self, validated_data):
        teacher_ids = validated_data.pop('teacher_ids', [])
        course_ids = validated_data.pop('course_ids', [])

        # Tạo đối tượng CurriculumCourse mới
        curriculum_course = CurriculumCourse.objects.create(**validated_data)

        # Thêm giáo viên vào CurriculumCourse nếu họ tồn tại trong cơ sở dữ liệu
        for teacher_id in teacher_ids:
            teacher = User.objects.filter(id_user=teacher_id).first()
            if teacher:
                curriculum_course.teacher.add(teacher)

        # Thêm các khóa học vào CurriculumCourse nếu chúng tồn tại trong cơ sở dữ liệu
        for course_id in course_ids:
            course = Course.objects.filter(id_curriculum=course_id).first()
            if course:
                curriculum_course.id_course.add(course)

        return curriculum_course
    
    
    
# class CurriculumSerializer_DeleteChild(serializers.ModelSerializer):
#     curriculum_course = CurriculumCourseSerializer(many=True, required=False)
#     curriculum_course_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     class Meta:
#         model = Curriculum
#         fields = ['id_curriculum', 'name', 'year', 'curriculum_course', 'curriculum_course_removal_request']
        
#     def update(self, instance, validated_data):
#         curriculum_course_ids_to_remove = validated_data.pop('curriculum_course_removal_request', [])
        
#         for id_to_remove in curriculum_course_ids_to_remove:
#             try:
#                 instance.curriculum_course.filter(id_curriculumCourse=id_to_remove).delete()
#             except CurriculumCourse.DoesNotExist:
#                 pass

#         return super().update(instance, validated_data)


    #     instance.name = validated_data.get('name', instance.name)
    #     instance.year = validated_data.get('year', instance.year)
    #     instance.save()
        
    #     if 'curriculum_course' in validated_data:
    #         curriculum_course_data_list = validated_data.pop('curriculum_course', [])
    #         print(curriculum_course_data_list)
    #         existing_curriculum_course_items = {item.id_curriculumCourse: item for item in instance.curriculum_course.all()}
            
    #         for item_data in curriculum_course_data_list:
    #             curriculum_course_id = item_data.get('id_curriculumCourse')
    #             curriculum_course_item = existing_curriculum_course_items.get(curriculum_course_id)
                
    #             if curriculum_course_item:
    #                 self.update_teacher_and_course(curriculum_course_item, item_data)
    #             else:
    #                 pass
    #     return instance
    
    # def update_teacher_and_course(self, curriculum_course_item, item_data):
    #     # update teachers
    #     teacher_ids_to_add = item_data.get('teacher_ids', [])
    #     for teacher_id in teacher_ids_to_add:
    #         teacher = User.objects.filter(id_user=teacher_id).first()
    #         # da ton tai san teacher
    #         if teacher and ( not curriculum_course_item.teacher.filter(id_user=teacher_id).exists() ):
    #             curriculum_course_item.teacher.add(teacher)
    #     # update courses
    #     course_ids_to_add = item_data.get('course_ids', [])
    #     for course_id in course_ids_to_add:
    #         course = Course.objects.filter(id_curriculum=course_id).first()
    #         if course and ( not curriculum_course_item.id_course.filter(id_curriculum=course_id).exists() ):
    #             curriculum_course_item.id_course.add(course)


    def update(self, instance, validated_data):
        curriculums_data_list = validated_data.pop('curriculums_ids', [])
        courses_data_list = validated_data.pop('courses_ids', [])
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gmail = validated_data.get('gmail', instance.gmail)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        self._handle_associations(instance, curriculums_data_list, courses_data_list)
        return instance

    def _handle_associations(self, user_instance, curriculums_ids, courses_ids):
        if curriculums_ids:
            existing_curriculum_ids = set(user_instance.Curriculum.all().values_list('id_curriculum', flat=True))
            for curriculum_id in curriculums_ids:
                if curriculum_id not in existing_curriculum_ids:
                    curriculum = Curriculum.objects.filter(id_curriculum=curriculum_id).first()
                    if curriculum:
                        user_instance.Curriculum.add(curriculum)
                    else:
                        pass
                        # raise serializers.ValidationError({"curriculums_ids": f"Curriculum with ID {curriculum_id} not found"})

        if courses_ids:
            existing_course_ids = set(user_instance.courses.all().values_list('id_curriculum', flat=True))
            for course_id in courses_ids:
                if course_id not in existing_course_ids:
                    course = Course.objects.filter(id_curriculum=course_id).first()
                    if course:
                        user_instance.courses.add(course)
                    else:
                        pass
                    
                    
    def create(self, validated_data):
        curriculum_course_ids = validated_data.pop('curriculum_course_ids', [])
        curriculum = Curriculum.objects.create(**validated_data)

        for curriculum_course_id in curriculum_course_ids:
            # Sử dụng get_or_create để tránh tạo mới nếu CurriculumCourse đã tồn tại
            curriculum_course, created = CurriculumCourse.objects.get_or_create(
                id_curriculumCourse=curriculum_course_id
            )
            # Chỉ thêm vào curriculum nếu curriculum_course được tạo mới
            if created:
                curriculum.curriculum_course.add(curriculum_course)

        return curriculum
    
    
class CurriculumCourseSerializer(serializers.ModelSerializer):
    id_course = CourseSerializer(many=True, required=False)
    teacher_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)  # Thêm trường này để nhận ID
    course_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)  # Thêm trường này để nhận ID
    teacher = UserSerializer(many=True, required = False)

    class Meta:
        model = CurriculumCourse
        fields = ['id_curriculumCourse', 'mandatory', 'is_confirm', 'semester', 'teacher', 'id_course', 'teacher_ids','course_ids']
        
    def create(self, validated_data):
        teacher_ids = validated_data.pop('teacher_ids', [])
        course_ids = validated_data.pop('course_ids', [])

        # Tạo đối tượng CurriculumCourse mới
        curriculum_course = CurriculumCourse.objects.create(**validated_data)

        # Thêm giáo viên vào CurriculumCourse nếu họ tồn tại trong cơ sở dữ liệu
        for teacher_id in teacher_ids:
            teacher = User.objects.filter(id_user=teacher_id).first()
            if teacher:
                curriculum_course.teacher.add(teacher)

        # Thêm các khóa học vào CurriculumCourse nếu chúng tồn tại trong cơ sở dữ liệu
        for course_id in course_ids:
            course = Course.objects.filter(id_course_main=course_id).first()
            if course:
                curriculum_course.id_course.add(course)

        return curriculum_course

    def update(self, instance, validated_data):
        instance.mandatory = validated_data.get('mandatory', instance.mandatory)
        instance.is_confirm = validated_data.get('is_confirm', instance.is_confirm)
        instance.semester = validated_data.get('semester', instance.semester)
        instance.save()

        # Xử lý thêm giáo viên
        if 'teacher_ids' in validated_data:
            teacher_ids = validated_data.pop('teacher_ids')
            current_teachers = set(instance.teacher.values_list('id_user', flat=True))
            new_teacher_ids = set(teacher_ids) - current_teachers  # Loại bỏ các ID đã tồn tại

            for teacher_id in new_teacher_ids:
                teacher = User.objects.filter(id_user=teacher_id).first()
                if teacher:  # Chỉ thêm nếu giáo viên tồn tại trong database
                    instance.teacher.add(teacher)

        # Tương tự, xử lý thêm khóa học nếu cần
        if 'course_ids' in validated_data:
            course_ids = validated_data.pop('course_ids')
            current_courses = set(instance.id_course.values_list('id_course_main', flat=True))
            new_course_ids = set(course_ids) - current_courses  # Loại bỏ các ID đã tồn tại

            for course_id in new_course_ids:
                course = Course.objects.filter(id_course_main=course_id).first()
                if course:  # Chỉ thêm nếu khóa học tồn tại trong database
                    instance.id_course.add(course)

        return instance
    
    
            # if 'subject_pre' in validated_data:
            #     subject_pre_data_list = validated_data.pop('subject_pre', [])
            #     existing_subject_pre_items = {item.name: item for item in instance.subject_pre.all()}

            #     for item_data in subject_pre_data_list:
            #         name = item_data['name']
            #         subject_pre_item = existing_subject_pre_items.get(name)

            #         if subject_pre_item:
            #             # Nếu tồn tại, cập nhật thông tin cho subject_pre_item
            #             for key, value in item_data.items():
            #                 setattr(subject_pre_item, key, value)
            #             subject_pre_item.save()  # Lưu thay đổi
            #         else:
            #             # Nếu không tồn tại, tạo mới và thêm vào instance.subject_pre
            #             new_subject_pre_item = SubjectPre.objects.create(**item_data)
            #             instance.subject_pre.add(new_subject_pre_item)
                        
            # if 'CLOs1' in validated_data:
            #     CLOs1_data_list = validated_data.pop('CLOs1', [])
            #     existing_CLOs1_items = {item.order: item for item in instance.CLOs1.all()}

            #     for item_data in CLOs1_data_list:
            #         order = item_data['order']
            #         CLOs1_item = existing_CLOs1_items.get(order)

            #         if CLOs1_item:
            #             # Nếu tồn tại, cập nhật thông tin cho CLOs1_item
            #             for key, value in item_data.items():
            #                 setattr(CLOs1_item, key, value)
            #             CLOs1_item.save()  # Lưu thay đổi
            #         else:
            #             # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs1
            #             new_CLOs1_item = CLOs1.objects.create(**item_data)
            #             instance.CLOs1.add(new_CLOs1_item)
                        
            # if 'CLOs2' in validated_data:
            #     CLOs2_data_list = validated_data.pop('CLOs2', [])
            #     existing_CLOs2_items = {item.order: item for item in instance.CLOs2.all()}

            #     for item_data in CLOs2_data_list:
            #         order = item_data['order']
            #         CLOs2_item = existing_CLOs2_items.get(order)

            #         if CLOs2_item:
            #             # Nếu tồn tại, cập nhật thông tin cho CLOs2_item
            #             for key, value in item_data.items():
            #                 setattr(CLOs2_item, key, value)
            #             CLOs2_item.save()  # Lưu thay đổi
            #         else:
            #             # Nếu không tồn tại, tạo mới và thêm vào instance.CLOs2
            #             new_CLOs2_item = CLOs2.objects.create(**item_data)
            #             instance.CLOs2.add(new_CLOs2_item)
            
            # if 'CLOs3' in validated_data:
            #     CLOs3_data_list = validated_data.pop('CLOs3', [])
            #     existing_CLOs3_items = {item.order: item for item in instance.CLOs3.all()}

            #     for item_data in CLOs3_data_list:
            #         order = item_data['order']
            #         CLOs3_item = existing_CLOs3_items.get(order)

            #         if CLOs3_item:
            #             # Nếu tồn tại, cập nhật thông tin cho CLOs3_item
            #             for key, value in item_data.items():
            #                 setattr(CLOs3_item, key, value)
            #             CLOs3_item.save()  # Lưu thay đổi
            #         else:
            #             # Nếu không tồn tại, tạo mới và thêm vào    instance.CLOs3
            #             new_CLOs3_item = CLOs3.objects.create(**item_data)
            #             instance.CLOs3.add(new_CLOs3_item)
            
            # if 'content' in validated_data:
            #     content_data_list = validated_data.pop('content', [])
            #     existing_content_items = {item.order: item for item in instance.content.all()}
                
            #     for item_data in content_data_list:
            #         order = item_data['order']
            #         content_item = existing_content_items.get(order)
                    
            #         if content_item:
            #             # Nếu tồn tại, cập nhật thông tin cho content_item
            #             for key, value in item_data.items():
            #                 setattr(content_item, key, value)
            #             content_item.save()  # Lưu thay đổi
            #         else:
            #             # Nếu không tồn tại, tạo mới và thêm vào instance.content
            #             new_content_item = Content.objects.create(**item_data)
            #             instance.content.add(new_content_item)
                        
                        


class CurriculumSerializer_DeleteChildChild(serializers.ModelSerializer):
    curriculum_course = CurriculumCourseSerializer(many=True, required=False)
    curriculum_course_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    teacher_remove_id = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    id_course_remove_id = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)

    class Meta:
        model = Curriculum
        fields = [
            # 'id_curriculum', 'name', 'year',
            'curriculum_course', 'curriculum_course_removal_request', 'teacher_remove_id', 'id_course_remove_id']
        
    def update(self, instance, validated_data):
        curriculum_course_ids_to_remove = validated_data.pop('curriculum_course_removal_request', [])
        teacher_ids_to_remove = validated_data.pop('teacher_remove_id', [])
        id_courses_to_remove = validated_data.pop('id_course_remove_id', [])
        # Duyệt qua các ID của CurriculumCourse cần xóa
        for id_to_remove in curriculum_course_ids_to_remove:
            curriculum_course = instance.curriculum_course.filter(id_curriculumCourse=id_to_remove).first()
            
            if curriculum_course:
                # Duyệt qua các ID giáo viên cần xóa từ mỗi CurriculumCourse
                for teacher_id in teacher_ids_to_remove:
                    try:
                        teacher = User.objects.get(id_user=teacher_id)
                        curriculum_course.teacher.remove(teacher)  # thuc hien di hai cap
                    except User.DoesNotExist:
                        pass
                
                for id_course in id_courses_to_remove:
                    try:
                        course_id = Course.objects.get(id_course_main=id_course)
                        curriculum_course.id_course.remove(course_id)
                    except Course.DoesNotExist:
                        pass
                # Xóa curriculum_course nếu không còn giáo viên liên kết
                # if not curriculum_course.teacher.all().exists():
                #     curriculum_course.delete()  
        return super().update(instance, validated_data)