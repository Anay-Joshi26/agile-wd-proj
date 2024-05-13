

let images_uploaded = [false, false, false, false];

document.querySelectorAll('.upload-input').forEach(function(input) {
    input.addEventListener('change', function(event) {

        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            const imgSrc = e.target.result;
            const imageId = event.target.id.replace('image-input', '');
            imageUpload(imgSrc, imageId);

        };

        reader.readAsDataURL(file);
    });
});

document.querySelectorAll('.change-img-icon').forEach(function(icon) {
    icon.addEventListener('click', function(event) {
        const imageId = event.target.id.replace('img-change', '');
        imageClear(imageId);
    });

});

function imageUpload(imgSrc, imageId) {
    const imgPrev = document.getElementById(`img${imageId}`);
    imgPrev.style.backgroundImage = `url(${imgSrc})`;
    imgPrev.style.objectFit = 'fill';
    imgPrev.style.backgroundRepeat = 'no-repeat';
    imgPrev.style.backgroundSize = 'cover';
    imgPrev.style.backgroundPosition = 'center';
    document.querySelector(`#img${imageId} label`).style.display = 'none';
    document.getElementById(`img-change${imageId}`).style.display = '';
}

function imageClear(imageId) {
    input = document.getElementById(`image-input${imageId}`);
    input.value = '';
    console.log(imageId);
    const imgPrev = document.getElementById(`img${imageId}`);
    imgPrev.style.backgroundImage = '';
    imgPrev.style.objectFit = '';
    imgPrev.style.backgroundRepeat = '';
    imgPrev.style.backgroundSize = '';
    imgPrev.style.backgroundPosition = '';
    document.querySelector(`#img${imageId} label`).style.display = '';
    document.getElementById(`img-change${imageId}`).style.display = 'none';
}

