<script setup>
import { Plus } from '@element-plus/icons-vue'
import { ref } from 'vue'
import {submitApi} from '@/apis'
import {cos} from '@/utils/cos.js'
import {submitTeacherApi} from '@/apis/index'
import {useUserStore} from '@/stores/index'
const store = useUserStore()
//上传图片
const imageUrl = ref([])

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
        imageUrl.value.push(
          `https://${data.Location}`
        ) 
        // console.log(imageUrl.value);
      }
    })
  }
}
                        
const upload2 = (res)=>{ //照片
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
        console.log(peopleInfoList.value[item.value]);
        peopleInfoList.value[item.value].Photo.link =  `https://${data.Location}`
        // console.log(imageUrl.value);
        // url.Photo.link =  `https://${data.Location}`
        // console.log(imageUrl.value);
      }
    })
  }
}

const upload3 = (res)=>{  //文档
   // console.log(res);
  //  console.log(res);
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
       
        fileList.value.push(
          `https://${data.Location}`
        ) 
        // console.log(imageUrl.value);
      }
    })
  }
}

const upload4 = (res)=>{ //论文
   // console.log(res);
  //  console.log(res);
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
       
        paper.value.push(
          `https://${data.Location}`
        ) 
        // console.log(imageUrl.value);
      }
    })
  }
}

const upload5 = (res)=>{ //成果文档
   // console.log(res);
  //  console.log(res);
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
       
        achedoc.value.push(
          `https://${data.Location}`
        ) 
        // console.log(imageUrl.value);
      }
    })
  }
}

const handleAvatarSuccess = ()=>{
}

const beforeAvatarUpload = ()=>{
}

const handlePictureCardPreview = ()=>{
        
}



// 提交任务
const input = ref('')

const submit = async()=>{

  const {dataList,people_list} =await submitApi({photos:imageUrl.value})
  Competition.value = dataList.Competition
  CompetitionAchievement.value = dataList.CompetitionAchievement
  peopleInfoList.value = people_list
  dialog.value = true
  console.log(dataList);
  console.log(people_list);
}

const Competition = ref({
  description:'',
  introduce:'',
  level:'',
  webLink:'',


})
const CompetitionAchievement = ref({
  CompetitionLevel:'',
  CompetitionRank:'',
  description:'',
  time:'',
  Award:'',
})
const peopleInfoList = ref([])

const CompetitionRules = ref({
  description:[
    {required:true,message:'请输入比赛名称',trigger:'blur'},
  ],
  introduce:[
    {required:true,message:'请输入比赛介绍',trigger:'blur'}
  ],
  level:[
    {required:true,message:'请输入比赛等级',trigger:'blur'}
  ],
  webLink:[
    {required:true,message:'请输入比赛网址',trigger:'blur'}
  ]
})

const CompetitionAchievementRules = ref({
  description:[
    {required:true,message:'请输入比赛名称',trigger:'blur'}
  ],
  CompetitionLevel:[
    {required:true,message:'请输入比赛级别',trigger:'blur'}
  ],
  CompetitionRank:[
    {required:true,message:'请输入比赛排名',trigger:'blur'}
  ],
  time:[
    {required:true,message:'请输入比赛时间',trigger:'blur'}
  ],
  Award:[
    {required:true,message:'请输入奖金',trigger:'blur'}
  ]
})
// const messageHistory = ref([
//   {
//     role:'assistant',
//     content:'Hi，我是 aks助手～很高兴遇见你！你可以上传图片并发布任务'
//   },
  
// ])

const dialog = ref(false)
const ClubName = ref('')
const submitForm = async ()=>{
  await submitTeacherApi({
    Competition:Competition.value,
    CompetitionAchievement:CompetitionAchievement.value,
    peopleInfoList:peopleInfoList.value,
    PersonId:store.UserInfo.PersonId,
    photo:imageUrl.value,
    paper:paper.value,  //文论
    fileList:fileList.value,   //文档
    achedoc:achedoc.value,   //成果文档
    ClubName:ClubName.value,//俱乐部名称

  })
  ElMessage({
    message: '提交成功',
    type: 'success',
  })
  dialog.value = false
}

const addteacher = ()=>{
  peopleInfoList.value.push({
    PersonName:'',
    PersonRole:'teacher',
    Photo:{
      link:''
    }
  })
  dialog.value = true
}

