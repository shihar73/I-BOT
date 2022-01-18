# I-BOT

## About

It's a web app on flask and selenium technology. This Instagram bot will log in to your Instagram account and search with the tag and take photos and videos of it and like it and comments on it. There is an option to add an Instagram account in this website there is an option to add an Instagram account in this website If the username and password are correct then the account will be added to the database. then you can add custom hashtags and comments if you don't want to add hashtags comments you can choose the default

## Installation
Instructions on how to install *I-BOT*
```bash
git clone https://github.com/shihar73/I-BOT.git
cd I-BOT

```
create a new virtual environment
 ```
 python3 -m venv virtualenv
 ```
 install requirements.txt
 ```
 pip install requirements.txt 
 ```
 *install geckodriver*
 
 Download geckodriver
 ```
 wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz
 ```
 Extract file
 ```
 tar -xvzf geckodriver-v0.24.0-linux32.tar.gz
 ```
 Make is executable 
 ```
  chmod +x geckodriver
 ```
 
 creat a .env file
 ```
 sudo nano .env
 ```
Add url and paths in .env file 
 ```
MONGO_URL = " <mongodb url> "
FIREFOX_BIN = " <firefox path> "
GECKODRIVER_PATH = " <geckodriver path> "
 ```
Then you can start your server
