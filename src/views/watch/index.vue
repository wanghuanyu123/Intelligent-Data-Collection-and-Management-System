<script setup>
import { ref ,onMounted} from 'vue'
import {useUserStore} from '@/stores/index'
import {getTaskApi,applyPassApi,fallApi} from '@/apis/index'
import {cos} from '@/utils/cos'
const store = useUserStore()
const taskList = ref([])
const  getTaskList =async ()=>{
    taskList.value = []
    const {data} =  await getTaskApi({PersonId:store.UserInfo.PersonId})
    console.log(data);

    data.forEach(e => {
        
        e.Competition=JSON.parse(e.Competition.replace(/'/g, '"'))
        e.CompetitionAchievement = JSON.parse(e.CompetitionAchievement.replace(/'/g, '"'))
        e.peopleInfoList = JSON.parse(e.peopleInfoList.replace(/'/g, '"'))
        if(e.status==0){
            taskList.value.push(e)
        }
       
    });
    // console.log(data);
    // taskList.value = data
    console.log(taskList.value);
    
} 

onMounted(()=>{
    getTaskList()
})

const success = async (created_at)=>{
    // console.log(created_at);
    await applyPassApi({created_at:created_at})
    ElMessage.success('审核成功')
    getTaskList()
}
const fall = async (created_at)=>{
    console.log(created_at);
    await fallApi({created_at:created_at})
    ElMessage.success('驳回成功')
    getTaskList()
}


const downloadFile = (e,mes,index) => {
  fetch(e)
    .then(response => response.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = mes+"_"+index;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    })
    .catch(err => console.error(err));
};

const downloaddoc = (item)=>{
    item.docunment.forEach((e,index)=>{
        downloadFile(e,"竞赛文档",index)
    })
}

const downloadpaper = (item)=>{
    item.paper.forEach((e,index)=>{
        downloadFile(e,"竞赛论文",index)
    })
}

const downloadahcdoc = (item)=>{
    item.achedoc.forEach((e,index)=>{
        downloadFile(e,"竞赛成果文档",index)
    })
}

</script>

<template>
   <div class="container" v-if="taskList.length>0">
    <el-card style="width: 800px;"  v-for="(item,index) in taskList" :key="index" v-show="taskList"  >
    <template #header>
      <div class="card-header">
        <span style="font-size: 30px">{{item.Competition.description}}</span>
        
      </div>
    </template>
    <div class="contnet">
        <div class="span"><span>介绍：</span><el-input style="width: 800px;" v-model="item.Competition.introduce" type="textarea"></el-input></div>
        
        <div class="span"><span>等级：</span><el-input v-model="item.Competition.level"></el-input></div>
        <div class="span"><span>网址：</span><el-input v-model="item.Competition.webLink"></el-input></div>
        <div class="span" style="font-size: 20px;margin-top: 5px;">竞赛成果</div>
        <div class="span"><span>名称：</span><el-input v-model="item.CompetitionAchievement.description"></el-input></div>
        <div class="span"><span>获得时间：</span><el-input v-model="item.CompetitionAchievement.time"></el-input></div>
        <div class="span"><span>比赛级别：</span><el-input v-model="item.CompetitionAchievement.CompetitionLevel"></el-input></div>
        <div class="span"><span>获奖级别：</span><el-input v-model="item.CompetitionAchievement.CompetitionRank"></el-input></div>
        <div class="span"><span>奖金：</span><el-input v-model="item.CompetitionAchievement.Award"></el-input></div>
        <div style="font-size: 20px;margin-top: 5px;" >参与人员</div>
        <div style="display: flex;flex-wrap: wrap;margin-bottom: 10px;">
            <div v-for="(people,index2) in item.peopleInfoList" :key="index2" style="margin-left: 10px">
            <img  class="img" :src="people.Photo.link" alt="">
            <div><span>姓名：</span><el-input v-model="people.PersonName"></el-input></div>
            <div><span>学号：</span><el-input v-model="people.PersonId"></el-input></div>
            <div><span>身份：</span><el-select v-model="people.PersonRole" >
                <el-option label="学生" value="student" />
                <el-option label="教师" value="teacher" />
                </el-select>   
                </div>
            </div>
        </div>
        <div class="span" style="margin-bottom: 10px"><span>相关图片</span>
        <img :src="item3" alt="" v-for="(item3,index3) in item.photo" :key="index3" style="width: 300px;margin-right: 10px">
        </div>
        <el-button @click="downloaddoc(item)">下载竞赛文档</el-button>
        <el-button @click="downloadpaper(item)">下载竞赛论文</el-button>
        <el-button @click="downloadahcdoc(item)">下载竞赛成果文档</el-button>

    </div>
    <template #footer>
        <el-button @click="success(item.created_at)">通过</el-button>
        <el-button @click="fall(item.created_at)">驳回</el-button>
        
    </template>
  </el-card>
   </div>
   <div v-else style="margin-top: 200px;font-size: larger">
    <span style="margin-left: 400px;">暂无</span>
   </div>
</template>
<style scoped>
.container{
    margin-top: 20px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    
    .contnet{
        .span{
        font-size: 15px;
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        span{
            width: 100px
        }
        }
        .img{
            width: auto;
            height: 100px;
            margin-top: 10px;
            margin-right: 10px;
        }
    }
    
}
</style>