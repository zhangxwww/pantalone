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
            <el-form-item label="币种" prop="currency">
                <el-select v-model="form.currency">
                    <el-option label="CNY" value="CNY" />
                    <el-option label="USD" value="USD" />
                </el-select>
            </el-form-item>
            <el-form-item v-if="form.currency !== 'CNY'" label="现汇买入价" prop="currencyRate">
                <el-input v-model="form.currencyRate">
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
import { Search, Loading, Check } from '@element-plus/icons-vue';
import { isNumberValidator } from '@/scripts/validator.js'
import { timeFormat } from '@/scripts/formatter';
import { getLatestCurrencyRate } from '@/scripts/requests';

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
                currency: 'CNY',
                currencyRate: 1.0,
                fastRedemption: false,
                holding: true
            },
            SearchSymbolState: {
                INIT: 'init',
                SEARCHING: 'searching',
                FOUND: 'found',
            },
            currentSymbolState: 'init',
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
                ],
                currencyRate: [
                    { required: true, message: '请输入现汇买入价', trigger: 'blur' },
                    {
                        message: '现汇买入价必须为数字值', trigger: 'blur', validator: isNumberValidator
                    }
                ]
            },

            onSearchClick: async () => {
                this.currentSymbolState = this.SearchSymbolState.SEARCHING;
                const resp = await getLatestCurrencyRate(this.form.currency);
                this.form.currencyRate = resp.rate;
                this.currentSymbolState = this.SearchSymbolState.FOUND;
            },

            onCancel: () => {
                this.showDialog = false;
                this.currentSymbolState = this.SearchSymbolState.INIT;
            },

            onConfirmAdd: () => {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.form.beginningTime = timeFormat(this.form.beginningTime);
                        this.$emit('add', this.form, 'monetary-fund');
                        this.showDialog = false;
                        this.currentSymbolState = this.SearchSymbolState.INIT;
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
                this.form.currency = row.currency;
                this.form.currencyRate = row.currencyRate;
                this.form.fastRedemption = row.fastRedemption;
                this.form.holding = row.holding;
                this.showDialog = true;
                this.currentSymbolState = this.SearchSymbolState.FOUND;
            },

            show: () => {
                this.showDialog = true;
                this.currentSymbolState = this.SearchSymbolState.INIT;
            },

            reset: () => {
                this.form.name = '';
                this.form.beginningAmount = 0;
                this.form.beginningTime = '';
                this.form.currentAmount = 0;
                this.form.currentShares = 0;
                this.form.currency = 'CNY';
                this.form.currencyRate = 1.0;
                this.form.fastRedemption = false;
                this.form.holding = true;
            }
        }
    },
    components: {
        Search,
        Loading,
        Check
    }
}


</script>