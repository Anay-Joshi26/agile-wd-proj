$(document).ready(function() {
    const gamesContainer = $('#games-container');
    let page = 1;

    function loadMoreGames() {
        $.ajax({
            url: `/api/games?page=${page}`, 
            type: 'GET',
            success: function(data) {
                if (data.games.length > 0 && data.success === true) {
                    // for (game of data.games) {
                    //     game_div = createGameDiv(game);
                        
                    // }
                    console.log(data.games);

                }
            },
            error: function(xhr, status, error) {
                console.error('Error loading games:', error);
            }
        });
    }

    loadMoreGames();

    
});
