# Numerical Methods

![GitHub Repo Size](https://img.shields.io/github/repo-size/joaosnet/numerical-methods?style=for-the-badge)
![GitHub Languages Count](https://img.shields.io/github/languages/count/joaosnet/numerical-methods?style=for-the-badge)
![GitHub Forks](https://img.shields.io/github/forks/joaosnet/numerical-methods?style=for-the-badge)
[![Language: pt-br](https://img.shields.io/badge/lang-pt--br-green.svg?style=for-the-badge)](https://github.com/joaosnet/numerical-methods/blob/master/README.pt-br.md)

<img align="right" src="screenshots/dash.png" width="256"/>

## Introduction

The **Numerical Methods** project provides an interactive platform to explore numerical methods applied to engineering. Developed in Python, this application allows for the application and visualization of mathematical algorithms, making it useful for learning and analysis. The site is available [here](https://numerical-methods-7wxf.onrender.com/).

## Technologies Used

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" /> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" /> <img src="https://img.shields.io/badge/dash-008DE4?style=for-the-badge&logo=dash&logoColor=white" /> <img src="https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D" />

## Table of Contents

* [Introduction](#introduction)
* [Technologies Used](#technologies-used)
* [How to Use](#how-to-use)
* [Screenshots](#screenshots)
* [Contributing](#contributing)
* [Updating the Repository](#updating-the-repository)

## How to Use

### Prerequisites

1. Install the `pyenv` version manager to manage Python versions:
   - [Instructions for Windows](https://github.com/pyenv-win/pyenv-win#installation)
   - [Instructions for Linux](https://github.com/pyenv/pyenv#installation)
   
2. Install `pipx` to manage isolated dependencies.

### Installation

#### Windows and Linux

1. Update `pyenv`:
   ```bash
   pyenv update
   ```
2. Install Python 3.12:
   ```bash
   pyenv install 3.12
   ```
3. Set the local and global Python environment:
   ```bash
   pyenv local 3.12
   pyenv global 3.12
   ```
4. Install `pipx`:
   ```bash
   pip install pipx
   ```
5. Install `poetry` using `pipx`:
   ```bash
   pipx install poetry
   ```
6. Configure `poetry` to create the virtual environment within the project directory:
   ```bash
   poetry config virtualenvs.in-project true
   ```
7. Clone the repository:
   ```bash
   git clone https://github.com/joaosnet/numerical-methods.git
   ```
8. Install the project dependencies:
   ```bash
   poetry install
   ```
9. Run the application:
   ```bash
   python main.py
   ```
   
### Create the `requirements.txt` File

If you need a `requirements.txt` file for other implementations:

```bash
poetry export --without-hashes --without-urls --without dev -f requirements.txt -o requirements.txt
```

## Screenshots

![Screenshot](screenshots/dash.png)

_Dashboard view showcasing applied numerical methods._

## Contributing

To contribute to this project, please follow these steps:

1. Fork the repository.
2. Clone your fork to your local environment.
3. Create a new branch for your changes:
   ```bash
   git checkout -b your-branch-name
   ```
4. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
   ```
5. Push your changes to the remote repository:
   ```bash
   git push origin your-branch-name
   ```
6. Open a pull request on the original repository.

## Updating the Repository

To keep your repository up to date with the latest changes:

1. Pull the latest changes:
   ```bash
   git pull
   ```
2. Add any new files or changes:
   ```bash
   git add .
   ```
3. Commit the changes:
   ```bash
   git commit -m "Updating repository"
   ```
4. Push to the remote repository:
   ```bash
   git push
   ```
