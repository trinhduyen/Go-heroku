from datetime import date
import datetime
import io
from urllib import request, response
from django.shortcuts import render
from .forms import *
from django.views.generic  import TemplateView
from django.views.generic.list import ListView
from .models import *
from django.db.models import Avg, Max, Min, Sum
# Create your views here.
from io import BytesIO, StringIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# print pdf file
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result= BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
  #  pdf = pisa.pisaDocument(BytesIO(html.encoding('utf8')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
     
    return None

class ViewPDF(View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        data = VatTuDung.objects.filter(XeVao_id = pk)
        vt = material.objects.all()
        dt = XeVao.objects.filter(id =pk)
        date = datetime.datetime.now()
        sum= VatTuDung.objects.filter(XeVao_id = pk).aggregate(total=Sum('thanhtien'))['total']
        data ={'data':data, 'date':date,'dt':dt, 'sum':sum, 'vt':vt}
        pdf = render_to_pdf('PDF/VT.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
  
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        data = VatTuDung.objects.filter(XeVao_id = pk)
        vt = material.objects.all()
        dt = XeVao.objects.filter(id =pk)
        date = datetime.datetime.now()
        sum= VatTuDung.objects.filter(XeVao_id = pk).aggregate(total=Sum('thanhtien'))['total']
        data ={'data':data, 'date':date,'dt':dt, 'sum':sum, 'vt':vt}
        pdf = render_to_pdf('PDF/VT.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "vt%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response

# end pdf

def index(request):
    return render(request, 'base.html')

# list data
class listDV(ListView):
    model= dv
    template_name= 'DV/index.html'
    context_object_name ='dv'
    paginate_by = 4

class listTB(ListView):
    model = thietbi
    template_name ='ThietBi/index.html'
    context_object_name ='TB'
    paginate_by = 4
    def get_queryset(self, **args) :
        queryset= super().get_queryset()
        qry = 'select a."NameTB",a."id" ,b."NameGroupTB" from "DX_thietbi" a , "DX_groupthietbi" b where a."id" = b."id"  '
        queryset = thietbi.objects.raw(qry)
        return queryset
    
class listNTB(ListView):
    model= groupthietbi
    template_name= 'NhomTB/index.html'
    context_object_name ='NTB'
    paginate_by = 4


class listNVT(ListView):
    model = groupmaterial
    template_name = 'NVT/index.html'
    context_object_name ='NVT'
    paginate_by =10
  
class listNhanVien(ListView):
    model = NhanVien
    template_name = 'NhanVien/index.html'
    context_object_name ='NV'
    paginate_by =10    
      
class listXe(ListView):
    model = Xe
    template_name = 'Xe/index.html'
    context_object_name ='Xe'
    paginate_by =10   

class listVT(ListView):
    template_name = 'VatTu/index.html'
    context_object_name ='VT'
    model = material
    paginate_by = 10
    def  get_queryset(self,**args):
        queryset=super().get_queryset()
        qry =' select a."id" ,a."IdVT",a."NameVT",b."NameNVT",c."NameDv" from "DX_material" a ,"DX_groupmaterial" b ,"DX_dv" c where a."IdNVTF_id" = b."id" and a."IdDV_id"= c."id"  '
        queryset= material.objects.raw(qry)
        return queryset

class  XeRaList(ListView):
    model= XeVao
    template_name ='chitietxe/index.html'
    context_object_name= 'XV'
    paginate_by =4
    def get_queryset(self,**args):
        queryset= super().get_queryset()
        qry ='select * from "DX_xevao" where "datetimeXera" is not null'
        queryset= XeVao.objects.raw(qry)
        return queryset
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)    
        context['vao']= 'ok'
        return context

class  XeCRaList(ListView):
    model= XeVao
    template_name ='chitietxe/index.html'
    context_object_name= 'XV'
    paginate_by =10
    def get_queryset(self,**args):
        queryset= super().get_queryset()
        qry ='select * from "DX_xevao" where "datetimeXera" is  null'
        queryset= XeVao.objects.raw(qry)
        return queryset
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)    
        context['test']= 'ok'
        return context


   
class showXeRa(ListView):
    model=VatTuDung
    template_name = 'chitietxe/ShowXeRa.html'
    context_object_name = 'XR'
    paginate_by = 10
    def get_queryset(self,**kwargs):
        queryset= super().get_queryset()
        pk= self.kwargs['pk']
        qry= 'select a.*,d.*,e.*,c."NameVT",c."IdDV_id",f."NameDv", b.* from "DX_vattudung" a ,"DX_dv" f, "DX_xevao" b ,"DX_material" c ,"DX_xe" d,"DX_nhanvien" e where c."IdDV_id"=f."id" and d."id"= b."BienSoXe_id" and e."id" = b."NhanVienPT_id" and a."VtSudung_id"=c."id" and  a."XeVao_id" = b."id" and a."XeVao_id"= %d '%pk
        queryset = VatTuDung.objects.raw(qry)
        return queryset
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)   
        pk= self.kwargs['pk']
        vt = VatTuDung.objects.filter(XeVao_id = pk)
        context['count'] = vt.count()
        context['xe']= XeVao.objects.filter(id=pk)
        context['date'] = datetime.datetime.now()
        context['sum'] = self.model.objects.filter(XeVao_id = pk).aggregate(total=Sum('thanhtien'))['total']
        return context
    
