console.log('Upload game script loaded');

$('#submit-upload-game').click(function(e) {
    $('.errors').css('display', 'none')
    e.preventDefault();

    let form = $('form');

    if (!form[0].checkValidity()) {

      e.preventDefault();
      e.stopPropagation();
      form[0].classList.add('was-validated');
      $('#fill-in-error').css('display', 'block')
      return;
  }

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
                console.log(data.msg);

                if (data.hasOwnProperty('image-error')) {
                  $('#images-error').html(data.msg)
                  $('#images-error').css('display', 'block')
                }
                else if (data.hasOwnProperty('answer-error')) {
                  $('#answer-error').html(data.msg)
                  $('#answer-error').css('display', 'block')
                }
                else if (data.hasOwnProperty('game-title-error')) {
                  $('#game-title-error').html(data.msg)
                  $('#game-title-error').css('display', 'block')
                }
                else if (data.hasOwnProperty('hint-error')) {
                  $('#hint-error').html(data.msg)
                  $('#hint-error').css('display', 'block')
                }
                else if (data.hasOwnProperty('answer-error')) {
                  $('#answer-error').html(data.msg)
                  $('#answer-error').css('display', 'block')
                }
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