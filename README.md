# Federated Industrial AI Dashboard

A small Flask dashboard for exploring privacy-aware federated model workflows in an industrial setting. It includes a local demo dashboard, dataset upload, simulated training rounds, update history, analytics, report generation, and settings.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app: `python app.py`
4. Open `http://127.0.0.1:5000`.

Uploads are stored in `data/uploads/`; demo state is stored in `data/state.json`; generated JSON reports go to `reports/`. The training action is a UI demo that updates local metrics; it is not a production federated learning implementation. Do not upload sensitive production data to this local demo.

## Project structure

```text
app.py                 Flask routes and local demo state
federated.py           Federated averaging utility example
data/uploads/          Uploaded datasets (ignored by Git)
models/                Saved model artifacts (ignored by Git)
reports/               Generated reports
static/css/style.css   Dashboard styling
static/js/dashboard.js Interactive charts
templates/             Jinja page templates
```