# end list

# bao cao    
class XeOnDay(ListView):
    model= XeVao
    template_name ='chitietxe/index.html'
    context_object_name= 'XV'
    paginate_by =10
    def get_queryset(self,**args):
        queryset= super().get_queryset()
        qry ='select * from "DX_xevao" where to_char("datetimeXevao",'"'yyyy-mm-dd'"') = to_char(now(),'"'yyyy-mm-dd'"')'
        queryset= XeVao.objects.raw(qry)
        return queryset  
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)    
        context['onday']= 'ok'
        return context
    
class BCindex(ListView):
    template_name = 'BC/index.html'
    context_object_name ='bc'
    model= VatTuDung
    def get_queryset(self,**kwargs):
        queryet= super().get_queryset()
        qry = 'select "id", "BienSoXe",sum(tt) as tt from (select a."BienSoXe_id" as id , b.*, c."BienSoXe" from "DX_xevao"  a, (select sum("thanhtien") as tt, "XeVao_id" from "DX_vattudung"group by "XeVao_id") b, "DX_xe" c where a."id"= b."XeVao_id" and a."datetimeXera" is not null and c."id"=a."BienSoXe_id") a group by "BienSoXe","id" '
        qry2 = 'select a."id", b.*, c."NameVT" from "DX_xevao" a, "DX_vattudung" b, "DX_material" c where to_char("datetimeXevao",'"'yyyy-mm-dd'"') = to_char(now(),'"'yyyy-mm-dd'"') and a."id" = b."XeVao_id" and c."id" = b."VtSudung_id"'
        qry1 ='select a.*,b."BienSoXe", c."TenNV" from "DX_xevao" a, "DX_xe" b, "DX_nhanvien" c where a."BienSoXe_id" = b."id" and  c."id" = a."NhanVienPT_id" and to_char("datetimeXevao",'"'yyyy-mm-dd'"') = to_char(now(),'"'yyyy-mm-dd'"')'
        queryet = {
           'one': self.model.objects.raw(qry),
           'two' : self.model.objects.raw(qry1),
           'three' : self.model.objects.raw(qry2),
        }
        return queryet       
    

