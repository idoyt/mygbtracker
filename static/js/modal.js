// get data and open modal on thread preview click
$(document).ready(function(){
    $('.threadinfo').click(function(){
        var id = $(this).data('id');
        $.ajax({
            url: '/popup',
            type: 'post',
            data: {id: id},
            success: function(data){
                $('.modal-body').html(data);
                $('.modal-body').append(data.htmlresponse);
                $('#Modal').modal('show');
            }
        });
    });
});

//escape key close popup
$(document).keydown(function(event) {
  if (event.keyCode == 27) {
    $('#Modal').modal('hide');
  }
});
