$(document).ready(function() {

    $('.vote-button').click(function() {

        let button = $(this);
        let span_tag = $(this).parent().find('span')

        val = span_tag.text().trim();
        console.log(val);

        const fetchUrl = button.attr('data-fetch-url');
        let new_upvote = null;

        if (fetchUrl.includes("upvote")) {
            new_upvote = changeUpvotes(val, 'upvote');
        }
        else {
            new_upvote = changeUpvotes(val, 'downvote');
        }

        console.log(new_upvote);

        span_tag.text(new_upvote);

        $.ajax({
            type: 'POST',
            url: fetchUrl,
            success: function(data) {
                if (!data.success) {
                    console.log("Error incrementing upvotes");
                    setTimeout(function() {
                        span_tag.text(val); // revert text after 1 second
                    }, 1000);
                }
            }
        });

    });

});

function changeUpvotes(str, action) {
    // ChatGPT generated
    // Prompt: "write a match() in js that matches the number of upvotes in a string and increments it by 1. 
    // If the string does not contain the number of upvotes, return the string as is"
    // (gpt only for regex)
    const match = str.match(/^(-?\d+) Upvotes$/);
    
    if (match && match[1]) {
        if (action === 'upvote') {
            const incrementedNum = parseInt(match[1]) + 1;
            return incrementedNum + " Upvotes";
        }
        else {
            const decrementedNum = parseInt(match[1]) - 1;
            return decrementedNum + " Upvotes";
        }
    } else {
        return str;
    }
}
