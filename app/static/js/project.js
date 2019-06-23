$(function(){

    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })



    $(".dataAddBtn").click(function(){
        var action = $(this).data('url') || '';
        if(action){
            layer.open({
              title: null,
              type: 2,
              area: ['100%', '100%'], //宽高
              content: action
            });
        }
    })
})