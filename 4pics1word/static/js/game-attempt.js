$(document).ready(function() {
    if(message === ""){
        $('#alert').hide();
    }
})

var attemptDisplay = document.getElementById('attempt-counter')

attemptDisplay.textContent = attempt;


// Used to toggle the hint display on the game play page
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
            sendData(guess, attempt, match, challenge_id).then(data => {
                console.log("HH", data)
                if (data){
                    document.getElementById('guess-count').textContent = data.num_attempts;
                    document.getElementById('leaderboard-position').textContent = data.position;

                    // Show the popup (hidden by default - now itll become visible)
                    document.getElementById('will-count-popup').style.display = 'flex';
                }


            });
        }
        else {
            document.getElementById('will-not-count-popup').style.display = 'flex';
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

async function sendData(guess, attempt, match, challenge_id) {
    let dataToSend = { 'guess': guess, 'attempts': attempt, 'correct': match, 'challenge_id': challenge_id };

    try {
        let response = await fetch('/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        let data = await response.json();
        console.log(data);
        return { num_attempts: data.num_attempts, position: data.position };

    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
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
