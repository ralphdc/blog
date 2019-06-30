$(function(){

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


    $('.closeLayer').click(function(){
        var index=parent.layer.getFrameIndex(window.name);
        //刷新父页面
        window.parent.location.reload();
        parent.layer.close(index);
    })

})