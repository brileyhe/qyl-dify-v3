<template>

    <div class="home-container">

        <div>
            <el-row :gutter="20" class="mb-5">
                <el-col :span="10">
                    <div class="text-xl font-medium">
                        兑换电力值
                    </div>
                </el-col>
            </el-row>
            <el-row class="flex items-center mb-2">
                <el-col :span="2">
                    <div class="text-base font-medium ">
                        选择空间
                    </div>
                </el-col>
                <el-col :span="3">
                    <el-select />
                </el-col>
            </el-row>
            <el-row class=" flex items-center mb-2">
                <el-col :span="2">
                    <div class="text-base font-medium ">
                        转账金额 <el-icon type="warning">
                            <WarningFilled />
                        </el-icon>
                    </div>

                </el-col>
                <el-col :span="2">
                    <el-input placeholder="请输入金额" v-model.number="moneyText"></el-input>
                </el-col>
                <el-col :span="1"></el-col>
                <el-col :span="2">
                    <div class="text-base font-medium ">
                        转账时间
                    </div>
                </el-col>
                <el-col :span="3">
                    <el-date-picker v-model="value1" type="datetime" placeholder="选择时间" />
                </el-col>
            </el-row>
            <el-row class=" flex items-center mb-2">
                <el-col :span="2">
                    <div class="text-base font-medium ">
                        兑换电力值
                    </div>

                </el-col>
                <el-col :span="4">
                    <el-input placeholder="请输入兑换电力值" v-model="exchangeText"></el-input>

                </el-col>
            </el-row>
            <el-row class=" flex items-center mb-4">
                <el-col :span="2">
                    <div class="text-base font-medium ">
                        备注
                    </div>
                </el-col>
                <el-col :span="4">
                    <el-input placeholder="请输入备注" v-model="remarkText"></el-input>
                </el-col>
            </el-row>
            <el-row>
                <el-button type="primary" class="btn btn-primary" @click="handleInvite">兑换</el-button>
            </el-row>
        </div>
        <div class="mt-6">
            <el-row class="mb-2">
                <el-col class="text-xl font-medium">
                    兑换记录
                </el-col>
            </el-row>
            <el-row class="mb-1" :span="24">
                <el-table :data="rechargeData" style="width: 100%" class=" card">
                    <el-table-column prop="workspaceName" label="空间名" min-width="140" />
                    <el-table-column prop="money" label="转账金额" min-width="140" />
                    <el-table-column prop="transferTime" label="转账时间" min-width="100" />
                    <el-table-column prop="exchangePower" label="兑换电力值" min-width="100" />
                    <el-table-column prop="enterTime" label="入账时间" min-width="100" />
                    <el-table-column prop="remark" label="备注" min-width="240" />

                </el-table>
            </el-row>
            <el-row justify="start" class="mt-5">
                <el-col :span="8">
                    <el-pagination v-model:current-page="PageInfo.page" v-model:page-size="PageInfo.limit" background
                        :total="PageInfo.total" @current-change="handleCurrentChange" />
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
const rechargeData = ref([{
    workspaceName: "112121",
    money: "112121",
    transferTime: "112121",
    exchangePower: "112121",
    enterTime: "112121",
    remark: "112121",
}])
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
            rechargeData.value = data.data
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
    margin: 32px;
    width: 98%;
}

.image-slot {
    text-align: center;
    color: #ccc;
    font-size: 14px;
    margin-top: 10px;
}

@import "./index";
</style>
