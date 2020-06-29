# England & Wales Crime Dashboard
Web application showing England & Wales crime statistics. Built using Python, Flask and Plotly. https://england-crime-stats.herokuapp.com
## Overview
A web application that displays crime statistics in England & Wales. The application was developed using the following architecture:

* Backend: Python (Flask framework)
* Frontend: HTML & CSS, JavaScript, Plotly and Bootstrap
* Deployment: Heroku

A CRISP-DM methodology will be followed and detailed here at a later stage of the project.
## Project Motivation
The project was being completed as part of the portfolio excercises for the Udacity Data Science Nanodegree. The portfolio excercise requires the student to develop a data-driven web application by making use of the Flask web framework and Plotly.
## Data Source
The data is being sourced from https://www.data.gov.uk. This website contains open-source UK gorvernment data. The dataset that is used within the web app is centered on arrest statistics in England & Wales.

The latest available data is made available in the application via a `requests` call to https://www.ethnicity-facts-figures.service.gov.uk/crime-justice-and-the-law/policing/number-of-arrests/latest#download-the-data.
