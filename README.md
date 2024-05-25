# Project Setup Guide

Follow these steps to set up and run the project in your local development environment.

## Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

## Installation Steps

1. Create a virtual environment using `venv`.

    ```bash
    py -m venv env
    ```

    Or if the above command doesn't work, use:

    ```bash
    python -m venv env
    ```

2. Activate the newly created virtual environment.

    For Windows users:

    ```bash
    env\Scripts\activate
    ```

    For macOS or Linux users:

    ```bash
    source env/bin/activate
    ```

3. Install all required packages from `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4. Run the development server.

    ```bash
    py manage.py runserver
    ```

## Explanation

- **Creating a Virtual Environment:** The first step is to create a virtual environment to ensure your project has isolated dependencies and does not conflict with globally installed packages.
- **Activating the Virtual Environment:** Activating the virtual environment ensures that any `pip` and `python` commands you run use the versions and packages within that environment.
- **Installing Requirements:** The `requirements.txt` file contains a list of all the Python packages needed for this project. The command `pip install -r requirements.txt` reads this file and installs all listed packages.
- **Running the Server:** The command `py manage.py runserver` starts the Django development server, allowing you to see your web application running in a browser.

## Notes

- Always ensure you have activated the virtual environment before running or developing this project.
- If you encounter issues, check that you have followed each step correctly and that all prerequisites are met.

Happy developing!
