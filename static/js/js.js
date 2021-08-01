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
