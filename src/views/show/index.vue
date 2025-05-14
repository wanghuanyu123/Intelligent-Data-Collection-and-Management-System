<template>
  <el-card class="container">
    <header class="header">
      <h1 class="title">俱乐部列表</h1>
      <div class="subtitle">发现你感兴趣的俱乐部</div>
    </header>
    
    <div class="club-grid">
      <div v-for="(item, index) in clubList" 
           :key="item.id" 
           @click="$router.push(`/item/${item.name}`)" 
           class="club-card">
        <div class="club-card__number">#{{index + 1}}</div>
        <div class="club-card__content">
          <h2 class="club-card__name">{{item.name}}</h2>
          <p class="club-card__description">{{item.description}}</p>
          <div class="club-card__footer">
            <el-button type="primary" size="small" class="view-btn">查看详情</el-button>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>
  
<script  setup>
import {ref,onMounted,computed} from 'vue'
import {getClubInfoApi,get_clubApi} from '@/apis/index'
import {useUserStore} from '@/stores/index'
const store = useUserStore()
const clubList = ref([])
const ClubNameList = ref([])
const getClubList = async ()=>{
    const res = await getClubInfoApi()
    clubList.value = res
    console.log(clubList.value);
    
}

const get_club = async ()=>{
    const res = await get_clubApi({PersonId:store.UserInfo.PersonId})
    ClubNameList.value = res
    // console.log(ClubNameList.value);
}



onMounted(()=>{
    getClubList()
    get_club()
    
    
})
</script>



<style>
.container {
  width: 90%;
  max-width: 1200px;
  margin: 20px auto;
  padding: 0;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.header {
  padding: 40px;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.5px;
}

.subtitle {
  margin-top: 10px;
  font-size: 1.1rem;
  opacity: 0.9;
}

.club-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  padding: 24px;
  background: #f8fafc;
}

.club-card {
  position: relative;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e2e8f0;
}

.club-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.club-card__number {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(79, 70, 229, 0.1);
  color: #4f46e5;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.club-card__content {
  padding: 24px;
}

.club-card__name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 12px 0;
  transition: color 0.3s ease;
}

.club-card:hover .club-card__name {
  color: #4f46e5;
}

.club-card__description {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0 0 20px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.club-card__footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.view-btn {
  background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
  border: none !important;
  padding: 8px 16px !important;
  border-radius: 8px !important;
  transition: transform 0.2s ease !important;
}

.view-btn:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .container {
    width: 95%;
    margin: 10px auto;
  }

  .header {
    padding: 30px 20px;
  }

  .title {
    font-size: 2rem;
  }

  .club-grid {
    grid-template-columns: 1fr;
    padding: 16px;
    gap: 16px;
  }

  .club-card__content {
    padding: 20px;
  }
}
</style>
