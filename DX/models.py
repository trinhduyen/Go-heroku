from datetime import timezone
from django.db import models
import uuid
from django.db.models.deletion import CASCADE



class groupmaterial(models.Model):
    NameNVT = models.CharField(max_length=255, unique=True,verbose_name='Tên Nhóm Vật Tư')
    class Meta:
        verbose_name_plural = 'Nhóm Vật Tư'
    def __str__(seft):
        return seft.NameNVT
    
class dv(models.Model):  
    NameDv= models.CharField(max_length = 255, unique=True,verbose_name='Tên Đơn Vị')
    class Meta:
       
        verbose_name_plural = 'Đơn Vị Tính'
    
    def __str__(seft):
            return seft.NameDv
    
class material(models.Model):
    IdVT = models.CharField(unique=True,max_length=255,verbose_name='Mã Vật Tư')   
    NameVT = models.CharField(max_length=255, unique=True,verbose_name='Tên Vật Tư')
    IdNVTF = models.ForeignKey(groupmaterial,on_delete = models.SET_NULL,verbose_name='Nhóm Vật Tư', null=True) 
    IdDV = models.ForeignKey(dv, on_delete =  models.SET_NULL,verbose_name='Đơn Vị Tính',null=True)
    class Meta:
           
        verbose_name_plural= 'Vật Tư'
    def __str__(self):
        return self.NameVT


    
class groupthietbi(models.Model):
    NameGroupTB = models.CharField(max_length=255, unique=True,verbose_name='Tên Nhóm Thiết Bị')    
    class Meta:
           
       verbose_name_plural = 'Nhóm Thiết Bị'
    def __str__(seft):
        return seft.NameGroupTB

class thietbi(models.Model):
    IdGroupTB= models.ForeignKey(groupthietbi, on_delete= models.SET_NULL,verbose_name='Nhóm Thiết Bị',null=True)    
    NameTB = models.CharField(max_length=255, unique=True,verbose_name='Tên Thiết Bị')
    class Meta:     
        verbose_name_plural = 'Thiết Bị'
    def __str__(seft):
        return seft.NameTB

class nhomxe(models.Model):
    Tennhomxe = models.CharField(max_length=255, verbose_name='Tên Nhóm Xe')
    class Meta:
        verbose_name_plural = 'Nhóm Xe Máy'
    def __str__(self):
            return self.Tennhomxe
        
class Xe(models.Model):
    IDNhomXe = models.ForeignKey(nhomxe, on_delete=models.SET_NULL,null=True, verbose_name='Tên Nhóm Xe')
    BienSoXe = models.CharField(max_length=255,unique=True, verbose_name='Biển Số Xe')
    TenXe = models.CharField(max_length=255, verbose_name='Tên Xe')
    class Meta:
           
        verbose_name_plural = 'Thông Tin Xe'
    def __str__(self):
        return self.BienSoXe
    
    
class NhanVien(models.Model):
    MaNV = models.CharField(max_length=255, unique=True,verbose_name='Mã Nhân Viên')
    TenNV = models.CharField(max_length=255,verbose_name='Tên Nhân Viên')
    TuoiNV= models.IntegerField(verbose_name='Tuổi Nhân Viên')
    Namlv= models.IntegerField(verbose_name='Số Năm Làm Việc')
    BangLai =  models.CharField( max_length=50 , verbose_name='Bằng Lái')
    class Meta:
        verbose_name_plural = 'Nhân Viên Bảo Dưỡng'
    def __str__(sefl):
        return sefl.TenNV
        
trangthaikho = {
    ("Có", "Có"),
    ("Không", "Không")
}    
    
trangthaixuat={
    ("Đã Xuất", "Đã Xuất"),
    ("Chưa Xuất", "Chưa Xuất")
} 

class XeVao(models.Model):
    sophieu = models.UUIDField(default=uuid.uuid4,verbose_name='Số Phiếu')
    datetimeXevao= models.DateField(verbose_name='Thời Gian Xe Vào')
    Status =models.BooleanField(default=False)
    datetimeXera = models.DateField(blank=True, null=True,verbose_name='Thời Gian Xe Ra')
    BienSoXe = models.ForeignKey(Xe,on_delete= models.SET_NULL,verbose_name='Biển Số Xe',null=True)
    NhanVienPT = models.ForeignKey(NhanVien,on_delete=  models.SET_NULL,verbose_name='Nhân Viên Phụ Trách',null=True)
    LyDoXeVao  = models.TextField(max_length=500,verbose_name='Tình Trạng Xe Vào')
    Lydo = models.TextField(max_length=500,verbose_name='Nội Dung Công Việc')
    class Meta:
           
       verbose_name_plural = 'Thông Tin Xe Vào'
    def __str__(self):
       return str(self.sophieu)
   
        

class VatTuDung(models.Model):
    XeVao= models.ForeignKey(XeVao, on_delete= models.SET_NULL,null=True)
    VtSudung = models.ForeignKey(material, on_delete= models.SET_NULL,verbose_name='Vật Tư',null=True)  
    dongia= models.FloatField(verbose_name='Đơn Giá')
    SoLuong = models.PositiveIntegerField(verbose_name='Số Lượng')
    thanhtien = models.FloatField(verbose_name='Thành Tiền')
    TrangThaiKho = models.CharField(choices=trangthaikho , max_length=50,verbose_name='Trạng Thái Kho')    
    TrangThaiXuat = models.CharField(choices=trangthaixuat, max_length=50,verbose_name='Trạng Thái Xuất')   
    DatetimeXuat = models.DateField(blank=True, null=True,verbose_name='Thời Gian Xuất' )
    class Meta:
           
        verbose_name_plural= 'Vật Tư Dùng Bảo Dưỡng Xe'
 
