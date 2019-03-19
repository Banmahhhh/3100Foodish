
export const required = (message, trigger = 'blur', required = true) => {
  const rule = {
    type: 'string',
    required,
    trigger,
    message,
    transform(value) {
      if (value === undefined) return ''
      return value + ''
    }
  }
  return rule
}

export const boolean = (message, trigger = 'blur', required = true) => {
  const rule = {
    type: 'boolean',
    required,
    trigger,
    message
  }
  return rule
}
export const array = (message, option = {}) => {
  const transform = value => {
    if (!value) return []
    return value.filter(item => item !== '')
  }
  const rule = {
    type: 'array',
    required,
    trigger: 'blur',
    transform,
    message
  }
  return Object.assign(rule, option)
}
export const object = (message, trigger = 'blur', required = true) => {
  const rule = {
    type: 'object',
    required,
    trigger,
    message
  }
  return rule
}
export const number = (message, option = {}) => {
  const rule = {
    type: 'number',
    required: true,
    trigger: 'blur,change',
    message
  }
  return Object.assign(rule, option)
}
