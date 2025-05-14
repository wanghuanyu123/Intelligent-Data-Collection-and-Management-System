<script setup>

import { defineProps,defineEmits,watch,ref } from 'vue';
import {} from '@/apis/index'
import {useUserStore} from '@/stores/index'
import {addClubApi} from '@/apis/index'
const store = useUserStore()

const prop= defineProps({
    clubDialog: Boolean
});

const emit = defineEmits(['closeDialog']);

const dialog = ref(prop.clubDialog)

watch(() => prop.clubDialog, (newVal) => {
    dialog.value = newVal
});



// 登录
const loginRef = ref(null)
const loginForm = ref({
    name:'',
    description:'',
    teacher:'',
})

const loginRules = ref({
    name:[{required:true,message:'请输入姓名',trigger:'blur'}],
    description:[{required:true,message:'请输入简介',trigger:'blur'}],
    teacher:[{required:true,message:'请输入指导老师',trigger:'blur'}],
})

const submitLogin = async () =>{
    loginRef.value.validate(async (valid) => {
    if (valid) {
        addClubApi({
            name:loginForm.value.name,
            description:loginForm.value.description,
            teacher:loginForm.value.teacher
        })
        ElMessage.success('添加成功')
        loginRef.value.resetFields()
        emit('closeDialog')
    } 
  })
}
</script>

<template>
    <el-dialog
    v-model="dialog"
    @close="emit('closeDialog')"
    title="添加俱乐部"
     width="1000"
    >
    <el-form :model="loginForm" :rules="loginRules" ref="loginRef">
        <el-form-item label="姓名" prop="name">
            <el-input v-model="loginForm.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="简介" prop="description">
            <el-input v-model="loginForm.description" placeholder="请输入简介"></el-input>
        </el-form-item>
        <el-form-item label="指导老师ID" prop="teacher"> 
            <el-input v-model="loginForm.teacher" placeholder="请输入指导老师ID"></el-input>
        </el-form-item>
        <el-button @click="submitLogin">添加</el-button>
    </el-form>
    </el-dialog>

  
</template>