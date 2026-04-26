$python = "C:\Users\Holly\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$project = "C:\Users\Holly\Documents\New project"

Set-Location $project
& $python -m streamlit run app.py --server.port 8501 --server.headless true
