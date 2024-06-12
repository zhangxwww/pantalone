function isNumberValidator (rule, value, callback) {
    if (!value) {
        callback();
    } else {
        const regPositiveRealNum = /^(([1-9]\d*)|([0][.]{1}[0-9]{0,2}[1-9]+)|([1-9]\d*[.]{1}[0-9]+))$/g;
        if (regPositiveRealNum.test(value)) {
            callback();
        } else if (parseInt(value) === 0) {
            callback();
        } else {
            return callback(new Error(rule.message));
        }
    }
}

export { isNumberValidator };