document.getElementById('srch').addEventListener('input', function() {
    var input = this.value;
    if (input.length < 2) {
        document.getElementById('search-result').style.display = 'none';
        return;
    }
    fetch(`/api/search_suggestions?q=${encodeURIComponent(input)}`)
        .then(response => response.json())
        .then(data => {
            var resultBox = document.getElementById('search-result');
            resultBox.innerHTML = '';
            if (data.length) {
                resultBox.style.display = 'block';
                data.forEach(item => {
                    var link = document.createElement('a');
                    link.textContent = item.title;  // Assuming 'title' is part of the suggestion objects
                    link.href = `/search?q=${encodeURIComponent(item.title)}`;
                    resultBox.appendChild(link);
                });
            } else {
                resultBox.style.display = 'none';
            }
        })
        .catch(err => console.error('Error fetching search suggestions:', err));
});