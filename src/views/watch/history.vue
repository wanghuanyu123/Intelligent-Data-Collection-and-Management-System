<template>
    <div class="container" v-if="taskList.length>0">


<el-card style="width: 800px;" v-for="(item,index) in taskList" :key="index" v-show="taskList">
    <template #header>
      <div class="card-header">
        <span style="font-size: 30px">{{item.Competition.description}}</span>
        
      </div>
    </template>
    <div class="contnet" >
        <div class="span"><span>介绍：</span>{{item.Competition.introduce}}</div>
        <div class="span"><span>等级：</span>{{item.Competition.level}}</div>
        <div class="span"><span>网址：</span>{{item.Competition.webLink}}</div>
        <div class="span" style="font-size: 20px;margin-top: 5px;">竞赛成果</div>
        <div class="span"><span>名称：</span>{{item.CompetitionAchievement.description}}</div>
        <div class="span"><span>获得时间：</span>{{item.CompetitionAchievement.time}}</div>
        <div class="span"><span>比赛级别：</span>{{item.CompetitionAchievement.CompetitionLevel}}</div>
        <div class="span"><span>获奖级别：</span>{{item.CompetitionAchievement.CompetitionRank}}</div>
        <div class="span"><span>奖金：</span>{{item.CompetitionAchievement.Award}}</div>
        <div style="font-size: 20px;margin-top: 5px;" >参与人员</div>
        <div style="display: flex;flex-wrap: wrap">
            <div v-for="(people,index2) in item.peopleInfoList" :key="index2" style="margin-left: 10px">
            <img  class="img" :src="people.Photo.link" alt="">
            <div><span>姓名：</span>{{people.PersonName}}</div>
            <div><span>学号：</span>{{people.PersonId}}</div>
            <div><span>身份：</span> {{people.PersonRole=="teacher"? "教师":"学生"}}
                </div>
            </div>
        </div>
    </div>
    
  </el-card>
</div>
</template>

<script setup>
import { ref ,onMounted} from 'vue'
import {useUserStore} from '@/stores/index'
import { getTeacherTask } from '@/apis/index'
const store = useUserStore()
const taskList = ref([])

const  getTaskList =async ()=>{
    const {data} =  await getTeacherTask({PersonId:store.UserInfo.PersonId})
    console.log(data);

    data.forEach(e => {
        e.Competition=JSON.parse(e.Competition.replace(/'/g, '"'))
        e.CompetitionAchievement = JSON.parse(e.CompetitionAchievement.replace(/'/g, '"'))
        e.peopleInfoList = JSON.parse(e.peopleInfoList.replace(/'/g, '"'))
       
    });
    console.log(data);
    taskList.value = data
    taskList.value = taskList.value.reverse();
} 

onMounted(()=>{
    getTaskList()
})

</script>

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