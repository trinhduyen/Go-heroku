jQuery(window).load(function (e) {
    
    function addZero(i) {
        if (i < 10) {i = "0" + i}
        return i;
      }
     
        $('#id_Status').on('change',function(){
            var _val = $(this).is(':checked') ? 'checked' : 'unchecked';
            if (_val=='checked'){
                currentDate = new Date();
                let current = new Date();
                let cDate = current.getFullYear() + '-' + addZero(current.getMonth() + 1) + '-' + addZero( current.getDate());
                let cTime =addZero( current.getHours()) + ":" +addZero( current.getMinutes())+ ":" +addZero( current.getSeconds());
                let dateTime = cDate  + cTime;
                $('#id_datetimeXera').val(dateTime)
               
            } else {
                $('#id_datetimeXera').val('')
            }
            
        });
    
        i=0
        $('#vattudung_set-group').on('click', function(){
            
            a=i+1
            return a
           
        }) 
         
    });
    
    
    function mykeyupTT01(){
            var str1 ='id_vattudung_set-'
            a=a+1
            for (let i=3 ; i<a; i++){
                var y = i +'-dongia'
                var x = str1+y
                alert(x)
            }
     }
     function formatDollar(num) {
        var p = num.toFixed(3).split(".");
        return  p[0].split("").reverse().reduce(function(acc, num, i, orig) {
            return num + (num != "-" && i && !(i % 3) ? "." : "") + acc;
        }, "") + "." + p[1];
    }

    function mykeyupTT(){
        var x = $('#id_dongia').val()
        var y = $('#id_SoLuong').val()
        $('#id_thanhtien').val(x*y)
    
        
        var x = $('#id_vattudung_set-0-dongia').val()
        var y = $('#id_vattudung_set-0-SoLuong').val()
        $('#id_vattudung_set-0-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-1-dongia').val()
        var y = $('#id_vattudung_set-1-SoLuong').val()
        $('#id_vattudung_set-1-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-2-dongia').val()
        var y = $('#id_vattudung_set-2-SoLuong').val()
        $('#id_vattudung_set-2-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-3-dongia').val()
        var y = $('#id_vattudung_set-3-SoLuong').val()
        $('#id_vattudung_set-3-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-4-dongia').val()
        var y = $('#id_vattudung_set-4-SoLuong').val()
        $('#id_vattudung_set-4-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-5-dongia').val()
        var y = $('#id_vattudung_set-5-SoLuong').val()
        $('#id_vattudung_set-5-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-6-dongia').val()
        var y = $('#id_vattudung_set-6-SoLuong').val()
        $('#id_vattudung_set-6-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-7-dongia').val()
        var y = $('#id_vattudung_set-7-SoLuong').val()
        $('#id_vattudung_set-7-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-8-dongia').val()
        var y = $('#id_vattudung_set-8-SoLuong').val()
        $('#id_vattudung_set-8-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-9-dongia').val()
        var y = $('#id_vattudung_set-9-SoLuong').val()
        $('#id_vattudung_set-9-thanhtien').val(x*y)
        var x = $('#id_vattudung_set-10-dongia').val()
        var y = $('#id_vattudung_set-10-SoLuong').val()
        $('#id_vattudung_set-10-thanhtien').val(x*y)
    }