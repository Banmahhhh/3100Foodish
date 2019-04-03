/**
 * @param {*} value
 * @param {string} [fmt='yyyy-MM-dd hh:mm:ss']
 * @returns
 */
export function dateFormat(value, fmt = 'yyyy-MM-dd hh:mm:ss') {
    try {
        return new Date(value).Format(fmt)
    } catch (e) {
        return ''
    }
}

export function money(value, dec = 2) {
    value = ~~value
    value = value / 100
    return value.toFixed(dec)
}

// remaining time
export function countDown(finishTime, defaultStr) {
    if (!finishTime) return defaultStr
    const M_TIME = 1000 * 60 // minute
    const H_TIME = M_TIME * 60 // hour
    const D_TIME = 24 * H_TIME // day
    const time = +new Date() - finishTime
    const day = parseInt(time / D_TIME) // day
    const hour = parseInt((time - day * D_TIME) / H_TIME) // hour
    const min = parseInt((time - day * D_TIME - hour * H_TIME) / M_TIME) // minute
    let result = ''
    if (day) {
        result += `${day}天`
    }
    if (hour) {
        result += `${hour}小时`
    }
    if (min) {
        result += `${min}分钟`
    }
    return result
}
