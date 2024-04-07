from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        # kiem tra du lieu id nay da ton tai hay chua
        if User.objects.filter(id_user = validated_data['id_user']).exists():
            raise ValidationError('User already exists')
        return User.objects.create(**validated_data)
        
class SubjectPreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectPre
        fields = '__all__'
        
class CLOs1Serializer(serializers.ModelSerializer):
    class Meta:
        model = CLOs1
        fields = '__all__'
        
class CLOs2Serializer(serializers.ModelSerializer):
    class Meta:
        model = CLOs2
        fields = '__all__'
        
class CLOs3Serializer(serializers.ModelSerializer):
    class Meta:
        model = CLOs3
        fields = '__all__'
        
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        
# class UserSerializer(serializers.ModelSerializer):
        
class CurriculumSerializer(serializers.ModelSerializer):
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
        model = Curriculum
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
        model = Curriculum
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
        

        
