## Setup

### Frontend:

```bash
cd frontend
npm install
npm run build
```

### Backend:

```bash
cd backend/core
conda create -n pantalone python=3.11
conda activate pantalone
pip install -r requirements.txt
```

### Prepare Services:

Refer to [here](backend/service/readme.md) for details.


### Start:

```bash
conda activate pantalone
cd backend/core/src
python app.py
```

Open `http://localhost:9876/` in browser.

### Test:

```bash
cd backend/core
./scripts/unittest.ps1
```

## TODO list

- major
  - chat with context (pandasai)
  - playground
    - correlation, linear regression
    - ()
    - rmax, rmin, rmean, rstd, rsum, csum, yoy, mom
    - chart type
  - percentile => oppertunity
    - probability of return > threshold
    - normalty test
    - connection among subcharts
- minor
  - more data
    - global
    - bond
  - market data
    - dual y axis for YoY and MoM data
  - select model
- further
  - push news summary
  - whoosh for news search, rag
