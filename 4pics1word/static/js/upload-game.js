console.log('Upload game script loaded');

$('#submit-upload-game').click(function(e) {
    e.preventDefault();

    let form = $('form');

    let url = form.attr('action');

    console.log(url)

    let form_data = new FormData($('form')[0]);
    
    $.ajax({
        type: 'POST',
        url: url,
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log('Success!');
        },
    });
});