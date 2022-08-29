
# NBAPI

A Flask app that renders twenty card elements featuring the top twenty players in the NBA, as ranked by CBS Sports, each with personalized data being pulled from an active API. The front of the card element provides general attributes, while the back of the card, when hovered over and rotated, provides the player's averages for the previous season. The button on the back also routes to that specific player's Google page with further info and updates.






## Authors

- [@KeithWootten](https://www.github.com/KeithJamesW)


## Demo


Homepage:
![](https://github.com/KeithJamesW/NBAPI/blob/main/img/NBAPIHomepage.jpg)


Card Display Page:
![](https://github.com/KeithJamesW/NBAPI/blob/main/img/NBAPICardPage.jpg)


Card Rotation:
![](https://github.com/KeithJamesW/NBAPI/blob/main/img/NBAPICardRotation.jpg)


## Installation

Prior to installing the project's dependencies, setup a virtual environment in order to avoid installing globally. To do this, enter the following commands:

```bash
  python3 -m venv venv

  source/venv/bin/activate
```



In order to install each of the project's dependencies, utilize the requirements.txt included with the project. To do this, please run the command provided below when within the project's root directory:

```bash
  pip install -r requirements.txt
```
    

To then activate the postgreSQL server necessary to access data from the SQL database, enter the following command:

```bash
  sudo service postgresql start
```

The application must then be deployed with a Flask server, which can be initialized with the following command being entered in the root directory:


```bash
  flask run
```


The server will then be actively running and the terminal prompt will provide you with the server address to input into your browser.
## Setup

After the dependencies have been successfully installed, activate the postgreSQL server necessary to access data from the SQL database, enter the following command:

```bash
  sudo service postgresql start
```

A seed.sql file has been included with the SQL commands necessary to create the database and tables needed for the player data to be properly populated into. To use this, enter the command below.

```bash
psql < seed.sql
```

The application must then be deployed with a Flask server, which can be initialized with the following command being entered in the root directory:


```bash
  flask run
```


The server will then be actively running and the terminal prompt will provide you with the server address to input into your browser.
