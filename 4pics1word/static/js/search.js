document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('srch');
    const searchDropdown = document.getElementById('search-result');

    if (!searchInput || !searchDropdown) {
        console.error("Search components not found!");
        return;
    }

    searchInput.addEventListener('input', function() {
        const input = this.value;
        console.log('Input changed:', input);
        
        if (input.length >= 2) {
            fetch(`/api/search_suggestions?q=${encodeURIComponent(input)}`)
                .then(response => response.json())
                .then(data => {
                    searchDropdown.innerHTML = ''; 
                    if (data.length) {
                        data.forEach(item => {
                            const link = document.createElement('a');
                            link.textContent = item.title;  
                            link.href = `/search?q=${encodeURIComponent(item.title)}`;
                            searchDropdown.appendChild(link);
                        });
                        searchDropdown.style.display = 'block';
                    } else {
                        searchDropdown.style.display = 'none';
                    }
                })
                .catch(err => {
                    console.error('Error fetching search suggestions:', err);
                    searchDropdown.style.display = 'none';
                });
        } else {
            searchDropdown.style.display = 'none';
        }
    });

    searchInput.addEventListener('focus', function() {
        
        if (searchDropdown.children.length > 0) {
            searchDropdown.style.display = 'block';
        }
    });

    searchInput.addEventListener('blur', function() {
        setTimeout(() => {
            
            searchDropdown.style.display = 'none';
        }, 200); 
    });
});
