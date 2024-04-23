let attempt = 1;

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

// CONTINUE ON VALIDATING GUESSES
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
        if (word_count != words.length){
            guess += ' '; 
        }
        word_count ++;
    });

    console.log('Input values:', words);
    console.log('Guess:', guess);

    // fetch('/api/data')
    // .then(response => response.json())
    // .then(data => {
    //     const answer = data.message;
    //     let match = (answer.trim() == guess.trim());
    //     console.log(match);
    //     console.log(guess.toString().valueOf());
    //     console.log(answer.toString().valueOf());
    //     if (match){
    //         console.log(match);
    //         notify_correct();
    //     }
    //     else if(answer.trim().length == guess.trim().length){
    //         notify_incorrect();
    //         incrementCounter();
    //         setTimeout(() =>{
    //             restore_inputs();
    //         }, 2000);
    //     }
    // })

    let match = (answer.trim() == guess.trim());

    if (match){
        console.log(match);
        notify_correct();
    }
    else if(answer.trim().length == guess.trim().length){
        notify_incorrect();
        incrementCounter();
        setTimeout(() =>{
            restore_inputs();
        }, 2000);

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
