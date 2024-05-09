from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import logging


from django.contrib.auth import login
from rest_framework import permissions, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView 
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.models import AuthToken
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator


User = get_user_model()

logger = logging.getLogger(__name__)

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Description of your API",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


# class LoginView(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)

        # Tạo token thông qua Knox
        # Sử dụng UserSerializer để trả về dữ liệu người dùng
        # Gộp dữ liệu người dùng và token vào cùng một response
        # token[1] là chuỗi token, token[0] là đối tượng token
        # token = AuthToken.objects.create(user)
        # user_serializer = UserSerializer(user)
        # data = {
        #     'user': user_serializer.data,
        #     'token': token[1]  
        # }
        # return Response(data, status=status.HTTP_200_OK)
    
class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            data = {
                "user": UserSerializer(user).data,
                "token": token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])     
@permission_classes([AllowAny])
def search_user(request):
    search_text = request.data.get('search_text', '')
    users = get_user_model().objects.filter(name_user__icontains=search_text)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

class SearchCurriculum(APIView):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    def post(self, request):
        search_text = request.data.get('search_text', '')  # Lấy dữ liệu từ body request
        list_users = Curriculum.objects.filter(name__icontains=search_text)
        serializer = CurriculumSerializer(list_users, many=True)
        return Response(serializer.data)
    

class SearchCourse(APIView):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    def post(self, request):
        search_text = request.data.get('search_text', '')  # Lấy dữ liệu từ body request
        list_users = Course.objects.filter(name__icontains=search_text)
        serializer = CourseSerializer(list_users, many=True)
        return Response(serializer.data)


class UserCreateAPIView(APIView):
    #  lay toan bo user 
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # dki user 
    # def post(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserCreateAPIViewDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # permission_classes = [IsAuthenticated]
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDeleteChildView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserRemoveAssociationsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CourseListView(APIView):
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get(self, request):
        curriculum = Course.objects.all()
        serializer = CourseSerializer(curriculum, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data,  partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CourseDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CourseSerializer(curriculum)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        curriculum = self.get_object(pk)
        curriculum.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        # logic co thi thay doi khong co thi them vao du lieu day 
        curriculum = self.get_object(pk)
        serializer = CourseSerializer(curriculum, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
# thuc hien xoa di bảng con trong bang chinh can thiet
class CourseDeleteChildView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CourseSerializer_DeleteChild(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# CURD cho làm curriculum
class CurriculumView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    

    def get(self, request):
        try:
            curriculum = Curriculum.objects.all()
            serializer = CurriculumSerializer(curriculum, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error while getting curriculum data: {str(e)}")
            raise
        
    def post(self, request):
        try:
            serializer = CurriculumSerializer(data=request.data, partial = True )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error while posting curriculum data: {str(e)}")
            raise
    # def put(self, request):
    #     try:
    #         serializer = CurriculumSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         logger.error(f"Error while putting curriculum data: {str(e)}")
    #         raise
    # def post(self, request):
    #     serializer = CurriculumSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CurriculumDetailView(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]
    
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
    
    # dang lôi ham nay 
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("toi yeu em")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request):
    #     serializer = CurriculumSerializer(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CurriculumDeleteChildView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Curriculum.objects.get(pk=pk)
        except Curriculum.DoesNotExist:
            raise Http404
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer_DeleteChild(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurriculumDeleteChildChildView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Curriculum.objects.get(pk=pk)
        except Curriculum.DoesNotExist:
            raise Http404
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer_DeleteChildChild(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CurriculumCourseView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
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
    
class CurriculumCourseDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_objects(self, pk):
        try:
            return CurriculumCourse.objects.get(pk=pk)
        except CurriculumCourse.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        curriculumCourse = self.get_objects(pk)
        serializer = CurriculumCourseSerializer(curriculumCourse)
        return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = CurriculumCourseSerializer(data=request.data, partial=True, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        curriculumCourse = self.get_objects(pk)
        serializer = CurriculumCourseSerializer(curriculumCourse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        curriculumCourse = self.get_objects(pk)
        curriculumCourse.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CurriculumCourseDeleteChild(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return CurriculumCourse.objects.get(pk=pk)
        except CurriculumCourse.DoesNotExist:
            raise Http404
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        curriculumCourse = self.get_object(pk)
        serializer = CurriculumCourseSerializer_DeleteChild(curriculumCourse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# def search_curr(request):
#     if request.method == "POST":
#         search_text = request.POST['search_text']
#     else:
#         search_text = ''
#     curriculum = Curriculum.objects.filter(name__contains=search_text)
#     return render(request, 'search/search.html', {'curriculum': curriculum})

# def search_user(request):
#     if request.method == "POST":
#         search_text = request.POST['search_text']
#     else:
#         search_text = ''
#     user = User.objects.filter(name__contains=search_text)
#     return render(request, 'search/search.html', {'user': user})


#  thuc hien ham search
# def search(request):
#     if request.method == "POST":
#         search_text = request.POST['search_text']
#     else:
#         search_text = ''
#     curriculum = Curriculum.objects.filter(name__contains=search_text)
#     return render(request, 'search/search.html', {'curriculum': curriculum})