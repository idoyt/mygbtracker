// get data and open modal on thread preview click
$(document).ready(function(){
    $('.gbinfo').click(function(){
        var gbid = $(this).data('id');
        $.ajax({
            url: '/popup',
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
