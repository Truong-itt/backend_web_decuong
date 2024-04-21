from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class UserSerializer(serializers.ModelSerializer):
    curriculums_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="Các ID của curriculums liên quan đến người dùng."
    )
    courses_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="Các ID của courses liên quan đến người dùng."
    )

    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'gmail', 'courses', 'Curriculum', 'curriculums_ids', 'courses_ids']

    def create(self, validated_data):
        curriculums_data_list = validated_data.pop('curriculums_ids', [])
        courses_data_list = validated_data.pop('courses_ids', [])
        user = User.objects.create(**validated_data)
        self._handle_associations(user, curriculums_data_list, courses_data_list)
        return user

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
            existing_course_ids = set(user_instance.courses.all().values_list('id_course_main', flat=True))
            for course_id in courses_ids:
                if course_id not in existing_course_ids:
                    course = Course.objects.filter(id_course_main=course_id).first()
                    if course:
                        user_instance.courses.add(course)
                    else:
                        pass
                        # raise serializers.ValidationError({"courses_ids": f"Course with ID {course_id} not found"})



class UserRemoveAssociationsSerializer(serializers.ModelSerializer):
    curriculums_ids_remove = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="Các ID của curriculums mà người dùng muốn loại bỏ."
    )
    courses_ids_remove = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="Các ID của courses mà người dùng muốn loại bỏ."
    )

    class Meta:
        model = User
        fields = ['id_user', 'curriculums_ids_remove', 'courses_ids_remove']

    def update(self, instance, validated_data):
        curriculums_ids_remove = validated_data.get('curriculums_ids_remove', [])
        courses_ids_remove = validated_data.get('courses_ids_remove', [])

        if curriculums_ids_remove:
            for curriculum_id in curriculums_ids_remove:
                curriculum = Curriculum.objects.filter(id_curriculum=curriculum_id).first()
                if curriculum:
                    instance.Curriculum.remove(curriculum)

        if courses_ids_remove:
            for course_id in courses_ids_remove:
                course = Course.objects.filter(id_course_main=course_id).first()
                if course:
                    instance.courses.remove(course)

        return instance
    
class SubjectPreSerializer(serializers.ModelSerializer):
    id_subjectpre = serializers.IntegerField(required=False)
    class Meta:
        model = SubjectPre
        fields = ['id', 'name', 'id_subjectpre']
        
class CLOs1Serializer(serializers.ModelSerializer):
    id_clos1 = serializers.IntegerField(required=False)
    class Meta:
        model = CLOs1
        fields = ['id', 'content', 'order', 'PLO', 'id_clos1']
        
class CLOs2Serializer(serializers.ModelSerializer):
    id_clos2 = serializers.IntegerField(required=False)
    class Meta:
        model = CLOs2
        fields = ['id', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'order', 'id_clos2']
        
class CLOs3Serializer(serializers.ModelSerializer):
    id_clos3 = serializers.IntegerField(required=False)
    class Meta:
        model = CLOs3
        fields = ['id', 'order','id_clos3', 'exam', 'method', 'point','criteria']
        
class ContentSerializer(serializers.ModelSerializer):
    id_content = serializers.IntegerField(required=False)
    class Meta:
        model = Content
        fields = ['id', 'order', 'content', 'id_content', 'number_session', 'CLOs', 'method', 'self_study']
        
        
# class UserSerializer(serializers.ModelSerializer):
        
