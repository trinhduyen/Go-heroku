function addZero(i) {
    if (i < 10) {i = "0" + i}
    return i;
  }
 

function loadXR(checkboxElem) {
    if (checkboxElem.checked) {
        currentDate = new Date();
        let current = new Date();
        let cDate = current.getFullYear() + '-' + addZero(current.getMonth() + 1) + '-' + addZero( current.getDate());
        let cTime =addZero( current.getHours()) + ":" +addZero( current.getMinutes());
        let dateTime = cDate + 'T' + cTime;
        $('#dateXR').val(dateTime)
        $('#id_datetimeXera').val(dateTime)
    } else {
        $('#dateXR').val('')
    }
}

function mychangeX() {
   
    var x = $('.ttXuat').val()

    if (x === 'Đã Xuất') {
      
        currentDate = new Date();
        let current = new Date();
        let cDate = current.getFullYear() + '-' + (current.getMonth() + 1) + '-' + current.getDate();
        let cTime = current.getHours() + ":" + current.getMinutes() + ":" + current.getSeconds();
        let dateTime = cDate + ' ' + cTime;
       
        $('.dateXVT').val(dateTime)

    } else {
        $('.dateXVT').val('')
    }
}



function mychangeY() {
    
   
    var x = $('.ttxuatvtedit').val()
    if (x===undefined){
        x =$('.ttxuatvtedit01').val()
    }
    if (x === 'Đã Xuất') {
        currentDate = new Date();
        let current = new Date();
        let cDate = current.getFullYear() + '-' + addZero(current.getMonth() + 1) + '-' + addZero(current.getDate());
        let cTime = addZero (current.getHours()) + ":" +addZero (current.getMinutes() )
        let dateTime = cDate + 'T' + cTime;
      
        $('.timexuatvtedit').val(dateTime)
        $('.timexuatvtedit01').val(dateTime)

    } else {
        $('.timexuatvtedit').val('')
        $('.timexuatvtedit01').val(dateTime)
    }
}



$(".print").on("click", function(e){
    $('#nav-header').hide()
    window.print()
    $('#nav-header').show()
    
            
})


function mykeyupTT(){
    var sl = document.getElementById('id_SoLuong').value
    var dg = document.getElementById('id_dongia').value
    document.getElementById('id_thanhtien').value = sl*dg
    document.getElementById('id_tt').value= sl*dg
}
function mykey(){
    var sl = document.getElementById('id_SoLuongvt').value
    var dg = document.getElementById('id_dongiavt').value
    document.getElementById('id_thanhtienvt').value = sl*dg
    document.getElementById('id_ttvt').value=sl*dg
}
