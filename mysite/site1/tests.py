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
    
    def delete(self, request, pk):
        curriculum = self.get_object(pk)
        curriculum.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        # logic co thi thay doi khong co thi them vao du lieu day 
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer(curriculum, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            
fields = [
    'id_user','role','first_name','last_name','gmail'
]

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
            return instance
        else:
            raise NotFound('User not found so do not updated')