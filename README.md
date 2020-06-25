# uk-crime-dashboard (currently under development)
Web application showing UK Crime statistics. Built using Python, Flask and Plotly.
## Overview
A web application that displays crime statistics in the UK. The application is being developed using the following architecture:

* Backend: Python (Flask framework)
* Frontend: HTML & CSS, JavaScript, Plotly and Bootstrap
* Deployment: Heroku

A CRISP-DM methodology will be followed and detailed here at a later stage of the project.
## Project Motivation
The project is being completed as part of the portfolio excercises for the Udacity Data Science Nanodegree. The portfolio excercise requires the student to develop a data-driven web application by making use of the Flask web framework and Plotly.
## Data Source
The data is being sourced from https://www.data.gov.uk. This website contains open-source UK gorvernment data. The dataset being used as part of the project is UK crime statistics on the number of arrests and ethnicities of those being arrested. 

The latest available data is made available in the application via a `requests` call to the appropiate url.
