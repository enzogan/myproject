from django.urls import path

from . import views

app_name = 'myapp1'
urlpatterns = [
    # ex: /app1/
    path('', views.index, name='index'),
    # ex: /app1/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /app1/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /app1/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /app1/list
    path('list/', views.qlist.as_view(), name='list'),
    # ex: /app1/question/5
    path('question/<int:question_id>', views.qview.as_view(), name='list'),


    # ex: /app1/student
    path('student/', views.studview, name='studview'),



    # ex: /app1/student/list
    path('student/list/', views.StudentList.as_view(), name='student_list'),
    # ex: /app1/student/5
    path('student/<int:pk>/', views.StudentDetail.as_view(), name='student_detail'),

    # ex: /app1/student/create
    path('student/create/', views.StudentCreate.as_view(), name='student_create'),
    # ex: /app1/student/5/update
    path('student/<int:pk>/update', views.StudentUpdate.as_view(), name='student_update'),
    # ex: /app1/student/5/delete
    path('student/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),

]
