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
cd backend/core
python app.py
```

Open `http://localhost:9876/` in browser.


## TODO list

- major
  - embedding for relevant holdings
  - holding relationship [https://echarts.apache.org/examples/zh/editor.html?c=graph-label-overlap]()
  - chat with context (pandasai)
- minor
  - cache with expiration
  - market data
    - dual y axis for YoY and MoM data
  - select model
- further
  - push news summary
  - charts panel, select data and draw
    - correlation, linear regression
  - whoosh for news search, rag
