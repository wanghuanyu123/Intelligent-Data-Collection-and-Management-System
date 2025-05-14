<template>
  <div class="club-container">
    <div class="page-header">
      <h1 class="title">俱乐部管理</h1>
      <p class="subtitle">管理所有俱乐部信息，包括添加、编辑和删除操作</p>
    </div>

    <el-card class="table-card">
      <el-table 
        :data="tableData" 
        style="width: 100%"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
        :row-style="{ transition: 'all 0.3s' }"
        :hover-row="true"
      >
        <el-table-column prop="name" label="俱乐部名称" min-width="200">
          <template v-slot="{row}">
            <el-link 
              type="primary" 
              :underline="false"
              class="club-name"
              @click="$router.push(`/item/${row.name}`)"
            >
              {{row.name}}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="teacher" label="指导老师" min-width="150" />
        <el-table-column prop="description" label="描述" min-width="300" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template v-slot="{row}">
            <el-button-group>
              <el-button
                type="primary"
                size="small"
                @click="showEditFun(row.name)"
                class="action-btn"
              >
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-popconfirm
                title="确定要删除这个俱乐部吗？"
                confirm-button-text="确定"
                cancel-button-text="取消"
                @confirm="deleteRow(row.name)"
              >
                <template #reference>
                  <el-button
                    type="danger"
                    size="small"
                    class="action-btn"
                  >
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-button 
      type="primary" 
      class="add-btn"
      @click="showClubDialog"
    >
      <el-icon><Plus /></el-icon>
      添加俱乐部
    </el-button>

    <clubadd :clubDialog="clubDialog" @closeDialog="close"></clubadd>
    <drawView v-if="showEdit" v-model="showEdit" :name="thisname"></drawView>
  </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { getClubInfoApi, deleteClubApi } from '@/apis/index'
import Clubadd from '@/Layout/componens/Clubadd.vue'
import drawView from './components/draw.vue'
import { Edit, Delete, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const tableData = ref([])

const getClubList = async () => {
  const res = await getClubInfoApi()
  tableData.value = res
}

onMounted(() => {
  getClubList()
})

const clubDialog = ref(false)
const showClubDialog = () => {
  clubDialog.value = true
}

const close = () => {
  clubDialog.value = false
  getClubList()
}

const deleteRow = async (name) => {
  try {
    await deleteClubApi({name})
    getClubList()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const showEditFun = (name) => {
  showEdit.value = true
  thisname.value = name
}

const showEdit = ref(false)
const thisname = ref('')
</script>

<style scoped>
.club-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.title {
  font-size: 28px;
  color: #303133;
  margin: 0;
  font-weight: 600;
}

.subtitle {
  color: #909399;
  margin: 8px 0 0;
  font-size: 14px;
}

.table-card {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.club-name {
  font-weight: 500;
  transition: color 0.3s;
}

.club-name:hover {
  color: #409EFF;
}

.action-btn {
  margin: 0 4px;
}

.add-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  font-weight: 600;
}

:deep(.el-table td) {
  padding: 12px 0;
}
</style>
