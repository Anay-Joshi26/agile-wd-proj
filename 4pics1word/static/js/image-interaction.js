document.addEventListener('DOMContentLoaded', function() {
    const imageCells = document.querySelectorAll('.image-cell img')
    const overlay = document.getElementById('overlay')

    imageCells.forEach(img => {
      img.addEventListener('click', function() {
        if (this.classList.contains('zoom')) {
          this.classList.remove('zoom')
          overlay.style.display = 'none'
        } else {
          imageCells.forEach(i => i.classList.remove('zoom'))
          this.classList.add('zoom')
          overlay.style.display = 'block'
        }
      })
    })

    overlay.addEventListener('click', function() {
      imageCells.forEach(img => img.classList.remove('zoom'))
      overlay.style.display = 'none'
    })
  })