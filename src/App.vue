<script setup>
import { watch } from 'vue'
import { useUserStore } from '@/stores/index'

const store = useUserStore()

// 监听 userInfo 变化
watch(
  () => store.UserInfo,
  (newVal) => {
    if (newVal && newVal.PersonName) {
      // 设置网站标题
      document.title = `${newVal.PersonName} - 数据采集系统`
    } else {
      // 如果没有用户信息，显示默认标题
      document.title = '数据采集系统'
    }
  },    
  { immediate: true } // 立即执行一次
)
</script>
<template>
    <router-view/>
</template>
