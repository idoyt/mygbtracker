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
  load_data();
  function load_data(query)
  {
   $.ajax({
    url:"/search",
    method:"POST",
    data:{query:query},
    success:function(data)
    {
      $('#result').html(data);
      $("#result").append(data.htmlresponse);
    }
   });
  }
  $('#search_text').keyup(function(){
    var search = $(this).val();
    if(search != ''){
    load_data(search);
   }else{
    load_data();
   }
  });
});
