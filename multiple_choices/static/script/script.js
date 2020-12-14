$(document).ready(function(){
    let count = 0;
    let count2 = 0;
    toggleAccountNavBar(count2);
    togglePrimaryNavBar(count);
    removePassageForm();
    //addPassageForm()
    addFloatingForm();
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
            $('#timer').html('Time out!').css({'color':'red'});
            $('#submit-btn').html('You can not submit').attr('disabled', true);
            $('input:radio').css('color', 'red').attr('disabled', true);
            $('body').css({'background': 'rgba(11, 23, 67, 0.6)'});
        }
        else if(time_diff > 0 && time_diff < 300000){
            $('#timer').css({'color':'red'});
        }
    }, secs);

});

// function to allow toggling of account navigation items in mobile mode.
function toggleAccountNavBar(count){
    $('div.nav-button.account').click(()=>{
        $('.account-nav > ul.nav').toggle(200, ()=>{
            if(count % 2 === 1){
                $('.account-nav > ul.nav').css({'display':'flex', 'justify-content':'stretch',  'font-size':'small'});
            }
            count = count+1;
        });
    }
    );
}

// function to allow toggling of primary navigation items in mobile mobile.
function togglePrimaryNavBar(count){
    $('div.nav-button.primary').click(()=>{
        $('.primary-nav > ul.nav').toggle(200, ()=>{
            if(count % 2 === 1){
                $('.primary-nav > ul.nav').css({'display':'flex', 'align-items':'center','justify-content':'flex-start'});
            }
            count = count+1;
        });
    }
    );
}

function addPassageForm(){
    //$("#passage-form").after(deleteButton);
    $('button.passage.add').click(()=>{
        $('#passage-form').html(passageForm());
        $('button.passage').remove();
        //$('button.passage').removeClass("add").addClass("danger").text("Delete passage");
        $('#passage-form + p > span').text("");

    });
}
function passageForm(){
    let formTitle = $(`
        <h2>Passage:</h2>
        <p>Add a passage for your questions</p>
    `);
    let title = $(`
        <p>
            <strong><label>Passage title:</label></strong><br>
            <input type='text' placeholder='Passage title'></input>
        </p>
    `);
    let body = $(
        `<p>
            <strong><label>Passage body:</label></strong><br>
            <textarea cols='100' rows='20' placeholder='Passage text'></textarea>
        </p>
    `)
    let numberOfQuestionField = $(`
        <p>
            <strong><label>Number of questions</label></strong><br>
            <input type='number' placeholder='Question in the Passage'></input>
        </p>
    `);
    let submitButton = $(`<p><button type='submit' >Save passage</button></p>`);
    let deleteButton = $(`<p><button class='danger passage' >Delete passage</button></p>`);
    let passageForm = $("<form></form>").html(formTitle).append(title).append(body).append(numberOfQuestionField).append(submitButton);
    return passageForm;
}
function addFloatingForm(){
    $('button.passage.add').click(()=>{
        $('body').html(passageForm()).css({
            'position':'relative',
            'top':'5%','left':'10%',
            'z':'-2', 'width':'100%',
            'color':'black',
            'background-color':'grey',
         });
        $('button.passage').remove();
        //$('button.passage').removeClass("add").addClass("danger").text("Delete passage");
        $('#passage-form + p > span').text("");

    });
}
function removePassageForm(){
    $('button.passage.danger').click(()=>{
        $('#passage-form').empty();
        $('button.passage').removeClass("danger").addClass("add").text("Add passage");
    });
}
