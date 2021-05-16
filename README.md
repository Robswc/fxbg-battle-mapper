
![header](https://github.com/robswc/fxbg-battle-mapper/blob/main/misc/header.png)

# About 

An open source project that maps various battles onto an interactive map, detailed with information.
Written in python, using dash and beautiful soup.

# How to use (locally)

*currently a work in progress*

This project uses dash-plotly for the front end.  This means in order to run, you will need to install dash via pip.  This is relatively quick and painless!  Below are instructions for running (works on any OS).

- After cloning the repository, use the pip command to install the required libraries.  This can be done with:

 `pip install -r requirements.txt`

- After verifying that pip has properly installed dependencies, run with: 

`python app.py`

- This will create a webpage which will then open in your default browser.

# Hosted
`https:\\battle-mapper.herokuapp.com`
You may have to wait a bit for it to start up if it hasnt been visted in a bit.

Pushing changes can be done by pushing to the heroku remote main branch after adding/commiting them locally.
For example pushing from the wip branch:
`git push heroku wip:main`

# Authors

Robert Carroll  
Jacob Carryer  
Kyle White  
Mikayla Stitts
