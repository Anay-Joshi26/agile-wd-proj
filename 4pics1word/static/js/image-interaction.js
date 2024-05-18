document.addEventListener('DOMContentLoaded', function() {

    // Make sure the image zoom is centered between bottom of navbar and bottom of viewport
    
    const navbar = document.querySelector('.navbar');
    const zoomHeight = document.documentElement;

    function updateNavbarHeight() {
      const navbarHeight = navbar.offsetHeight;
      zoomHeight.style.setProperty('--navbar-height', `${navbarHeight}px`);
    }

    // Set height and update on resize
    updateNavbarHeight();
    window.addEventListener('resize', updateNavbarHeight);


    const imageCells = document.querySelectorAll('.image-cell img')
    const overlay = document.getElementById('overlay')
    let zoomedImage = null

    imageCells.forEach(img => {
        img.addEventListener('click', function() {
            if (zoomedImage) {
                overlay.removeChild(zoomedImage)
                overlay.style.display = 'none'
                zoomedImage = null
            }
            zoomedImage = img.cloneNode(true)
            zoomedImage.classList.add('zoom')
            overlay.appendChild(zoomedImage)
            overlay.style.display = 'block'
            zoomedImage.addEventListener('click', function(e) {
                e.stopPropagation()
            })
        })
    })

    overlay.addEventListener('click', function() {
        if (zoomedImage) {
            overlay.removeChild(zoomedImage)
            overlay.style.display = 'none'
            zoomedImage = null
        }
    })
})
