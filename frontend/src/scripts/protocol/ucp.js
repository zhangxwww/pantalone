export function parseUCPString (ucpString) {
    const ucpParts = ucpString.slice(4).split("/");
    const ucp = {
        type: ucpParts[0],
        code: ucpParts[1],
        column: ucpParts[2]
    };
    return ucp;
}

export function UCPStringToFormula (string) {
    const operationCodeToSymbol = {
        'plus': '+',
        'minus': '-',
        'mul': '*',
        'div': '/'
    };
    return string.split(' ')
        .map(s => parseUCPString(s).code)
        .map(c => operationCodeToSymbol[c] || c)
        .join(' ');
}