class CourseSerializer(serializers.ModelSerializer):
    subject_pre = SubjectPreSerializer(many=True, required=False)
    CLOs1 = CLOs1Serializer(many=True, required=False)
    CLOs2 = CLOs2Serializer(many=True, required=False)
    CLOs3 = CLOs3Serializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    primary_teacher_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    head_department_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    teachers_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    
    # user_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     source='user',
    #     write_only=True)
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id_course_main', 'name',
                  'title', 'number_credit', 'document', 'target', 'description',
                  'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2',
                  'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department',
                  'primary_teacher_ids', 'head_department_ids', 'teachers_ids','teacher']
    
    def create(self, validated_data):
        # Bỏ qua pop user ở đây vì đã handle ở PrimaryKeyRelatedField
        # if validated_data.get('user'):
            subject_pre_data_list = validated_data.pop('subject_pre', [])
            CLOs1_data_list = validated_data.pop('CLOs1', [])
            CLOs2_data_list = validated_data.pop('CLOs2', [])
            CLOs3_data_list = validated_data.pop('CLOs3', [])
            content_data_list = validated_data.pop('content', [])
            primary_teacher_data_list = validated_data.pop('primary_teacher_ids', [])
            head_department_data_list = validated_data.pop('head_department_ids', [])
            teachers_data_list = validated_data.pop('teachers_ids', [])
            
            curriculum = Course.objects.create(**validated_data)
            
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
                
            for user_id in primary_teacher_data_list:
                primary_teacher = User.objects.filter(id_user=user_id).first()
                if primary_teacher:
                    curriculum.primary_teacher.add(primary_teacher)
            
            for user_id in head_department_data_list:
                head_department = User.objects.filter(id_user=user_id).first()
                if head_department:
                    curriculum.head_department.add(head_department)
                
            for user_id in  teachers_data_list:
                teacher = User.objects.filter(id_user=user_id).first()
                if teacher:
                    curriculum.teacher.add(teacher)
            return curriculum
        # else:
        #     raise NotFound('User not found so do not created')

    def update(self, instance, validated_data):
        # instance.id_curriculum = validated_data.get('id_curriculum', instance.id_curriculum)
        # if validated_data.get('user'):
            # nhũng dữ liệu cơ bản chỉ get và lưu lại
            instance.name = validated_data.get('name', instance.name)
            instance.title = validated_data.get('title', instance.title)
            instance.number_credit = validated_data.get('number_credit', instance.number_credit)
            instance.document = validated_data.get('document', instance.document)
            instance.target = validated_data.get('target', instance.target)
            instance.description = validated_data.get('description', instance.description)
            instance.subject_similar = validated_data.get('subject_similar', instance.subject_similar)
            instance.time_update = validated_data.get('time_update', instance.time_update)
            # instance.primary_teacher = validated_data.get('primary_teacher', instance.primary_teacher)
            # instance.head_department = validated_data.get('head_department', instance.head_department)
            instance.save()
            
            if 'subject_pre' in validated_data:
                new_items_data = validated_data.pop('subject_pre', [])
                # new_ids = {item['id'] for item in new_items_data}  
                print(new_items_data)
                # cap nhat va tao moi 
                for item_data in new_items_data:
                    item_id = item_data.get('id_subjectpre', None)
                    # giai quyet  co và co trong he thong  
                    #  co va chua co trong he  thong
                    
                    # neu item_id ton tai va co trong db thi cap nhat
                    if (item_id is not None) and SubjectPre.objects.filter(id=item_id).exists() :
                        item = SubjectPre.objects.filter(id=item_id).first()  #tim kiem co hay khong
                        if item:
                            for key, value in item_data.items():
                                setattr(item, key, value)
                            item.save()
                    else:
                        item_data.pop('id_subjectpre', None)   # dam bao cho id la None de cap nhat khong bi sai logic 
                        new_item = SubjectPre.objects.create(**item_data)
                        instance.subject_pre.add(new_item)

            if 'CLOs1' in validated_data:
                new_items_data = validated_data.pop('CLOs1', [])
                for item_data in new_items_data:
                    item_id = item_data.get('id_clos1', None)
                    if item_data and CLOs1.objects.filter(id=item_id).exists():
                        item = CLOs1.objects.filter(id=item_id).first()
                        if item:
                            for key, value in item_data.items():
                                setattr(item, key, value)
                            item.save()
                    else:
                        item_data.pop('id_clos1', None)
                        new_item = CLOs1.objects.create(**item_data)
                        instance.CLOs1.add(new_item)
                            
            if 'CLOs2' in validated_data:
                new_items_data = validated_data.pop('CLOs2', [])
                print(new_items_data)
                for item_data in new_items_data:
                    item_id = item_data.get('id_clos2', None)
                    if item_data and CLOs2.objects.filter(id=item_id).exists():
                        item = CLOs2.objects.filter(id=item_id).first()
                        if item:
                            for key, value in item_data.items():
                                setattr(item, key, value)
                            item.save()
                    else:
                        item_data.pop('id_clos2', None)
                        new_item = CLOs2.objects.create(**item_data)
                        instance.CLOs2.add(new_item)
                
            if 'CLOs3' in validated_data:
                new_items_data = validated_data.pop('CLOs3', [])
                
                for item_data in new_items_data:
                    item_id = item_data.get('id_clos3', None)
                    if item_data and CLOs3.objects.filter(id=item_id).exists():
                        item = CLOs3.objects.filter(id=item_id).first()
                        if item:
                            for key, value in item_data.items():
                                setattr(item, key, value)
                            item.save()
                    else:
                        item_data.pop('id_clos3', None)
                        new_item = CLOs3.objects.create(**item_data)
                        instance.CLOs3.add(new_item)
                
            if 'content' in validated_data:
                new_items_data = validated_data.pop('content', [])
                
                for item_data in new_items_data:
                    item_id = item_data.get('id_content', None)
                    if item_data and Content.objects.filter(id=item_id).exists():
                        item = Content.objects.filter(id=item_id).first()
                        if item:
                            for key, value in item_data.items():
                                setattr(item, key, value)
                            item.save()
                    else:
                        item_data.pop('id_content', None)
                        new_item = Content.objects.create(**item_data)
                        instance.content.add(new_item)

            # neu ton tai thi bo qua chua ton tai thi them vao nhung voi dieu kien du lieu day da co trong  db
            if 'primary_teacher_ids' in validated_data:
                primary_teacher_data_list = validated_data.pop('primary_teacher_ids', [])
                # lay id  user tu du lieu da co trong db tu truong primary_teacher trong model Course
                existing_primary_teacher_ids = set(instance.primary_teacher.values_list('id_user', flat=True))
                new_primary_teacher_ids = set(primary_teacher_data_list) - existing_primary_teacher_ids
                for teacher_id in new_primary_teacher_ids:
                    teacher = User.objects.filter(id_user=teacher_id).first()
                    if teacher:
                        instance.primary_teacher.add(teacher)
            
            if 'head_department_ids' in validated_data:
                head_department_data_list = validated_data.pop('head_department_ids', [])
                existing_head_department_ids = set(instance.head_department.values_list('id_user', flat=True))
                new_head_department_ids = set(head_department_data_list) - existing_head_department_ids
                for head_id in new_head_department_ids:
                    head_department = User.objects.filter(id_user=head_id).first()
                    if head_department:
                        instance.head_department.add(head_department)
            if 'teachers_ids' in validated_data:
                teachers_data_list = validated_data.pop('teachers_ids', [])
                existing_teacher_ids = set(instance.teacher.values_list('id_user', flat=True))
                new_teacher_ids = set(teachers_data_list) - existing_teacher_ids
                for teacher_id in new_teacher_ids:
                    teacher = User.objects.filter(id_user=teacher_id).first()
                    if teacher:
                        instance.teacher.add(teacher)
            return instance
        # else:
        #     raise NotFound('User not found so do not updated')
    
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

