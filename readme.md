## Setup

### Frontend:

```bash
cd frontend
npm install
npm run build
```

### Backend:

```bash
cd backend
conda create -n pantalone python=3.11
conda activate pantalone
pip install -r requirements.txt
```

### Start:

```bash
conda activate pantalone
cd backend
python app.py
```

Open `http://localhost:9876/` in browser.


## TODO list

- major
  - percentile of the current asset price in historical prices
  - embedding for relevant holdings
- minor
  - cache with expiration
  - market data