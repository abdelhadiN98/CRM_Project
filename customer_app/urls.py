from django.urls import path     
from . import views
urlpatterns = [
    path('services', views.service_page),
    path('add/service', views.create_service),
    path('service/details/<service_id>', views.service_details),
    path('delete/service/<service_id>', views.delete_service),
    path('update/service/<service_id>', views.update_service),
    path('edit/<service_id>', views.update_service_info),
    path('create/new_customer', views.create_customer),
    path('addCustomer', views.addCustomer),
    path('myProfile', views.myProfile),
    path('update_info', views.update_info),
    path('addSevriceCustomer/<service_id>', views.addCsutomerToService),
    path('removeService/<service_id>/<customer_id>', views.removeCsutomerToService),
    path('logout', views.logout),
    path('allCustomers', views.allCustomers),
    path('deleteCustomer/<customer_id>', views.deleteCustomer),
]