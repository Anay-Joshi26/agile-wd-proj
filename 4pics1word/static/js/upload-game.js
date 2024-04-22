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
            if (data.success) {
                console.log("Game uploaded successfully");
                // the re-direct should be to the newly created game page
                // but it is set to the challenges page for now
                window.location.href = '/challenges';
            }
            else {
                console.log(data.message);
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            if (xhr.status === 400) {
              let errorResponse = JSON.parse(xhr.responseText);
              
              console.log("Error: " + errorResponse.error);
              console.log("Message: " + errorResponse.message);
            } else {
              
              console.log("Error: " + textStatus);
            }
          }
    });
});