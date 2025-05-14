<template>
    <el-row class="tac">
        <el-col :span="3">
          <h5 class="mb-2">我加入班级</h5>
          <el-menu
            active-text-color="#ffd04b"
            background-color="#545c64"
            class="el-menu-vertical-demo"
            default-active="2"
            text-color="#fff"
            @open="handleOpen"
            @close="handleClose"
          >
            <el-menu-item v-for="(items,index) in myClassList" :key="items.name" :index="index"  @click="indexNow(items.name)">
              <el-icon><icon-menu /></el-icon>
              <span>{{items.name}}</span>
            </el-menu-item>
          </el-menu>
        </el-col>
        <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick" style="width: 1000px;">
            <el-tab-pane label="历史作业" name="first">
                <div v-for="(item,index) in historyworkList" :key="index" class="work">
                 
                    <div class="work-header">
                        <div class="work-title">
                            <span class="title-text">题目: {{item.HomeWork.TestName}}</span>
                            <el-button @click="download(item)" class="view-btn">查看作业</el-button>
                        </div>
                        <div class="status-icon" v-if="item.SubmitWork.flag=='ing'">
                            <i class="iconfont icon-daishenhe"></i>
                        </div>
                        <div class="status-icon" v-if="item.SubmitWork.flag=='true'">
                            <i class="iconfont icon-yitongguo"></i>
                        </div>
                    </div>
                    <div class="work-content">
                        <div class="content-label">作业内容：</div>
                        <el-button type="primary" @click="onclick2(index,item.SubmitWork?.fileList)" class="view-doc-btn">查看我的作业文档</el-button>
                        <div class="remark-section">
                            <span class="remark-label">备注：</span>
                            <el-text class="remark-text" size="large">{{item.SubmitWork?.place}}</el-text>
                        </div>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane label="作业提交" name="third">
                <div v-for="(item,index) in homeworkList" :key="index" class="work">
                    <div class="work-header">
                        <div class="work-title">
                            <span class="title-text">题目: {{item.TestName}}</span>
                            <el-button @click="download(item)" class="view-btn">查看作业</el-button>
                        </div>
                    </div>
                    <div class="work-content">
                        <div class="content-label">作业内容：</div>
                        <el-upload
                            v-model="item.fileList"
                            class="upload-section"
                            action="#"
                            :http-request="upload3"
                            list-type="text"
                        >
                            <el-button type="primary" @click="onclick(index)" class="upload-btn">提交作业文档-(docx,txt,图片)</el-button>
                        </el-upload>
                        <div class="file-list" v-if="item.fileList.length > 0">
                            <span v-for="(item2,index2) in item.fileList" :key="index2" class="file-item">上传{{index2+1}}: {{item2}}</span>
                        </div>
                        <div class="action-buttons">
                            <el-button type="warning" @click="handleRemove(index)" class="clear-btn">清除</el-button>
                        </div>
                        <div class="remark-section">
                            <span class="remark-label">备注：</span>
                            <el-input v-model="item.place" type="textarea" class="remark-input"></el-input>
                        </div>
                        <el-button @click="submit(index)" class="submit-btn">提交</el-button>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </el-row>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import {useRoute} from 'vue-router'
import {getmyclassApi,gethomeworkApi,submitworkApi,gethistoryworkListApi,continueworkApi} from '@/apis/index'
import router from '@/router'
import {cos} from '@/utils/cos'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
const item = ref(null)
item.value = useRoute().params.id

const myClassList = ref([])
const getmyClass = async () => {
    myClassList.value = await getmyclassApi({PersonId:item.value})
    
    // console.log(myClassList.value[0].name);
}

const activeName = ref('first')//默认

// 切换班级
const thisClass = ref(myClassList.value[0]?.name)
const indexNow = (name)=>{
    thisClass.value = name
    getworkList()
    gethistoryworkList()
    // console.log(historyworkList);
    
}
// const imageUrl = ref()

// 提交作业
const submit = async (index)=>{
    console.log(homeworkList.value[index].fileList);
    
    
    if(homeworkList.value[index].fileList.length==0){
        ElMessage({
            message:'请先上传作业文档',
        })
    }
    else{
         // console.log({...homeworkList.value[index],Class:thisClass.value});
    const res = await submitworkApi({...homeworkList.value[index],Class:thisClass.value,stuId:item.value})
    console.log(res.award);
    
    if( res.award<=60 ){
        ElMessageBox.confirm(
        '你提交的作业存在一定问题：'+res.aiask+'ai评分（仅参考）为'+res.award+'，建议修改后提交',
        'Warning',
    {
      confirmButtonText: '继续提交',
      cancelButtonText: '待会再交',
      type: 'warning',
    }
  )
    .then(async () => {
      const res2 = await continueworkApi({...homeworkList.value[index],Class:thisClass.value,stuId:item.value, aiask:res.aiask, award:res.award})
      ElMessage({
        type: 'success',
        message: '提交成功',
      })
      getworkList()
      gethistoryworkList()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Delete canceled',
      })
    })
    }
    
    else{
        ElMessage({
                message:'提交成功',
                type:'success'
            })
        getworkList()
        gethistoryworkList()
    }
    }

}

