from django.urls import path
from .views import *


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('courses/', CourseListView.as_view(), name='Courseview'),
    path('courses/<str:pk>', CourseDetailView.as_view(), name='Coursedetailview'),
    path('courses_delete_child/<str:pk>', CourseDeleteChildView.as_view(), name='Curriculumm'),
    #  toan bo user get
    path('users/', UserCreateAPIView.as_view(), name='UserCreateAPIView'),
    # path('users_item/<str:pk>', UserCreateAPIViewDetailItem.as_view(), name='UserCreateAPIViewItem'),
    
    path('users/<str:pk>', UserCreateAPIViewDetail.as_view(), name='UserCreateAPIViews'),
    path('usersdeletechild/<str:pk>', UserDeleteChildView.as_view(), name='UserDeleteChildView'),
    path('search_user/', search_user, name='UserSearchView'),
    
    path('curriculums/', CurriculumView.as_view(), name='CurriculumView'),
    path('curriculums/<str:pk>', CurriculumDetailView.as_view(), name='CurriculumDetailView'),
    # path('search_curriculum/', search_curr, name='CurriculumSearchView'),
    # path('curriculums/<str:pk>', CurriculumDetailView.as_view(), name='CurriculumDetailView'),
    
    path('curriculumdeletechildview/<str:pk>', CurriculumDeleteChildView.as_view(), name='CurriculumDeleteChildView'),
    path('curriculumdeletechildchildview/<str:pk>', CurriculumDeleteChildChildView.as_view(), name='CurriculumDeleteChildChildView'),
    
    path('curriculumcourseview/', CurriculumCourseView.as_view(), name='CurriculumCourseView'),
    path('curriculumcourseview/<str:pk>', CurriculumCourseDetailView.as_view(), name='CurriculumCourseViewDetailItem'),
    path('curriculumcoursedeletechild/<str:pk>', CurriculumCourseDeleteChild.as_view(), name='CurriculumCourseDeleteChild'),

    #  bo xung user token 
    path('login/', LoginView.as_view(), name='loginview'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('get-user/', GetUserView.as_view(), name='get-user'),
    
    
    # search 
    path('searchuser/', search_user, name='search-user'),
    path('searchcurr/', SearchCurriculum.as_view(), name='search-user'),
    path('searchcourse/', SearchCourse.as_view(), name='search-course'),
    
]