class BC (ListView):
    template_name = 'BC/VT.html'
    context_object_name ='bc'
    model= VatTuDung
    def post(self,request):
        start = request.POST['start_date']
        end = request.POST['end_date']
        qry ='select "id","BienSoXe_id","LyDoXeVao","Lydo" ,"NhanVienPT_id" ,"datetimeXera","datetimeXevao",   extract( day from(  "DX_xevao"."datetimeXera"- "DX_xevao"."datetimeXevao") ) as days from "DX_xevao" where to_char("datetimeXera",'"'yyyy-mm-dd'"' ) >= '" '"+start+"' "' and to_char("datetimeXera",'"'yyyy-mm-dd'"' ) <= '" '"+end+"' "' order by days DESC LIMIT 5'
        qry1 ='select sum(tt), count("XeVao_id"), "BienSoXe" as id from "DX_xe" a, "DX_xevao" b ,(select a."XeVao_id",sum (a."thanhtien") as tt from "DX_vattudung" a group by a."XeVao_id" ) d where  to_char(b."datetimeXevao",'"'yyyy-mm-dd'"' ) >= '" '"+start+"' "' and to_char(b."datetimeXevao",'"'yyyy-mm-dd'"' ) <= '" '"+end+"' "' and a."id" = b."BienSoXe_id" and b."id"= d."XeVao_id"  group by "BienSoXe"'
        qry2= 'select a.*, b."BienSoXe",  extract( day from(  now()- a."datetimeXevao") ) as days from "DX_xevao" a, "DX_xe" b where a."BienSoXe_id" = b."id" and  a."datetimeXera" is null and  to_char(a."datetimeXevao",'"'yyyy-mm-dd'"' ) >= '" '"+start+"' "' and to_char(a."datetimeXevao",'"'yyyy-mm-dd'"' ) <= '" '"+end+"' "' order by days DESC '
       # qry2 = 'select "BienSoXe" as id, sum(tt) as sum from (select a."id", c."BienSoXe", sum(b."thanhtien") as tt  from "DX_xevao" a, "DX_vattudung" b,"DX_xe" c where c."id"= a."BienSoXe_id" and a."id" = b."XeVao_id" group by c."BienSoXe",a."id") as a group by "BienSoXe"'
        data = VatTuDung.objects.raw(qry)
        data1 = VatTuDung.objects.raw(qry1)
        data2 = VatTuDung.objects.raw(qry2)
        #print(qry)
        return render(request,'BC/VT.html', {'data':data,'data1':data1,'data2': data2,'start': start,'end': end})
    
        
    def get_queryset(self,**kwargs):
        queryset= super().get_queryset()
        qry= 'select a."NameVT",a."id", sum(b."thanhtien") as tt from "DX_material" a, "DX_vattudung" b group by a."NameVT",a."id"'
        qry1 = 'select "BienSoXe" as id, sum(tt) as sum from (select a."id", c."BienSoXe", sum(b."thanhtien") as tt  from "DX_xevao" a, "DX_vattudung" b,"DX_xe" c where c."id"= a."BienSoXe_id" and a."id" = b."XeVao_id" group by c."BienSoXe",a."id") as a group by "BienSoXe"'
        queryset = {
          'one' :  VatTuDung.objects.raw(qry),
          'two' :VatTuDung.objects.raw(qry1)
        }
        return queryset

