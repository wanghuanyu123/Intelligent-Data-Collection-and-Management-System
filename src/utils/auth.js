import Cookies from 'js-cookie'

const TokenKey = 'vue_admin_template_token'

export function getToken_au() {
  return Cookies.get(TokenKey)
}

export function setToken_au(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken_au() {
  return Cookies.remove(TokenKey)
}
