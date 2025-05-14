<script setup>
import {ref} from 'vue'
import StudentLogin from './componens/StudentLogin.vue'
import clubadd from './componens/Clubadd.vue'
import {useUserStore} from '@/stores/index'
import router from '@/router';
const store = useUserStore()
// 学生登录

const stuDialog = ref(false)

const showStudenDialog = ()=>{
    stuDialog.value = true
}

const clubDialog = ref(false) 
const showClubDialog
 = ()=>{
    clubDialog.value = true
}
//退出登录

const loginOut = ()=>{
    ElMessageBox.confirm('确定退出登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        store.removeUserInfo()
        ElMessage({
            type: 'success',
            message: '退出登录成功!'
        })
        router.push('/home')

    })
}
const openPage = ()=>{
    window.open('http://localhost:5173/upload')
}

const openPage2 = ()=>{
    window.open('http://localhost:5173/watch')
}

const openPage3 = ()=>{
    window.open('http://localhost:5173/addmember')
}

const openpage4 = ()=>{
    window.open('http://localhost:5173/show')
}

const openpage1 = ()=>{
    router.push('/home')
}

const openpage5 = ()=>{
    window.open('http://localhost:5173/class')
}

const openpage6 = ()=>{
    window.open(`http://localhost:5173/work/${store.UserInfo.PersonId}`)

}

const openpage7 = ()=>{
    window.open(`http://localhost:5173/mywork/${store.UserInfo.PersonId}`)
}

// 最新新闻数据
const newsList = ref([
{
        title: '人工智能在医疗领域的突破',
        summary: '最近，人工智能在医疗诊断方面取得了重大突破，能够更准确地识别疾病。这项技术有望在未来几年内广泛应用于医院和诊所，提高诊断效率和准确性。',
        date: '2023-10-10',
        source: '科技日报',
        author: '张三',
        comments: 42,
        tags: ['人工智能', '医疗', '科技'],
        url: 'https://example.com/news1'
      },
      {
        title: '在线教育的未来发展趋势',
        summary: '随着互联网技术的不断发展，在线教育市场呈现出快速增长的趋势。越来越多的学生选择通过在线平台学习新知识，这种学习方式不仅灵活方便，还能提供个性化的学习体验。',
        date: '2023-10-11',
        source: '教育时报',
        author: '李四',
        comments: 35,
        tags: ['在线教育', '互联网', '学习'],
        url: 'https://example.com/news2'
      },
      {
        title: '新能源汽车的崛起',
        summary: '新能源汽车市场在近年来呈现出爆发式增长，各大汽车制造商纷纷加大在电动汽车领域的投入。新技术的不断涌现，使得新能源汽车的续航里程和性能不断提升，逐渐成为市场主流。',
        date: '2023-10-12',
        source: '汽车周刊',
        author: '王五',
        comments: 58,
        tags: ['新能源汽车', '电动汽车', '市场'],
        url: 'https://example.com/news3'
      },
      {
        title: '5G技术的广泛应用',
        summary: '5G技术的普及为物联网、智能城市和自动驾驶等领域带来了巨大的变革。其高速率、低延迟的特点，使得这些领域的应用更加稳定和高效，推动了相关产业的快速发展。',
        date: '2023-10-13',
        source: '通信世界',
        author: '赵六',
        comments: 67,
        tags: ['5G', '物联网', '智能城市'],
        url: 'https://example.com/news4'
      },
      {
        title: '可持续发展的挑战与机遇',
        summary: '在全球气候变化的背景下，可持续发展成为各国面临的共同挑战。各国政府和企业纷纷采取措施，推动绿色经济转型，探索可持续发展的新路径。',
        date: '2023-10-14',
        source: '环境与可持续发展',
        author: '钱七',
        comments: 45,
        tags: ['可持续发展', '气候变化', '绿色经济'],
        url: 'https://example.com/news5'
      },
      {
        title: '虚拟现实技术的未来',
        summary: '虚拟现实（VR）技术在娱乐、教育和培训等领域的应用逐渐普及。随着技术的不断进步，VR设备的性能和用户体验不断提升，为未来的发展带来了更多可能性。',
        date: '2023-10-15',
        source: '科技前沿',
        author: '孙八',
        comments: 32,
        tags: ['虚拟现实', 'VR', '娱乐'],
        url: 'https://example.com/news6'
      },
      {
        title: '区块链技术的应用前景',
        summary: '区块链技术在金融、供应链管理和数字身份认证等领域的应用逐渐成熟。其去中心化、不可篡改的特点，为解决信任问题提供了新的思路。',
        date: '2023-10-16',
        source: '金融科技',
        author: '周九',
        comments: 78,
        tags: ['区块链', '金融', '供应链'],
        url: 'https://example.com/news7'
      },
      {
        title: '量子计算的突破',
        summary: '量子计算技术在近年来取得了显著进展，其强大的计算能力为解决复杂问题提供了新的方法。科学家们正在探索量子计算在密码学、材料科学和人工智能等领域的应用。',
        date: '2023-10-17',
        source: '科学探索',
        author: '吴十',
        comments: 56,
        tags: ['量子计算', '密码学', '材料科学'],
        url: 'https://example.com/news8'
      },
      {
        title: '太空探索的新进展',
        summary: '太空探索领域在近年来取得了多项重要进展，包括火星探测、太空旅游和卫星通信等。这些进展不仅推动了科学技术的发展，也为人类未来的太空移民提供了更多可能性。',
        date: '2023-10-18',
        source: '太空探索',
        author: '郑十一',
        comments: 48,
        tags: ['太空探索', '火星探测', '太空旅游'],
        url: 'https://example.com/news9'
      },
      {
        title: '生物技术的创新',
        summary: '生物技术在基因编辑、细胞治疗和生物制药等领域的创新不断涌现。这些技术的发展为治疗疑难杂症和提高人类健康水平带来了新的希望。',
        date: '2023-10-19',
        source: '生物技术杂志',
        author: '王十二',
        comments: 63,
        tags: ['生物技术', '基因编辑', '细胞治疗'],
        url: 'https://example.com/news10'
      }
]);

