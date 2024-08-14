```bash
cd frontend
npm install

cd ../backend
conda create -n pantalone python=3.11
conda activate pantalone
pip install -r requirements.txt
```


```bash
conda activate pantalone
uvicorn app:app --reload --host localhost --port 9876
```