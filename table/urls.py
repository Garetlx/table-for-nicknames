from django.urls import path
from .  import views

urlpatterns = [
        path('',views.table, name = 'table'),
        path('archive/',views.archive, name = 'archive'),
        path('add_image/',views.add_image, name = 'add_image'),
        path('add_data/',views.add_data, name = 'add_data'),
        path('edit_data/',views.edit_data, name = 'edit_data'),
        
]
