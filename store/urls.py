from django.urls import path
from .views import product_list,search_view,checkout,generate_pdf


urlpatterns = [
    path('store/', product_list, name='store'),
    path('checkout/', checkout, name='checkout'),
    path("search/",search_view, name="search"),
    path('generate-pdf/',generate_pdf, name='generate_pdf'),

]
