// Authored by Jack Hales

$(document).ready(function() {

    // User begins quiz so hide start button and text
    // Show quiz questions and time limit
    $("#start").click(function(event){
        $('#start').attr('hidden', true);
        $('#daily-quiz-subheading').attr('hidden', true);
        $('#daily_quiz').removeAttr('hidden');
        quizTimer();
    });

    // Time limit countdown
    function quizTimer() {
        const displayTimer=document.getElementById('display-timer')
        const timer=document.getElementById('timer')

        t = displayTimer.innerHTML.replace("Time limit: ", "").replace(" seconds", "")
        t = parseInt(t)
        setInterval(()=>{
            t-=1
            displayTimer.innerHTML = "Time limit: " + t + " seconds"
            timer.value = t
            if (t == 0) {
                document.getElementById('submit').click();
            }
        },1000)
    }
});