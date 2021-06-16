$(document).ready(function(){
    $('.gbinfo').click(function(){
        var gbid = $(this).data('id');
        $.ajax({
            url: '/ajaxfile',
            type: 'post',
            data: {gbid: gbid},
            success: function(data){
                $('.modal-body').html(data);
                $('.modal-body').append(data.htmlresponse);
                $('#Modal').modal('show');
            }
        });
    });
});

$(document).ready(function(){
     $("#livebox").on("input",function(e){
         $("#datalist").empty();
         $.ajax({
             method:"post",
             url:"/livesearch",
             data:{text:$("#livebox").val()},
             success:function(res){
                 var data = "<ul>";
                 $.each(res,function(index,value){
                     data += "<li>"+value.word_eng+"</li>";
                 });
                 data += "</ul>";
                 $("#datalist").html(data);
             }
         });
     });
 });
