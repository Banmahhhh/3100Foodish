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

// 剩余时间 :14天16小时5分钟
export function countDown(finishTime, defaultStr) {
    if (!finishTime) return defaultStr
    const M_TIME = 1000 * 60 // 分钟
    const H_TIME = M_TIME * 60 // 小时
    const D_TIME = 24 * H_TIME // 天
    const time = +new Date() - finishTime
    const day = parseInt(time / D_TIME) // 天
    const hour = parseInt((time - day * D_TIME) / H_TIME) // 小时
    const min = parseInt((time - day * D_TIME - hour * H_TIME) / M_TIME) // 分钟
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
