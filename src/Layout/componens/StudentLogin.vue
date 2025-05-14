<script setup>

import { defineProps,defineEmits,watch,ref } from 'vue';
import {RegistApi,LoginApi} from '@/apis/index'
import {useUserStore} from '@/stores/index'
import router from '@/router';
const store = useUserStore()
const prop= defineProps({
    stuDialog: Boolean
});

const emit = defineEmits(['closeDialog']);

const dialog = ref(prop.stuDialog)

watch(() => prop.stuDialog, (newVal) => {
    dialog.value = newVal
});


// 注册
const resRef = ref(null)

const resDialog = ref(false)

const resForm = ref({
    PersonName:'',
    PersonId:'',
    PersonRole:'',
    password:''
})

const resRules = ref({
    PersonName:[
        {required:true,message:'请输入姓名',trigger:'blur'},
        {min:2,max:10,message:'姓名长度在2-10个字符之间',trigger:'blur'},
        {pattern:/^[\u4e00-\u9fa5a-zA-Z]+$/,message:'姓名只能包含中文或英文字母，不能包含特殊字符',trigger:'blur'}
    ],
    PersonId:[
        {required:true,message:'请输入学号',trigger:'blur'},
        {pattern:/^\d{8,12}$/,message:'学号必须是8-12位数字，不能包含特殊字符',trigger:'blur'}
    ],
    PersonRole:[{required:true,message:'请选择角色',trigger:'blur'}],
    password:[
        {required:true,message:'请输入密码',trigger:'blur'},
        {min:6,max:20,message:'密码长度在6-20个字符之间',trigger:'blur'},
        {pattern:/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,20}$/,message:'密码必须包含大小写字母和数字，不能包含特殊字符',trigger:'blur'}
    ]
})

const submitRes = async () =>{

    resRef.value.validate(async (valid) => {
    if (valid) {
        await RegistApi(resForm.value)
        ElMessage.success('注册成功')
        resForm.value = {
            PersonName:'',
            PersonId:'',
            PersonRole:'',
            password:''
        }
        
        resDialog.value = false
        // resRef.value.resetFields()
        // resRef.value = null
    } 
  })
}

// 登录
const loginRef = ref(null)
const loginForm = ref({
    PersonName:'',
    PersonId:'',
    password:''
})

const loginRules = ref({
    PersonName:[{required:true,message:'请输入姓名',trigger:'blur'}],
    PersonId:[{required:true,message:'请输入学号',trigger:'blur'}],
    password:[{required:true,message:'请输入密码',trigger:'blur'}]
})

const submitLogin = async () =>{
    loginRef.value.validate(async (valid) => {
    if (valid) {
        const {token,PersonRole} = await LoginApi(loginForm.value)
        // console.log(PersonRole);
        console.log(token);
        
        ElMessage.success('登录成功')
        // console.log(loginForm.value);
        store.setUserInfo({...loginForm.value,token},token,PersonRole.PersonRole)
        // console.log(token);
        loginRef.value.resetFields()
        emit('closeDialog')
    } 
  })
}
</script>

<template>
    <div>
        <el-dialog
            v-model="dialog"
            @close="emit('closeDialog')"
            title="登录"
            width="1000"
            class="custom-dialog"
        >
            <el-form :model="loginForm" :rules="loginRules" ref="loginRef">
                <el-form-item label="姓名" prop="PersonName">
                    <el-input v-model="loginForm.PersonName" placeholder="请输入姓名"></el-input>
                </el-form-item>
                <el-form-item label="学号" prop="PersonId">
                    <el-input v-model="loginForm.PersonId" placeholder="请输入学号"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password"> 
                    <el-input v-model="loginForm.password" placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-button @click="submitLogin">登录</el-button>
                <el-button @click="resDialog=true">还没注册？点击注册</el-button>
            </el-form>
        </el-dialog>

        <el-dialog 
            v-model="resDialog"
            title="注册"
            width="1000"
            class="custom-dialog"
        >
            <el-form :model="resForm" :rules="resRules" ref="resRef">
                <el-form-item label="姓名" prop="PersonName">
                    <el-input v-model="resForm.PersonName" placeholder="请输入姓名"></el-input>
                </el-form-item>
                <el-form-item label="学号" prop="PersonId">
                    <el-input v-model="resForm.PersonId" placeholder="请输入学号"></el-input>
                </el-form-item>
                <el-form-item label="成员类型" prop="PersonRole">
                    <el-select v-model="resForm.PersonRole" placeholder="请选择角色">
                        <el-option label="学生" value="student" />
                        <el-option label="教师" value="teacher" />
                        <el-option label="管理员" value="manager" />
                    </el-select>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="resForm.password" placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-button style="width: 100px;" @click="submitRes">注册</el-button>
            </el-form>
        </el-dialog>
    </div>
</template>

<style scoped>
.custom-dialog {
    border: 5px solid #409EFF !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1) !important;
}

.custom-dialog :deep(.el-dialog__header) {
    border-bottom: 2px solid #EBEEF5 !important;
    padding: 20px !important;
}

.custom-dialog :deep(.el-dialog__body) {
    padding: 30px 20px !important;
}

.custom-dialog :deep(.el-dialog__footer) {
    border-top: 2px solid #EBEEF5 !important;
    padding: 20px !important;
}

:deep(.el-dialog) {
    border: 5px solid #409EFF !important;
    border-radius: 8px !important;
}
</style>