<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Equipment list</p>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="equipments"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:top>
            <q-btn color="primary" :disable="loading" label="Add equipment" @click="addDialog = true" />
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn dense round flat color="primary" @click="onImgClick(props)" icon="image"></q-btn>
              <q-btn dense round flat color="primary" @click="onMaintain(props)" icon="engineering"></q-btn>
              <q-btn dense round flat color="red" @click="onDeleteClick(props)" icon="delete"></q-btn>
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
          <q-file filled bottom-slots v-model="new_img" label="Equipment picture *" counter
                  accept=".jpg, image/*"
                  @rejected="onImgRejected"
                  lazy-rules
                  :rules="[ val => val || 'Please upload a equipment picture']">
            <template v-slot:prepend>
              <q-icon name="cloud_upload" @click.stop />
            </template>
            <template v-slot:append>
              <q-icon name="close" @click.stop="new_img = null" class="cursor-pointer" />
            </template>
          </q-file>

          <q-input
            filled
            v-model="new_name"
            label="Equipment name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a equipment name']"
          />

          <q-input
            filled
            type="number"
            v-model="new_fee"
            label="Equipment price *"
            lazy-rules
            :rules="[
              val => val !== null && val !== '' || 'Please type equipment price',
              val => val > 0 || 'Please type a positive equipment price'
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
        Are you sure to delete equipment?
        <div>
          <q-btn label="Remove" color="red" @click="onDelete" flat v-close-popup/>
          <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="imgDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        Equipment picture:
        <q-img
        :src="show_img"
        width="200px"></q-img>
        <div>
          <q-btn label="OK" flat class="q-ml-sm" v-close-popup />
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: "Equipment",
  data () {
    return {
      loggedIn: false,
      user_type: '',
      equipments: [],
      filter: '',
      loading: true,
      addDialog: false,
      deleteDialog: false,
      imgDialog: false,
      show_img: '',
      delete_id: -1,
      new_fee: 0,
      new_name: '',
      new_img: null,
      options: [],
      columns: [
        {
          name: 'ID',
          required: true,
          label: 'Equipment ID',
          align: 'left',
          field: row => row.equipment_id,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'name',
          required: true,
          label: 'Equipment name',
          align: 'left',
          field: row => row.equipname,
          sortable: true
        },
        {
          name: 'price',
          required: true,
          label: 'Equipment price',
          align: 'left',
          field: row => row.price,
          format: val => `￥`+ val,
          sortable: true
        },
        {
          name: 'Last maintenance',
          required: true,
          label: 'Last maintenance',
          align: 'left',
          field: row => row.last_fix,
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
    this.$axios.get('http://127.0.0.1:8000/api/show_all_equipment').then(function (response) {
      let res = response.data
      console.log(res)
      _this.equipments = res.equipment_list
      console.log(_this.equipments)
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    onSubmit() {

      let reader = new FileReader()
      let _this = this

      reader.onload = function () {
        _this.$axios.post('http://127.0.0.1:8000/api/create_equipment', {
          equipname: _this.new_name,
          price: _this.new_fee,
          equipdata: reader.result
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
      }

      reader.readAsDataURL(this.new_img)
    },
    onDelete() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/delete_equipment', {
        equipment_id: this.delete_id
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
            message: 'Successfully maintained.'
          })
          _this.deleteDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Buy error.'
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
      this.delete_id = props.row.equipment_id
      this.deleteDialog = true
    },
    onMaintain(props) {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/create_maintainence', {
        equip_id: props.row.equipment_id,
        user_id: sessionStorage.getItem('user_id')
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully bought.'
          })
          _this.deleteDialog = false
          _this.$router.go(0);
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Maintain error.'
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
    onImgClick(props) {
      this.show_img = props.row.equipdata
      console.log(this.show_img)
      this.imgDialog = true
    },
    onChangeShow() {
      if(this.showAll === 'Show all') {
        this.table_data = this.classes
      } else {
        this.table_data = this.customer_classes
      }
    },
    onImgRejected() {
      this.$q.notify({
        type: 'negative',
        message: 'Error, selected file is not a image.'
      })
    },
  }
}
</script>

<style scoped>
</style>
