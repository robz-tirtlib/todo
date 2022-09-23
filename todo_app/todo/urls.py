from django.urls import path

from todo import views


urlpatterns = [
    path('', views.TodoListView.as_view(), name='todos'),
    path('delete/<int:todo_pk>', views.TodoDeleteView.as_view(),
         name='todos-delete'),
    path('create/', views.TodoCreateView.as_view(), name='todos-create'),
    path('update/<int:todo_pk>', views.TodoUpdateView.as_view(),
         name='todos-update'),
]