const addstudent = ()=>{
  peopleInfoList.value.push({
    PersonId:'',
    PersonName:'',
    PersonRole:'student',
    Photo:{
      link:''
    }
  })
  dialog.value = true
}

const item = ref()

const ct = (index) =>{
  item.value  = index
}

const deletepeople = (index)=>{
   peopleInfoList.value.splice(index,1)
}

const fileList = ref([])   //文档
const paper = ref([])   //论文
const achedoc = ref([])

const handleRemove = (file, uploadFiles)=>{
  console.log(file, uploadFiles)
  fileList.value = uploadFiles
}

const handleRemove2 = (file, uploadFiles)=>{
  console.log(file, uploadFiles)
  paper.value = uploadFiles
}

const handleRemove3 = (file, uploadFiles)=>{
  console.log(file, uploadFiles)
  achedoc.value = uploadFiles
}

</script>

<template>
  <div class="containner">
    <div class="upload">
      <!-- 照片墙 -->
      <ul class="img" >
        <li v-for="(item,index) in imageUrl" :key="item" >
          <el-image :preview-src-list="imageUrl" class="img-item" :initial-index="index" style="width: 150px;height: 150px;margin-left: 10px;" :src="item" />
        </li>
        <!-- 上传 -->
        <el-upload
        class="avatar-uploader"
        action="#"
        list-type="picture-card"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"  
        :http-request="upload"
        :on-preview="handlePictureCardPreview"
        >
        <el-icon class="icon"><Plus /></el-icon>
        </el-upload>
      </ul>
    </div>

    <div class="submit">
      <!-- <div class="dialog" >
        <div class="content-list" v-for="(item,index) in messageHistory" :key="index">
            <div v-if="item.role=='assistant'" class="role">
              <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"/>
              <div class="role-content">{{item.content}}</div>
            </div>
            <div v-else class="user">
              <div class="user-content">{{item.content}}</div>
              <el-avatar src=""/>
            </div>
        </div>
      </div> -->
      <!-- <el-input class="inp" v-model="input" type="textarea"  autosize>
      </el-input>
       -->
      <el-button class="btn" type="primary" @click="submit">提交照片</el-button>
    </div>
    <div style="display: flex;">
      <el-button @click="addteacher">添加指导老师</el-button>
      <el-button @click="addstudent">添加人员</el-button>
    </div>
    <div class="form" >
      <div>
        <span class="span">俱乐部名称:</span>
        <el-input v-model="ClubName" style="width: 600px;" placeholder="请输入俱乐部名称"></el-input>
        <span class="span">竞赛信息:</span>
        <el-form :model="Competition" :rules="CompetitionRules" style="width: 600px;">
          <el-form-item prop="description" label="比赛名称">
              <el-input v-model="Competition.description"></el-input>
          </el-form-item>
          <el-form-item prop="introduce" label="比赛介绍">
              <el-input v-model="Competition.introduce"></el-input>
          </el-form-item>
          <el-form-item prop="level" label="比赛等级">
              <el-input v-model="Competition.level"></el-input>
          </el-form-item>
          <el-form-item prop="webLink" label="比赛网址">
              <el-input v-model="Competition.webLink"></el-input>
          </el-form-item>
          <el-upload
            v-model="fileList"
            class="avatar-uploader"
            action="#"
            :http-request="upload3"
            :on-remove="handleRemove"
          >
          <el-button type="primary">提交文档</el-button>
          <template #tip>
            <div class="el-upload__tip">
              files with a size less than 500KB.
            </div>
          </template>
        </el-upload>
        <el-upload
            v-model="fileList"
            class="avatar-uploader"
            action="#"
            :http-request="upload4"
            :on-remove="handleRemove2"
        >
          <el-button type="primary">提交论文</el-button>
          <template #tip>
            <div class="el-upload__tip">
              files with a size less than 500KB.
            </div>
          </template>
        </el-upload>
        </el-form>

        <span class="span">竞赛成果信息:</span>
        <el-form :model="CompetitionAchievement" :rules="CompetitionAchievementRules" style="width: 600px;">
          <el-form-item prop="description" label="比赛名称">
              <el-input v-model="CompetitionAchievement.description"></el-input>
          </el-form-item>
          <el-form-item prop="CompetitionLevel" label="比赛级别">
              <el-input v-model="CompetitionAchievement.CompetitionLevel"></el-input>
          </el-form-item>
          <el-form-item prop="CompetitionRank" label="比赛排名">
              <el-input v-model="CompetitionAchievement.CompetitionRank"></el-input>
          </el-form-item>
          <el-form-item prop="Award" label="比赛奖金">
              <el-input v-model="CompetitionAchievement.Award"></el-input>
          </el-form-item>
          <el-form-item prop="time" label="比赛时间">
              <el-input v-model="CompetitionAchievement.time"></el-input>
          </el-form-item>
          <el-upload
            v-model="fileList"
            class="avatar-uploader"
            action="#"
            :http-request="upload5"
            :on-remove="handleRemove3"
        >
          <el-button type="primary">提交文档</el-button>
          <template #tip>
            <div class="el-upload__tip">
              files with a size less than 500KB.
            </div>
          </template>
        </el-upload>
        </el-form>

        <span class="span">附件:</span>
        
      
       


        <div  v-show="dialog">
          <span class="span">指导老师: </span>
        <div v-for="(item,index) in peopleInfoList" :key="index" >
          
          <div v-show="item.PersonRole==='teacher'">
            <el-button type="danger" style="margin-left: 600px;" @click="deletepeople(index)">删除</el-button>
            <el-upload
            class="avatar-uploader"
            action="#"
            :http-request="upload2"
            @click="ct(index)"
            >
            <img v-if="item.Photo?.link" :src="item.Photo?.link" class="avatar" />
            <el-icon style="border: 1px solid gray;" v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <el-form :model="item">
            <el-form-item label="姓名">
              <el-input v-model="item.PersonName"></el-input>
            </el-form-item>
          </el-form>
          <el-form :model="item">
            <el-form-item label="学号">
              <el-input v-model="item.PersonId"></el-input>
            </el-form-item>
          </el-form>
          </div>
        </div>

        <span class="span">人员:</span>
        <div v-for="(item,index) in peopleInfoList" :key="index" >
          
          <div v-show="item.PersonRole==='student'">
            <el-button type="danger" style="margin-left: 600px;" @click="deletepeople(index)">删除</el-button>
            <el-upload
            class="avatar-uploader"
            action="#"
            :http-request="upload2"
            @click="ct(index)"
            >
            <img v-if="item.Photo?.link" :src="item.Photo?.link" class="avatar" />
            <el-icon style="border: 1px solid gray;" v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>


          <el-form :model="item">
            <el-form-item label="姓名">
              <el-input v-model="item.PersonName"></el-input>
            </el-form-item>
            <el-form-item label="学号">
              <el-input v-model="item.PersonId"></el-input>
            </el-form-item>
            <el-form-item label="身份">
              <el-select v-model="item.PersonRole" >
                <el-option label="学生" value="student" />
                <el-option label="教师" value="teacher" />
              </el-select>
            </el-form-item>
          </el-form>
          </div>
        </div>
        </div>
        
        
      </div>
    </div>

    <el-button v-if="dialog" @click="submitForm" style="width: 200px;">提交</el-button>
  </div>
