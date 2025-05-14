<script setup>
import { ref ,onMounted} from 'vue'
import {useUserStore} from '@/stores/index'
import {getStudentSaskApi,addmoreApi} from '@/apis/index'
const store = useUserStore()
const taskList = ref([])
const  getTaskList =async ()=>{
    const {data} =  await getStudentSaskApi({PersonId:store.UserInfo.PersonId})
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

const syp =(index) => change.value.includes(index)


const addmore = async (created_at,index)=>{
    // console.log(created_at);
    await addmoreApi({created_at:created_at,Competition:taskList.value[index].Competition,CompetitionAchievement: taskList.value[index].CompetitionAchievement,peopleInfoList: taskList.value[index].peopleInfoList})
    ElMessage.success('再次申请成功成功')
    console.log(taskList.value[index])
    getTaskList()
}


const change = ref([])
</script>

<template>
   <div class="container">
    <el-card style="width: 800px;" v-for="(item,index) in taskList" :key="index" v-show="taskList">
        <template #header>
            
      <div class="card-header">
        <span style="font-size: 30px">{{item.Competition.description}}</span>
        <div v-if="item.status==0">
            <i class="iconfont icon-daishenhe" style="font-size: 60px;color: red;"></i>
        </div>
        <div v-if="item.status==2">
            <i class="iconfont icon-yitongguo" style="font-size: 60px;color: red;"></i>
        </div>
        

        <el-button @click="change.push(index)" v-if="!syp(index)&&item.status==1">修改</el-button>
        <el-button v-if="syp(index)" @click="change.splice(change.indexOf(index),1)">确定</el-button>
        <div v-if="item.status==1">
            <i class="iconfont icon-beibohui-biaoshi" style="font-size: 60px;color: red;"></i>
        </div>
      </div>
    </template>
    <div class="contnet" v-show="syp(index)">
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
        <div style="display: flex;flex-wrap: wrap">
            <div v-for="(people,index2) in item.peopleInfoList" :key="index2" style="margin-left: 10px">
            <img v-if="people.PersonRole !== 'teacher'" class="img" :src="people.Photo.link" alt="">
            <el-avatar v-else :size="120" :src="'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
            <div><span>姓名：</span><el-input v-model="people.PersonName"></el-input></div>
            <div><span>学号：</span><el-input v-model="people.PersonId"></el-input></div>
            <div><span>身份：</span><el-select v-model="people.PersonRole" >
                <el-option label="学生" value="student" />
                <el-option label="教师" value="teacher" />
                </el-select>   
                </div>
            </div>
        </div>
    </div>

    <div class="contnet" v-show="!syp(index)">
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
            <img v-if="people.PersonRole !== 'teacher'" class="img" :src="people.Photo.link" alt="">
            <el-avatar v-else :size="120" :src="'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
            <div><span>姓名：</span>{{people.PersonName}}</div>
            <div><span>学号：</span>{{people.PersonId}}</div>
            <div><span>身份：</span> {{people.PersonRole=="teacher"? "教师":"学生"}}
                </div>
            </div>
        </div>
    </div>
    <template #footer>
        <el-button v-if="item.status==1" @click="addmore(item.created_at,index)">再次提交</el-button>
    </template>
  </el-card>
   </div>
</template>
<style scoped>
.container {
  margin-top: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

:deep(.el-card) {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: none;
  overflow: hidden;
}

:deep(.el-card:hover) {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

:deep(.el-card__header) {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(to right, #f8f9fa, #ffffff);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  background: linear-gradient(45deg, #409eff, #36cfc9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.contnet {
  padding: 20px;
}

.span {
  font-size: 15px;
  margin-top: 15px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: #606266;
  line-height: 1.6;
}

.span span {
  width: 100px;
  color: #909399;
  font-weight: 500;
}

.img {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.img:hover {
  transform: scale(1.05);
}

.iconfont {
  font-family: "iconfont" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -webkit-text-stroke-width: 0.2px;
  -moz-osx-font-smoothing: grayscale;
}

:deep(.el-button) {
  border-radius: 6px;
  padding: 8px 20px;
  transition: all 0.3s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #409eff inset;
}

:deep(.el-select) {
  width: 100%;
}

:deep(.el-card__footer) {
  padding: 15px 20px;
  border-top: 1px solid #ebeef5;
  background: #f8f9fa;
}

:deep(.el-textarea__inner) {
  min-height: 100px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

:deep(.el-textarea__inner:hover) {
  border-color: #409eff;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

/* 状态图标样式 */
.iconfont {
  font-size: 48px;
  transition: all 0.3s ease;
}

.icon-daishenhe {
  color: #e6a23c !important;
}

.icon-yitongguo {
  color: #67c23a !important;
}

.icon-beibohui-biaoshi {
  color: #f56c6c !important;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  :deep(.el-card) {
    width: 100% !important;
  }
  
  .card-header span {
    font-size: 20px;
  }
  
  .span {
    flex-direction: column;
  }
  
  .span span {
    width: auto;
    margin-bottom: 5px;
  }
}

.teacher-avatar {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  background: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.teacher-avatar:hover {
  transform: scale(1.05);
  background: #e6e8eb;
}

.teacher-icon {
  font-size: 48px;
  color: #909399;
}

:deep(.el-avatar) {
  border: 4px solid #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

:deep(.el-avatar:hover) {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
</style>