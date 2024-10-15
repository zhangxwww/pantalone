Frontend:

```bash
cd frontend
npm install
npm run build
```

Backend:

```bash
cd backend
conda create -n pantalone python=3.11
conda activate pantalone
pip install -r requirements.txt
```

Start:

```bash
conda activate pantalone
cd backend
python app.py
```