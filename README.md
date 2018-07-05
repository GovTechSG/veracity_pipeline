# Veracity Pipeline

## Set up
  Run these commands:

    sudo easy_install pip
    sudo pip install python
    sudo pip install cx_Oracle
    sudo pip install robotframework==3.0
    sudo pip install robotframework-selenium2library
    sudo pip install robotframework-databaselibrary
    sudo pip install robotframework-faker --upgrade --ignore-installed six
    sudo pip install requests
    sudo pip install psycopg2-binary

    curl https://chromedriver.storage.googleapis.com/2.40/chromedriver_mac64.zip -o ~/Downloads/chromedriver_mac64.zip
    unzip ~/Downloads/chromedriver_*.zip -d ~/Downloads
    chmod +x ~/Downloads/chromedriver
    sudo mv -f ~/Downloads/chromedriver /usr/local/share/chromedriver
    sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver

If the last one fails, run this:

    sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

## Run Integration Test

    pybot -A argfile.txt