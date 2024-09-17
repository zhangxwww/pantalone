<template>
    <el-dialog v-model="showDialog" title="添加基金项目" @closed="reset" width="300px">
        <el-form :model="form" :rules="rules" ref="form">
            <el-form-item label="名称" prop="name">
                <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="当期份额" prop="currentShares">
                <el-input v-model="form.currentShares"></el-input>
            </el-form-item>
            <el-form-item label="当期净值" prop="currentNetValue">
                <el-input v-model="form.currentNetValue"></el-input>
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
                <el-button @click="onCancel">取消</el-button>
                <el-button type="primary" @click="onConfirmAdd">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script>
import { isNumberValidator, isIntegerValidator } from '@/scripts/validator.js'

export default {
    name: "AddFundDialog",
    data () {
        return {
            showDialog: false,
            form: {
                name: '',
                currentShares: 0,
                currentNetValue: 0,
                lockupPeriod: 180,
                holding: true
            },
            rules: {
                name: [
                    { required: true, message: '请输入名称', trigger: 'blur' }
                ],
                currentShares: [
                    { required: true, message: '请输入当期份额', trigger: 'blur' },
                    {
                        message: '当期份额必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ],
                currentNetValue: [
                    { required: true, message: '请输入当期净值', trigger: 'blur' },
                    {
                        message: '当期净值必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ],
                lockupPeriod: [
                    { required: true, message: '请输入锁定期', trigger: 'blur' },
                    {
                        message: '锁定期必须为整数值', trigger: 'blur', validator: isIntegerValidator
                    }
                ]
            },

            onCancel: () => {
                this.showDialog = false;
            },

            onConfirmAdd: () => {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$emit('add', this.form, 'fund');
                        this.showDialog = false;
                    }
                });
            },

            edit: (row) => {
                console.log(row);
                this.form.name = row.name;
                this.form.currentShares = row.currentShares;
                this.form.currentNetValue = row.currentNetValue;
                this.form.lockupPeriod = row.residualLockupPeriod;
                this.form.holding = row.holding;
                this.showDialog = true;
            },

            show: () => {
                this.showDialog = true;
            },

            reset: () => {
                this.form.name = '';
                this.form.currentNetValue = 0;
                this.form.currentShares = 0;
                this.form.lockupPeriod = 180;
                this.form.holding = true;
            }
        }
    },
}


</script>