class base(ListView):
    template_name = 'base_smallbox.html'
    model = VatTuDung
    context_object_name ='sm_box'
    def get_queryset(self,**kwargs):
        queryset = super().get_queryset()
        qry1 = 'select  count(*) as id from "DX_xevao"  where to_char("datetimeXevao",'"'yyyy-mm-dd'"') = to_char(now(),'"'yyyy-mm-dd'"')'
        qry ='select sum(a."thanhtien") as tt, b."idnhomxe" as id  from "DX_vattudung" a, (select a."id" as idnhomxe, b."id" as IDXe, c."id"  as idxevao from "DX_nhomxe" a, "DX_xe" b , "DX_xevao" c where a."id" = b."IDNhomXe_id" and b."id"= c."BienSoXe_id") as b where b."idxevao" = a. "XeVao_id"group by  b."idnhomxe"'
        qry2 ='select sum(a."thanhtien") as id, b."idnhomxe",b."Tennhomxe"  from "DX_vattudung" a, (select a."id" as idnhomxe, a."Tennhomxe", b."id" as IDXe, c."id"  as idxevao from "DX_nhomxe" a,"DX_xe" b , "DX_xevao" c where a."id" = b."IDNhomXe_id" and b."id"= c."BienSoXe_id") as b where b."idxevao" = a. "XeVao_id" group by  b."idnhomxe" ,b."Tennhomxe" '
        queryset ={'one': VatTuDung.objects.raw(qry),
                   'two': VatTuDung.objects.raw(qry1),
                   'three':VatTuDung.objects.raw(qry2),
                    }
        return queryset
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        qry2 ='select sum(a."thanhtien") as id, b."idnhomxe",b."Tennhomxe"  from "DX_vattudung" a, (select a."id" as idnhomxe, a."Tennhomxe", b."id" as IDXe, c."id"  as idxevao from "DX_nhomxe" a,"DX_xe" b , "DX_xevao" c where a."id" = b."IDNhomXe_id" and b."id"= c."BienSoXe_id") as b where b."idxevao" = a. "XeVao_id" group by  b."idnhomxe" ,b."Tennhomxe" '
        context['vtdata']=  VatTuDung.objects.raw(qry2)
        return context
    
    def post(self,request):
        month= request.POST.get('month')
        qry ='select sum(a."thanhtien") as id, b."idnhomxe",b."Tennhomxe" ,extract( MONTH  from (a."DatetimeXuat")) as month from "DX_vattudung" a, (select a."id" as idnhomxe, a."Tennhomxe", b."id" as IDXe, c."id"  as idxevao from "DX_nhomxe" a,"DX_xe" b , "DX_xevao" c where a."id" = b."IDNhomXe_id" and b."id"= c."BienSoXe_id") as b where extract( MONTH  from (a."DatetimeXuat")) = '"'"+month+"'"' and b."idxevao" = a. "XeVao_id" group by  b."idnhomxe", month ,b."Tennhomxe" '
        vtdata = VatTuDung.objects.raw(qry)
       
        return render(request,'BC/xe/index1.html',{'vtdata':vtdata})
    
class BaoCaoXe(ListView):
    template_name ='BC/xe/index.html'
    model = VatTuDung
    context_object_name = 'bcxe'
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nhomxe"] = nhomxe.objects.all()
        qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"'
        context["vattu"] = VatTuDung.objects.raw(qr)
        context['loaipt']= nhomxe.objects.all()
        context['tenpt']= Xe.objects.all()
        
        return context
    def get_queryset(self):
        queryset= super().get_queryset()
        qry ='select sum(a."thanhtien") as id, b."idnhomxe", extract( MONTH  from (a."DatetimeXuat")) as month from "DX_vattudung" a, (select a."id" as idnhomxe, a."Tennhomxe", b."id" as IDXe, c."id"  as idxevao from "DX_nhomxe" a,"DX_xe" b , "DX_xevao" c where a."id" = b."IDNhomXe_id" and b."id"= c."BienSoXe_id") as b where b."idxevao" = a. "XeVao_id" group by  b."idnhomxe", month  '
        queryset = VatTuDung.objects.raw(qry)
        return queryset   
    
class LSvattu(ListView):
    paginate_by =10
    template_name ='BC/xe/lichsuvt.html'
    context_object_name ='vattu'
    model=VatTuDung
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nhomxe"] = nhomxe.objects.all()
      
        context['loaipt']= nhomxe.objects.all()
        context['tenpt']= Xe.objects.all()
        return context
    def get_queryset(self):
        queryset= super().get_queryset()
        qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"'
        queryset= VatTuDung.objects.raw(qr)
        return queryset
    
