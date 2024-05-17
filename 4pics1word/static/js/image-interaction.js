document.addEventListener('DOMContentLoaded', function() {
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
