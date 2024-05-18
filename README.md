# Agile Web Development CITS3403 Project

SnapCipher is a game where you can upload images and other guess the the word or phrase which relates those images. 

If you've ever played 4pics1word you'll know exactly where we got our inspiration from.

## How to Play

1. Create an account and login
2. Explore challenges created by others **OR** Make your own game
3. Click on a challenge you'd like to play and check out the leaderboard
4. Play the challenge and check what score you got!


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

To run the website execuete the following:

```bash
python3 4pics1word\main.py
```

to run the app via flask, execute the following:

```bash
flask --app 4pics1word\main.py run
```

To run `flask` commands such as `shell, run` etc the `--app 4pics1word/main.py` must be given so flask can locate our main app.

To deactivate the virtual environment runL

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