class CurriculumCourseSerializer_DeleteChild(serializers.ModelSerializer):
    # teacher = UserSerializer(many=True, required=False)
    # id_course = CourseSerializer(many=True, required=False)
    teacher_remove_id = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    id_course_remove_id = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    
    class Meta:
        model = CurriculumCourse
        fields = [
            # 'id_curriculumCourse', 'mandatory', 'is_confirm', 'semester', 'teacher', 'id_course', 
                  'teacher_remove_id', 'id_course_remove_id'
                  ]
    
    def update(self, instance, validated_data):
        teacher_ids_to_remove = validated_data.pop('teacher_remove_id', [])
        id_courses_to_remove = validated_data.pop('id_course_remove_id', [])
        
        for teacher_id in teacher_ids_to_remove:
            try:
                teacher = User.objects.get(id_user=teacher_id)
                instance.teacher.remove(teacher)
            except User.DoesNotExist:
                pass
        
        for id_course in id_courses_to_remove:
            try:
                course = Course.objects.get(id_course_main=id_course)
                instance.id_course.remove(course)
            except Course.DoesNotExist:
                pass
        
        return super().update(instance, validated_data)
    
class CourseSerializer_DeleteChild(serializers.ModelSerializer):
    subject_pre_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs1_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs2_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    CLOs3_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    content_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    primary_teacher_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    head_department_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    teacher_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    class Meta:
        model = Course
        fields = [
            # 'id_course_main', 'name', 'title', 'number_credit',
                #   'document', 'target', 'description', 'subject_similar', 
                #   'time_update',
                #   'primary_teacher', 'head_department', 'teacher'
                'subject_pre_removal_request','CLOs1_removal_request','CLOs2_removal_request', 'CLOs3_removal_request','content_removal_request', 
                'primary_teacher_removal_request', 'head_department_removal_request', 'teacher_removal_request'
                ]
    def update(self, instance, validated_data):
        subject_pre_names_to_remove = validated_data.pop('subject_pre_removal_request', [])
        CLOs1_orders_to_remove = validated_data.pop('CLOs1_removal_request', [])
        CLOs2_orders_to_remove = validated_data.pop('CLOs2_removal_request', [])
        CLOs3_orders_to_remove = validated_data.pop('CLOs3_removal_request', [])
        content_orders_to_remove = validated_data.pop('content_removal_request', [])
        
        # user gerneral
        primary_teacher_list_to_remove = validated_data.pop('primary_teacher_removal_request', [])
        head_list_to_remove = validated_data.pop('head_department_removal_request', [])
        teacher_list_to_remove = validated_data.pop('teacher_removal_request', [])

        for id in subject_pre_names_to_remove:
            try:
                instance.subject_pre.filter(id=id).delete()
            except SubjectPre.DoesNotExist:
                pass
        # Removing CLOs1 by order
        for id in CLOs1_orders_to_remove:
            try:
                instance.CLOs1.filter(id=id).delete()
            except CLOs1.DoesNotExist:
                pass
        # Removing CLOs2 by order
        for id in CLOs2_orders_to_remove:
            try:
                instance.CLOs2.filter(id=id).delete()
            except CLOs2.DoesNotExist:
                pass
        # Removing CLOs3 by order
        for id in CLOs3_orders_to_remove:
            try:
                instance.CLOs3.filter(id=id).delete()
            except CLOs3.DoesNotExist:
                pass
        # Removing Content by order
        for id in content_orders_to_remove:
            try:
                instance.content.filter(id=id).delete()
            except Content.DoesNotExist:
                pass
            
        for item in primary_teacher_list_to_remove:
            try:
                teacher = User.objects.get(id_user=item)
                instance.primary_teacher.remove(teacher)
            except User.DoesNotExist:
                pass
        
        for item in head_list_to_remove:
            try:
                head = User.objects.get(id_user=item)
                instance.head_department.remove(head)
            except User.DoesNotExist:
                pass
            
        for item in teacher_list_to_remove:
            try:
                teacher = User.objects.get(id_user=item)
                instance.teacher.remove(teacher)
            except User.DoesNotExist:
                pass
        return super().update(instance, validated_data)
        
