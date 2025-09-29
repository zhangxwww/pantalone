export function timeFormat (t, short = false) {
    let year = t.getFullYear();
    let month = t.getMonth() + 1;
    let day = t.getDate();
    let formatted;
    if (short) {
        formatted = `${year}/${month < 10 ? '0' + month : month}`;
    } else {
        formatted = `${year}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`;
    }
    return formatted;
}

export function percentileFormat (value) {
    return Number.isNaN(value) || value === Infinity || value === -Infinity ? '-' : (value * 100).toFixed(2) + '%';
}