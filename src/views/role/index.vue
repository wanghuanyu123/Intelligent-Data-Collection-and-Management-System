<script setup>
import { Plus } from '@element-plus/icons-vue'
import {ref,onMounted} from 'vue'
import {cos} from '@/utils/cos'
import {addroleApi,getroleListApi,deleteroleApi} from '@/apis/index.js'
const imageUrl = ref()
const formData = ref({
    PersonName:'',
    PersonId:'',
    Gender:null,

})

const rules = ref({
    PersonName:[{required:true,message:'请输入姓名',trigger:'blur'}],
    PersonId:[{required:true,message:'请输入工号',trigger:'blur'}],
    Gender:[{required:true,message:'请选择性别',trigger:'change'}],
})

const formRef = ref(null)
const upload = (res)=>{
  // console.log(res);
  if (res.file) {
    // 执行上传操作
    cos.putObject({
      Bucket: 'reniantupian-1325679727', /* 存储桶 */
      Region: 'ap-nanjing', /* 存储桶所在地域，必须字段 */
      Key: res.file.name, /* 文件名 */
      StorageClass: 'STANDARD', // 上传模式, 标准模式
      Body: res.file, // 上传文件对象
      onProgress: (progressData) => { // 上传进度
        console.log(JSON.stringify(progressData))
      }
    }, (err, data) => {
      // console.log(err || data)
      // 上传成功之后
      if (data.statusCode === 200) {
        imageUrl.value=`https://${data.Location}`
        // console.log(imageUrl.value);
      }
    })
  }
}

//添加成员
const addrole =  ()=>{
    //   console.log(name.value,imageUrl.value);
    const data = {
        PersonName:formData.value.PersonName,
        PersonId:formData.value.PersonId,
        Gender:parseInt(formData.value.Gender),
        Url:imageUrl.value
    }
    formRef.value.validate(async (valid) => {
    if (valid) {
      await addroleApi(data)
        ElMessage({
        message: '添加成功',
        type: 'success',
        })
        formRef.value.resetFields()
        imageUrl.value = ''
        getRoleList()
    } 
  })
}

// 表格
const tableData = ref([])

const getRoleList = async ()=>{
    const res = await getroleListApi()
    tableData.value = res.data
}

onMounted(()=>{
    getRoleList()
})

// 修改人员信息

//删除人员

const delrole = async(row)=>{
  await deleteroleApi({PersonId:row.PersonId})
  ElMessage({
        message: '删除成功',
        type: 'success',
        })
  getRoleList()
}
</script>

<template>
    <div class="header">
    <el-form ref="formRef"  :model="formData" :rules="rules">
        <el-form-item prop="PersonName">
            <el-input v-model="formData.PersonName" style="width: 400px;" placeholder="请输入人员姓名"></el-input>
        </el-form-item>
        <el-form-item prop="PersonId">
            <el-input v-model="formData.PersonId" style="width: 400px;" placeholder="请输入人员学号"></el-input>
        </el-form-item>
        <el-form-item prop="Gender">
            <el-select v-model="formData.Gender" placeholder="请选择性别">
                <el-option label="男" value=1 />
                <el-option label="女" value=0 />
            </el-select>
        </el-form-item>
        <el-form-item>
            <el-upload
            class="avatar-uploader"
            action="#"
            :http-request="upload"
            >
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="addrole">
                添加成员
            </el-button>
        </el-form-item>
    </el-form>
    </div>
<!-- 表格区域 -->
    <div class="content">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="PersonName" label="姓名" />
          <el-table-column prop="PersonId" label="学号" />
          <el-table-column prop="Gender" label="性别" />
          <el-table-column prop="Url" label="头像"
>
            <template #default="{row}">
                <img :src="row.Url" alt="" style="width: 50px;height: 50px;">
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template v-slot="{row}">
                <el-button type="primary" size="small" >添加人脸</el-button>
                <el-button type="danger" size="small" @click="delrole(row)">删除</el-button>
            </template>

          </el-table-column>

        </el-table>
    </div>
</template>


<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>