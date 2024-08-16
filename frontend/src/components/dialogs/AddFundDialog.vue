<template>
    <el-dialog v-model="showDialog" title="添加基金项目" width="300px">
        <el-form :model="form" :rules="rules" ref="form">
            <el-form-item label="名称" prop="name">
                <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="期初金额" prop="beginningAmount">
                <el-input v-model="form.beginningAmount"></el-input>
            </el-form-item>
            <el-form-item label="期初时间" prop="beginningTime">
                <el-date-picker v-model="form.beginningTime" type="date" placeholder="选择日期">
                </el-date-picker>
            </el-form-item>
            <el-form-item label="当期金额" prop="currentAmount">
                <el-input v-model="form.currentAmount"></el-input>
            </el-form-item>
            <el-form-item label="锁定期" prop="lockupPeriod">
                <el-input v-model.number="form.lockupPeriod"></el-input>
            </el-form-item>
            <el-form-item label="当前持有" prop="holding">
                <el-switch v-model="form.holding"></el-switch>
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
import { isNumberValidator, isIntegerValidator } from '@/scripts/validator.js'
import { timeFormat } from '@/scripts/formatter';

export default {
    name: "AddFundDialog",
    data () {
        return {
            showDialog: false,
            form: {
                name: '',
                beginningAmount: 0,
                beginningTime: '',
                currentAmount: 0,
                lockupPeriod: 0,
                holding: true
            },
            rules: {
                name: [
                    { required: true, message: '请输入名称', trigger: 'blur' }
                ],
                beginningAmount: [
                    { required: true, message: '请输入期初金额', trigger: 'blur' },
                    {
                        message: '期初金额必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ],
                beginningTime: [
                    { required: true, message: '请选择期初时间', trigger: 'blur' }
                ],
                currentAmount: [
                    { required: true, message: '请输入当期金额', trigger: 'blur' },
                    {
                        message: '当期金额必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ],
                lockupPeriod: [
                    { required: true, message: '请输入锁定期', trigger: 'blur' },
                    {
                        message: '锁定期必须为整数值', trigger: 'blur', validator: isIntegerValidator
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
                        this.form.beginningTime = timeFormat(this.form.beginningTime);
                        this.$emit('add', this.form, 'fund');
                        this.showDialog = false;
                        this.$refs.form.resetFields();
                    }
                });
            },

            edit: (row) => {
                console.log(row);
                this.form.name = row.name;
                this.form.beginningAmount = row.beginningAmount;
                this.form.beginningTime = row.beginningTime;
                this.form.currentAmount = row.currentAmount;
                this.form.lockupPeriod = row.lockupPeriod;
                this.form.holding = row.holding;
                this.showDialog = true;
            },

            show: () => {
                this.showDialog = true;
            }
        }
    },
}


</script>