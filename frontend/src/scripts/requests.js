import axios from 'axios';

async function getChinaBondYieldDataRequest (dates) {
    const res = await axios.post('/api/CN1YR', { 'dates': dates });
    return res.data;
}

async function getLPRDataRequest (dates) {
    const res = await axios.post('/api/lpr', { 'dates': dates })
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


export {
    getChinaBondYieldDataRequest,
    getLPRDataRequest,
    uploadRequest,
    loadDataRequest,
    addDataRequest,
    getTIntervalRequest,
    getNormalIntervalRequest
}