class Chiphixe(ListView):
    template_name ='BC/xe/index3.html'
    model=VatTuDung
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nhomxe"] = nhomxe.objects.all()
        qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"'
        qr1 ='select sum(a."thanhtien"),a."XeVao_id", b."BienSoXe_id", c."BienSoXe", c."TenXe"  , d."id" from "DX_vattudung" a, "DX_xevao" b, "DX_xe" c , "DX_nhomxe" d where a."XeVao_id" = b."id" and c."id" = b."BienSoXe_id" and d."id"= c."IDNhomXe_id" and extract(month from (a."DatetimeXuat"))=extract(month from (now()))group by a."XeVao_id", b."BienSoXe_id" ,c."BienSoXe", c."TenXe",d."id"'
        qr2 ='select sum(a."thanhtien"), d."id", d."Tennhomxe" from "DX_vattudung" a, "DX_xevao" b, "DX_xe" c , "DX_nhomxe" d where a."XeVao_id" = b."id" and c."id" = b."BienSoXe_id" and d."id"= c."IDNhomXe_id" and extract(month from (a."DatetimeXuat"))=extract(month from (now()))group by d."id", d."Tennhomxe"'
        context["vattu"] = VatTuDung.objects.raw(qr)
        context["cp"] = VatTuDung.objects.raw(qr1)
        context["cpt"] = VatTuDung.objects.raw(qr2)
        context['loaipt']= nhomxe.objects.all()
        context['tenpt']= Xe.objects.all()
        return context

def search_vt_m(request):
    if request.method=='POST':
        month= request.POST.get('month')
        nhomxevt= request.POST.get('nhomxevt')
        if nhomxevt =='all':
            qr1 ='select sum(a."thanhtien"),a."XeVao_id", b."BienSoXe_id", c."BienSoXe", c."TenXe"  , d."id" from "DX_vattudung" a, "DX_xevao" b, "DX_xe" c , "DX_nhomxe" d where a."XeVao_id" = b."id" and c."id" = b."BienSoXe_id" and d."id"= c."IDNhomXe_id" and extract(month from (a."DatetimeXuat"))='"'" +month+"'"'  group by a."XeVao_id", b."BienSoXe_id" ,c."BienSoXe", c."TenXe",d."id"'
            qr2 ='select sum(a."thanhtien"), d."id", d."Tennhomxe" from "DX_vattudung" a, "DX_xevao" b, "DX_xe" c , "DX_nhomxe" d where a."XeVao_id" = b."id" and c."id" = b."BienSoXe_id" and d."id"= c."IDNhomXe_id" and extract(month from (a."DatetimeXuat"))='"'" +month+"'"'  group by d."id", d."Tennhomxe"'
        else:    
            qr1 ='select sum(a."thanhtien"),a."XeVao_id", b."BienSoXe_id", c."BienSoXe", c."TenXe"  , d."id" from "DX_vattudung" a, "DX_xevao" b, "DX_xe" c , "DX_nhomxe" d where a."XeVao_id" = b."id" and c."id" = b."BienSoXe_id" and d."id"= c."IDNhomXe_id" and extract(month from (a."DatetimeXuat"))='"'" +month+"'"' and d."id"='+nhomxevt+' group by a."XeVao_id", b."BienSoXe_id" ,c."BienSoXe", c."TenXe",d."id"'
            qr2 ='select sum(a."thanhtien"), d."id", d."Tennhomxe" from "DX_vattudung" a, "DX_xevao" b, "DX_xe" c , "DX_nhomxe" d where a."XeVao_id" = b."id" and c."id" = b."BienSoXe_id" and d."id"= c."IDNhomXe_id" and extract(month from (a."DatetimeXuat"))='"'" +month+"'"' and d."id"='+nhomxevt+' group by d."id", d."Tennhomxe"'
        cp = VatTuDung.objects.raw(qr1)
        cpt=  VatTuDung.objects.raw(qr2)
        loaipt =nhomxe.objects.all()
        
    return render(request,'include/bcxe/cpxe_month.html',{'cp':cp, 'cpt':cpt, 'loaipt':loaipt})    
             

    
