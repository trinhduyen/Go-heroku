from django.urls.conf import include
from django.contrib import admin
from django.urls import path
from .views import *
from . import views
urlpatterns = [
  path('', base.as_view(), name='base'),
  path('List_DV/', listDV.as_view(), name='List_DV'),
  path('List_TB/', listTB.as_view(), name='List_TB'),
  path('List_NTB/', listNTB.as_view(), name='List_NTB'),
  path('List_NVT/', listNVT.as_view(), name='List_NVT'),
  path('List_NV/', listNhanVien.as_view(), name='List_NV'),
  path('List_VT/', listVT.as_view(), name='List_VT'),
  path('List_Xe/', XeRaList.as_view(), name='List_Xe'),
  path('List_Xe2/', XeCRaList.as_view(), name='List_Xe2'),
  path('ShowXeRa/<int:pk>', showXeRa.as_view(), name='showXeRa'),
  path('dowloadPDF/<int:pk>', DownloadPDF.as_view(), name='DownloadPDF'),
  path('ViewPDF/<int:pk>', ViewPDF.as_view(), name='ViewPDF'),
  path('listXe/', listXe.as_view(), name='list_Xe'),
  # bao cao xe
  path('bc/', BCindex.as_view(), name='bcindex'),
  path('bc_xe/', BC.as_view(), name='bcxe'),
  path('bc_xe01/', BaoCaoXe.as_view(), name='bcxe01'),
  path('bc_xe01/chiphitheoxe', Chiphixe.as_view(), name='chiphitheoxe'),
  path('bc_xe01/LSvattu', LSvattu.as_view(), name='LSvattu'),
  path('searchVTMonth/', views.search_vt_m, name ='searchVTMonth'),
  path('XeOnDay/', XeOnDay.as_view(), name='XeOnDay'),

  path('bc_xe01/<int:pk>', BCchiphi.as_view(), name='bchiphi'),
  #bao cao nhan vien
  path('listNV/', listnhanvien.as_view(), name='listnhanvien'),
  
  
 
]
htmlx_urlpatterns=[
 path('abc/', views.test, name='test'),
 path('search_body/', views.search_body, name='search'),
 path('search_nhanvien/', views.search_nhanvien, name='searchNV'),
 path('search_vt_nhanvien/<str:pk>', views.search_vt_nhanvien, name='searchVTNV'),
 path('search_xevt/', views.search_xevt, name='searchxevt'),

 
 
]
urlpatterns += htmlx_urlpatterns