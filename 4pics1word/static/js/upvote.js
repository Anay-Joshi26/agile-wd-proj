$(document).ready(function() {

    $('.upvote-button').click(function() {

        let button = $(this);

        let val = button.text();
        new_upvote = incrementUpvotes(val);
        button.text(new_upvote);
        const fetchUrl = button.attr('data-fetch-url');

        $.ajax({
            type: 'POST',
            url: fetchUrl,
            success: function(data) {
                if (!data.success) {
                    console.log("Error incrementing upvotes");
                    setTimeout(function() {
                        button.text(val); // revert text after 1 second
                    }, 1000);
                }
            }
        });

    });

});

function incrementUpvotes(str) {
    const match = str.match(/^(\d+) Upvotes$/);
    
    if (match && match[1]) {
        const incrementedNum = parseInt(match[1]) + 1;
        return incrementedNum + " Upvotes";
    } else {
        return str;
    }
}