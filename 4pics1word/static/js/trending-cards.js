document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/trending')
        .then(response => response.json())
        .then(games => {
            const container = document.getElementById('trendingCards');
            const containerMobile = document.getElementById('trendingCardsMobile');
            // Clear existing content
            container.innerHTML = '';
            containerMobile.innerHTML = '';
            games.forEach(game => {
                const cardHtml = `
                    <div class="col-md-3">
                        <div class="card">
                            <img src="${game.image1}" class="card-img-top" alt="Image">
                            <div class="card-img-overlay">
                                <h5 class="card-title">${game.game_title}</h5>
                                <p class="card-poster">Posted by ${game.creator_username}</p>
                            </div>
                        </div>
                    </div>
                `;
                container.innerHTML += cardHtml;
                containerMobile.innerHTML += `<div class="card" style="min-width: 80%; margin-right: 20px;">${cardHtml}</div>`;
            });
        })
        .catch(error => console.error('Error fetching trending games:', error));
});