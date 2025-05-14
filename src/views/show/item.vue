<template>
  <div class="page-wrapper">
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-title">{{item}}</h1>
        <div class="hero-subtitle">项目详情展示</div>
      </div>
      <div class="hero-background">
        <div class="gradient-sphere"></div>
        <div class="gradient-sphere"></div>
        <div class="gradient-sphere"></div>
      </div>
    </div>

    <div class="content">
      <div class="project-list">
        <div class="project-card" v-for="project in List" :key="project.name">
          <div class="card-header">
            <div class="header-content">
              <div class="title-wrapper">
                <h2 class="project-title">{{ project.description }}</h2>
                <div class="project-meta">
                  <span class="level-badge">{{ project.level }}</span>
                  <a v-if="project.webLink" :href="project.webLink" class="website-link">
                    <span class="link-icon">🌐</span>
                    <span>访问网站</span>
                  </a>
                </div>
              </div>
            </div>
            <div class="header-decoration">
              <div class="decoration-line"></div>
              <div class="decoration-dot"></div>
            </div>
          </div>

          <div class="card-body">
            <div class="project-intro">
              <div class="intro-icon">📝</div>
              <div class="intro-content">
                {{ project.introduce }}
              </div>
            </div>

            <div v-if="project.competitionachievement && project.competitionachievement.length" 
                 class="achievement-section">
              <div class="section-header">
                <div class="section-title">
                  <span class="section-icon">🏆</span>
                  <span class="section-text">竞赛成就</span>
                </div>
              </div>
              <div class="achievement-grid">
                <div v-for="achievement in project.competitionachievement" 
                     :key="achievement.description" 
                     class="achievement-card">
                  <div class="achievement-content">
                    <div class="achievement-header">
                      <div class="award-info">
                        <span class="award-icon">💰</span>
                        <span class="award-text">{{ achievement.Award }}</span>
                      </div>
                      <div class="level-info">
                        <span class="level-icon">⭐</span>
                        <span class="level-text">{{ achievement.CompetitionLevel }}</span>
                      </div>
                    </div>
                    <div class="achievement-details">
                      <div class="detail-item">
                        <span class="detail-label">奖项：</span>
                        <span class="detail-value">{{ achievement.CompetitionRank }}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">时间：</span>
                        <span class="detail-value">{{ achievement.time }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="team-section">
              <div class="section-header">
                <div class="section-title">
                  <span class="section-icon">👥</span>
                  <span class="section-text">参与人员</span>
                </div>
              </div>
              <div class="team-grid">
                <div v-for="(people,index2) in project.person" 
                     :key="index2" 
                     class="team-member">
                  <div class="member-avatar">
                    <div class="avatar-content">
                      {{ people.PersonName.charAt(0) }}
                    </div>
                    <div class="avatar-background"></div>
                  </div>
                  <div class="member-info">
                    <div class="member-name">{{ people.PersonName }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="gallery-section">
              <div class="section-header">
                <div class="section-title">
                  <span class="section-icon">📸</span>
                  <span class="section-text">项目照片</span>
                </div>
              </div>
              <div class="gallery-grid">
                <div v-for="(photo,index2) in project.photo" 
                     :key="index2" 
                     class="gallery-item">
                  <div class="gallery-image-wrapper">
                    <img :src="photo.link" alt="项目照片" class="gallery-image">
                   
                    <div class="gallery-overlay">
                      <div class="overlay-content">
                        <span class="view-icon">👁️</span>
                        <span class="view-text">查看</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import {useRoute} from 'vue-router'
import {lastStep} from '@/apis/index'
const item = ref(null)
item.value = useRoute().params.id

const List = ref([])
const getlastStep = async () => {
    const res = await lastStep({name:item.value})
    List.value = res
    console.log(List.value);
    
}
onMounted(() => {
    getlastStep()
})
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: #f8fafc;
}

.hero {
  position: relative;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.gradient-sphere {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: float 20s infinite ease-in-out;
}

.gradient-sphere:nth-child(1) {
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.gradient-sphere:nth-child(2) {
  top: 50%;
  right: -100px;
  animation-delay: -5s;
}

.gradient-sphere:nth-child(3) {
  bottom: -100px;
  left: 50%;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0);
  }
  25% {
    transform: translate(50px, 50px);
  }
  50% {
    transform: translate(0, 100px);
  }
  75% {
    transform: translate(-50px, 50px);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  animation: fadeInUp 1s ease-out;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-top: 1rem;
  opacity: 0.9;
  animation: fadeInUp 1s ease-out 0.2s backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content {
  max-width: 1200px;
  margin: -50px auto 0;
  padding: 0 20px;
  position: relative;
  z-index: 2;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.project-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  position: relative;
}

.project-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.project-card:hover::before {
  opacity: 1;
}

.card-header {
  padding: 30px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
  position: relative;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title-wrapper {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.project-title {
  font-size: 1.8rem;
  color: #1e293b;
  margin: 0;
  font-weight: 600;
  line-height: 1.3;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: 15px;
}

.level-badge {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(79, 70, 229, 0.1);
}

.website-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 6px 12px;
  border-radius: 20px;
  background: rgba(79, 70, 229, 0.1);
}

.website-link:hover {
  background: rgba(79, 70, 229, 0.2);
  transform: translateY(-2px);
}

.link-icon {
  font-size: 1.1rem;
}

.header-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, #4f46e5, transparent);
}

.decoration-dot {
  position: absolute;
  bottom: -4px;
  left: 50%;
  width: 8px;
  height: 8px;
  background: #4f46e5;
  border-radius: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.5);
}

.card-body {
  padding: 30px;
}

.project-intro {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.project-intro:hover {
  background: #f1f5f9;
  transform: translateX(5px);
}

.intro-icon {
  font-size: 1.5rem;
  color: #4f46e5;
}

.intro-content {
  flex: 1;
  color: #64748b;
  line-height: 1.6;
}

.section-header {
  margin-bottom: 25px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-icon {
  font-size: 1.5rem;
}

.section-text {
  font-size: 1.4rem;
  color: #1e293b;
  font-weight: 600;
}

.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.achievement-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #4f46e5;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.achievement-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.achievement-card:hover::before {
  opacity: 1;
}

.achievement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e2e8f0;
}

.award-info, .level-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.award-icon, .level-icon {
  font-size: 1.2rem;
}

.award-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: #4f46e5;
}

.level-text {
  font-size: 0.9rem;
  color: #64748b;
  background: #e0e7ff;
  padding: 4px 8px;
  border-radius: 12px;
}

.achievement-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
}

