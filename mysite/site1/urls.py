from django.urls import path
from .views import *


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('courses/', CourseListView.as_view(), name='Courseview'),
    path('courses/<str:pk>', CourseDetailView.as_view(), name='Coursedetailview'),
    path('courses_delete_child/<str:pk>', CourseDeleteChildView.as_view(), name='Curriculumm'),
    path('users/', UserCreateAPIView.as_view(), name='UserCreateAPIView'),
    path('users/<str:pk>', UserCreateAPIViewDetail.as_view(), name='UserCreateAPIViews'),
    path('usersdeletechild/<str:pk>', UserDeleteChildView.as_view(), name='UserDeleteChildView'),
    
    path('curriculums/', CurriculumView.as_view(), name='CurriculumView'),
    path('curriculums/<str:pk>', CurriculumDetailView.as_view(), name='CurriculumDetailView'),
    
    # path('curriculums/<str:pk>', CurriculumDetailView.as_view(), name='CurriculumDetailView'),
    
    path('curriculumdeletechildview/<str:pk>', CurriculumDeleteChildView.as_view(), name='CurriculumDeleteChildView'),
    path('curriculumdeletechildchildview/<str:pk>', CurriculumDeleteChildChildView.as_view(), name='CurriculumDeleteChildChildView'),
    
    path('curriculumcourseview/', CurriculumCourseView.as_view(), name='CurriculumCourseView'),
    path('curriculumcourseview/<str:pk>', CurriculumCourseDetailView.as_view(), name='CurriculumCourseView'),
    path('curriculumcoursedeletechild/<str:pk>', CurriculumCourseDeleteChild.as_view(), name='CurriculumCourseDeleteChild'),

]

