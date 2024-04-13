from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView

class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
class UserCreateAPIViewDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, pardir= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CurriculumListView(APIView):
    def get(self, request):
        curriculum = Curriculum.objects.all()
        serializer = CurriculumSerializer(curriculum, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CurriculumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    # def put(self, request, pk):
    #     # logic co thi thay doi khong co thi them vao du lieu day 
    #     curriculum = self.get_object(pk)
    #     serializer = CurriculumSerializer(curriculum, data=request.data, partial = True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
# thuc hien xoa di bảng con trong bang chinh can thiet
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