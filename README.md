# LLM Text Pipeline Visualizer

A Streamlit app for visualizing sentence extraction, custom overlapping chunks, tokenization, and text-processing metrics for LLM workflows.

## Features

- Sentence extraction with a lightweight regex splitter
- Custom sliding-window chunks with configurable overlap
- Token visualization using simple word and punctuation token splitting
- Analytics dashboard with chunk and token metrics

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app2.py
```

The app opens at `http://localhost:8501`.

## Deploy on Render for Free

This repo includes a Render Blueprint in `render.yaml`, so Render can auto-fill the service settings.

1. Push this folder to a GitHub repository.
2. Go to `https://render.com` and sign in.
3. Click `New +` and choose `Blueprint`.
4. Connect the GitHub repository for this project.
5. Select the `render.yaml` file if Render asks for it.
6. Click `Apply` or `Deploy`.

Render will create a free Python web service with:

- Build command: `pip install --upgrade pip && pip install -r requirements.txt`
- Start command: `streamlit run app2.py --server.port=$PORT --server.address=0.0.0.0`
- Python version: `3.11.11`, pinned in `.python-version` and `render.yaml`

After deploy, your app URL will look like:

```text
https://llm-text-pipeline.onrender.com
```

If that name is already taken, Render will assign a slightly different URL.

## Free Tier Notes

This project pins Python to 3.11.11 because Render's current Python 3.14 default can break older Streamlit/protobuf dependencies. If you previously saw TypeError: Metaclasses with custom tp_new are not supported, redeploy after pushing these changes.\n\nRender free web services are good for demos and hobby apps, but they have limits:

- The app spins down after 15 minutes without traffic.
- The first request after spin-down can take about a minute.
- Local file changes are not permanent after restarts or redeploys.
- Free usage is limited by monthly included instance hours, bandwidth, and build minutes.

## Project Structure

```text
.
â”œâ”€â”€ app2.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ render.yaml
â”œâ”€â”€ .python-version
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
```
