from django.contrib import admin
from . models import *
from .forms import *
# Register your models here.


class VTDAdmin(admin.TabularInline):
    model = VatTuDung
    form = F_VatTuDung
    extra = 1
    
class XeVaoAdmin(admin.ModelAdmin):
    list_display =('sophieu','datetimeXevao','datetimeXera',
                   'BienSoXe','NhanVienPT','LyDoXeVao','Lydo')
    list_filter=('BienSoXe','datetimeXevao')
    search_fields=('sophieu','BienSoXe__BienSoXe','NhanVienPT__TenNV','LyDoXeVao')
    inlines=[VTDAdmin,]
    form =F_XeVao
class XeAdmin(admin.ModelAdmin):
    list_display =('id','BienSoXe','TenXe','IDNhomXe')
    list_filter=('BienSoXe','IDNhomXe')
    search_fields=('id','BienSoXe','TenXe')
    
class NhanVienAdmin(admin.ModelAdmin):
    list_display =('MaNV','TenNV','TuoiNV','Namlv','BangLai')
    search_fields=('MaNV','TenNV','BangLai')    
    
class VatTuDungAdmin(admin.ModelAdmin):
    list_display =('XeVao_id','VtSudung_id','dongia','SoLuong','thanhtien','TrangThaiKho','TrangThaiXuat','DatetimeXuat')
    search_fields=('XeVao__id',)       
    form = F_VatTuDung
class thietbiAdmin(admin.ModelAdmin):
    list_display =('id','IdGroupTB','NameTB')
    search_fields=('NameTB',) 
    form= F_TB

class dvAdmin(admin.ModelAdmin):
    list_display =('id','NameDv')
    search_fields=('NameDv',) 
    form= F_DV    

class materialAdmin(admin.ModelAdmin):
    list_display =('IdVT','NameVT','IdNVTF','IdDV')
    search_fields=('NameVT',)
    form = F_Me

class groupmaterialAdmin(admin.ModelAdmin):
    list_display =('id','NameNVT')
    search_fields=('NameNVT','id')



class groupthietbiAdmin(admin.ModelAdmin):
    list_display =('id','NameGroupTB')
    search_fields=('NameGroupTB','id')    

class nhomxeAdmin(admin.ModelAdmin):
    list_display =('id','Tennhomxe')
    search_fields=('id','Tennhomxe')   
    
admin.site.register(NhanVien,NhanVienAdmin)
admin.site.register(XeVao,XeVaoAdmin)
admin.site.register(dv,dvAdmin)
admin.site.register(thietbi,thietbiAdmin)
admin.site.register(groupthietbi,groupthietbiAdmin)
admin.site.register(groupmaterial,groupmaterialAdmin)
admin.site.register(material,materialAdmin)
admin.site.register(Xe,XeAdmin)
admin.site.register(nhomxe,nhomxeAdmin)
admin.site.register(VatTuDung,VatTuDungAdmin)
