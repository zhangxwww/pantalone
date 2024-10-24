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
  - percentile of the current asset price in historical prices [https://echarts.apache.org/examples/zh/editor.html?c=scatter-single-axis]()
  - embedding for relevant holdings
  - holding relationship [https://echarts.apache.org/examples/zh/editor.html?c=graph-label-overlap]()
- minor
  - cache with expiration
  - market data
    - dual y axis for YoY and MoM data
- further
  - push news summary
  - charts panel, select data and draw
