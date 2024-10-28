<template>

    <div class="home-container bg-white">

        <div style="width:80%">

            <el-row>
                <el-col :span="2" class="flex items-center mb-2">
                    <div class="text-base font-medium">
                        选择空间
                    </div>
                </el-col>
                <el-col :span="3">
                    <el-select />
                </el-col>
            </el-row>
            <el-row class="mb-5 mt-10">
                <div class="text-xl font-medium">
                    用户充值
                </div>
            </el-row>
            <el-row class="mb-5">
                <el-col :span="2" class="flex items-center mb-2 ">
                    <div class="text-base font-medium ">
                        查询时段
                    </div>
                </el-col>
                <el-col :span="8">
                    <el-date-picker v-model="value1" type="datetimerange" range-separator="To"
                        start-placeholder="选择开始时间" end-placeholder="选择结束时间" />
                </el-col>


            </el-row>
            <el-row class="mb-5">
                <el-table :data="tableData" style="width: 100%" class="table card">
                    <el-table-column prop="invited_by" label="用户名" min-width="240" />
                    <el-table-column prop="invited_by" label="电力值" min-width="240" />
                    <el-table-column prop="invited_by" label="充值时间" min-width="240" />
                    <el-table-column prop="invited_by" label="订单号" min-width="240" />
                    <el-table-column prop="invited_by" label="操作" min-width="240" />
                </el-table>
            </el-row>
            <el-row justify="end" align="middle" style="background-color: #fff;" class="mb-10">
                <el-col :span="3">
                    <div>
                        总充值金额：{{ moneyTotal }}元
                    </div>
                </el-col>
                <el-col :span="3">
                    <div>
                        总电力值：{{ powerTotal }}
                    </div>
                </el-col>

                <el-col :span="10">
                    <el-pagination v-model:current-page="currentPage1" :page-size="100" size="large" background
                        layout="total, prev, pager, next" :total="1000" @size-change="handleSizeChange"
                        @current-change="handleCurrentChange" />

                </el-col>
            </el-row>

            <el-row class="mb-5">
                <el-col class="text-xl font-medium">电力消耗</el-col>
            </el-row>
            <el-row :gutter="30" class="flex  items-center mb-5">
                <el-col :span="2" class="text-base font-medium">
                    查询时段
                </el-col>
                <el-col :span="8">
                    <el-date-picker v-model="value1" type="datetimerange" range-separator="To"
                        start-placeholder="选择开始时间" end-placeholder="选择结束时间" />
                </el-col>
                <el-col xs="8" :sm="6" :md="4" :lg="3" :xl="2">
                    <el-select placeholder="选择应用" />
                </el-col>
            </el-row>
            <el-row class="mb-5">

                <el-table :data="tableData" style="width: 100%" class="table card" max-height="250">
                    <el-table-column prop="invited_by" label="用户名" min-width="240" />
                    <el-table-column prop="invited_by" label="应用名" min-width="240" />
                    <el-table-column prop="invited_by" label="电力值" min-width="240" />
                    <el-table-column prop="invited_by" label="时间" min-width="240" />
                    <el-table-column prop="invited_by" label="备注" min-width="240" />

                </el-table>
            </el-row>
            <el-row :gutter="0" justify="end" align="middle" style="background-color: #fff;" class="flex items-center">
                <el-col :span="5">
                    <div>
                        总消耗电力值：{{ consumePowerTotal }}
                    </div>
                </el-col>
                <el-col style="background-color: #fff;" :span="10">
                    <el-pagination v-model:current-page="currentPage1" :page-size="100" size="large"
                        layout="total, prev, pager, next" :total="1000" background @size-change="handleSizeChange"
                        @current-change="handleCurrentChange" />
                </el-col>
            </el-row>
        </div>
    </div>

</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { Plus, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { inviteUser, members, memberChangeRole, memberRemove, getAuthList } from "@/api/api"
import clip from "@/utils/clipboard"

import { formatTime } from "@/utils"
import { useUserStore } from "@/store/modules/user"

const { token, roles } = useUserStore()
const workspaceRole = ref("")
const router = useRouter()
const tableData = ref([])
const inviteDialog = ref(false)
const invitText = ref("")
const remarkText = ref("")
const invitUrl = ref("")
const PageInfo = ref({
    "page": 1,
    "limit": 20,
    "total": 0,
    "keyword": ""

})
const buttonStatus = ref(false)
const newRole = ref("")
const editRoles = ref(false)
const currEditRoleInfo = ref({})
const handleCopy = (text, event) => {
    clip(text, event)
}

function handleCurrentChange() {
    authList()
}
function handleSizeChange() {
    authList()
}

function openInvite() {
    inviteDialog.value = true
    invitUrl.value = ""
    buttonStatus.value = false
}
const editRolesDialog = (arg) => {
    currEditRoleInfo.value = arg;
    console.log(arg);

    editRoles.value = true
}


function authList() {
    getAuthList(PageInfo.value).then(res => {
        let { code, msg, data } = res.data
        console.log(code, msg, data);

        if (code == 0) {
            tableData.value = data.data
            PageInfo.value.total = data.total
            PageInfo.value.page = data.page
            PageInfo.value.limit = data.limit
        } else {

            ElMessage({
                message: msg,
                type: "error",
                duration: 3000,
            })
        }


    })
}

function sendInvite() {

    if (roles == "superAdmin") {
        workspaceRole.value = "owner"
    } else if (workspaceRole.value == "") {
        ElMessage({
            message: "请选择邀请角色!",
            type: "error",
            duration: 3000,
        })
        return
    }

    inviteUser({
        email: invitText.value,
        domain: "racio.chat",
        role: workspaceRole.value,
        tenant_id: localStorage.getItem("tenant_id") || "",
        remark: remarkText.value

    })
        .then(res => {
            let { code, data, msg } = res.data
            if (code == 0) {
                invitUrl.value = data.url
                buttonStatus.value = true
            }
        })
        .catch(error => {
            ElMessage({
                message: error.message,
                type: "error",
                duration: 3000,
            })
        })
        .finally(() => {
            authList()
        })
}
onMounted(async () => {

    authList()
})
</script>
<style lang="scss" scoped>
.home-container {
    width: 98%;
    margin: 32px;
}

.image-slot {
    text-align: center;
    color: #ccc;
    font-size: 14px;
    margin-top: 10px;
}

@import "./index";
</style>
