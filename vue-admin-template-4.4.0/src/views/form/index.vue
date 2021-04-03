<template>
  <div class="app-container">
    <el-form ref="form" :model="form" status-icon :rules="rules" label-width="120px">
      <el-form-item label="贷款总额(万)" prop="totalLoan">
        <el-input v-model="form.totalLoan" autocomplete="off" @input="checkTotalLoan($event,'totalLoan')" maxlength="11" />
      </el-form-item>

      <el-form-item label="贷款类型">
        <el-radio-group v-model="form.loanType">
          <el-radio label="1" >商业贷款</el-radio>
          <el-radio label="2" :disabled="true" >公积金贷款</el-radio>
          <el-radio label="3" :disabled="true" >组合贷款</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="还款类型">
        <el-select v-model="form.repaymentMode" placeholder="">
          <el-option label="等额本金(每月递减还款)" value="1" />
          <el-option label="等额本息(每月等额还款)" value="2" />
        </el-select>
      </el-form-item>

      <el-form-item label="还款年数">
        <el-select v-model="form.repaymentPeriod" placeholder="">
          <div v-for="(item,index) in repaymentPeriodTable" :key="index">
          <el-option  :label="item.Year+'年('+item.Month+'个月)'" :value="item.Year" />
          </div>
        </el-select>
      </el-form-item>

      <el-form-item label="首次还款日期">
        <el-date-picker v-model="form.repaymentDate" type="date" value-format="yyyy-MM-dd" prop="repaymentDate" :editable="false" :clearable="false" style="width: 100%;"  />
      </el-form-item>

      <el-form-item label="利率标准">
        <el-select v-model="form.interestRateStandard" placeholder="">
          <el-option label="LPR" value="1" />
          <el-option label="基准利率" value="2" />
        </el-select>
      </el-form-item>

      <el-form-item v-if="form.interestRateStandard =='1'" label="LPR(%)" prop="LPR">
        <el-input v-model="form.LPR" @input="checkLPR($event,'LPR')" maxlength="8" />
      </el-form-item>

      <el-form-item v-if="form.interestRateStandard =='1'" label="基点(‱)" prop="basePoint">
        <el-input v-model="form.basePoint" @input="checkBasePoint($event,'basePoint')" maxlength="8" />
      </el-form-item>

      <el-form-item v-if="form.interestRateStandard =='1'" label="贷款利率">
        <span>{{showInterestRateStandard}}</span>
      </el-form-item>

      <el-form-item v-if="form.interestRateStandard =='2'" label="贷款利率">
        <el-select v-model="form.baseInterestRate" placeholder="">
          <el-option label="7折(3.43%)" value="3.43" />
          <el-option label="8折(3.92%)" value="3.92" />
          <el-option label="8.3折(4.067%)" value="4.067" />
          <el-option label="8.5折(4.165%)" value="4.165" />
          <el-option label="8.8折(4.312%)" value="4.312" />
          <el-option label="9折(4.41%)" value="4.41" />
          <el-option label="9.5折(4.655%)" value="4.655" />
          <el-option label="基准利率(4.9%)" value="4.9" />
          <el-option label="1.05倍(5.145%)" value="5.145" />
          <el-option label="1.1倍(5.39%)" value="5.39" />
          <el-option label="1.15倍(5.635%)" value="5.635" />
          <el-option label="1.2倍(5.88%)" value="5.88" />
          <el-option label="1.25倍(6.125%)" value="6.125" />
          <el-option label="1.3倍(6.37%)" value="6.37" />
          <el-option label="1.35倍(6.615%)" value="6.615" />
          <el-option label="1.4倍(6.86%)" value="6.86" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm()">计算</el-button>
        <el-button @click="resetForm('form')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { showLoanList } from '@/api/showLoanList'
import { title } from '@/settings';
 function changeDate(dateA) {
  var dateee = new Date(dateA).toJSON();
  var date = new Date(+new Date(dateee)+8*3600*1000).toISOString().replace(/T/g,' ').replace(/\.[\d]{3}Z/,'').match(/^\d{4}-\d{2}-\d{2}/g)[0]|| "";;
  return date;
 };
