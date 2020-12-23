$(document).ready(function(){
    $questionTypeDiv = $('div#passage-question-type').hover(function(){
        // make ajax request:
        var  passages;
        var questions;
        var choices;
        $.ajax({
            url: '/scrolling-image/sample-questions/',
            dataType: 'json',
            async:false,
            success: function(data){
                passages = data.passages;
                questions = data.questions;
                choices = data.choices;
                $questionTypeDiv.html(data.passages[0].body);
               // alert(data.passages[0].body)
            },
            error: function(){
                alert('error')
            }
        });
    });
});