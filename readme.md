[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/PredictBigDataProj/Predict-Athlete.git)
<a href="https://render.com/deploy?repo=https://github.com/PredictBigDataProj/Predict-Athlete">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

| Terminal Command                | Description                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| pip install -r requirements.txt | Initialises all requirements based on the requirements.txt file in the project directory. |
| flask init                      | Initilises database                                                                       |
| flask run                       | Runs server                                                                               |
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
