from shiny import reactive
from shiny.express import input, render, ui

import pandas as pd
import json
import urllib.request

# 1. Page Configuration
ui.page_opts(title="Live Google Sheets Dashboard", fillable=True)

# 🔗 Apps Script Web App URL
URL = "https://script.google.com/macros/s/AKfycbx3bEAax6SED8WnYwx8GifuxeVJs2Q-5ZlinMQ4smzFzLtqdtYhg9eiXUqXpyLoVBoNXw/exec"

# 2. Logic (Reactive Calculations)
@reactive.calc
def data():
    try:
        # Note: In Shinylive, urllib works well for simple JSON fetches
        with urllib.request.urlopen(URL) as r:
            json_data = json.loads(r.read().decode())
        return pd.DataFrame(json_data)
    except Exception as e:
        return pd.DataFrame({"ERROR": [str(e)]})

# 3. UI Layout
ui.h2("Live Google Sheets Dashboard")

# Status Bar
with ui.div(style="padding:10px; background:#f8f9fa; border-radius:6px; margin-bottom: 20px;"):
    @render.text
    def status():
        return "✅ Connected via Apps Script" if "ERROR" not in data().columns else "❌ Failed to load"

# Value Box for Count
with ui.value_box(theme="primary"):
    "Total Records"
    ui.br()
    ui.br()
    
    @render.text
    def count():
        df = data()
        return str(len(df)) if "ERROR" not in df.columns else "0"

# Main Data Table
with ui.card():
    @render.data_frame
    def table():
        return render.DataTable(data())