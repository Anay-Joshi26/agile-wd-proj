$(document).ready(function() {
    const gamesContainer = $('#games-container');
    let page = 1;
    finished_loading = false;


    function loadMoreGames() {
        if (finished_loading) return;

        $.ajax({
            url: `/api/games?page=${page}`, 
            type: 'GET',
            success: function(data) {
                console.log(data)
                if (data.games.length > 0 && data.success === true) {

                    for (game of data.games) {
                        game_div = createGameDiv(game);
                        gamesContainer.append(game_div);
                    }
                    page++;

                }
            },
            error: function(xhr, status, error) {
                console.error('Error loading games:', error);
                finished_loading = true;
            }
        });
    }

    function createGameDiv(game) {

        let format_date_created = formatDate(game.date_created);


        let upvoteClass = ''
        let downvoteClass = ''

        if (game.user_vote === 1) {
            upvoteClass = 'active-upvote';
        }
        else if (game.user_vote === -1) {
            downvoteClass = 'active-downvote';
        }



        return `
        <div class="col-md-12 mb-4 card">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        <a href="/challenge/${game.gameId}" class="text-decoration-none card-title">
                            <h3 class="card-title text-decoration-none">${game.game_title}</h3>
                            <p class="card-text"><small class="text-muted">${format_date_created}</small></p>
                        </a>
                        <p class="card-text"><small class="text-muted">Posted by: ${game.creator_username}</small></p>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="image-wrapper-box">
                                    <img src="${game.image1}" alt="Image 1">
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="image-wrapper-box">
                                    <img src="${game.image2}" alt="Image 2">
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="image-wrapper-box">
                                    <img src="${game.image3}" alt="Image 3">
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="image-wrapper-box">
                                    <img src="${game.image4}" alt="Image 4">
                                </div>
                            </div>
                        </div>
                        <div class="d-flex gap-2">
                            <div class="vote-container">
                                <button type="button" class="btn btn-sm vote-button upvote-button" data-fetch-url="/api/upvote/${game.gameId}">
                                    <svg fill="black" height="16" data-icon-name="upvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M12.877 19H7.123A1.125 1.125 0 0 1 6 17.877V11H2.126a1.114 1.114 0 0 1-1.007-.7 1.249 1.249 0 0 1 .171-1.343L9.166.368a1.128 1.128 0 0 1 1.668.004l7.872 8.581a1.25 1.25 0 0 1 .176 1.348 1.113 1.113 0 0 1-1.005.7H14v6.877A1.125 1.125 0 0 1 12.877 19ZM7.25 17.75h5.5v-8h4.934L10 1.31 2.258 9.75H7.25v8ZM2.227 9.784l-.012.016c.01-.006.014-.01.012-.016Z"></path>
                                    </svg>
                                </button>
                                <span>${game.number_of_upvotes} Upvotes</span>
                                <button type="button" class="btn btn-sm vote-button downvote-button" data-fetch-url="/api/downvote/${game.gameId}">
                                    <svg fill="black" height="16" data-icon-name="downvote-outline" viewBox="0 0 20 20" width="16" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M10 20a1.122 1.122 0 0 1-.834-.372l-7.872-8.581A1.251 1.251 0 0 1 1.118 9.7 1.114 1.114 0 0 1 2.123 9H6V2.123A1.125 1.125 0 0 1 7.123 1h5.754A1.125 1.125 0 0 1 14 2.123V9h3.874a1.114 1.114 0 0 1 1.007.7 1.25 1.25 0 0 1-.171 1.345l-7.876 8.589A1.128 1.128 0 0 1 10 20Zm-7.684-9.75L10 18.69l7.741-8.44H12.75v-8h-5.5v8H2.316Zm15.469-.05c-.01 0-.014.007-.012.013l.012-.013Z"></path><!--?-->
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    }

    // ChatGPT generated date format
    function formatDate(date_created) {
        const date = new Date(date_created);

        const options = {
            weekday: 'short', 
            day: '2-digit', 
            month: 'short', 
            year: 'numeric', 
            timeZone: 'UTC'
        };

        const format_date_created = date.toLocaleString('en-GB', options);

        return format_date_created;
    }


    // first round of loading more games
    loadMoreGames();

    // then, we can create an infinite scroll event listener
    // for when a user scrolls to the bottom of the page (with some margin)
    const threshold = 450;
    let timer = null;
    timer_is_running = false;

    window.addEventListener('scroll', function() {
        if (timer_is_running) return;

        // Reference: https://www.educative.io/answers/how-to-implement-infinite-scrolling-in-javascript
        // ^ for the if statement as shown below
        if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - threshold) {

            timer_is_running = true;
            timer = setTimeout(function() {
                loadMoreGames();
                timer_is_running = false;
                clearTimeout(timer);
            }, 500);
        }

    });

    
});