def search_body(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    loaipt = request.POST.get('loaipt')
    tenpt = request.POST.get('tenpt')
    BienSoXe = request.POST.get('BienSoXe')
    
         
    if BienSoXe=='':    
        if start_date =='' and end_date =='':
            if loaipt =='all':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"' 
            if loaipt =='all' and tenpt!='':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and  e."id" = '+(tenpt)+' and f."id" = b."IdDV_id"' 
            if loaipt =='all' and tenpt=='all' :
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"' 
            else:
                
                if loaipt !='all' and tenpt=='all':  
                    qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."IDNhomXe_id" = %d' % int(loaipt)
                if  loaipt !='all' and tenpt!='all':
                    qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and e."id" = '+(tenpt)+' and f."id" = b."IdDV_id"   and e."IDNhomXe_id" = %d' % int(loaipt)
          
        else:
            if loaipt =='all':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"' 
            if loaipt =='all' and tenpt!='':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and  e."id" = '+(tenpt)+' and f."id" = b."IdDV_id" and  to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "'' 
            if loaipt =='all' and tenpt=='all' :
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and  to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "'' 
            else:
                
                if loaipt !='all' and tenpt=='all':  
                    qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and  to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and e."IDNhomXe_id" = %d' % int(loaipt)
                if  loaipt !='all' and tenpt!='all':
                    qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and e."id" = '+(tenpt)+' and f."id" = b."IdDV_id"  and  to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "'  and e."IDNhomXe_id" = %d' % int(loaipt)
    else:    
        if start_date !='' and end_date !='':
            qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."BienSoXe"  = '" '"+BienSoXe+"' "''
        else:
            qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where   a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."BienSoXe"  = '" '"+BienSoXe+"' "''
      
    vattut = VatTuDung.objects.raw(qr)     
    paginator = Paginator(vattut, 1)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    return render(request,'include/search_body.html',{'vattut':vattut, 'page_obj': page_obj})

#htmlx
class search(ListView):
    template_name ='include/search_body.html'
    model= 'VatTuDung'
    paginate_by =1
    def post(request,self):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        loaipt = request.POST.get('loaipt')
        tenpt = request.POST.get('tenpt')
        BienSoXe = request.POST.get('BienSoXe')
        if start_date =='' and end_date =='':
            if loaipt =='all'  and BienSoXe=='' :
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id"' 
            else:
                if loaipt !='all' and tenpt=='all'  and  BienSoXe=='' :
                    qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."IDNhomXe_id" = %d' % int(loaipt)
                if  loaipt !='all' and tenpt!='all' and  BienSoXe=='' : 
                    qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and e."id" = '+(tenpt)+' and f."id" = b."IdDV_id"   and e."IDNhomXe_id" = %d' % int(loaipt)
            if BienSoXe!='':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."BienSoXe"  = '" '"+BienSoXe+"' "''
        else:
            if start_date !='' and end_date !='' and BienSoXe!='':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."BienSoXe"  = '" '"+BienSoXe+"' "''
            if start_date !='' and end_date !='' and loaipt =='all':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" '
            if start_date !='' and end_date !='' and loaipt !='all' and tenpt=='all':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and e."IDNhomXe_id" = %d' % int(loaipt) 
            if start_date !='' and end_date !='' and loaipt !='all' and tenpt!='all':
                qr ='select a."SoLuong",a."dongia", a."thanhtien", a."DatetimeXuat",b.*, c."NameNVT", e."BienSoXe" , f."NameDv"from "DX_vattudung" a , "DX_material" b, "DX_groupmaterial" c,"DX_xevao" d, "DX_xe" e ,"DX_dv" f where to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') >= '" '" + start_date + "' "' and to_char(a."DatetimeXuat",'"'yyyy-mm-dd'"') <= '" '" + end_date + "' "' and a."VtSudung_id" = b."id" and c."id" = b. "IdNVTF_id" and d."id" = a."XeVao_id" and e."id" = d."BienSoXe_id" and f."id" = b."IdDV_id" and  e."id" = '+(tenpt)+' and e."IDNhomXe_id" = %d' % int(loaipt) 

        vattu = VatTuDung.objects.raw(qr)        
        return render(request,'include/search_body.html',{'vattu':vattu})

