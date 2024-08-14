import axios from 'axios';

function getChinaBondYieldDataRequest (dates, callback) {
    axios.post('/api/CN1YR', { 'dates': dates }).then(res => {
        callback(res.data);
    }).catch(err => {
        console.log(err);
    });
}

function uploadRequest (file) {
    const reader = new FileReader(file);
    reader.onload = (e) => {
        const base64Data = e.target.result.split(',')[1];
        axios.post('/api/upload', { 'file': base64Data }).then(res => {
            console.log(res);
        }).catch(err => {
            console.log(err);
        });
    }
}

export {
    getChinaBondYieldDataRequest,
    uploadRequest
}