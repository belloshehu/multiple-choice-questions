$(document).ready(function(){
    var scrollingObjects = {'images':null, 'text':'',};
    $.ajax({
        url: '/scrolling-image/list/',
        dataType: 'json',
        async: false,
        success: function(data){
            //alert('success');
            scrollingObjects.images = data.image_urls;
            scrollingObjects.text = data.scrolling_images
        },
        error: function(){
           // alert('error');
        }
    });
    var $scrollingPanel = $('article#scrolling-panel');
    setInterval(() => {
        var index  = Math.floor((Math.random())*(scrollingObjects.images.length));
        img = $(`<img src='${scrollingObjects.images[index]}' width='500' height='400'>`);
        text = $(`<h1>${scrollingObjects.text[index].name}</h1>`).css(
            {
                'position':'relative',
                'z-index':3,
                'top':'0px',
                'color':'gold',
                'fontSize':'xx-large',
                'backgroundColor':'rgba(0, 0, 0, 0.6)',
                'fontWeight':'bolder',
                'textAlign':'center',
                'width':'wrap-content',
                'padding':'0px'
            }
        )
        $scrollingPanel.html(img).append(text).delay(100).animate(
            {
                left: ['+=10', 'swing'],
            },
        300);
    }, 2000);
});