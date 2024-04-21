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



class UserCreateAPIView(APIView):
    # def post(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self, request):
    #     user = User.objects.all()
    #     serializer = UserSerializer(user, many=True)
    #     return Response(serializer.data)
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class UserCreateAPIViewDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#     def get(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

class UserCreateAPIViewDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDeleteChildView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserRemoveAssociationsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListView(APIView):
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
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CourseSerializer_DeleteChild(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# CURD cho làm curriculum
class CurriculumView(APIView):
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
    def get_object(self, pk):
        try:
            return Curriculum.objects.get(pk=pk)
        except Curriculum.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer_DeleteChild(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurriculumDeleteChildChildView(APIView):
    def get_object(self, pk):
        try:
            return Curriculum.objects.get(pk=pk)
        except Curriculum.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        curriculum = self.get_object(pk)
        serializer = CurriculumSerializer_DeleteChildChild(curriculum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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
    
class CurriculumCourseDetailView(APIView):
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
    def get_object(self, pk):
        try:
            return CurriculumCourse.objects.get(pk=pk)
        except CurriculumCourse.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        curriculumCourse = self.get_object(pk)
        serializer = CurriculumCourseSerializer_DeleteChild(curriculumCourse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Delete child success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