.detail-label {
  font-weight: 500;
  color: #475569;
}

.detail-value {
  color: #1e293b;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.team-member {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.team-member:hover {
  transform: translateY(-3px);
}

.member-avatar {
  position: relative;
  width: 60px;
  height: 60px;
}

.avatar-content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  background: #e0e7ff;
  color: #4f46e5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.avatar-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #4f46e5;
  border-radius: 50%;
  transform: scale(1.1);
  opacity: 0.1;
  transition: all 0.3s ease;
}

.team-member:hover .avatar-content {
  transform: scale(1.1);
}

.team-member:hover .avatar-background {
  opacity: 0.2;
}

.member-info {
  text-align: center;
}

.member-name {
  color: #64748b;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.team-member:hover .member-name {
  color: #4f46e5;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.gallery-item {
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.gallery-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}

.gallery-image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.gallery-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

.gallery-item:hover .gallery-image {
  transform: scale(1.1);
}

.overlay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: white;
  transform: translateY(10px);
  transition: transform 0.3s ease;
}

.gallery-item:hover .overlay-content {
  transform: translateY(0);
}

.view-icon {
  font-size: 1.5rem;
}

.view-text {
  font-size: 0.9rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .content {
    padding: 0 15px;
  }
  
  .card-header {
    padding: 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .project-title {
    font-size: 1.5rem;
  }
}
</style>