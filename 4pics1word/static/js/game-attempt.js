$(document).ready(function() {
    if(message === ""){
        $('#alert').hide();
    }
})

var attemptDisplay = document.getElementById('attempt-counter')

attemptDisplay.textContent = attempt;

const toggleButton = document.getElementById('hintButton');
const hiddenText = document.getElementById('hintText');

toggleButton.addEventListener('click', () => {
    if (hiddenText.classList.contains('showHint')) {
        hiddenText.classList.remove('showHint');
        toggleButton.textContent = 'Hint';
    } else {
        hiddenText.classList.add('showHint');
        toggleButton.textContent = 'Hide';
    }
});

// Make sure the image zoom is centered between bottom of navbar and bottom of viewport
document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.querySelector('.navbar');
    const zoomHeight = document.documentElement;

    function updateNavbarHeight() {
      const navbarHeight = navbar.offsetHeight;
      zoomHeight.style.setProperty('--navbar-height', `${navbarHeight}px`);
    }

    // Set height and update on resize
    updateNavbarHeight();
    window.addEventListener('resize', updateNavbarHeight);
});

function isValidPhrase(str) {
    // Reference: chatGPT generated regex => "write a regex that matches when contains only letters or numbers, 
    //                                        does not start with a space and is less than 18 characters long. 
    //                                        It must also not allow double spaces"
    return /^(?!.*\s\s)(?!^\s)[a-zA-Z0-9\s]{1,17}$/.test(str);
}

function incrementCounter() {
    attempt++;
    document.getElementById('attempt-counter').textContent = attempt;
}

function nextInput(current, next) {
    letter = document.getElementById(current).value;

    if (letter.length == 1 && letter != ' ' && isValidPhrase(letter)) {
        document.getElementById(current).value = letter.toUpperCase();
        document.getElementById(next).focus();
    }
    else{
        document.getElementById(current).value = '';
    }
}

function previousInput(event, current, previous) {
    if (event.key === 'Backspace' && document.getElementById(current).value === '') {
      if (previous !== 'input-1') { 
        document.getElementById(previous).focus();
      }
    }
    restore_inputs();
}

function makeGuess() {
    const word_divs = document.querySelectorAll('.word-container');

    const words = [];
    
    word_divs.forEach(div => {
        const inputs = div.querySelectorAll('input');
        let word = "";
        inputs.forEach(input => {
            word += input.value
        });
        words.push(word);
    });
    
    let guess = "";
    let word_count = 0;

    words.forEach(word => {
        guess += word;
        if (word_count != words.length - 1){
            guess += ' '; 
        }
        word_count ++;
    });

    console.log('Input values:', words);
    console.log('Guess:', guess);

    let match = (answer == guess)

    if (match){
        console.log(match);
        notify_correct();
        if (message === ""){
            sendData(guess, attempt, match, challenge_id)
        }
    }
    else if(answer.length == guess.length){
        console.log("WE HERE");
        notify_incorrect();
        if (message === ""){
            sendData(guess, attempt, match, challenge_id)
        }
        incrementCounter();
        setTimeout(() =>{
            restore_inputs();
        }, 1500);
    }
}

function sendData(guess, attempt, match, challenge_id){
    var dataToSend = { 'guess' : guess, 'attempts' : attempt, 'correct' : match, 'challenge_id' : challenge_id };
            fetch('/guess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); 
            })
            .catch(error => console.error('Error:', error));
}

function notify_incorrect(){
    inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('letter-input');
        input.classList.add("incorrect-input");
    })
}

function notify_correct(){
    inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.classList.remove('letter-input');
        input.classList.add("correct-input");
    })
}

function restore_inputs(){
    inputs = document.querySelectorAll('input');
            inputs.forEach(input => {
                input.classList.remove('incorrect-input');
                input.classList.add("letter-input");
            })
}
