<template>
  <q-page class="flex flex-center" style="flex-direction: column">
    <h1 class="flex-block">
      Hello, {{ username }}
    </h1>
    <p class="text-h2 flex-block" v-if="user_type === 'http://127.0.0.1:8000'">
      Your balance:
      <q-badge class="text-h2" :label="'￥' + balance"></q-badge>
    </p>
    <q-badge class="text-h2" :label="user_type" v-if="user_type !== 'http://127.0.0.1:8000'"></q-badge>
    <q-btn v-if="user_type === 'Manager'"
           class="q-mt-md"
      size="xl"
      label="Deposit for customer"
           rounded
           color="primary"
           @click="depositDialog = true"
    ></q-btn>
    <q-dialog v-model="depositDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmit"
          style="width: 400px"
        >
          <q-select v-model="deposit_customer" :options="ids" :option-label="(item) => this.customers[this.ids.indexOf(item)]" :display-value="getName(deposit_customer)" label="Customer to deposit *" class="q-mb-lg"
            lazy-rules
                    :rules="[val => val !== null && val !== '' || 'Please select a customer',]"
          />

          <q-input
            filled
            type="number"
            v-model="deposit_num"
            label="Deposit amount *"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type deposit amount',
              val => val > 0 || 'Please type a positive deposit amount'
            ]"
          />
          <div>
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
export default {
  name: 'PageIndex',
  data () {
    return {
      loggedIn: false,
      username: '',
      user_type: '',
      balance: 0,
      depositDialog: false,
      customers: [],
      ids: [],
      deposit_customer: '',
      deposit_num: 0
    }
  }
  ,created() {
    this.loggedIn = sessionStorage.getItem('loggedIn') !== null
    if(this.loggedIn) {
      if(this.$route.path === '/' || this.$route.path === '/reg')
        this.$router.push('/index')
    }
    else {
      if(this.$route.path !== '/' && this.$route.path !== '/reg')
        this.$router.push('/')
    }
    this.user_type = sessionStorage.getItem('user_type')
    this.username = sessionStorage.getItem('loggedIn')
    let _this = this
    this.$axios.get('http://192.168.31.115:8000/api/get_deposit/' + sessionStorage.getItem('user_id')).then(function (response) {
      let res = response.data
      console.log(res)
      _this.balance = res.deposit
    })
    this.$axios.get('http://192.168.31.115:8000/api/get_all_customer').then(function (response) {
      let res = response.data
      console.log(res)
      for(let i = 0; i < res.customer_list.length; i++) {
        _this.customers.push(res.customer_list[i].customer_name)
        _this.ids.push(res.customer_list[i].id)
      }
    })
  },
  methods: {
    onSubmit() {
        let _this = this
        this.$axios.post('http://192.168.31.115:8000/api/deposit', {
          customer_id: this.deposit_customer,
          deposit: this.deposit_num
        }).then(function (response) {
          console.log(response)
          let res = response.data
          if(res.status === 'Success') {
            _this.$q.notify({
              type: 'positive',
              message: 'Successfully deposited.'
            })
            _this.depositDialog = false
          } else {
            _this.$q.notify({
              type: 'negative',
              message: 'Deposit error.'
            })
          }
        }).catch(function (error) {
          console.log(error)
          _this.$q.notify({
            type: 'negative',
            message: 'Internal error.'
          })
        })
      },
      getName(id) {
        return this.customers[this.ids.indexOf(id)]
      }
    }
}
</script>