// 留言板数据
const messageList = ref([
  
  // 更多留言...
]);
const newMessage = ref('');

const submitMessage = () => {
  // 提交留言的逻辑
  messageList.value.push({ content: newMessage.value, author: store.UserInfo.PersonName, date: new Date() });
  newMessage.value = ''; // 清空输入
};

const scrollToSection = (sectionId) => {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }

</script>

<template>
    <div class="container">
        <div class="logo">
            <img src="/src/assets/img/logo.png" alt="" class="img">
            <span class="span">福州大学至诚学院</span>
        </div>
        <div class="nav">
            <el-menu
            :default-active="1"
            class="el-menu-demo"
            mode="horizontal"
        >
            <el-menu-item index="1" @click="openpage1">首页</el-menu-item>
            <el-menu-item index="2" @click="scrollToSection('latest-news')">新闻资讯</el-menu-item>
            <el-menu-item index="3" @click="scrollToSection('message-board')">留言板</el-menu-item>
            <el-menu-item index="4" @click="openpage4">作品展示</el-menu-item>
            <el-menu-item index="5" @click="showStudenDialog" v-if="!store.UserInfo.PersonId">登录</el-menu-item>
            <el-menu-item index="6" @click="openPage " v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='student'">发布作品</el-menu-item>
            <el-menu-item index="7" @click="openPage2 " v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='teacher'">审核作品</el-menu-item>
            <el-menu-item index="8"  @click="showClubDialog" v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='manager'">添加俱乐部</el-menu-item>
            <el-menu-item index="9"  @click="openPage3" v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='teacher'||store.UserInfo.PersonRole=='manager'">查看俱乐部</el-menu-item>
            <el-menu-item index="10"  @click="openpage5" v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='manager'">班级管理</el-menu-item>
            <el-menu-item index="11"  @click="openpage6" v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='teacher'">作业管理</el-menu-item>
            <el-menu-item index="12"  @click="openpage7" v-if="store.UserInfo.PersonId&&store.UserInfo.PersonRole==='student'">提交作业</el-menu-item>
            <span class="span" v-if="store.UserInfo.PersonId"> 欢迎您：{{store.UserInfo.PersonName}}</span> <span class="span2" v-if="store.UserInfo.PersonRole==='student'">同学</span>  <span class="span2" v-if="store.UserInfo.PersonRole==='teacher'">老师</span>
            <span class="span2" v-if="store.UserInfo.PersonRole==='manager'">管理员</span>
            
            <el-menu-item index="13" style="margin-left: 100px" @click="loginOut" v-if="store.UserInfo.PersonId">退出登录</el-menu-item>
        </el-menu>
        </div>
        <div class="carousel">
            <el-carousel >
                <el-carousel-item v-for="item in 2" :key="item">
                    <img src="../assets/img/轮播1.jpg" alt="">
                    <!-- <h3 class="small justify-center" text="2xl">{{ item }}</h3> -->
                </el-carousel-item>
            </el-carousel>    
        </div>                                                              
        
        <!-- 学生登录弹窗 -->       
        <StudentLogin :stuDialog="stuDialog" @closeDialog="stuDialog = false"></StudentLogin>

        <clubadd :clubDialog="clubDialog" @closeDialog="clubDialog = false"></clubadd>
        <!-- <el-dialog v-model="stuDialog"></el-dialog> -->
        <!-- <router-view></router-view> -->


    
    
    
    <div class="latest-news" id="latest-news">
  <h2>最新新闻</h2>
  <div class="news-item" v-for="(news, index) in newsList" :key="index">
    <div class="news-content">
      <h3>{{ news.title }}</h3>
      <p>{{ news.summary }}</p>
      <div class="news-meta">
        <small>发布日期: {{ news.date }}</small>
        <small>来源: {{ news.source }}</small>
        <small>作者: {{ news.author }}</small>
        <small>评论数: {{ news.comments }}</small>
      </div>
      <div class="news-tags">
        <span v-for="(tag, tagIndex) in news.tags" :key="tagIndex" class="tag">{{ tag }}</span>
      </div>
      <a :href="news.url" target="_blank" class="read-more">阅读更多</a>
    </div>
  </div>
