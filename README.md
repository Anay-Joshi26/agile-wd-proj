# Agile Web Development CITS3403 Project

## Contributers

| UWA ID      | Name          | GitHub Username |
|-------------|---------------|-----------------|
| 23364506    | Anay Bhargav Joshi      | Anay-Joshi26         |
| 23443143    | Connor Fernie    | CJFernie       |
| 23351863    | Aaryan Haresh Sachdevani   | AaryanSachdevani2003      |
| 23352583    | Ashkaan Gaurav Singh   | ashcansingh      |

*Note: Most members had their local and global `user.email` variable in `git config` not linked to their GitHub account hence many commits do **not** show directly from the 'Contributers'. This also resulted in separate accounts under the same person making commits*

This was changed eventually by running (towards the end):
`git config --global user.email <actual-email-linked-to-github>`

## About the Website

SnapCipher is an interactive game, inspired by 4pics1word where you can upload images and players will try guess the the word or phrase which relates those images. SnapCipher's colourful design is sure to engage users and get them to put their thinking caps on!

**Users can create challenges for others, play other people's challenge, top leaderboards, upvote/downvote posts and more!**

### Homepage
- Brief overview of SnapCipher, how to find games and how to create challenges
- Users can navigate to the other pages and login/register

### Create Challenge
- Allows users to create their own challenges when they're logged in
- Users can upload images and enter the text for the secret word/phrase, title and hint

### Challenges
- Trending posts displayed at the top of the page ranked by highest upvotes in the last 7 days
- All challenges found here, users click a post to view more detail about the challenge
- **Community:** Users can upvote or downvote challenges here if they're logged in and your challenge can get featured if it is popular

### Detailed Challenge View
- After a user clicks on a game they're shown more detail about the challenge including a leaderboard of people who have attempted the challenge based on their attempts
- User can choose to play the game here

### Play Game
- Users are shown the 4 images for the challenge and can guess the word or phrase that relates them
- Guesses/attempts are tracked and the top 10 players are shown on the leaderboard based on the number of guesses in ascending order

## How to Play

1. Create an account and login, you can find this in the top right on the page, or we will prompt you to login if we need you too
2. Start on the homepage for a quick introduction to the site or navigate straight to the challenges page
3. On the challenges page you can see trending games, explore challenges created by others
4. Click on a challenge you'd like to play and check out the leaderboard
5. Play the challenge and check what score you got! After this you can give the game an upvote if you liked it (or a downvote)!
6. **OR** Make your own game by navigating to Create Game, here you can select a title of your challenge, upload 4 photos and select the word/phrase that relates them


To run the app, you must be within the `agile-wd-proj` directory, but first you will need to `git clone` the repo.

## Running the app

When running the app, if a database isn't present it will generate a database with fake data, where the titles of all games are just random words (they have no meaning).
The images and answers **are** infact related and so the images can be used to play the game.

Before running the app, in the `agile-wd-proj` directory create a `.env` file, and type a secret key of your choosing:

```bash
SECRET_KEY_APP = 'your_secret_key'
```

### Linux/MacOS/WSL

Set up virtual environment (`myenv`)

To create a virtual environment in your current directory run:

```bash
python3 -m venv myenv
```

Then to activate the virtual environment run:

```bash
source myenv/bin/activate
```

Then to install the dependencies run,

```bash
pip install -r requirements.txt
```

You must ensure the python interpreter is **from within the virtual environment**.

To run the website execuete the following:

```bash
python3 4pics1word\main.py
```

To run the app via flask, execute the following:

```bash
flask --app 4pics1word\main.py run
```

To run `flask` commands such as `shell, run` etc the `--app 4pics1word/main.py` must be given so flask can locate our main app.

To deactivate the virtual environment run:

```bash
deactivate
```

or 

```bash
source deactivate
```


### Windows

Set up virtual environment (`myenv`)

*Note: There may be policies on windows which prevent activation or even creation of virtual environments*

```powershell
python -m venv myenv
```

or

```powershell
py -m venv myenv
```

**May need to run the following from Powershell admin to activate the env**
```powershell
set-executionpolicy remotesigned
```

Then to activate the virtual environment run the following:
```powershell
myenv\Scripts\activate
```

Then to install the dependencies run,

```powershell
pip install -r requirements.txt
```

You must ensure the python interpreter is **from within the virtual environment**

To run the app, execute the following
```powershell
py .\4pics1word\main.py
```

to run the app via flask, execute the following:

```powershell
python -m flask --app 4pics1word\main.py run
```

or 

```powershell
py -m flask --app 4pics1word\main.py run
```

To deactivate the virtual environment runL

```powershell
deactivate
```

*Note: The main directory is named `4pics1word` as we initially began with that as the name, as the project evolved the name SnapCiper was chosen, but the directory name remains as 4pics1word as an easter egg*

## Testing

The tests were developed on a MacOS operating system, and **will not work** when running on WSL (applies to the Selenium tests).

When running tests, the tests will automatically teardown and repopulate the database with fake data. **Before running tests delete `/4pics1word/instance`**. Running the app will automatically make the database, otherwise issues not related to tests will spawn.

If you are in the `agile-wd-proj` directory, you may run the following commands:

To run the unit tests:
```bash
python3 -m unittest 4pics1word/tests/unit-tests.py
```

To run the web driver tests:
*First you must set `debug=False` in the `4pics1word/main.py` init function at the bottom (as we do not want the app to reload)*
Then open a new terminal and run the web app as shown before (with the above `debug = False` param). While the app is running, in a new clean terminal run:
```bash
python3 -m unittest 4pics1word/tests/web-driver-tests.py
```

When running on Windows changes to the python interpreter may require `python3` to be changed to `python` or `py`

## References/Assets used

Tab Favicon Icon:
https://www.flaticon.com/free-icon/puzzle_1371320
From: Puzzle icons created by Freepik - Flaticon