# class CourseSerializer_DeleteChild(serializers.ModelSerializer):
#     subject_pre = SubjectPreSerializer(many=True, required=False)
#     CLOs1 = CLOs1Serializer(many=True, required=False)
#     CLOs2 = CLOs2Serializer(many=True, required=False)
#     CLOs3 = CLOs3Serializer(many=True, required=False)
#     content = ContentSerializer(many=True, required=False)

    
#     subject_pre_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     CLOs1_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
#     CLOs2_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
#     CLOs3_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
#     content_removal_request = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)  
#     primary_teacher_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     head_department_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     teacher_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     class Meta:
#         model = Course
#         fields = [
#                   'id_course_main', 'name', 
#                   'title', 'number_credit', 'document', 'target', 'description',
#                   'subject_similar', 'subject_pre', 'CLOs1', 'CLOs2','teacher'
#                   'CLOs3', 'content', 'time_update', 'primary_teacher', 'head_department',
#                   'subject_pre_removal_request', 'CLOs1_removal_request', 'CLOs2_removal_request',
#                   'CLOs3_removal_request', 'content_removal_request'
#                   'primary_teacher_removal_request', 'head_department_removal_request', 'teacher_removal_request'
#                   ]
    
#     def update(self, instance, validated_data):
#         subject_pre_names_to_remove = validated_data.pop('subject_pre_removal_request', [])
#         CLOs1_orders_to_remove = validated_data.pop('CLOs1_removal_request', [])
#         CLOs2_orders_to_remove = validated_data.pop('CLOs2_removal_request', [])
#         CLOs3_orders_to_remove = validated_data.pop('CLOs3_removal_request', [])
#         content_orders_to_remove = validated_data.pop('content_removal_request', [])
        
