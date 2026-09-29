# Everyday Store

A simple Flask e-commerce starter project with a product catalog, session-based cart, quantity updates, removal controls, and a checkout cost summary. Prices are shown in Indian rupees. This demo does not process payments or collect customer address details.

## Project structure

- app.py - Flask routes, sample products, and cart calculations
- templates/ - product, cart, and checkout pages
- static/css/style.css - responsive styling
- requirement.txt - Python package dependency
- azure-pipelines.yml - Azure DevOps pipeline

## Run on Windows

Open PowerShell in this project folder and run:

    py -3.11 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r .\requirement.txt
    .\.venv\Scripts\python.exe app.py

Open http://127.0.0.1:5000/ in your browser.

For deployment, set a strong random FLASK_SECRET_KEY environment variable. The built-in fallback key is intended only for local development.
