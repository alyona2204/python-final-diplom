from django.urls import path
from backend.views import main_index

app_name = 'backend'
urlpatterns = [
    path('', main_index, name='main_index'),
]