#         # user gerneral
#         primary_teacher_list_to_remove = validated_data.pop('primary_teacher_removal_request', [])
#         head_list_to_remove = validated_data.pop('head_department_removal_request', [])
#         teacher_list_to_remove = validated_data.pop('teacher_removal_request', [])

#         for id in subject_pre_names_to_remove:
#             try:
#                 instance.subject_pre.filter(id=id).delete()
#             except SubjectPre.DoesNotExist:
#                 pass
#         # Removing CLOs1 by order
#         for id in CLOs1_orders_to_remove:
#             try:
#                 instance.CLOs1.filter(id=id).delete()
#             except CLOs1.DoesNotExist:
#                 pass
#         # Removing CLOs2 by order
#         for id in CLOs2_orders_to_remove:
#             try:
#                 instance.CLOs2.filter(id=id).delete()
#             except CLOs2.DoesNotExist:
#                 pass
#         # Removing CLOs3 by order
#         for id in CLOs3_orders_to_remove:
#             try:
#                 instance.CLOs3.filter(id=id).delete()
#             except CLOs3.DoesNotExist:
#                 pass
#         # Removing Content by order
#         for id in content_orders_to_remove:
#             try:
#                 instance.content.filter(id=id).delete()
#             except Content.DoesNotExist:
#                 pass
            
#         for item in primary_teacher_list_to_remove:
#             try:
#                 teacher = User.objects.get(id_user=item)
#                 instance.primary_teacher.remove(teacher)
#             except User.DoesNotExist:
#                 pass
        
#         for item in head_list_to_remove:
#             try:
#                 head = User.objects.get(id_user=item)
#                 instance.head_department.remove(head)
#             except User.DoesNotExist:
#                 pass
            
#         for item in teacher_list_to_remove:
#             try:
#                 teacher = User.objects.get(id_user=item)
#                 instance.teacher.remove(teacher)
#             except User.DoesNotExist:
#                 pass
#         return super().update(instance, validated_data)
        
