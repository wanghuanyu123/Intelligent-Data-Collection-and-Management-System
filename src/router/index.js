import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
    path:'/home',
    component: () => import('@/Layout/Home.vue'),
    children:[
    
    ]
    },
    
   {
    path:'/',
    component: () => import('@/Layout/index.vue'),
    redirect:'/home',
    children:[
      {
        path:'upload',
        name:'upload',
        component:()=>import('@/views/ulpoad/index.vue'),
        meta:{
          title:'发布任务'
        }
      },
      // {
      //   path:'addrole',
      //   name:'addrole',
      //   component:()=>import('@/views/role/index.vue'),
      //   meta:{
      //     title:'添加人员'
      //   }
      // },
      {
        path:'news',
        name:'news',
        component:() => import('@/views/news/index.vue'),
        meta:{
          title:'我的发布'
        }
      },
      {
        path:'addFace',
        name:'addFace',
        component:() => import('@/views/role/addFace.vue'),
        meta:{
          title:'添加人脸'
        }
      },
      {
        path:'myinfo',
        name:'myinfo',
        component:() => import('@/views/role/myinfo.vue'),
        meta:{
          title:'基本信息'
        }
      },
      {
        path:'watch',
        name:'watch',
        component:() => import('@/views/watch/index.vue'),
        meta:{
          title:'审核作品'
        }
      },
      {
        path:'history',
        name:'history',
        component:() => import('@/views/watch/history.vue'),
        meta:{
          title:'历史记录'
        }
      }
     
    ]
   },
   {
    path:'/addmember',
    component: () => import('@/views/Club/index.vue'),
   },
   
  {
    path:'/askai',
    name:'askai',
    component:() => import('@/views/askAi/index.vue'),
    meta:{
      title:'AI助手'
    }
  },
  {
    path:'/show',
    name:'show',
    component:() => import('@/views/show/index.vue'),
    meta:{
      title:'展示作品'
    }
  },
  {
    path:'/item/:id',
    component:() => import('@/views/show/item.vue'),
  },
  {
    path:'/class',
    component:() => import('@/views/class/index.vue'),
  },
  {
    path:'/work/:id',
    component:() => import('@/views/class/work.vue'),
  },
  {
    path:'/mywork/:id',
    component:() => import('@/views/class/mywork.vue'),
  }
  ]
})

export default router
