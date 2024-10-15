<template>
    <el-dialog v-model="showDialog" title="添加基金项目" @closed="reset" width="300px">
        <el-form :model="form" :rules="rules" ref="form">
            <el-form-item label="代码" prop="symbol">
                <el-input v-model="form.symbol">
                    <template #append>
                        <el-button @click="onSearchClick" v-if="currentSymbolState === SearchSymbolState.INIT">
                            <el-icon>
                                <search />
                            </el-icon>
                        </el-button>
                        <el-icon v-else-if="currentSymbolState === SearchSymbolState.SEARCHING">
                            <loading />
                        </el-icon>
                        <el-icon v-else>
                            <check />
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>
            <el-form-item label="名称" prop="name">
                <el-input v-model="form.name" disabled></el-input>
            </el-form-item>
            <el-form-item label="当期份额" prop="currentShares">
                <el-input v-model="form.currentShares"></el-input>
            </el-form-item>
            <el-form-item label="当期净值" prop="currentNetValue">
                <el-input v-model="form.currentNetValue"></el-input>
            </el-form-item>
            <el-form-item label="分红比例" prop="dividendRatio">
                <el-input v-model="form.dividendRatio"></el-input>
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
import { Search, Loading, Check } from '@element-plus/icons-vue';
import { isNumberValidator, isIntegerValidator } from '@/scripts/validator.js';
import {
    getFundNameRequest,
    getRefreshedFundNetValueRequest
} from '@/scripts/requests.js';


export default {
    name: "AddFundDialog",
    data () {
        return {
            showDialog: false,
            SearchSymbolState: {
                INIT: 'init',
                SEARCHING: 'searching',
                FOUND: 'found',
            },
            currentSymbolState: 'init',
            form: {
                symbol: '',
                name: '',
                currentShares: 0,
                currentNetValue: 0,
                lockupPeriod: 180,
                dividendRatio: 0.0,
                holding: true
            },
            rules: {
                symbol: [
                    { required: true, message: '请输入基金代码', trigger: 'blur' },
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
                dividendRatio: [
                    { required: true, message: '请输入分红比例', trigger: 'blur' },
                    {
                        message: '分红比例必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ],
                lockupPeriod: [
                    { required: true, message: '请输入锁定期', trigger: 'blur' },
                    {
                        message: '锁定期必须为整数值', trigger: 'blur', validator: isIntegerValidator
                    }
                ]
            },

            onSearchClick: async () => {
                console.log(this.form.symbol);
                if (this.form.symbol === '') {
                    return;
                }
                this.currentSymbolState = this.SearchSymbolState.SEARCHING;
                const data = await getFundNameRequest(this.form.symbol);
                const fund_name = data.fund_name;
                console.log(fund_name);

                const netValueData = await getRefreshedFundNetValueRequest([this.form.symbol]);
                console.log(netValueData);

                const netValue = netValueData.refresh.find(item => item.symbol === this.form.symbol).value;
                console.log(netValue);

                this.form.name = fund_name;
                this.form.currentNetValue = netValue;
                this.currentSymbolState = this.SearchSymbolState.FOUND;
            },

            onCancel: () => {
                this.showDialog = false;
                this.currentSymbolState = this.SearchSymbolState.INIT;
            },

            onConfirmAdd: () => {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$emit('add', this.form, 'fund');
                        this.showDialog = false;
                        this.currentSymbolState = this.SearchSymbolState.INIT;
                    }
                });
            },

            edit: (row) => {
                console.log(row);
                this.form.name = row.name;
                this.form.symbol = row.symbol;
                this.form.currentShares = row.currentShares;
                this.form.currentNetValue = row.currentNetValue;
                this.form.lockupPeriod = row.residualLockupPeriod;
                this.form.holding = row.holding;
                this.form.dividendRatio = 0;
                this.showDialog = true;
                this.currentSymbolState = this.SearchSymbolState.FOUND;
            },

            show: () => {
                this.showDialog = true;
                this.currentSymbolState = this.SearchSymbolState.INIT;
            },

            reset: () => {
                this.form.name = '';
                this.form.symbol = '';
                this.form.currentNetValue = 0;
                this.form.currentShares = 0;
                this.form.lockupPeriod = 180;
                this.form.dividendRatio = 0.0;
                this.form.holding = true;
            }
        }
    },
    mounted () {

    },
    components: {
        Search,
        Loading,
        Check
    }
}


</script>