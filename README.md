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

Then to install the dependencies run,

```bash
pip install -r requirements.txt
```

You must ensure the python interpreter is **from within the virtual environment**

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


