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

**Create Challenges:** You get to upload 4 images, a title, hint and the secret word or phrase which is related to the 4 images you chose.

**Solve Challenges:** Other players can then try to guess the secret word or phrase based on the 4 images you chose. 

**Top The Leaderboards:** When you play someone's game we count your guesses and you get ranked against every other player for that game.

**Community:** Players who liked your challenge can upvote your post, these upvotes are used to select trending games which get featured at the top of the challenges!

## How to Play

1. Create an account and login, you can find this in the top right on the page, or we will prompt you to login if we need you too
2. Start on the homepage for a quick introduction to the site or navigate straight to the challenges page
3. On the challenges page you can see trending games, explore challenges created by others
4. Click on a challenge you'd like to play and check out the leaderboard
5. Play the challenge and check what score you got! After this you can give the game an upvote if you liked it (or a downvote)!
6. **OR** Make your own game by navigating to Create Game, here you can select a title of your challenge, upload 4 photos and select the word/phrase that relates them


To run the app, you must be within the `agile-wd-proj` directory, but first you will need to `git clone` the repo.

## Running the app

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

### MacOS/Linux

The tests were developed on a MacOS operating system, and **will not work** when running on WSL (applies to the Selenium tests)