const handleRemove = (index)=>{
    // const uploadRef = `upload-${index}`;
    // const uploadComponent = uploadRefs.value[uploadRef];
    
    // if (uploadComponent) {
    //     uploadComponent.clearFiles();
    // }
    homeworkList.value[index].fileList = [];
}
const fileList = ref([])

const upload3 = (res)=>{
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
        homeworkList.value[click.value].fileList.push(
          `https://${data.Location}`
        ) 
        console.log('上传作业'+homeworkList.value[click.value].fileList+'图片');
        

      }
    })
  
  
  }
}
const click = ref()
//获取学生作业
const onclick = (index)=>{
    click.value = index
    console.log('第'+click.value+'个作业');
    
}
const homeworkList = ref([])
const getworkList = async ()=>{
    homeworkList.value = await gethomeworkApi({PersonId:item.value,Class:thisClass.value,})
    
    homeworkList.value = homeworkList.value.map(classItem => ({
    ...classItem,
    fileList: [], // 初始化fileList为空数组
    place: "" // 初始化place为空字符串
  }));
  console.log(homeworkList.value);
}
onMounted(() => {
    getmyClass()
    // getworkList()
})


//下载查看作业
const download = (item)=>{
    console.log(item);
    
    console.log(item.TestUrl);
    downloadFile(item.TestUrl)
}
const downloadFile = (urls) => {
  // 从url中获取原始文件名和后缀
  const originalFileName = urls.split('/').pop(); // 获取原始文件名
  const fileExtension = originalFileName.includes('.') ? 
    '.' + originalFileName.split('.').pop() : ''; // 获取文件后缀

  fetch(urls)
    .then(response => response.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      // 添加后缀名到文件名
      a.download = `作业${fileExtension}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    })
    .catch(err => console.error(err));
};

//、、、、、、、、、、、、、、、、、、、、、、、、、、、
//获取历史作业：
const historyworkList = ref([])
const gethistoryworkList = async ()=>{
    historyworkList.value = await gethistoryworkListApi({PersonId:item.value,Class:thisClass.value,})
    // console.log(historyworkList.value);
}

const onclick2 = (index,fileList)=>{
    click.value = index
    for (let index = 0; index < fileList.length; index++) {
        // console.log(fileList[index]);
        downloadFile2(fileList[index],"我的作业",index+1)
    }
} 

const downloadFile2 = (e, mes, index) => {
  // 从url中获取原始文件名和后缀
  const originalFileName = e.split('/').pop(); // 获取原始文件名
  const fileExtension = originalFileName.includes('.') ? 
    '.' + originalFileName.split('.').pop() : ''; // 获取文件后缀

  fetch(e)
    .then(response => response.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      // 在文件名后添加后缀
      a.download = `${mes}_${index}${fileExtension}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    })
    .catch(err => console.error('下载文件出错：', err));
};
</script>

<style scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
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
  width: 100px;
  height: 100px;
  text-align: center;
}
.btn{
    margin-top: 20px;
    margin-left: 40px;
}
.avatar-uploader .avatar {
  width: 100px;
  height: 100px;
  display: block;
}
.work {
  margin: 20px 0;
  padding: 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
}

.work-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
}

.work-title {
  display: flex;
  align-items: center;
  gap: 15px;
}

.title-text {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.status-icon {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.status-icon .iconfont {
  font-size: 48px;
  transition: all 0.3s;
}

.icon-daishenhe {
  color: #e6a23c !important;
}

.icon-yitongguo {
  color: #f56c6c !important;
}

.work-content {
  padding: 15px 0;
}

.content-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
}

.view-btn {
  margin-left: 0;
}

.view-doc-btn {
  margin-bottom: 15px;
}

.upload-section {
  margin: 15px 0;
}

.upload-btn {
  width: 100%;
}

.file-list {
  margin: 10px 0;
}

.file-item {
  display: block;
  font-size: 12px;
  color: #909399;
  margin: 5px 0;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin: 15px 0;
}

.remark-section {
  margin: 15px 0;
}

.remark-label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.remark-text {
  color: #303133;
  font-size: 14px;
}

.remark-input {
  margin-top: 8px;
}

.submit-btn {
  margin-top: 15px;
  width: 100%;
}

/* 响应式布局调整 */
@media screen and (max-width: 768px) {
  .work-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .status-icon {
    position: static;
    transform: none;
    margin-top: 10px;
  }
  
  .work-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .view-btn {
    width: 100%;
  }
}
.iconfont{
    font-family:"iconfont" !important;
    font-size:16px;font-style:normal;
    -webkit-font-smoothing: antialiased;
    -webkit-text-stroke-width: 0.2px;
    -moz-osx-font-smoothing: grayscale;
}
</style>