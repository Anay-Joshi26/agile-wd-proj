$(document).ready(function() {

    $(document).on('click', '.vote-button', function() {

        let button = $(this);
        let spanTag = button.parent().find('span');

        let val = spanTag.text().trim();
        console.log(val);

        const fetchUrl = button.attr('data-fetch-url');
        let new_upvote = null;

        let gameContainer = button.closest('.vote-container');
        let upvoteButton = gameContainer.find('.upvote-button');
        let downvoteButton = gameContainer.find('.downvote-button');

        // Check if the button has active-upvote or active-downvote classes
        let isUpvoted = upvoteButton.hasClass('active-upvote');
        let isDownvoted = downvoteButton.hasClass('active-downvote');

        if (fetchUrl.includes("upvote")) {
            new_upvote = changeUpvotes(val, 'upvote');
            if (!isUpvoted) {
                if (isDownvoted) {
                    downvoteButton.removeClass('active-downvote'); // Remove active-downvote class
                }
                else {
                    upvoteButton.addClass('active-upvote');
                }
            }
        }
        else {
            new_upvote = changeUpvotes(val, 'downovte');
            if (!isDownvoted) {
                if (isUpvoted) {
                    upvoteButton.removeClass('active-upvote');
                }
                else {
                    downvoteButton.addClass('active-downvote');
                }
            } 
        }

        console.log(new_upvote);

        spanTag.text(new_upvote);

        $.ajax({
            type: 'POST',
            url: fetchUrl,
            success: function(data) {
                if (!data.success) {
                    console.log("Error incrementing upvotes");
                    console.log(data)
                    setTimeout(function() {
                        spanTag.text(val); // revert text after 0.6 second
                    }, 600);
                }
            },
            error: function() {
                console.log("Error actual incrementing upvotes");
                setTimeout(function() {
                    spanTag.text(val); // revert text after 0.6 second
                }, 600);
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
