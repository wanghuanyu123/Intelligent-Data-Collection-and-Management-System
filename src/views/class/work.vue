<template>
    <el-row class="tac">
        <el-col :span="4" class="sidebar">
            <div class="sidebar-header">
                <el-icon class="header-icon"><School /></el-icon>
                <h5 class="header-title">我的班级</h5>
            </div>
            <el-menu
                active-text-color="#409EFF"
                background-color="#ffffff"
                class="el-menu-vertical"
                default-active="2"
                text-color="#2c3e50"
                @open="handleOpen"
                @close="handleClose"
            >
                <el-menu-item 
                    v-for="(items,index) in myClassList" 
                    :key="items.name" 
                    :index="index"  
                    @click="indexNow(items.name)"
                    class="menu-item"
                >
                    <el-icon><Notebook /></el-icon>
                    <span>{{items.name}}</span>
                </el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span="20" class="main-content">
            <el-tabs v-model="activeName" class="homework-tabs" @tab-click="handleClick">
                <el-tab-pane label="历史作业" name="first">
                    <div v-for="(item,index) in history.homework_list" :key="index" class="homework-card">
                        <div class="homework-header" @click="watchHistroyTest(item)">
                            <div class="homework-title">
                                <span class="title-text">题目: {{item.TestName}}</span>
                                <el-tag size="small" type="success" class="count-tag">
                                    已交 {{item.alreadySubmit}}/{{history.student_count}}
                                </el-tag>
                            </div>
                            <el-button type="primary" @click.stop="download(item)" class="view-btn">
                                <el-icon><View /></el-icon>
                                查看作业
                            </el-button>
                        </div>
                        <div v-if="item.Aiwatch" class="homework-footer">
                            <div class="keywords">
                                <span class="label">关键词：</span>
                                <span class="content">{{item.Important}}</span>
                            </div>
                            <el-tag type="primary" effect="dark" class="ai-tag">AI 智能批改</el-tag>
                        </div>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="作业发布" name="second">
                    <div class="publish-form">
                        <div class="form-item">
                            <div class="form-label">作业内容：</div>
                            <el-input
                                v-model="testName"
                                class="textarea-input"
                                :rows="4"
                                type="textarea"
                                placeholder="请输入作业内容"
                            />
                        </div>
                        <div class="form-item">
                            <div class="form-label">批改关键词：</div>
                            <el-input
                                v-model="important"
                                class="textarea-input"
                                :rows="4"
                                type="textarea"
                                placeholder="请输入批改关键词"
                            />
                        </div>
                        <div class="form-footer">
                            <div class="upload-section">
                                <span class="form-label">作业照片（可选）：</span>
                                <el-upload
                                    class="avatar-uploader"
                                    action="#"
                                    :http-request="upload"
                                >
                                    <img v-if="imageUrl" :src="imageUrl" class="avatar" />
                                    <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                                </el-upload>
                            </div>
                            <div class="ai-switch">
                                <span class="form-label">AI批改:</span>
                                <el-switch
                                    v-model="Aiwatch"
                                    active-color="#13ce66"
                                    inactive-color="#ff4949"
                                />
                            </div>
                            <el-button type="primary" class="submit-btn" @click="submit">发布作业</el-button>
                        </div>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </el-col>
    </el-row>

    <drawView 
        v-if="showEdit" 
        v-model="showEdit" 
        :name="clickTstName" 
        :teacher="teacherId" 
        :class="thisClass" 
        @close="handleclose" 
        @handlePic="handlePic" 
        ref="drawViewRef" 
        @handleWatch="handleWatch"
    />

    <el-dialog
        v-model="dialogVisible"
        fullscreen
        :top="40"
        class="check-dialog"
    >
        <template #header>
            <div class="dialog-title">作业批改</div>
        </template>
        <div class="dialog-content">
            <div v-if="PicInfo.aiask" class="ai-result">
                <div class="result-item">
                    <span class="label">AI批改结果：</span>
                    <span class="content">{{PicInfo.aiask}}</span>
                </div>
                <div class="result-item">
                    <span class="label">AI批改分数：</span>
                    <span class="score">{{PicInfo.award}}</span>
                </div>
            </div>
            
            <div class="teacher-opinion">
                <div class="opinion-header">
                    <span class="title">你的意见（最终标准）</span>
                    <el-button type="primary" @click="agreeAi" v-if="PicInfo.aiask">参考AI</el-button>
                </div>
                <div class="form-item">
                    <div class="form-label">评语：</div>
                    <el-input type="textarea" v-model="teacherAsk" :rows="4" />
                </div>
                <div class="form-item">
                    <div class="form-label">你的评分：</div>
                    <el-input-number v-model="teacherScore" :min="0" :max="100" />
                </div>
            </div>
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="Confirm">确认</el-button>
            </div>
        </template>
    </el-dialog>

    <el-dialog
        v-model="dialogVisible2"
        fullscreen
        :top="40"
        class="view-dialog"
    >
        <template #header>
            <div class="dialog-title">查看批改</div>
        </template>
        <div class="dialog-content">
            <div v-if="WatchInfo.teacherAsk" class="result-item">
                <span class="label">批改结果：</span>
                <span class="content">{{WatchInfo.teacherAsk}}</span>
            </div>
            <div v-if="WatchInfo.teacherScore" class="result-item">
                <span class="label">批改分数：</span>
                <span class="score">{{WatchInfo.teacherScore}}</span>
            </div>
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible2 = false">退出</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import {useRoute} from 'vue-router'
import {getmyclassApi,addhomeworkApi,gethistoryworkListTeacherApi,TeachercheckworkApi} from '@/apis/index'
import router from '@/router'
import {cos} from '@/utils/cos'
import { Plus, School, Notebook, View } from '@element-plus/icons-vue'
import drawView from './components/draw2.vue'
import { ElMessage } from 'element-plus'
const showEdit = ref(false)
const item = ref(null)
item.value = useRoute().params.id

