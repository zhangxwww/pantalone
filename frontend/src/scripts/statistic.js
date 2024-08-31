function mean (array) {
    if (array.length === 0) {
        return Number.NaN;
    }
    return array.reduce((a, b) => a + b) / array.length;
}

function std (array) {
    if (array.length <= 1) {
        return Number.NaN;
    }
    const mu = mean(array);
    const diff = array.map((a) => (a - mu) ** 2);
    const n = array.length;
    const sum = diff.reduce((a, b) => a + b);
    return Math.sqrt(sum / (n - 1));
}

function nanmean (array) {
    const filtered = array.filter((a) => !isNaN(a));
    return mean(filtered);
}

function nanstd (array) {
    const filtered = array.filter((a) => !isNaN(a));
    return std(filtered);
}

function countNotNaN (array) {
    const filtered = array.filter((a) => !isNaN(a));
    return filtered.length;
}

function rolling (array, windowSize, func) {
    const result = [];
    for (let end = 1; end < array.length + 1; end++) {
        const start = Math.max(0, end - windowSize);
        result.push(func(array.slice(start, end)));
    }
    return result;
}

function averageReturn (ret1, ret2, span1, span2, method = 'arithmetic') {
    if (method === 'arithmetic') {
        return (ret1 * span1 + ret2 * span2) / (span1 + span2);
    } else if (method === 'geometric') {
        return Math.pow(
            Math.pow(ret1 + 1, span1 / 365) *
            Math.pow(ret2 + 1, span2 / 365),
            365 / (span1 + span2))
            - 1;
    } else {
        throw new Error(`Invalid method ${method}`);
    }
}

export default { mean, std, rolling, nanmean, nanstd, countNotNaN, averageReturn };