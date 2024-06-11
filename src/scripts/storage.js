function save (data) {
    localStorage.setItem("pantalone-data", JSON.stringify(data));
}

function load () {
    const empty = {
        cashData: [],
        monetaryFundData: [],
        fixedDepositData: []
    };
    try {
        const data = JSON.parse(localStorage.getItem("pantalone-data"));
        return data || empty;
    } catch (e) {
        console.error(e);
        localStorage.removeItem("pantalone-data");
        return empty;
    }
}

function upload (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        localStorage.setItem("pantalone-data", e.target.result);
        location.reload();
    }
    reader.readAsText(file.raw);
}

function download () {
    const content = localStorage.getItem("pantalone-data");
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pantalone.json';
    a.click();
    window.URL.revokeObjectURL(url);
}

export default {
    save,
    load,
    upload,
    download
};