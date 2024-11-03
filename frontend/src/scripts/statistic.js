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

function expanding (array, func) {
    const result = [];
    for (let end = 1; end < array.length + 1; end++) {
        result.push(func(array.slice(0, end)));
    }
    return result;
}

function averageMean (value1, value2, weight1, weight2, method = 'arithmetic') {
    if (method === 'arithmetic') {
        return (value1 * weight1 + value2 * weight2) / (weight1 + weight2);
    } else if (method === 'geometric') {
        return Math.pow(
            Math.pow(value1 + 1, weight1 / 365) *
            Math.pow(value2 + 1, weight2 / 365),
            365 / (weight1 + weight2))
            - 1;
    } else {
        throw new Error(`Invalid method ${method}`);
    }
}

export default { mean, std, rolling, expanding, nanmean, nanstd, countNotNaN, averageMean };