class CurriculumSerializer(serializers.ModelSerializer):
    curriculum_course_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    curriculum_course = CurriculumCourseSerializer(many=True, required=False)
    curriculum_course_ids = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    class Meta:
        model = Curriculum
        fields = ['id_curriculum', 'name', 'year','curriculum_course','curriculum_course_ids','curriculum_course_data']
        
    #  them dua tren id_course muon co thi thuc thi ham ben kia truoc
    # def create(self, validated_data):
    #     curriculum_course_data_list = validated_data.pop('curriculum_course_ids', [])
    #     curriculum = Curriculum.objects.create(**validated_data)
    #     for curriculum_course_id in curriculum_course_data_list:
    #         curriculum_course = CurriculumCourse.objects.filter(id_curriculumCourse=curriculum_course_id).first()
    #         if curriculum_course:
    #             curriculum.curriculum_course.add(curriculum_course)
    #     return curriculum

    # thuc hien don gian cap nhat truong don gian vâcp nhat them moi curriculum_course
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.year = validated_data.get('year', instance.year)
    #     instance.save()
    #     curriculum_courses_data = validated_data.get('curriculum_course_ids', [])
    #     existing_ids = set([str(course.id) for course in instance.curriculum_course.all()])
    #     new_ids = set(curriculum_courses_data) - existing_ids
    #     for course_id in new_ids:
    #         course_instance = CurriculumCourse.objects.filter(id_curriculumCourse=course_id).first()
    #         if course_instance:
    #             instance.curriculum_course.add(course_instance)
    #     return instance
        
    def create(self, validated_data):
        curriculum_course_data = validated_data.pop('curriculum_course_data', [])
        curriculum = Curriculum.objects.create(**validated_data)

        for course_data in curriculum_course_data:
            curriculum_course, created = CurriculumCourse.objects.get_or_create(
                id_curriculumCourse=course_data['id_curriculumCourse'],
                defaults={
                    'mandatory': course_data.get('mandatory', False),
                    'is_confirm': course_data.get('is_confirm', False),
                    'semester': course_data.get('semester', None)  # Cung cấp giá trị mặc định cho semester
                }
            )
            print(created)
            if created:
                curriculum.curriculum_course.add(curriculum_course)
            if created == False:
                curriculum.curriculum_course.add(curriculum_course)

            # Cập nhật danh sách giáo viên và khóa học
            self._update_curriculum_course_teachers(curriculum_course, course_data.get('teacher_ids', []))
            self._update_curriculum_course_courses(curriculum_course, course_data.get('course_ids', []))

        return curriculum
    
    # def create(self, validated_data):
    #     curriculum_course_data = validated_data.pop('curriculum_course_data', [])
    #     curriculum = Curriculum.objects.create(**validated_data)

    #     for course_data in curriculum_course_data:
    #         try:
    #             curriculum_course, created = CurriculumCourse.objects.get_or_create(
    #                 id_curriculumCourse=course_data['id_curriculumCourse'],
    #                 defaults={
    #                     'mandatory': course_data.get('mandatory', False),
    #                     'is_confirm': course_data.get('is_confirm', False),
    #                     'semester': course_data.get('semester', 1)  # Giá trị mặc định cho semester
    #                 }
    #             )
    #             if created:
    #                 curriculum.curriculum_course.add(curriculum_course)

    #             # Cập nhật danh sách giáo viên và khóa học
    #             self._update_curriculum_course_teachers(curriculum_course, course_data.get('teacher_ids', []))
    #             self._update_curriculum_course_courses(curriculum_course, course_data.get('course_ids', []))
    #         except Exception as e:
    #             # Bạn có thể log ra ngoại lệ này hoặc xử lý thêm
    #             print(f"Error while creating/updating curriculum course: {e}")

    #     return curriculum

            
        # return super().create(validated_data)
    # cai tien cạp nhat curriculum_course neu chua co va them moi bo xung vao cai da co yeu cau co su xac thuc
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.save()

        curriculum_courses_data = validated_data.pop('curriculum_course_data', [])
        existing_curriculum_courses = {cc.id_curriculumCourse: cc for cc in instance.curriculum_course.all()}

        for course_data in curriculum_courses_data:
            course_id = course_data.get('id_curriculumCourse')
            teacher_ids = course_data.get('teacher_ids', [])
            course_ids = course_data.get('course_ids', [])
            
            mandatory = course_data.get('mandatory', False)
            is_confirm = course_data.get('is_confirm', False)
            semester = course_data.get('semester', None)

            # Kiểm tra sự tồn tại của curriculum_course
            curriculum_course = existing_curriculum_courses.get(course_id)
            if not curriculum_course:
                # Tạo mới nếu không tồn tại
                curriculum_course = CurriculumCourse.objects.create(
                    id_curriculumCourse=course_id,
                    mandatory= mandatory,
                    is_confirm= is_confirm,
                    semester= semester
                    )
                instance.curriculum_course.add(curriculum_course)
            else:
                # Cập nhật thông tin nếu đã tồn tại
                curriculum_course.mandatory = mandatory
                curriculum_course.is_confirm = is_confirm
                curriculum_course.semester = semester
                curriculum_course.save()

            # Cập nhật teachers và courses
            self._update_curriculum_course_teachers(curriculum_course, teacher_ids)
            self._update_curriculum_course_courses(curriculum_course, course_ids)

        return instance

    def _update_curriculum_course_teachers(self, curriculum_course, teacher_ids):
        existing_teacher_ids = set(curriculum_course.teacher.values_list('id_user', flat=True))
        for teacher_id in teacher_ids:
            if teacher_id not in existing_teacher_ids:
                try:
                    teacher = User.objects.get(id_user=teacher_id)
                    curriculum_course.teacher.add(teacher)
                except User.DoesNotExist:
                    continue

    def _update_curriculum_course_courses(self, curriculum_course, course_ids):
        existing_course_ids = set(curriculum_course.id_course.values_list('id_course_main', flat=True))
        for course_id in course_ids:
            if course_id not in existing_course_ids:
                try:
                    course = Course.objects.get(id_course_main=course_id)
                    curriculum_course.id_course.add(course)
                except Course.DoesNotExist:
                    continue

