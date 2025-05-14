<script  setup>
import { ref ,defineModel,defineProps,onMounted,defineEmits,defineExpose} from 'vue'
import {TeachergethistoryworkApi} from '@/apis/index'

const prop = defineProps(['name','teacher','class'])
const showEdit = defineModel('showEdit',false)
const emit = defineEmits(['close','handlePic','handleWatch'])
const info = ref([])
const getInfo = async ()=>{
    info.value = await TeachergethistoryworkApi({
    PersonId: prop.teacher,
    Class: prop.class,
    TestName:prop.name
  })
  console.log(info.value);
  
}
defineExpose({
  getInfo
});
const handleClose = () => {
  emit('close')
}

//下载查看作业
const download = (item,index)=>{
    console.log(item.fileList);
        
    downloadFile(item.fileList,index)
}
const downloadFile = (urls, index) => {
  for (let i = 0; i < urls.length; i++) {
    fetch(urls[i])
      .then(response => response.blob())
      .then(blob => {
        // 从url中获取文件名和后缀
        const originalFileName = urls[i].split('/').pop(); // 获取原始文件名
        const fileExtension = originalFileName.includes('.') ? 
          '.' + originalFileName.split('.').pop() : ''; // 获取文件后缀
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        // 在文件名后添加后缀
        a.download = `${info.value[index].PersonInfo.PersonName}的作业_${i+1}${fileExtension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      })
      .catch(err => console.error('下载文件出错：', err));
  }
};


const handlePic = (index)=>{
    emit('handlePic',info.value[index])
    // emit('close')
}
const handleWatch = (index)=>{
    emit('handleWatch',info.value[index])
}
onMounted(()=>{
  getInfo()
  
})
</script>

<template>
    <el-drawer v-model="showEdit" title="提交历史" size="35%" :before-close="handleClose"> 
    <div v-if="info.length>0">
        <div v-for="(item,index) in info" :key="index" class="work">
        <div style="display:flex ;align-items: center; position: relative;">
            学生：{{item.PersonInfo.PersonName}} <br>
            <el-button @click="download(item,index)" style="margin-left: 20px;"> 查看作业</el-button>
            <el-button @click="handlePic(index)" v-if="item.flag=='ing'">去批改</el-button>
            <el-button v-if="item.flag=='true'" style="color: green;" @click="handleWatch(index)">查看批改</el-button>
            <span v-if="item.flag=='ing'" style="color: red;position: absolute;right: 5%; " >待批改</span>
            
        </div>
        <div v-if="item.aiAsk">ai评价：</div> 
    </div>
    </div>
    <div v-else>
        <span>暂无</span>
    </div>
    </el-drawer>
    
</template>
<style scoped>
.description{
  
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}
.work{
    width:400px;
    margin-top: 20px;
    margin-left: 40px;
    margin-right: 40px;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}
</style>

  