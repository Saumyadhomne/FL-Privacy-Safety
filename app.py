"""Federated Industrial AI dashboard demo."""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
for folder in (UPLOAD_DIR, MODEL_DIR, REPORT_DIR):
    folder.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-demo-change-me")
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
ALLOWED_EXTENSIONS = {"csv", "json", "xlsx", "parquet"}


def load_state() -> dict:
    path = DATA_DIR / "state.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    state = {"models": 12, "updates": 8, "accuracy": 92, "predictions": {"Normal": 68, "Warning": 22, "Critical": 10}, "history": [70, 75, 80, 85, 90], "events": []}
    save_state(state)
    return state


def save_state(state: dict) -> None:
    (DATA_DIR / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.context_processor
def inject_globals():
    return {"year": datetime.now().year}


@app.get("/")
@app.get("/dashboard")
def dashboard():
    state = load_state()
    datasets = len([p for p in UPLOAD_DIR.iterdir() if p.is_file()])
    return render_template("dashboard.html", active="dashboard", state=state, datasets=datasets)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Choose a file to upload.", "error")
        elif not allowed_file(file.filename):
            flash("Supported formats: CSV, JSON, XLSX, and Parquet.", "error")
        else:
            name = secure_filename(file.filename)
            file.save(UPLOAD_DIR / name)
            state = load_state()
            state["events"].insert(0, f"Dataset uploaded: {name}")
            save_state(state)
            flash(f"{name} uploaded successfully.", "success")
            return redirect(url_for("upload"))
    files = sorted((p.name for p in UPLOAD_DIR.iterdir() if p.is_file()), reverse=True)
    return render_template("upload.html", active="upload", files=files)


@app.route("/train", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        state = load_state()
        state["updates"] += 1
        state["accuracy"] = min(99, state["accuracy"] + 1)
        state["history"] = (state["history"] + [state["accuracy"]])[-5:]
        state["events"].insert(0, f"Federated training round {state['updates']} completed")
        save_state(state)
        flash("Training round completed. Only model updates were aggregated.", "success")
        return redirect(url_for("train"))
    return render_template("train.html", active="train", state=load_state())


@app.get("/updates")
def updates():
    state = load_state()
    events = state.get("events", []) or ["Model update received from Plant North", "Secure aggregation completed", "Model version 1.0 is active"]
    return render_template("updates.html", active="updates", events=events)


@app.get("/analytics")
def analytics():
    return render_template("analytics.html", active="analytics", state=load_state())


@app.route("/reports", methods=["GET", "POST"])
def reports():
    if request.method == "POST":
        state = load_state()
        report = {"generated_at": datetime.now().isoformat(timespec="seconds"), "model_accuracy": state["accuracy"], "training_rounds": state["updates"], "uploaded_datasets": len(list(UPLOAD_DIR.iterdir()))}
        path = REPORT_DIR / f"federated_report_{datetime.now():%Y%m%d_%H%M%S}.json"
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        flash(f"Report generated: {path.name}", "success")
        return redirect(url_for("reports"))
    files = sorted((p.name for p in REPORT_DIR.iterdir() if p.is_file()), reverse=True)
    return render_template("reports.html", active="reports", files=files)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        flash("Settings saved for this demo session.", "success")
        return redirect(url_for("settings"))
    return render_template("settings.html", active="settings")


@app.get("/api/summary")
def api_summary():
    state = load_state()
    return jsonify({"datasets": len(list(UPLOAD_DIR.iterdir())), **state})


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