export default {
  data() {
    var checkempty = (rule, value, callback) => {
      if ((!value)||(value == null)) {
        return callback(new Error('不能为空'));
      }
      else
        callback();
    };
    var checkDate = (rule, value, callback) => {
      if ((value == "")||(value == null)) {
        return callback(new Error('不能为空'));
      }
      else
        callback();
    };
    return {
      
      repaymentPeriodTable: [
        { Year:'1', Month:'12'}, {Year:'2',Month:'24'}, {Year:'3',Month:'36'}, {Year:'4',Month:'48'}, {Year:'5',Month:'60'},
        { Year:'6', Month:'72'}, {Year:'7',Month:'84'}, {Year:'8',Month:'96'}, {Year:'9',Month:'108'}, {Year:'10',Month:'120'},
        { Year:'11', Month:'132'}, {Year:'12',Month:'144'}, {Year:'13',Month:'156'}, {Year:'14',Month:'168'}, {Year:'15',Month:'180'},
        { Year:'16', Month:'192'}, {Year:'17',Month:'204'}, {Year:'18',Month:'216'}, {Year:'19',Month:'228'}, {Year:'20',Month:'240'},
        { Year:'21', Month:'252'}, {Year:'22',Month:'264'}, {Year:'23',Month:'276'}, {Year:'24',Month:'288'}, {Year:'25',Month:'300'},
        { Year:'26', Month:'312'}, {Year:'27',Month:'324'}, {Year:'28',Month:'336'}, {Year:'29',Month:'348'}, {Year:'30',Month:'360'},

      ],
      form: {
        totalLoan: '',
        loanType: '1',
        repaymentMode: '1',
        repaymentPeriod: '20',
        repaymentDate: changeDate(new Date()),
        interestRateStandard: '1',
        LPR: '4.65',
        basePoint: '0',
        baseInterestRate: '4.9',  
      },
      rules: {
        totalLoan: [
          { required: true, message: '请输入贷款总额',},
          {validator: checkempty},
        ],
        repaymentDate: [
          { type: 'string', required: true, message: '请输入首次还款日期',},
          {validator: checkDate},
        ],
        LPR: [
          { required: true, message: '请输入LPR', trigger: 'blur' },
          { required: true, message: '请输入LPR', trigger: 'change' },
          {validator: checkempty},
        ],
        basePoint: [
          { required: true, message: '请输入基点', trigger: 'blur' },
          { required: true, message: '请输入基点', trigger: 'change' },
          {validator: checkempty},
        ],

      },
    };
  },
  computed: {
    showInterestRateStandard: function () {
      var $a = this.form.LPR;
      var $b = this.form.basePoint;
      var $c = Number($a) +Number($b)*0.01;
      return $a + '% + ' + $b +'‱ = ' + $c.toFixed(6).replace(/[.]?0+$/g,"") +'%'
    }
  },
  methods: {
    checkTotalLoan(value, name) {
      this.form[name] =
        ("" + value) // 第一步：转成字符串
          .replace(/[^\d^\.]+/g, "") // 第二步：把不是数字，不是小数点的过滤掉
          .replace(/^0+(\d)/, "$1") // 第三步：第一位0开头，0后面为数字，则过滤掉，取后面的数字
          .replace(/^\./, "0.") // 第四步：如果输入的第一位为小数点，则替换成 0. 实现自动补全
          .match(/^\d*(\.?\d{0,2})/g)[0] || ""; // 第五步：最终匹配得到结果 以数字开头，只有一个小数点，而且小数点后面只能有0到2位小数
    },
    checkLPR(value, name) {
      this.form[name] =
        ("" + value) // 第一步：转成字符串
          .replace(/[^\d^\.]+/g, "") // 第二步：把不是数字，不是小数点的过滤掉
          .replace(/^0+(\d)/, "$1") // 第三步：第一位0开头，0后面为数字，则过滤掉，取后面的数字
          .replace(/^\./, "0.") // 第四步：如果输入的第一位为小数点，则替换成 0. 实现自动补全
          .match(/^\d*(\.?\d{0,4})/g)[0] || ""; // 第五步：最终匹配得到结果 以数字开头，只有一个小数点，而且小数点后面只能有0到2位小数
    },
    checkBasePoint(value, name) {
      this.form[name] =
        ("" + value) // 第一步：转成字符串
          .replace(/[^\d^\.]+/g, "") // 第二步：把不是数字，不是小数点的过滤掉
          .replace(/^0+(\d)/, "$1") // 第三步：第一位0开头，0后面为数字，则过滤掉，取后面的数字
          .replace(/^\./, "0.") // 第四步：如果输入的第一位为小数点，则替换成 0. 实现自动补全
          .match(/^\d*(\.?\d{0,4})/g)[0] || ""; // 第五步：最终匹配得到结果 以数字开头，只有一个小数点，而且小数点后面只能有0到2位小数
    },
    onSubmit() {
      this.$message('submit!')
    },
    submitForm: function() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.$options.methods.showList.bind(this)();
        } else {
          return false;
        }
      });
    },
    showList: function(){
      let arr=[]
      showLoanList(this.$data.form).then((response) =>{
        //console.log(response);
        //console.log(response.data);
        //console.log(response.data.title);
        //console.log(response.data.result);
        //console.log(response.data.repaymentDate);
        this.$router.push({ 
          name:'Test',
          params:{
            title: response.data.title,
            totalLoan: response.data.totalLoan,
            loanType: response.data.loanType,
            repaymentMode: response.data.repaymentMode,
            repaymentPeriod: response.data.repaymentPeriod,
            repaymentDate: response.data.repaymentDate,
            interestRateStandard: response.data.interestRateStandard,
            LPR: response.data.LPR,
            basePoint: response.data.basePoint,
            baseInterestRate: response.data.baseInterestRate,
            repaymentPeriod: response.data.repaymentPeriod,
            monthPrincipalPayment: response.data.monthPrincipalPayment,
            monthInterestPayment: response.data.monthInterestPayment,
            currentRemaining: response.data.currentRemaining,
          }  
          })
          
        
      }).catch((err)=>{
        console.log(err);
      })
    },
    
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    resetForm(formName) {
        this.$refs[formName].resetFields();
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

