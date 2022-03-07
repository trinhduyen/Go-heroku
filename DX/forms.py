from tkinter import HIDDEN
from xml.dom.minidom import Attr
from django.forms import DateTimeField, DateTimeInput, ModelForm, widgets
from .models import *
from django import forms
from django.utils.translation import gettext_lazy as _


class F_groupMe(ModelForm):
    class Meta:
        verbose_name_plural = 'Nhóm Vật Tư'
        model = groupmaterial
        fields = '__all__'  
        labels={
            'NameNVT':_('Tên Nhóm Vật Tư'),
        }
        widgets ={
  
            'NameNVT': forms.TextInput(attrs={"class":"form-control"}),
            
        }
        
        
class  F_Me(ModelForm):
    class Meta:
        model= material
        fields = '__all__'      
        labels={
            'IdVT': _('Mã Vật Tư'),
            'NameVT':_('Tên Vật Tư'),
            'IdNVTF':_('Nhóm Vật Tư'),
            'IdDV':_('Đơn Vị Tính'),

        }    
        widgets ={
            'IdVT': forms.TextInput(attrs={"class":"form-control"}),
            'NameVT': forms.TextInput(attrs={"class":"form-control"}),
            'IdNVTF': forms.Select(attrs={"class":"form-control"}),
            'IdDV': forms.Select(attrs={"class":"form-control"}),
           
        }
        
        
class F_DV(ModelForm):        
    class Meta:
        model = dv
        exclude= ('id',)
        labels={ 
            'NameDv':_('Tên Đơn Vị Tính'),           
        }       
        widgets ={
            'NameDv': forms.TextInput(attrs={"class":"form-control"}),
            
        }

class F_TB(ModelForm):
    
    class Meta:
        model =thietbi
        exclude=('id',)
        labels={

          'NameTB': _('Tên Thiết Bị')
        }
        widgets = {
    
           'NameTB' : forms.TextInput(attrs={"class":"form-control"}),
           
        }
        
class F_NTB(ModelForm):
    
    class Meta:
        model = groupthietbi
        fields = '__all__'  
        labels={
          'NameGroupTB': _('Tên Nhóm Thiết Bị')
        }
        widgets = {
           'NameGroupTB' : forms.TextInput(attrs={"class":"form-control"}),
           
        }        

class  F_XeVao(ModelForm):

    class Meta:
      
        model= XeVao
        fields = '__all__'  
        exclude = ('id',)
       
        labels={
            'datetimeXevao':_('Thời Gian Xe Vào'),
            'BienSoXe': _('Biển Số Xe'),
            'NhanVienPT':_('Nhân Viên Phụ Trách'),
            'LyDoXeVao':_('Tình Trạng Xe Vào'),
            'Lydo': _('Nội Dung Công Việc'),
            'datetimeXera':_('Thời Gian Xe Ra'),
            'Status': _('Chọn nếu xe ra')
        }
        widgets={
        
           'BienSoXe': forms.Select(attrs={"class":"form-control", "id":"bsxvao","onchange":"myFunction()"}),
           'NhanVienPT': forms.Select(attrs={"class":"form-control"}),
           'sophieu': forms.TextInput(attrs={"class":"form-control","readonly": "readonly"}),
           'LyDoXeVao': forms.Textarea(attrs={"class":"form-control","rows":"5"}),
           'Lydo': forms.Textarea(attrs={"class":"form-control","rows":"5"}),
         
        }

      

class F_VatTuDung(ModelForm):
    class Meta:
        model=VatTuDung
        exclude = ('id','XeVao_id',)
        labels={
            'VtSudung':_('Vật Tư Dùng'),
            'SoLuong': _('Số Lượng'),
            'TrangThaiKho':_('Trạng Thái Kho'),
            'TrangThaiXuat':_('Trạng Thái Xuất'),
            'BienSoXeSD' :_('Biển Số Xe'),
            'DatetimeXuat':_('Thời Gian Xuất'),
            'dongia' :_('Đơn Giá'),
            'thanhtien':_('Thành Tiền'),
        }
        widgets={
           'VtSudung': forms.Select(attrs={"class":"form-control"}),
           'SoLuong': forms.NumberInput(attrs={"class":"form-control","onkeyup":" mykeyupTT()","step":"1"}),
           'dongia': forms.NumberInput(attrs={"class":"form-control","onkeyup":" mykeyupTT()","step":"0.1"}),
           'thanhtien': forms.TextInput(attrs={"class":"form-control","readonly": "readonly","step":"0.01"}),
           'BienSoXeSD': forms.TextInput(attrs={"class":"form-control", "type":"hidden"}),
           'TrangThaiKho': forms.Select(attrs={"class":"form-control" }),
           'TrangThaiXuat': forms.Select(attrs={"class":"form-control ttXuat","onchange":"mychangeX()"}),
        
        }         