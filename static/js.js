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

$(document).ready(function() {
    $('.navbtn').click(function(){
      var typeid = $(this).data('id');
      $.ajax({
        url: '/nav',
        type: 'post',
        data: {typeid: typeid},
        success: function(data){
          $('.container').append(data.htmlresponse);
    }

$(document).ready(function)(){
  $('#search').keydown(function()){
      var search = $(this).val();
  }
}
