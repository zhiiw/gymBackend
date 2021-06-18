<template>
  <q-page class="flex flex-center" style="flex-direction: column">
    <p class="text-subtitle1"></p>
    <ve-line :data="registerData" width="800px"></ve-line>
    <ve-histogram :data="customerData" width="800px"></ve-histogram>
    <ve-line :data="maintainData" width="800px"></ve-line>
  </q-page>
</template>

<script>
export default {
  name: 'Manage',
  created() {
    let _this = this
    this.$axios.get('http://127.0.0.1:8000/api/maintainence_count').then(function (response) {
      let res = response.data
      console.log(res)
      _this.maintainData.rows = res.maintainence_list
    })
    this.$axios.get('http://127.0.0.1:8000/api/register_count').then(function (response) {
      let res = response.data
      console.log(res)
      _this.registerData.rows = res.register_list
    })
    this.$axios.get('http://127.0.0.1:8000/api/get_all_customer').then(function (response) {
      let res = response.data
      console.log(res)
      _this.customerData.rows = res.customer_list
    })
  },
  data () {
    return {
      maintainData: {
        columns: ['time', 'Maintainence count'],
        rows: []
      },
      registerData: {
        columns: ['time', 'Register count'],
        rows: []
      },
      customerData: {
        columns: ['customer_name', 'deposit'],
        rows: []
      },
    }
  }
}
</script>