#search nhan vien htmlx






def test(request):
    a = request.POST.get('loaipt')
    if a =='all':
        data = Xe.objects.all()
    else:     
        data = Xe.objects.filter(IDNhomXe=a)
 
    return render (request,'search.html',{'data': data})


#end htmlx
class BCchiphi(ListView):
    template_name = 'BC/xe.html'
    model = VatTuDung
    context_object_name ='cpbcxe'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nhomxe"] = nhomxe.objects.all()
        return context
    def get_queryset(self):
        queryset= super().get_queryset()
        pk= self.kwargs['pk'] 
        qry ='select sum(a."thanhtien") as tt, b."idnhomxe" , extract( MONTH  from (a."DatetimeXuat")) as month  from "DX_vattudung" a, (select a."id" as idnhomxe, b."id" as IDXe, c."id"  as idxevao from "DX_nhomxe" a, "DX_xe" b , "DX_xevao" c where a."id" = b."IDNhomXe_id" and b."id"= c."BienSoXe_id") as b where b."idxevao" = a. "XeVao_id"group by  b."idnhomxe", month and idnhomxe =%d '%pk
        queryset = VatTuDung.objects.raw(qry)
        return queryset 

# bc nhan vien


class listnhanvien(ListView):
    model = XeVao
    template_name = 'BC/nhanvien/search.html'
    context_object_name ='ac'
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        qry ='select count(a.*) as id, b."TenNV" ,b."MaNV" from "DX_xevao" a, "DX_nhanvien" b where a."datetimeXera" is not null and b."id" = a."NhanVienPT_id" group by  b."TenNV" ,b."MaNV"'
        queryset = self.model.objects.raw(qry)
        return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['range'] = range(1,11)
        return context


def search_nhanvien( request):
    if request.method =='POST':
        pk = request.POST.get('thang')
        qr = 'select count(a.*) as id, b."TenNV" ,b."MaNV" from "DX_xevao" a, "DX_nhanvien" b where a."datetimeXera" is not null and b."id" = a."NhanVienPT_id" and extract( MONTH from( a."datetimeXera")) = '"'"+pk+"'"' group by  b."TenNV" ,b."MaNV"'
        ac = XeVao.objects.raw(qr)
    return render (request,'BC/nhanvien/month.html' , {'ac':ac, 'pk': pk})    


def search_vt_nhanvien(request,pk):
    qr = 'select sum("thanhtien"), "BienSoXe","id", "TenXe" from ( select a."thanhtien" , d."BienSoXe", d."TenXe", c."id", c."MaNV", c."TenNV", b."datetimeXevao", b."datetimeXera" from "DX_vattudung" a, "DX_xevao" b, "DX_nhanvien" c, "DX_xe" d where extract(month from (b."datetimeXera")) = '"'"+pk+"'"' and a."XeVao_id" = b."id"  and c."id"= b."NhanVienPT_id" and b."datetimeXera" is not null and b."BienSoXe_id" = d."id") as b group by  "BienSoXe","TenXe","id"'
    data = VatTuDung.objects.raw(qr)
    return render (request,'BC/nhanvien/chiphiVT.html',{'data':data})

def search_xevt(request):
    nhomxe = request.GET.get('nhomxevt')
    if nhomxe =='all':
        tenpt = Xe.objects.all()
    else:    
        tenpt = Xe.objects.filter(IDNhomXe_id=nhomxe)
    return render(request,'include/bcxe/search_xe.html',{'tenpt':tenpt})                    
