from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('item/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    # path('load/', views.load_products)
]
