<script setup>
import { Plus } from '@element-plus/icons-vue'
import {ref,onMounted} from 'vue'
import {cos} from '@/utils/cos'
import {addFaceApi} from '@/apis/index'
import {useUserStore} from '@/stores/index'
const store = useUserStore()
const imageUrl = ref()


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

const ruleForm = ref(null)

const formData = ref({
    type:'',
    description:'',
})
const rules = ref({
    type:[
        {required:true,message:'请选择上传图片的类别',trigger:'blur'}
    ],
    description:[
        {required:true,message:'请输入描述',trigger:'blur'}
    ],
   
  
})


const addface = async ()=>{
    const data = {
        PersonId:store.UserInfo.PersonId,
        PhotoId:store.UserInfo.PersonId+imageUrl.value,
        link:imageUrl.value,
        description:formData.value.description,
        type:formData.value.type,
    }
    ruleForm.value.validate(async (valid)=>{
        if(valid){
            await addFaceApi(data)
            ElMessage({
                message:'录入成功',
                type:'success'
            })
            imageUrl.value = ''
            ruleForm.value.resetFields()
        }
    })

}

</script>

<template>
    <el-form :model="formData" :rules="rules"  class="demo-ruleForm" ref="ruleForm">
        <el-upload
            class="avatar-uploader"
            action="#"
            :http-request="upload"
            >
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
        <el-form-item prop="type" label="图片类别">
            <el-select  v-model="formData.type" placeholder="请选择上传图片的类别">
                <el-option label="证明文件" value="provefile" />
                <el-option label="证书" value="prove" />
                <el-option label="普通照片" value="normal" />
            </el-select>
        </el-form-item>
       
        <el-form-item prop="description" label="图片描述">
            <el-input v-model="formData.description" placeholder="请输入描述" />
        </el-form-item>
        <el-button class="btn" @click="addface">录入人脸</el-button>
    </el-form>
</template>

<style  scoped>

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
.btn{
    margin-top: 20px;
    margin-left: 40px;
}
</style>

