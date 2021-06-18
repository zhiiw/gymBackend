<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Class list</p>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="table_data"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:top>
            <q-btn v-if="user_type === 'Manager'" color="primary" :disable="loading" label="Add class" @click="addDialog = true" />

            <q-toggle
              :label="showAll"
              color="primary"
              false-value="Show mine"
              true-value="Show all"
              v-model="showAll"
              @input="onChangeShow"
            />
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn dense round flat color="primary" @click="onBuyClick(props)" icon="shopping_bag" v-if="user_type==='Student'"></q-btn>
              <q-btn dense round flat color="red" @click="onDeleteClick(props)" icon="delete" v-if="user_type==='Manager'"></q-btn>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
    <q-dialog v-model="addDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmit"
          style="width: 400px"
        >
          <q-select v-model="new_coach" :options="options" label="Coach" class="q-mb-lg" />

          <q-input
            filled
            v-model="new_type"
            label="Class type *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a class type']"
          />

          <q-input
            filled
            type="number"
            v-model="new_fee"
            label="Class fee price *"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type class fee',
              val => val > 0 || 'Please type a positive class fee'
            ]"
          />
          <div>
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
          Are you sure to delete class #{{delete_id}}?
          <div>
            <q-btn label="Remove" color="red" @click="onDelete" flat v-close-popup/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="buyDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        Are you sure to buy this class #{{buy_id}}?
        <div>
          <q-btn label="Cancel" flat class="q-ml-sm" v-close-popup />
          <q-btn label="Buy" color="primary" @click="onBuy" flat v-close-popup/>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: "Class",
  data () {
    return {
      loggedIn: false,
      user_type: '',
      table_data: [],
      classes: [],
      customer_classes: [],
      filter: '',
      loading: true,
      showAll: 'Show all',
      addDialog: false,
      deleteDialog: false,
      buyDialog: false,
      buy_id: -1,
      delete_id: -1,
      new_type: '',
      new_fee: 0,
      new_coach: '',
      options: [],
      columns: [
        {
          name: 'ID',
          required: true,
          label: 'Class ID',
          align: 'left',
          field: row => row.id,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'Coach',
          required: true,
          label: 'Coach name',
          align: 'left',
          field: row => row.coach,
          sortable: true
        },
        {
          name: 'Class price',
          required: true,
          label: 'Class fee',
          align: 'left',
          field: row => row.fee,
          format: val => `¥${val}`,
          sortable: true
        },
        {
          name: 'Class type',
          required: true,
          label: 'Class type',
          align: 'left',
          field: row => row.class_type,
          format: val => val,
          sortable: true
        },
        { name: 'actions', label: 'Actions', field: '', align:'center' }
      ],
      pagination: {
        rowsPerPage: 10
      }
    }
  },
  created() {
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
    this.loading = true
    this.$axios.get('http://127.0.0.1:8000/api/show_all_class').then(function (response) {
      let res = response.data
      console.log(res)
      for(let i = 0; i < res.class_list.length; i++) {
        _this.classes.push({
          id: res.class_list[i].class_id,
          fee: res.class_list[i].fee,
          coach: res.class_list[i].coach,
          class_type: res.class_list[i].classtype
        })
      }
      console.log(_this.classes)
      _this.$forceUpdate()
    })
    this.$axios.get('http://127.0.0.1:8000/api/get_all_coach').then(function (response) {
      let res = response.data
      for(let i = 0; i < res.coach_list.length; i++) {
        _this.options.push(res.coach_list[i].coach_name)
      }
      _this.new_coach = _this.options[0]
      console.log(_this.options)
      _this.$forceUpdate()
    })
    this.$axios.post('http://127.0.0.1:8000/api/customer_class',{
        customer_id: sessionStorage.getItem('user_id')
    }).then(function (response) {
      let res = response.data
      for(let i = 0; i < res.class_list.length; i++) {
        _this.customer_classes.push({
          id: res.class_list[i].class_id,
          fee: res.class_list[i].fee,
          coach: res.class_list[i].coach,
          class_type: res.class_list[i].classtype
        })
      }
      console.log(_this.customer_classes)
      _this.$forceUpdate()
    })
    this.table_data = this.classes
    this.loading = false
  },
  methods: {
    onSubmit() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/create_class', {
        class_type: this.new_type,
        coach: this.new_coach,
        fee: this.new_fee
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully added.'
          })
          _this.addDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Add error.'
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
    onDelete() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/delete_class', {
        class_id: this.delete_id
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully removed.'
          })
          _this.deleteDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Remove error.'
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
    onBuy() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/buy_class', {
        class_id: this.buy_id,
        customer_id: sessionStorage.getItem('user_id')
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully bought.'
          })
          _this.deleteDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Buy error.' + res.message
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
    onDeleteClick(props) {
      this.delete_id = props.row.id
      this.deleteDialog = true
    },
    onBuyClick(props) {
      this.buy_id = props.row.id
      this.buyDialog = true
    },
    onChangeShow() {
      if(this.showAll === 'Show all') {
        this.table_data = this.classes
      } else {
        this.table_data = this.customer_classes
      }
    }
  }
}
</script>

<style scoped>
</style>
