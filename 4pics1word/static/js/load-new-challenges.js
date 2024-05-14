$(document).ready(function() {
    const gamesContainer = $('#games-container');
    let page = 1;

    function loadMoreGames() {
        loading = true;
        $.ajax({
            url: `/api/games?page=${page}&limit=6`, 
            type: 'GET',
            success: function(data) {
                if (data.games.length > 0) {
                    for (game of data.games) {
                        game_div = createGameDiv(game);
                        
                    }

                }
                loading = false;
            },
            error: function(xhr, status, error) {
                console.error('Error loading games:', error);
                loading = false;
            }
        });
    }

    
});
