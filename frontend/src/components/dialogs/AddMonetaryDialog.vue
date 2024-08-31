<template>
    <el-dialog v-model="showDialog" title="添加货币基金项目" @closed="reset" width="300px">
        <el-form :model="form" ref="form" :rules="rules">
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
            <el-form-item label="累计投入金额" prop="currentShares">
                <el-input v-model="form.currentShares"></el-input>
            </el-form-item>
            <el-form-item label="快速赎回" prop="fastRedemption">
                <el-switch v-model="form.fastRedemption"></el-switch>
            </el-form-item>
            <el-form-item label="当前持有" prop="holding">
                <el-switch v-model="form.holding"></el-switch>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="onCancel">取消</el-button>
                <el-button type="primary" @click="onConfirmAdd">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script>
import { isNumberValidator } from '@/scripts/validator.js'
import { timeFormat } from '@/scripts/formatter';

export default {
    name: "AddMonetaryDialog",
    data () {
        return {
            showDialog: false,
            form: {
                name: '',
                beginningAmount: 0,
                beginningTime: '',
                currentAmount: 0,
                currentShares: 0,
                fastRedemption: false,
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
                currentShares: [
                    { required: true, message: '请输入累计投入金额', trigger: 'blur' },
                    {
                        message: '当期金额必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ]
            },

            onCancel: () => {
                this.showDialog = false;
            },

            onConfirmAdd: () => {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.form.beginningTime = timeFormat(this.form.beginningTime);
                        this.$emit('add', this.form, 'monetary-fund');
                        this.showDialog = false;
                    }
                });
            },

            edit: (row) => {
                console.log(row);
                this.form.name = row.name;
                this.form.beginningAmount = row.beginningAmount;
                this.form.beginningTime = row.beginningTime;
                this.form.currentAmount = row.currentAmount;
                this.form.currentShares = row.currentShares;
                this.form.fastRedemption = row.fastRedemption;
                this.form.holding = row.holding;
                this.showDialog = true;
            },

            show: () => {
                this.showDialog = true;
            },

            reset: () => {
                this.form.name = '';
                this.form.beginningAmount = 0;
                this.form.beginningTime = '';
                this.form.currentAmount = 0;
                this.form.currentShares = 0;
                this.form.fastRedemption = false;
                this.form.holding = true;
            }
        }
    },
}


</script>