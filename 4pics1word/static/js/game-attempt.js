let attempt = 1;

function incrementCounter() {
    attempt++;
    document.getElementById('attempt-counter').textContent = attempt;
}

function nextInput(current, next) {
    if (current.value.length == 1) {
      document.getElementById(next).focus();
    }
}

function previousInput(event, current, previous) {
    if (event.key === 'Backspace' && document.getElementById(current).value === '') {
      if (previous !== 'input-1') { 
        document.getElementById(previous).focus();
      }
    }
}

function makeGuess() {
    // Select all input elements within divs with class 'input-container'
    const word_divs = document.querySelectorAll('.word-container');
    
    // Array to store input values
    const words = [];
    
    // Loop through each input element and push its value to the array
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

    // Here you can send 'values' to the backend using AJAX or fetch
    console.log('Input values:', words);
    console.log('Guess:', guess);
}

