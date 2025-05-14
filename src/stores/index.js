import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {getToken_au,setToken_au,removeToken_au} from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
    const UserInfo = ref({})
    const token = ref('')
    const setUserInfo = (data,tokens,PersonRoles)=>{
        UserInfo.value = {...data,PersonRole:PersonRoles}
        setToken_au(tokens)
        token.value = tokens
    }

    const removeUserInfo = ()=>{
        UserInfo.value = {}
        removeToken_au()
        token.value = ''
    }
    return { UserInfo,token,setUserInfo,removeUserInfo }
  },
  {
    persist: {
        enabled: true,
    }
}
)


  