<!-- <template>
    <div class="common-layout">
      <el-container>
        <el-aside width="200px">
            <el-menu class="el-menu-vertical-demo">
                <el-sub-menu index="1" >
                    <template #title>
                        <el-icon><location /></el-icon>
                        <span>人员管理</span>
                    </template>
                    <el-menu-item index="1-1" @click="$router.push('/addrole')">
                        <el-icon><location /></el-icon>
                        <span>添加人员</span>
                    </el-menu-item>
                </el-sub-menu>
                <el-menu-item index="2" @click="$router.push('/upload')">
                    <el-icon><Document /></el-icon>
                    <span>发布任务</span>
                </el-menu-item>
                <el-menu-item index="3" @click="$router.push('/news')">
                    <el-icon><Document /></el-icon>
                    <span>查看新闻</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-main>
          <span style="font-size: large; font-weight: bold; margin-bottom: 20px;">{{title}}</span>
          <router-view></router-view>
        </el-main>
      </el-container>
    </div>
  </template>


<script  setup>
import {ref,watchEffect} from 'vue'
import {useRoute,useRouter} from 'vue-router'
const router = useRouter()
const route = useRoute()
const title = ref('')
title.value = route.meta.title
watchEffect(() => {
    title.value = route.meta.title;
    });
</script>
 -->

<script setup>
import {ref,watchEffect} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {useUserStore} from '@/stores/index'
const store = useUserStore()
const router = useRouter()
const route = useRoute()
const title = ref('')
title.value = route.meta.title
watchEffect(() => {
    title.value = route.meta.title;
    });
</script>
<template>
<div class="common-layout">
      <el-container style="border: 1px solid #cacdd6;"  class="container">
        <el-aside width="200px" height="100%">
            <el-menu class="el-menu-vertical-demo">
                <el-sub-menu index="1" >
                    <template #title>
                        <el-icon><location /></el-icon>
                        <span>个人信息</span>
                    </template>
                    <el-menu-item index="1-1" @click="$router.push('/myinfo')">
                        <el-icon><location /></el-icon>
                        <span>查看信息</span>
                    </el-menu-item>
                    <el-menu-item index="1-2" @click="$router.push('/addFace')">
                        <el-icon><location /></el-icon>
                        <span>录入人脸（唯一）</span>
                    </el-menu-item>
                </el-sub-menu>
                <el-menu-item index="2" @click="$router.push('/upload')" v-if="store.UserInfo.PersonRole=='student'">
                    <el-icon><Document /></el-icon>
                    <span>发布任务</span>
                </el-menu-item>
                <el-menu-item index="3" @click="$router.push('/watch')" v-if="store.UserInfo.PersonRole=='teacher'">
                    <el-icon><Document /></el-icon>
                    <span>待审核</span>
                </el-menu-item>
                <el-menu-item index="4" @click="$router.push('/news')" v-if="store.UserInfo.PersonRole=='student'">
                    <el-icon><Document /></el-icon>
                    <span>我的发布</span>
                </el-menu-item>
                <el-menu-item index="5" @click="$router.push('/history')" v-if="store.UserInfo.PersonRole=='teacher'">
                    <el-icon><Document /></el-icon>
                    <span>审核历史</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-main>
          <span style="font-size: large; font-weight: bold; margin-bottom: 20px;">{{title}}</span>
          <router-view></router-view>
        </el-main>
      </el-container>
    </div>
</template>
<style scoped>
.common-layout{
    padding: 50px;
    
}
.container{
    ;
}
</style>