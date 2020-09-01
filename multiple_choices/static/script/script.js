$(document).ready(function(){
    let dur = $('#duration').text();
    let duration = parseInt(dur);
    let hour = Math.floor(duration / 60);
    let minute = duration;
    let secs = Math.floor(duration * 60);
    let millsecs = Math.floor(duration * 60 * 1000);
    let now = new Date().getTime();
    let countDownTime = new Date(millsecs).getTime() + now;
    let ret = setInterval(function(){
        let current_time = new Date().getTime();
        let time_diff = countDownTime - current_time;
        let hours_diff = Math.floor((time_diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes_diff = Math.floor((time_diff % (1000 * 60 * 60)) / (1000 * 60));
        let seconds_diff = Math.floor((time_diff % (1000 * 60)) / 1000);
        $('#timer').html(hours_diff + ' h : ' + minutes_diff + ' m : ' + seconds_diff +' s' );
        if (time_diff < 0){
            clearInterval(ret);
            $('#timer').html('Time out!').attr({'color':'red'});
            $('#submit-btn').css('color', 'rgb(11, 23, 67)').attr('disabled', true);
            $('button:radio').css('color', 'red').attr('disabled', true);
            $('body').css({'background': 'rgba(11, 23, 67, 0.6)'});
        }
    }, secs);
});