const myClassList = ref([])
const getmyClass = async () => {
    myClassList.value = await getmyclassApi({PersonId:item.value})

    // console.log(myClassList.value[0].name);
}

const activeName = ref('first')//默认
const testName = ref()//作业内容
const important = ref()//批改关键词

// 切换班级
const thisClass = ref(myClassList.value[0]?.name)
const indexNow = (name)=>{
    thisClass.value = name
    getHistory()
    
}
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

const Aiwatch = ref(false)
// 提交作业
const submit = async ()=>{
    await addhomeworkApi({
        PersonId:item.value,
        Class:thisClass.value,
        TestName:testName.value,
        Important:important.value,
        TestUrl:imageUrl.value,
        Aiwatch:Aiwatch.value
    })
    ElMessage({
                message:'提交成功',
                type:'success'
            })
    imageUrl.value = ''
    testName.value = ''
    important.value = ''
    getHistory()
    
}
//历史作业
const history = ref([])
const getHistory = async ()=>{
    history.value = await gethistoryworkListTeacherApi({PersonId:item.value,Class:thisClass.value})
    // console.log(history.value);
    
}

//下载查看作业
const download = (item)=>{
    // console.log(item.TestUrl);
    downloadFile(item.TestUrl)
}
const downloadFile = (urls) => {
  fetch(urls)
    .then(response => response.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "作业";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    })
    .catch(err => console.error(err));
};
const clickTstName = ref()
const teacherId = ref()
const TestName = (name)=>{
    clickTstName.value = name.TestName
    teacherId.value = name.PersonId
}


const watchHistroyTest = (item)=>{
    TestName(item)
    showEdit.value = true
    
}

const handleclose = ()=>{
    showEdit.value = false
    clickTstName.value = ''
    teacherId.value = ''
    
}
//批改作业

const PicInfo = ref({})

const handlePic = (info)=>{
    console.log(info);
    dialogVisible.value = true
    PicInfo.value = info
}

const dialogVisible = ref(false)
const teacherAsk = ref('')
const teacherScore = ref()
const drawViewRef = ref(null)
const agreeAi = ()=>{
    teacherAsk.value = PicInfo.value.aiask
    teacherScore.value = PicInfo.value.award
}
const Confirm = async()=>{
    console.log({
        PersonId:teacherId.value,
        TestName:clickTstName.value,
    });
    const res = await TeachercheckworkApi({
        class:thisClass.value,
        PersonId:teacherId.value,
        TestName:clickTstName.value,
        stuId:PicInfo.value.stuId,
        teacherAsk:teacherAsk.value,
        teacherScore:teacherScore.value
    })
    ElMessage({
                message:'批改成功',
                type:'success'
    })
    console.log(res);
    dialogVisible.value = false
    teacherAsk.value = ''
    teacherScore.value = ''
    getHistory()
    drawViewRef.value.getInfo()
}
//查看批改作业
const WatchInfo = ref({})
const dialogVisible2 = ref(false)

