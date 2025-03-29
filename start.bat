@echo off
start /B waitress-serve --listen=0.0.0.0:5000 app:app
timeout /t 3
start streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
