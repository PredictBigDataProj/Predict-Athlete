 [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/PredictBigDataProj/Predict-Athlete.git)
<a href="https://render.com/deploy?repo=https://github.com/PredictBigDataProj/Predict-Athlete">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

# Project Scope and Purpose
This project aims to assist aspiring footballers in identifying the most suitable playing position and league based on their physical and performance statistics. Using machine learning and statistical analysis, the system evaluates user-provided attributes and compares them against a dataset of professional players to deliver personalized insights.

# Key Features

- Position Prediction Model: A supervised learning model predicts the most suitable position (e.g., striker, midfielder, defender) for a user based on attributes like speed, stamina, strength, passing accuracy, etc.
- League-Specific Insights: Interactive graphs and visualizations provide an in-depth look into trends and average stats within various top leagues, helping users understand where they best fit.
- League Suitability Estimator: Based on the user's position, nationality, and stats, the system recommends the most compatible football leagues, using comparative analysis across all professional players in that role.

| Terminal Command                | Description                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| pip install -r requirements.txt | Initialises all requirements based on the requirements.txt file in the project directory. |
| flask init                      | Initilises database                                                                       |
| flask run                       | Runs development server                                                                               |
# Setup Requirements
Before running the project ensure the following:
* **Python Version Requirement**: Please ensure that **Python 3.9.10** is installed. This specific version was used during the development of the Flask application, and we cannot guarantee its compatibility or proper functioning with other Python versions.
## Installing Dependencies
```bash
pip install -r requirements.txt
```
## Initialising the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command.

```bash
flask init
```

## Run the server with the following command

```bash
flask run
```
