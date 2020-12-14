$(document).ready(function(){
    let attemptedQuestions = []
    let counter = 1;
    let choices;
    // get Questions from backend
    let questions =  getQuestions();
    let randomQuestion = getRandomQuestion(questions, attemptedQuestions);
    let oldRandomQuestion = randomQuestion;
    if(counter < questions.length){
        choices = getChoices(randomQuestion);
        addQuestionAndChoices(choices, randomQuestion);
        showAssessmentDetails(questions, counter);
    }
    $('#assessment-window form').submit(()=>{
        if(counter <=  questions.length){//if there is still more questions unattempted
            let $choiceButton = $('form input[name=choice]:checked');
            let selectedChoiceValue = $choiceButton.val();
            oldRandomQuestion.choice = selectedChoiceValue;
            // the question to the list of the attempted questions
            attemptedQuestions = addAttemptedQuestion(oldRandomQuestion, attemptedQuestions);
           // addQuestionAndChoices(choices, randomQuestion);
            if(counter === questions.length){
                var scores = getScores(attemptedQuestions);
                showAssessmentResult(scores, attemptedQuestions);
            }
            else{
                counter++;
                randomQuestion = getRandomQuestion(questions, attemptedQuestions);
                choices = getChoices(randomQuestion);
                // add the DOM element for both question and choices
                addQuestionAndChoices(choices, randomQuestion);
                oldRandomQuestion = randomQuestion;
                showAssessmentDetails(questions, counter);
            }
        }
        return false;
    });

});

function addQuestionAndChoices(questionChoices, randomQuestion){
    let assessmentWindowForm = $('#assessment-window form');
    let questionElement = $(`
        <p class='orange-font'><strong>${randomQuestion.question_asked}</strong></p>
        <p><strong><i class='orange-font'>Select an answer below:</i></strong></p>
    `);
    assessmentWindowForm.html(questionElement);
    let questionListContainer = $('<div></div>').css({'padding':'20px'});
    questionChoices.forEach((choice, index)=>{
        questionListContainer.append(`
               ${index+1}.<label for='${choice.id}'>
                    <input
                        type='radio'
                        name='choice'
                        value='${choice.is_correct}'
                        id='${choice.id}'
                        required
                    />
                     ${choice.choice_statement}
                </label>
                <br>
                <br>
            `);
        });
        let nextButton = $(`
            <button id='next' type='submit'>
                Next Question <i class='orange-font fa fa-arrow-right'></i>
            </button>
        `)
        .css({'marginBottom':'0px'});
        assessmentWindowForm.append(questionListContainer).append(nextButton);
}

function getChoices(question){
    // Get choices for a question from the backend and returns them
    var associatedChoices;
    $.ajax(
        {
            url: '/assessment/get-associated-choices/',
            data: {'question_id':question.id},
            dataType: 'json',
            async: false,
            success: function(data){
                associatedChoices = data.choices;
            },
            error: function(){
                alert(`Error while fetching choices for: ${question.title}`);
            }
        }
    );
    return associatedChoices;
}

function getQuestions(){
    // Fetches Question objects from backend and returns it.
    let assessment_id = $('section#window').children('p:first').attr('id');
    var returnedQuestions;
    $.ajax({
        url: `/assessment/assessment-window/`,
        dataType: 'json',
        data: {'assessment_id':assessment_id},
        async:false,
        success: function(data){
            returnedQuestions = data.questions;
        },
        error: function(err){
            alert("Error while gettting questions!");
        }
    });
    return returnedQuestions;
}


function getRandomQuestion(questions, attemptedQuestions){
    // Returns a random question from the question Array
    let index = Math.floor((Math.random())*(questions.length))
    let question = questions[index]
    // check if question is already attempted
    while($.inArray(question, attemptedQuestions) !== -1){
        question = getRandomQuestion(questions, attemptedQuestions);
    }
    return question;
}


function showAssessmentDetails(questions, counter){
    $('article#assessment-dashboard').html(`
        <span class='white-font'>
            Question ${counter} of ${questions.length}
        </span>
    `);
}


function getScores(questions){
    /*
        Get score from each question and sum them up to get
        the total score based on the selected choices.
    */

    var totalScore = 0;
    $.each(questions, function(index, question){
        if(question.hasOwnProperty('choice')){
            if(question.choice === 'true'){
                totalScore += question.score;
            }
            else{
                totalScore += 0;
            }
        }
    });
    return totalScore;
}

function showAssessmentResult(scores, questions){
    /*
        Displays the scores obtained along side congratulatory message.
    */
   var  homeUrl = '{% url `cbt:home` %}';
    $('body').html(`
        <article class='cbt-form'>
            <h2 class='white-font'>
                You are done answering ${questions.length} questions.
            </h2>
            <h1 class='orange-font'>Congratulations!</h1>
            <p class='white-font'>You scored: ${scores}</p>
            <i class='white-font fas fa-smile'></i>
            <button>Submit Assessment</button>
            <a href='/'><button>Home</button></a>
        </article>
    `).css(
        {
            'position': 'relative',
            'top':'0px',
            'left':'0px',
            'z':'3',
            'backgroundColor':'rgba(0, 0, 0,1)',
            'display':'flex',
            'flexDirection':'column',
            'justifyContent':'space-between',
            'alignItems':'center',
        }
    );
}


function addAttemptedQuestion(attemptedQuestion, attemptedQuestions){
    // append attempted question to the list of attempted questions
    if($.inArray(attemptedQuestion, attemptedQuestions ) === -1){
        attemptedQuestions.push(attemptedQuestion);
    }
    return attemptedQuestions;
}