class CurriculumSerializer_DeleteChild(serializers.ModelSerializer):
    curriculum_course = CurriculumCourseSerializer(many=True, required=False)
    curriculum_course_removal_request = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        help_text="Danh sách các ID của CurriculumCourse mà bạn muốn loại bỏ khỏi Curriculum này."
    )

    class Meta:
        model = Curriculum
        fields = [
            # 'id_curriculum', 'name', 'year', 
            'curriculum_course',
                  'curriculum_course_removal_request']

    def update(self, instance, validated_data):
        curriculum_course_ids_to_remove = validated_data.pop('curriculum_course_removal_request', [])

        # Duyệt qua danh sách ID và chỉ loại bỏ mối quan hệ
        for id_to_remove in curriculum_course_ids_to_remove:
            curriculum_course = CurriculumCourse.objects.filter(id_curriculumCourse=id_to_remove).first()
            if curriculum_course:
                instance.curriculum_course.remove(curriculum_course)

        # Cập nhật các thuộc tính khác của instance nếu cần
        # instance.name = validated_data.get('name', instance.name)
        # instance.year = validated_data.get('year', instance.year)
        # instance.save()

        return instance

# {
#     "list": [
#         {
#             "curriculum_course_removal_request": "course1",
#             "teacher_remove_id": ["teacher1", "teacher3"],
#             "id_course_remove_id": ["courseID1", "courseID3"]
#         },
#         {
#             "curriculum_course_removal_request": "course2",
#             "teacher_remove_id": ["teacher1", "teacher3"],
#             "id_course_remove_id": ["courseID1", "courseID3"]
#         }
#     ]
# }

class CurriculumSerializer_DeleteChildChild(serializers.ModelSerializer):
    # list = serializers.DictField(child=serializers.CharField(), write_only=True, required=False)
    curriculum_course = CurriculumCourseSerializer(many=True, required=False)
    list = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Curriculum
        fields = ['list','curriculum_course']
        
    def update(self, instance, validated_data):
        # lay list de duyet qua
        list_data = validated_data.pop('list', [])
        print(list_data)
        for data in list_data:
            curriculum_course = instance.curriculum_course.filter(id_curriculumCourse=data['curriculum_course_removal_request']).first()
            if curriculum_course:
                for teacher_id in data['teacher_remove_id']:
                    try:
                        teacher = User.objects.get(id_user=teacher_id)
                        curriculum_course.teacher.remove(teacher)
                    except User.DoesNotExist:
                        pass
                for id_course in data['id_course_remove_id']:
                    try:
                        course_id = Course.objects.get(id_course_main=id_course)
                        curriculum_course.id_course.remove(course_id)
                    except Course.DoesNotExist:
                        pass
        return super().update(instance, validated_data)

# class CurriculumSerializer_DeleteChildChild(serializers.ModelSerializer):
#     curriculum_course = CurriculumCourseSerializer(many=True, required=False)
#     curriculum_course_removal_request = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     teacher_remove_id = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
#     id_course_remove_id = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)

#     class Meta:
#         model = Curriculum
#         fields = [
#             # 'id_curriculum', 'name', 'year',
#             'curriculum_course', 'curriculum_course_removal_request', 'teacher_remove_id', 'id_course_remove_id']
        
#     def update(self, instance, validated_data):
#         curriculum_course_ids_to_remove = validated_data.pop('curriculum_course_removal_request', [])
#         teacher_ids_to_remove = validated_data.pop('teacher_remove_id', [])
#         id_courses_to_remove = validated_data.pop('id_course_remove_id', [])
#         # Duyệt qua các ID của CurriculumCourse cần xóa
#         for id_to_remove in curriculum_course_ids_to_remove:
#             curriculum_course = instance.curriculum_course.filter(id_curriculumCourse=id_to_remove).first()
            
#             if curriculum_course:
#                 # Duyệt qua các ID giáo viên cần xóa từ mỗi CurriculumCourse
#                 for teacher_id in teacher_ids_to_remove:
#                     try:
#                         teacher = User.objects.get(id_user=teacher_id)
#                         curriculum_course.teacher.remove(teacher)  # thuc hien di hai cap
#                     except User.DoesNotExist:
#                         pass
                
#                 for id_course in id_courses_to_remove:
#                     try:
#                         course_id = Course.objects.get(id_course_main=id_course)
#                         curriculum_course.id_course.remove(course_id)
#                     except Course.DoesNotExist:
#                         pass
                # Xóa curriculum_course nếu không còn giáo viên liên kết
                # if not curriculum_course.teacher.all().exists():
                #     curriculum_course.delete()  
        # return super().update(instance, validated_data)
