<template>
    <el-dialog v-model="showDialog" title="添加定期存款项目" @closed="reset" width="300px">
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
            <el-form-item label="利率" prop="rate">
                <el-input v-model="form.rate"></el-input>
            </el-form-item>
            <el-form-item label="期限" prop="maturity">
                <el-input v-model.number="form.maturity"></el-input>
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
    name: "AddFixedDialog",
    data () {
        return {
            showDialog: false,
            form: {
                name: '',
                beginningAmount: 0,
                beginningTime: '',
                rate: 0,
                maturity: 0
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
                rate: [
                    { required: true, message: '请输入利率', trigger: 'blur' },
                    {
                        message: '利率必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ],
                maturity: [
                    { required: true, message: '请输入期限', trigger: 'blur' },
                    {
                        message: '期限必须为数字值', trigger: 'blur', type: 'number'
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
                        this.$emit('add', this.form, 'fixed-deposit');
                        this.showDialog = false;
                    }
                });
            },

            edit: (row) => {
                console.log(row);
                this.form.name = row.name;
                this.form.beginningAmount = row.beginningAmount;
                this.form.beginningTime = row.beginningTime;
                this.form.rate = row.rate;
                this.form.maturity = row.maturity;
                this.showDialog = true;
            },

            show: () => {
                this.showDialog = true;
            },

            reset: () => {
                this.form.name = '';
                this.form.beginningAmount = 0;
                this.form.beginningTime = '';
                this.form.rate = 0;
                this.form.maturity = 0;
            }
        }
    },
}


</script>