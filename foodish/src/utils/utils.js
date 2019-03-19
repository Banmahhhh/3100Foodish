/**
 * @description 格式化
 * @param {String} fmt yyyy-MM-dd hh:mm:ss
 */
Date.prototype.Format = function (fmt) {
  const o = {
    'M+': this.getMonth() + 1, // 月份
    'd+': this.getDate(), // 日
    'H+': this.getHours(), // 小时
    'h+': this.getHours(), // 小时
    'm+': this.getMinutes(), // 分
    's+': this.getSeconds(), // 秒
    'q+': Math.floor((this.getMonth() + 3) / 3), // 季度
    S: this.getMilliseconds() // 毫秒
  }
  if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length))
  for (const k in o) if (new RegExp('(' + k + ')').test(fmt)) fmt = fmt.replace(RegExp.$1, RegExp.$1.length === 1 ? o[k] : ('00' + o[k]).substr(('' + o[k]).length))
  return fmt
}

/**
 * @description 解析url字符串
 * @param {String} url
 * @return {Object}
 */

export function URLObject(url) {
  url = url || window.location.href
  const theRequest = {}
  let strs = ''
  if (url.indexOf('?') !== -1) {
    const str = url.substring(url.indexOf('?') + 1)
    strs = str.split('&')
    for (let i = 0; i < strs.length; i++) {
      theRequest[strs[i].split('=')[0]] = decodeURIComponent(strs[i].split('=')[1])
    }
  }
  return theRequest
}

/**
 * @description 对象深拷贝
 * @param {Object} obj
 * @returns {Object}
 */
export function ObjectParse(obj) {
  try {
    return JSON.parse(JSON.stringify(obj))
  } catch (e) {
    console.error('copy error')
  }
  return {}
}


export function getFileName(url) {
  if (!url) return ''
  return url.substring(url.lastIndexOf('/') + 1)
}

export const flavor = [
  { text: 'sweet', val: 1 },
  { text: 'spicy', val: 2 },
  { text: 'light food', val: 3 },
  { text: 'curry', val: 4 },
  { text: 'home style', val: 5 },
  { text: 'dessert', val: 6 },
  { text: 'fry', val: 7 },
  { text: 'western style', val: 8 }
]

export const dislike = [
  { text: 'seafood', val: 1 },
  { text: 'maize', val: 2 },
  { text: 'egg', val: 3 },
  { text: 'sheep meat', val: 4 },
  { text: 'pork', val: 5 },
  { text: 'garlic', val: 6 },
  { text: 'caraway', val: 7 },
  { text: 'cheese', val: 8 },
  { text: 'innards', val: 9 }
]