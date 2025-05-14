<template>
    <div>
        <el-table :data="tableData" style="width: 100% ;margin-top: 20px;">
          <el-table-column prop="name" label="班级名称" width="400">
          <template v-slot="{row}">
            <span @click="$router.push(`/item/${row.name}`)">
              {{row.name}}
            </span>
           
          </template>
          </el-table-column>
         
           
            <el-table-column prop="teacher" label="指导老师" width="400" />
            <el-table-column prop="description" label="描述" width="400" />
            <el-table-column  label="Operations" min-width="320">
              <template  v-slot="{row}">
                <el-button
                  link
                  type="primary"
                  size="small"
                  @click="showEditFun(row.name)"
                >
                  编辑/查看
                </el-button>
                <el-button
                  link
                  type="primary"
                  size="small"
                  @click="deleteRow(row.name)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
        </el-table>
        <el-button class="mt-4" style="width: 100%;margin-top: 3px;" @click="showClubDialog">
        添加
        </el-button>
    </div>    
    <Classadd :clubDialog="clubDialog" @closeDialog="close"></Classadd>
    <drawView v-if="showEdit" v-model="showEdit" :name="thisname"></drawView>

</template>
  
<script  setup>
import { ref,onMounted } from 'vue'
import {getClassListApi,deleteClassApi} from '@/apis/index'
import Classadd from '@/Layout/componens/Classadd.vue'
import drawView from './components/draw.vue'
const tableData = ref([])

//
const getClubList = async ()=>{
    const res = await getClassListApi()
    tableData.value = res
    console.log(res);
    
}
//
onMounted(()=>{
    getClubList()
})
const clubDialog = ref(false) 
const showClubDialog
 = ()=>{
    clubDialog.value = true
}

const close = ()=>{
    clubDialog.value = false
    getClubList()
}
const deleteRow = async (name) => {
    await deleteClassApi({name})
    getClubList()
    ElMessage
    .success('删除成功')
}
const showEditFun = (name)=>{
    showEdit.value = true
    thisname.value = name
    console.log(thisname.value);
    
}

const showEdit = ref(false)
const thisname = ref('')
</script>
  