from django.urls import path
from .views import *

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('curriculums/', CurriculumListView.as_view(), name='Curriculum'),
    path('curriculums/<str:pk>', CurriculumDetailView.as_view(), name='Curriculum'),
    path('curriculums_delete_child/<str:pk>', CurriculumDeleteChildView.as_view(), name='Curriculumm'),
    path('users/', UserCreateAPIView.as_view(), name='UserCreateAPIView'),
    path('users/<str:pk>', UserCreateAPIViewDetail.as_view(), name='UserCreateAPIViews'),

]