</div>

    <div class="message-board" id="message-board">
      <h2>留言板</h2>
      <div class="message-item" v-for="(message, index) in messageList" :key="index">
        <p>{{ message.content }}</p>
        <small>- {{ message.author }} - {{ message.date }}</small>
      </div>
      <form @submit.prevent="submitMessage">
        <textarea v-model="newMessage" placeholder="留下你的想法..."></textarea>
        <button type="submit">提交</button>
    </form>
</div>


<div class="about-us">
      <h2>关于我们</h2>
      <p>这里是关于福州大学至诚学院的介绍。可以包括学院的历史、愿景、使命和核心价值等信息。</p>
      <img src="../assets/img/轮播1.jpg" alt="About Us" class="about-us-img">
    </div>
    </div>
    
   

</template>

<style>
    .container{
        width: 100%;
        background-color: #ebebeb;
        .logo{
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            .img{
                width: 50px;
            }
            .span{
                margin-left: 10px;
                font-family: STHupo;
                font-size: 40px;
                color: #0a3a50;
            }
           
        }
        .nav{
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            .el-menu-demo{
                width: 1200px;
            }
            .span{
                margin-top: 20px;
                margin-left: 200px;
            }
            .span2{
                margin-top: 20px;
                margin-left: 5px;
            }

        }
        .carousel{
            margin: 30px auto;
            height: 300px;
            width: 80%;
            /* background-color: aqua; */
            .img{
                width: 100%;
                height: 100%;
            }
        }
        .about-us, .latest-news, .message-board, .works-showcase {
  width: 80%;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.about-us-img, .work-img {
  width: 100%;
  height: auto;
  margin-top: 20px;
}
.news-item, .message-item, .work-item {
  margin-bottom: 20px;
}
    }
</style>