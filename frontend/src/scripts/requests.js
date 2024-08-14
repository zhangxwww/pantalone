import axios from 'axios';

function getChinaBondYieldDataRequest (dates, callback) {
    axios.post('/api/CN1YR', { 'dates': dates }).then(res => {
        callback(res.data);
    }).catch(err => {
        console.log(err);
    });
}

export {
    getChinaBondYieldDataRequest
}