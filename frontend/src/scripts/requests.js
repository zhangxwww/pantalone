import axios from 'axios';

function getChinaBondYieldDataRequest (dates, callback) {
    axios.post('/api/CN1YR', { 'dates': dates }).then(res => {
        callback(res.data);
    }).catch(err => {
        console.log(err);
    });
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
    })
}


export {
    getChinaBondYieldDataRequest,
    uploadRequest,
    loadDataRequest,
    addDataRequest
}