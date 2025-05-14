<template>
  <div class="three-background"></div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';

let scene, camera, renderer, particles;
let animationFrameId;

const init = () => {
  // 创建场景
  scene = new THREE.Scene();
  
  // 创建相机
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;
  
  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 0);
  document.querySelector('.three-background').appendChild(renderer.domElement);
  
  // 创建粒子
  const particleCount = 2000;
  const particlesGeometry = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  
  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 10;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
    
    colors[i * 3] = Math.random() * 0.2 + 0.1; // 蓝色
    colors[i * 3 + 1] = Math.random() * 0.2 + 0.3; // 绿色
    colors[i * 3 + 2] = Math.random() * 0.2 + 0.5; // 红色
  }
  
  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  
  const particlesMaterial = new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
  });
  
  particles = new THREE.Points(particlesGeometry, particlesMaterial);
  scene.add(particles);
  
  // 添加环境光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);
  
  // 添加点光源
  const pointLight = new THREE.PointLight(0xffffff, 1);
  pointLight.position.set(5, 5, 5);
  scene.add(pointLight);
  
  // 动画循环
  const animate = () => {
    animationFrameId = requestAnimationFrame(animate);
    
    particles.rotation.x += 0.0005;
    particles.rotation.y += 0.0005;
    
    renderer.render(scene, camera);
  };
  
  animate();
  
  // 窗口大小调整
  const handleResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  };
  
  window.addEventListener('resize', handleResize);
};

onMounted(() => {
  init();
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
  window.removeEventListener('resize', handleResize);
  if (renderer) {
    renderer.dispose();
  }
});
</script>

<style scoped>
.three-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}
</style> 