<script setup>
import {ref,onMounted} from 'vue'
import {getPersonInfoApi} from '@/apis/index'
import {useUserStore} from '@/stores/index'
import {changePasswordApi} from '@/apis/index'
const store = useUserStore()
const PersonId = store.UserInfo.PersonId
const PersonInfo = ref({})
const photoList = ref([])
onMounted(()=>{
    getPersonInfo()
})

const onlypass = ref('')
const getPersonInfo =async ()=>{
   const {person,photos} = await getPersonInfoApi({PersonId:PersonId})
   PersonInfo.value = person
   photoList.value = photos
   console.log(photoList.value);
   onlypass.value =  hidden(PersonInfo.value.password,2,1)
}
let show = ref(false)
let newpass = ref('')
const changePass =async ()=>{
    await changePasswordApi({PersonId:PersonId,newpass:newpass.value})
    ElMessage({
                message:'修改成功',
                type:'success'
            })
    newpass.value = ''
    getPersonInfo()
}
const hidden = (str, frontLen, endLen)=> {
  //str：要进行隐藏的变量  frontLen: 前面需要保留几位    endLen: 后面需要保留几位
  var len = str.length - frontLen - endLen;
  var xing = "";
  for (var i = 0; i < len; i++) {
    xing += "*";
  }
  return (
    str.substring(0, frontLen) + xing + str.substring(str.length - endLen)
  );
}
</script>

<template>
    <div class="info-container">
        <div class="info-card">
            <div class="info-header">
                <h2>个人信息</h2>
                <el-button type="primary" @click="show = !show" class="change-pwd-btn">
                    {{ show ? '取消修改' : '修改密码' }}
                </el-button>
            </div>

            <div class="password-change-section" v-show="show">
                <el-input 
                    v-model="newpass" 
                    placeholder="请输入新密码" 
                    type="password"
                    class="password-input"
                ></el-input>
                <el-button type="success" @click="changePass" class="confirm-btn">确认修改</el-button>
            </div>

            <div class="info-content">
                <div class="info-item">
                    <span class="label">人员名称</span>
                    <span class="value">{{PersonInfo.PersonName}}</span>
                </div>
                <div class="info-item">
                    <span class="label">人员学号</span>
                    <span class="value">{{PersonInfo.PersonId}}</span>
                </div>
                <div class="info-item">
                    <span class="label">人员身份</span>
                    <span class="value">{{PersonInfo.PersonRole}}</span>
                </div>
                <div class="info-item">
                    <span class="label">密码</span>
                    <span class="value">{{onlypass}}</span>
                </div>
            </div>

            <div class="photo-section">
                <h3>个人照片</h3>
                <div class="photo-grid">
                    <div v-for="(item,index) in photoList" 
                         :key="index" 
                         class="photo-item">
                        <img :src="item.link" alt="个人照片">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.info-container {
    padding: 20px;
    min-height: 100vh;
    background-color: #f5f7fa;
}

.info-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 24px;
    max-width: 800px;
    margin: 0 auto;
}

.info-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #ebeef5;
}

.info-header h2 {
    margin: 0;
    color: #303133;
    font-size: 24px;
}

.password-change-section {
    background: #f5f7fa;
    padding: 16px;
    border-radius: 4px;
    margin-bottom: 24px;
}

.password-input {
    width: 300px;
    margin-right: 16px;
}

.info-content {
    margin-bottom: 32px;
}

.info-item {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 12px;
    background: #f5f7fa;
    border-radius: 4px;
}

.label {
    width: 100px;
    color: #606266;
    font-weight: 500;
}

.value {
    color: #303133;
    flex: 1;
}

.photo-section {
    margin-top: 32px;
}

.photo-section h3 {
    color: #303133;
    margin-bottom: 16px;
}

.photo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 16px;
}

.photo-item {
    aspect-ratio: 1;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.photo-item:hover {
    transform: scale(1.05);
}

.photo-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.change-pwd-btn {
    padding: 8px 20px;
}

.confirm-btn {
    margin-left: 16px;
}
</style>