<script  setup>
import { ref ,defineModel,defineProps,onMounted} from 'vue'
import {getStudentListApi,addClassMenberApi,getclassMenberApi,deleteclassMemberApi} from '@/apis/index'
// const drawer = ref(false)
const prop = defineProps(['name'])
const showEdit = defineModel('showEdit',false)
const clubInfo = ref({})
const teacherName = null
const tcName = ref(null)
const show = ref(false)  
const tableData = ref([])
const getInfo = async ()=>{
  const {Club,TeacherName} = await getStudentListApi({
    name: prop.name
  })
  clubInfo.value = Club
  tcName.value = TeacherName
}

onMounted(()=>{
  getInfo()
  getRuleMember()
  console.log(prop.name);
  
})

const addId = ref(null)

const addRole = async ()=>{
  await addClassMenberApi({
    PersonId:addId.value,
    name:prop.name
  })
  ElMessage.success('添加成功')
  addId.value = null
  getRuleMember()
  getInfo()
}

const getRuleMember = async()=>{
  tableData.value = await getclassMenberApi(
    {name:prop.name}
  )
  console.log(tableData.value);
  
}

const handleDelete = async(id)=>{
  console.log(id);
  
  await deleteclassMemberApi({
    PersonId:id,
    name:prop.name
  })
  ElMessage.success('删除成功')
  getRuleMember()
  getInfo()
}
</script>

<template>
    <el-drawer v-model="showEdit" :title="clubInfo.name" size="35%">
      <div class="description">{{clubInfo.description}}</div>
      <div><span style="margin-right: 5px;">指导老师:</span>{{tcName}}</div>
      <el-button style="margin-top: 10px;margin-bottom: 10px" @click="addRole">添加成员</el-button>
      <el-input placeholder="请输入添加成员学号" v-model="addId" style="margin-bottom: 10px"></el-input>
      
      <el-table :data="tableData">
        <el-table-column label="头像" width="180">
          <template v-slot="{row}">
            <el-avatar :size="60" :src="row.photoLink" />
          </template>
        </el-table-column>
        <el-table-column label="姓名" width="180" prop="PersonName">
        </el-table-column>
        <el-table-column label="Operations">
          <template v-slot="{row}">
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(row.PersonId)"
            >
              Delete
            </el-button>
          </template>
    </el-table-column>
      </el-table>

     

    </el-drawer>

  
    
</template>
  


<style scoped>
.description{
  
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}
</style>

  