from django.urls import path

from . import views

urlpatterns = [
    path('create', views.CreateRealEstateAPIView.as_view(), name='create_real_estate'),
    path('get-all', views.GetAllRealEstatesAPIView.as_view(), name='get_all_real_estates'),
    path('get/<real_estate_id>', views.GetRealEstateAPIView.as_view(), name='get_real_estate'),
    path('search', views.SearchRealEstatesAPIView.as_view(), name='search_real_estates'),
    path('upload-image', views.UploadRealEstateImageAPIView.as_view(), name='upload_real_estate_image'),
    path('edit/<int:real_estate_id>', views.EditRealEstateAPIView.as_view(), name='edit_real_estate'),
]