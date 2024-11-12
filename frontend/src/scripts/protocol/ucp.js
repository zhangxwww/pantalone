import { INSTRUMENT_INDICATOR_TRANSLATION_LONG } from '../constant';

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
        .map(c => operationCodeToSymbol[c]
            || INSTRUMENT_INDICATOR_TRANSLATION_LONG[c]
            || c)
        .join(' ');
}
