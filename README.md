# VisualizeCovid

## Overview
A webapp built using Django and Python to help visualize data on the COVID19 outbreak. Currently, the sources for the data are the Coronavirus COVID19 API (https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest) and COVID-19 API (https://github.com/Omaroid/Covid-19-API).

The live version deployed using Heroku can be found here: [visualizecovid19.herokuapp.com](https://visualizecovid.herokuapp.com/)

## Screenshot
![Screenshot of the home page](https://i.imgur.com/Xi6ALm9.png)

## Installation
* ```git clone https://github.com/j0hnk1m/visualize_covid.git```
* ```pip install -r requirements.txt```
* ```cd visualize_covid/```
* ```python manage.py makemigrations```
* ```python manage.py migrate```
* ```python manage.py runserver```

Now that the server is running, visit ```localhost:8000```
