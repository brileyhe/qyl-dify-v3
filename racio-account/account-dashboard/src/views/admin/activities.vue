<template>

    <div class="home-container">

        <div style="width:80%">
            <el-row>
                <el-col>
                    当前空间优惠值余额<el-icon>
                        <WarningFilled />
                    </el-icon>
                    ⚡️{{ discountsRemaining }}
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="2">
                    优惠券面值<el-icon>
                        <WarningFilled />
                    </el-icon>
                </el-col>
                <el-col :span="3">
                    <el-input placeholder="请输入优惠券面值" />
                </el-col>
                <el-col :span="6">
                    余额可以支持 3 位新注册用户的优惠券
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="2">
                    生效时段
                </el-col>
                <el-col :span="3">
                    <el-input placeholder="请输入优惠券面值" />
                </el-col>
                <el-col :span="6">
                    余额可以支持 3 位新注册用户的优惠券
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="2">
                    限制数量
                </el-col>
                <el-col :span="3">
                    <el-input placeholder="请输入优惠券面值" />
                </el-col>
                <el-col :span="6">
                    请基于每日注册用户数量进行合理设置
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="2">
                    券有效期
                </el-col>
                <el-col :span="3">
                    <el-input placeholder="请输入优惠券面值" />
                </el-col>
                <el-col :span="6">
                    用户领取之后多少天过期
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="2">
                    活动名称
                </el-col>
                <el-col :span="3">
                    <el-input placeholder="请输入活动名称" />
                </el-col>
                <el-col :span="6">
                    <el-button type="primary" @click="addActivity">开启活动</el-button>
                </el-col>
            </el-row>
            <el-row>
                <el-col>
                    <div>活动记录</div>
                </el-col>
            </el-row>
            <el-row>
                <el-table :data="tableData" border style="width: 100%">
                    <el-table-column prop="invited_by" label="活动名称" min-width="240" />
                    <el-table-column prop="invited_by" label="活动时段" min-width="240" />
                    <el-table-column prop="invited_by" label="优惠券面值" min-width="100" />
                    <el-table-column prop="invited_by" label="已领取" width="100" />
                    <el-table-column prop="invited_by" label="待领取" width="100" />
                    <el-table-column prop="invited_by" label="操作" width="140">
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-switch class="ml-2" inline-prompt inactive-text="停止" active-text="启动"
                                    style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </el-row>
            <el-row justify="end" style="background-color: #fff;">
                <el-col :span="9">
                    <el-pagination v-model:current-page="currentPage1" :page-size="100" size="large"
                        layout="total, prev, pager, next" :total="1000" @size-change="handleSizeChange"
                        @current-change="handleCurrentChange" />
                </el-col>
            </el-row>

            <el-row>
                <el-col>
                    <div>优惠领券记录</div>
                </el-col>
            </el-row>
            <el-row>
                <el-table :data="tableData" border>
                    <el-table-column prop="invited_by" label="用户名" min-width="240" />
                    <el-table-column prop="invited_by" label="优惠券" min-width="240" />
                    <el-table-column prop="invited_by" label="领取时间" min-width="100" />
                </el-table>
            </el-row>
            <el-row justify="end" style="background-color: #fff;">
                <el-col :span="9">
                    <el-pagination v-model:current-page="currentPage1" :page-size="100" size="large"
                        layout="total, prev, pager, next" :total="1000" @size-change="handleSizeChange"
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
const discountsRemaining = ref(0)
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
