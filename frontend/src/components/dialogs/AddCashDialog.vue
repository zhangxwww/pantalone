<template>
    <el-dialog v-model="showDialog" title="添加现金项目" width="300px">
        <el-form :model="form" ref="form" :rules="rules">
            <el-form-item label="账户" prop="name">
                <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="金额" prop="amount">
                <el-input v-model="form.amount"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="onCancelAdd">取消</el-button>
                <el-button type="primary" @click="onConfirmAdd">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script>
import { isNumberValidator } from '@/scripts/validator.js'

export default {
    name: "AddCashDialog",
    data () {
        return {
            showDialog: false,
            form: {
                name: '',
                amount: 0
            },
            rules: {
                name: [
                    { required: true, message: '请输入账户名称', trigger: 'blur' }
                ],
                amount: [
                    { required: true, message: '请输入金额', trigger: 'blur' },
                    {
                        message: '金额必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ]
            },

            onCancelAdd: () => {
                this.showDialog = false;
                this.$refs.form.resetFields();
            },

            onConfirmAdd: () => {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$emit('add', this.form, 'cash');
                        this.showDialog = false;
                        this.$refs.form.resetFields();
                    }
                });
            },

            edit: (row) => {
                this.form.name = row.name;
                this.form.amount = row.amount;
                this.showDialog = true;
            },

            show: () => {
                this.showDialog = true;
            }
        }
    },
}


</script>