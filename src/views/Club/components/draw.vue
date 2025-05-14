<script setup>
import { ref, defineModel, defineProps, onMounted } from 'vue'
import { getClubInfoListApi, addClubMenberApi, getClubMenberApi, deleteMemberApi } from '@/apis/index'
import { ElMessage } from 'element-plus'
import { Plus, Delete, User } from '@element-plus/icons-vue'

const prop = defineProps(['name'])
const showEdit = defineModel('showEdit', false)
const clubInfo = ref({})
const tcName = ref(null)
const tableData = ref([])
const addId = ref(null)

const getInfo = async () => {
  const { Club, TeacherName } = await getClubInfoListApi({
    name: prop.name
  })
  clubInfo.value = Club
  tcName.value = TeacherName
}

onMounted(() => {
  getInfo()
  getRuleMember()
})

const addRole = async () => {
  if (!addId.value) {
    ElMessage.warning('请输入成员学号')
    return
  }
  try {
    await addClubMenberApi({
      PersonId: addId.value,
      name: prop.name
    })
    ElMessage.success('添加成功')
    addId.value = null
    getRuleMember()
    getInfo()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

const getRuleMember = async () => {
  tableData.value = await getClubMenberApi({ name: prop.name })
}

const handleDelete = async (id) => {
  try {
    await deleteMemberApi({
      PersonId: id,
      name: prop.name
    })
    ElMessage.success('删除成功')
    getRuleMember()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}
</script>

<template>
  <el-drawer 
    v-model="showEdit" 
    :title="clubInfo.name" 
    size="35%"
    class="club-drawer"
  >
    <div class="drawer-content">
      <div class="club-info">
        <div class="info-item">
          <el-icon><User /></el-icon>
          <span class="label">指导老师：</span>
          <span class="value">{{ tcName }}</span>
        </div>
        <div class="description">
          <span class="label">俱乐部简介：</span>
          <p class="value">{{ clubInfo.description }}</p>
        </div>
      </div>

      <div class="member-section">
        <div class="section-header">
          <h3>成员管理</h3>
          <div class="add-member">
            <el-input
              v-model="addId"
              placeholder="请输入成员学号"
              class="member-input"
            >
              <template #append>
                <el-button 
                  type="primary" 
                  @click="addRole"
                  :icon="Plus"
                >
                  添加
                </el-button>
              </template>
            </el-input>
          </div>
        </div>

        <el-table 
          :data="tableData"
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
          :row-style="{ transition: 'all 0.3s' }"
          :hover-row="true"
        >
          <el-table-column label="头像" width="100">
            <template v-slot="{ row }">
              <el-avatar 
                :size="50" 
                :src="row.photoLink"
                class="member-avatar"
              >
                <template #default>
                  <el-icon><User /></el-icon>
                </template>
              </el-avatar>
            </template>
          </el-table-column>
          <el-table-column label="姓名" prop="PersonName" />
          <el-table-column label="操作" width="100" fixed="right">
            <template v-slot="{ row }">
              <el-popconfirm
                title="确定要删除该成员吗？"
                confirm-button-text="确定"
                cancel-button-text="取消"
                @confirm="handleDelete(row.PersonId)"
              >
                <template #reference>
                  <el-button
                    type="danger"
                    size="small"
                    :icon="Delete"
                    circle
                    class="delete-btn"
                  />
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </el-drawer>
</template>

<style scoped>
.club-drawer {
  :deep(.el-drawer__header) {
    margin-bottom: 0;
    padding: 20px;
    border-bottom: 1px solid #ebeef5;
  }
}

.drawer-content {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.club-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  color: #606266;

  .el-icon {
    margin-right: 8px;
    font-size: 18px;
  }

  .label {
    font-weight: 500;
    margin-right: 8px;
  }

  .value {
    color: #303133;
  }
}

.description {
  .label {
    display: block;
    font-weight: 500;
    margin-bottom: 8px;
    color: #606266;
  }

  .value {
    color: #303133;
    line-height: 1.6;
    margin: 0;
  }
}

.member-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    margin: 0;
    font-size: 16px;
    color: #303133;
  }
}

.add-member {
  width: 300px;
}

.member-input {
  :deep(.el-input-group__append) {
    padding: 0;
  }
}

.member-avatar {
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.member-avatar :deep(.el-icon) {
  font-size: 24px;
  color: #909399;
}

.delete-btn {
  transition: all 0.3s;
  
  &:hover {
    transform: scale(1.1);
  }
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
  