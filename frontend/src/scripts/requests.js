import axios from 'axios';

export async function getChinaBondYieldDataRequest (dates) {
    const res = await axios.post('/api/CN1YR', { 'dates': dates });
    return res.data;
}

export async function getLPRDataRequest (dates) {
    const res = await axios.post('/api/lpr', { 'dates': dates })
    return res.data;
}

export async function getIndexCloseRequest (dates) {
    const res = await axios.post('/api/index-close', { 'dates': dates });
    return res.data;
}

export async function getFundNameRequest (symbol) {
    const res = await axios.post('/api/fund-name', { 'symbol': symbol });
    return res.data;
}

export async function getRefreshedFundNetValueRequest (symbols) {
    const res = await axios.post('/api/refresh', { 'symbols': symbols });
    return res.data;
}

export async function getFundHoldingDataRequest (symbols) {
    const res = await axios.post('/api/holding', { 'symbols': symbols });
    return res.data;
}

export async function getFundHoldingRelevanceDataRequest (holding) {
    const res = await axios.post('/api/relevance', { 'holding': holding });
    return res.data;
}

export async function getKLineDataRequest (symbol, period, market) {
    const res = await axios.post('/api/kline',
        { 'code': symbol, 'period': period, 'market': market });
    return res.data;
}

export async function getMarketDataRequest (instrument) {
    const res = await axios.post('/api/market', { 'instrument': instrument });
    return res.data;
}

export async function getLatestCurrencyRateRequest (symbol) {
    const res = await axios.post('/api/latest-currency-rate', { 'symbol': symbol });
    return res.data;
}

export async function getPricePercentileRequest (data) {
    const res = await axios.post('/api/price-percentile', data);
    return res.data;
}

export async function getStockBondInfoRequest (stocks, bonds) {
    const res = await axios.post('/api/stock-bond-info', { 'stocks': stocks, 'bonds': bonds });
    return res.data;
}

export function uploadRequest (file, callback) {

    const reader = new FileReader();
    reader.onload = (e) => {
        const base64Data = e.target.result.split(',')[1];

        // eslint-disable-next-line no-unused-vars
        axios.post('/api/upload', { 'file': base64Data }).then(res => {
            callback();
        }).catch(err => {
            console.error(err);
        })
    }
    reader.readAsDataURL(file.raw);
}

export async function loadDataRequest () {
    const res = await axios.get('/api/data');
    return res.data;
}


export async function addDataRequest (type, data, id) {
    await axios.post(`/api/data/${type}`, {
        id: id,
        content: data
    });
}


export async function getTIntervalRequest (p, df) {
    const res = await axios.get('/api/statistics/t/interval', {
        params: {
            p: p,
            df: df
        }
    });
    return res.data;
}


export async function getNormalIntervalRequest (p) {
    const res = await axios.get('/api/statistics/normal/interval', {
        params: {
            p: p
        }
    });
    return res.data;
}


export async function getGitUpdatedRequest () {
    const res = await axios.get('/api/git/updated');
    return res.data;
}

export async function getBackendVersionRequest () {
    const res = await axios.get('/api/version');
    return res.data;
}

export async function chatStreamRequest (body, onMessage, onEnd) {
    const response = await fetch('/api/ai/chat/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
        },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        console.error('Failed to connect to the chat server');
        console.error(response);
        return;
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // eslint-disable-next-line no-constant-condition
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        onMessage(chunk);

    }
    onEnd();
}
