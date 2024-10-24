import axios from 'axios';

async function getChinaBondYieldDataRequest (dates) {
    const res = await axios.post('/api/CN1YR', { 'dates': dates });
    return res.data;
}

async function getLPRDataRequest (dates) {
    const res = await axios.post('/api/lpr', { 'dates': dates })
    return res.data;
}

async function getIndexCloseRequest (dates) {
    const res = await axios.post('/api/index-close', { 'dates': dates });
    return res.data;
}

async function getFundNameRequest (symbol) {
    const res = await axios.post('/api/fund-name', { 'symbol': symbol });
    return res.data;
}

async function getRefreshedFundNetValueRequest (symbols) {
    const res = await axios.post('/api/refresh', { 'symbols': symbols });
    return res.data;
}

async function getFundHoldingDataRequest (symbols) {
    const res = await axios.post('/api/holding', { 'symbols': symbols });
    return res.data;
}

async function getFundHoldingRelevanceDataRequest (holding) {
    const res = await axios.post('/api/relevance', { 'holding': holding });
    return res.data;
}

async function getKLineDataRequest (symbol, period, market) {
    const res = await axios.post('/api/kline',
        { 'code': symbol, 'period': period, 'market': market });
    return res.data;
}

async function getMarketDataRequest (instrument) {
    const res = await axios.post('/api/market', { 'instrument': instrument });
    return res.data;
}

async function getLatestCurrencyRate (symbol) {
    const res = await axios.post('/api/latest-currency-rate', { 'symbol': symbol });
    return res.data;
}

function uploadRequest (file, callback) {

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

async function loadDataRequest () {
    const res = await axios.get('/api/data');
    return res.data;
}


async function addDataRequest (type, data, id) {
    await axios.post(`/api/data/${type}`, {
        id: id,
        content: data
    });
}


async function getTIntervalRequest (p, df) {
    const res = await axios.get('/api/statistics/t/interval', {
        params: {
            p: p,
            df: df
        }
    });
    return res.data;
}


async function getNormalIntervalRequest (p) {
    const res = await axios.get('/api/statistics/normal/interval', {
        params: {
            p: p
        }
    });
    return res.data;
}


async function getGitUpdatedRequest () {
    const res = await axios.get('/api/git/updated');
    return res.data;
}

async function getBackendVersionRequest () {
    const res = await axios.get('/api/version');
    return res.data;
}


export {
    getChinaBondYieldDataRequest,
    getLPRDataRequest,
    getFundNameRequest,
    uploadRequest,
    loadDataRequest,
    addDataRequest,
    getTIntervalRequest,
    getNormalIntervalRequest,
    getIndexCloseRequest,
    getRefreshedFundNetValueRequest,
    getFundHoldingDataRequest,
    getFundHoldingRelevanceDataRequest,
    getKLineDataRequest,
    getGitUpdatedRequest,
    getMarketDataRequest,
    getLatestCurrencyRate,
    getBackendVersionRequest
}