</template>


<style scoped>
.containner{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  .upload{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    align-items: center;
    width: 840px;
    border: 1px solid gray;
    padding: 10px;
    .img{
      list-style-type: none;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      padding: 0px;
    }

    .avatar-uploader{
      width: 150px;
      height: 150px;
      margin-left: 10px;
      
    }
  }
  .submit{
    margin-top: 10px;
    width: 900px;
    .dialog{
      margin-top: 5px;
      width: 100%;
      height: 450px;
      overflow-y: scroll;
      .content-list{
        margin-top: 5px;
        .role{
        display: flex;
        justify-content: flex-start;
        .role-content{
          border: 1px solid gray;
          border-radius: 10px;
          padding: 10px;
          margin-right: 10px;
          margin-left: 5px;
          max-width: 92%;
        }
      }
      .user{
        display: flex;
        justify-content: flex-end;
        .user-content{
          border: 1px solid gray;
          border-radius: 10px;
          padding: 10px;
          margin-left: 10px;
          margin-right: 5px;
          max-width: 92%
        }
      }
      }
    }
   
    .btn{
      margin-left: 800px;
    }
  }
  .form{
    align-self: flex-start;
  }
 
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
.demo-image__error .image-slot {
  font-size: 30px;
}
.demo-image__error .image-slot .el-icon {
  font-size: 30px;
}
.demo-image__error .el-image {
  width: 100%;
  height: 200px;
}
.span{
  display: block;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}

</style>
