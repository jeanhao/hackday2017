import axios from 'axios'

const errorMessages = res => `${res.status} ${res.statusText}`

const check404 = (res) => {
  if (res.status === 404) {
    return Promise.reject(errorMessages(res))
  }
  return res
}

const checkStatus = (res) => {
  if (res.status >= 200 && res.status < 300) {
    return res
  }
    // 这里补充更多错误参数
  return res.text().then(errorMsg => new Error({
    statusCode: res.status,
    msg: errorMsg,
  })).then((err) => { throw err })
}

const jsonParse = res => res.json()

const setUriParam = (keys, value, keyPostfix) => {
  let keyStr = keys[0]

  keys.slice(1).forEach((key) => {
    keyStr += `[${key}]`
  })

  if (keyPostfix) keyStr += keyPostfix

  return `${encodeURIComponent(keyStr)}=${encodeURIComponent(value)}`
}

const getUriParam = (key, param) => {
  const array = []

  if (Array.isArray(param)) {
    param.forEach(value => array.push(setUriParam(key, value, '[]')))
  } else if (param instanceof Object) {
    param.entries().forEach((curVal) => {
      array.push(getUriParam(key.concat(curVal[0]), curVal[1]))
    })
  } else if (param !== undefined) array.push(setUriParam(key, param))

  return array.join('&')
}

const toQueryString = params => params.entries().reduce((urlArr, curVal) => {
  const str = getUriParam(curVal[0], curVal[1])
  return str === '' ? urlArr : urlArr.concat(str)
}).join('&')


export default {
  install(Vue) {
    const vFetch = (options) => {
      const defaultOptions = {
        method: 'get',
      }

      const opts = Object.assign({}, defaultOptions, { ...options })

      // add query params to url when method is GET
      if (opts && opts.method === 'get' && opts.data) {
        opts.url += `?${toQueryString(opts.data)}`
      }

      return axios(opts)
        .then(check404)
        .then(checkStatus)
        .then(jsonParse)
    }
    const vGet = (url, data) => vFetch({ url, data })
    const vPost = (url, data) => vFetch({ url, data, method: 'post' })
    /* eslint-disable no-param-reassign */
    Vue.$fetch = vFetch
    Vue.prototype.$fetch = vFetch
    Vue.$get = vGet
    Vue.prototype.$get = vGet
    Vue.$post = vPost
    Vue.prototype.$post = vPost
    /* eslint-enable no-param-reassign */
  },
}

