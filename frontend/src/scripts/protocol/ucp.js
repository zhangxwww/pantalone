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

export const OPERATION_CODE_2_SYMBOL = {
    'plus': '+',
    'minus': '-',
    'mul': '*',
    'div': '/',
    'comma': ',',
    'l_paren': '(',
    'r_paren': ')',
};

export function UCPStringToFormula (string) {
    return string.split(' ')
        .map(s => parseUCPString(s).code)
        .map(c => OPERATION_CODE_2_SYMBOL[c]
            || INSTRUMENT_INDICATOR_TRANSLATION_LONG[c]
            || c)
        .join(' ')
        .replace(/\(\s+/g, '(')
        .replace(/\s+\)/g, ')')
        .replace(/,\s+/g, ',');
}