const handleWatch = (info)=>{
    console.log(2);
    dialogVisible2.value = true
    WatchInfo.value = info
}


onMounted(() => {
    getmyClass()
})
</script>

<style scoped>
.tac {
    height: 100vh;
    background-color: #f0f2f5;
    display: flex;
}

.sidebar {
    background: #fff;
    box-shadow: 2px 0 8px rgba(0,0,0,0.06);
    border-radius: 0 24px 24px 0;
    padding: 0;
    position: relative;
    z-index: 1;
}

.sidebar-header {
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, #3498db, #2980b9);
    border-radius: 0 24px 0 0;
}

.header-icon {
    font-size: 24px;
    color: #fff;
}

.header-title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #fff;
    letter-spacing: 1px;
}

.el-menu-vertical {
    border-right: none !important;
    padding: 16px;
}

.menu-item {
    height: 50px !important;
    line-height: 50px !important;
    border-radius: 12px !important;
    margin: 8px 0 !important;
    padding: 0 16px !important;
}

.menu-item:hover {
    background-color: #ecf5ff !important;
    color: #409EFF !important;
}

.menu-item.is-active {
    background-color: #ecf5ff !important;
    color: #409EFF !important;
    font-weight: 600 !important;
}

.menu-item .el-icon {
    font-size: 18px;
    margin-right: 12px;
    color: #909399;
}

.menu-item:hover .el-icon,
.menu-item.is-active .el-icon {
    color: #409EFF;
}

.menu-item span {
    font-size: 15px;
}

.main-content {
    padding: 24px 32px;
    background-color: transparent;
}

.homework-tabs {
    background: #fff;
    border-radius: 8px;
    padding: 24px;
    min-height: calc(100vh - 40px);
}

.homework-card {
    background: #fff;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid #ebeef5;
}

.homework-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.homework-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.homework-title {
    display: flex;
    align-items: center;
    gap: 16px;
}

.title-text {
    font-size: 16px;
    font-weight: 500;
    color: #303133;
}

.count-tag {
    padding: 0 12px;
    height: 24px;
    line-height: 24px;
}

.view-btn {
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.homework-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;
}

.keywords {
    display: flex;
    align-items: center;
    gap: 12px;
}

.keywords .label {
    color: #909399;
}

.keywords .content {
    color: #606266;
}

.publish-form {
    max-width: 800px;
    margin: 0 auto;
    padding: 32px;
    background: #fff;
    border-radius: 8px;
}

.form-item {
    margin-bottom: 32px;
}

.form-label {
    font-size: 15px;
    color: #606266;
    margin-bottom: 12px;
    font-weight: 500;
}

.textarea-input {
    width: 100%;
}

.form-footer {
    display: flex;
    align-items: flex-start;
    gap: 32px;
    margin-top: 40px;
}

.upload-section {
    flex: 1;
}

.avatar-uploader {
    margin-top: 12px;
}

.ai-switch {
    display: flex;
    align-items: center;
    gap: 12px;
}

.submit-btn {
    padding: 12px 24px;
}

.dialog-title {
    font-size: 20px;
    font-weight: 600;
    color: #303133;
}

.dialog-content {
    padding: 40px;
}

.ai-result {
    background: #f8f9fa;
    padding: 24px;
    border-radius: 8px;
    margin-bottom: 32px;
}

.result-item {
    margin-bottom: 16px;
}

.result-item .label {
    color: #909399;
    margin-right: 12px;
}

.result-item .content {
    color: #606266;
}

.result-item .score {
    color: #f56c6c;
    font-weight: 600;
}

.teacher-opinion {
    background: #fff;
    padding: 24px;
    border-radius: 8px;
}

.opinion-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}

.opinion-header .title {
    font-size: 16px;
    font-weight: 500;
    color: #303133;
}

.dialog-footer {
    padding: 16px 40px;
    border-top: 1px solid #ebeef5;
}
</style>