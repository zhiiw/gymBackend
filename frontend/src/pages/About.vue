<template>
  <q-card class="my-card q-mx-auto q-my-xl flex-center" style="width: 40%;flex-direction: column">
    <img src="https://i.loli.net/2021/06/18/NQaJHBhSGRYxDgv.jpg">

    <q-list>
      <q-item clickable>
        <q-item-section avatar>
          <q-icon color="primary" name="local_bar" />
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h6">Position</q-item-label>
          <q-item-label class="text-subtitle1" caption>Apple St. 1023, Shanghai, China.</q-item-label>
        </q-item-section>
      </q-item>

      <q-item clickable>
        <q-item-section avatar>
          <q-icon color="red" name="phone" />
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h6">Contact</q-item-label>
          <q-item-label class="text-subtitle1" caption>+86 12345678910</q-item-label>
        </q-item-section>
      </q-item>

      <q-item clickable>
        <q-item-section avatar>
          <q-icon color="amber" name="email" />
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h6">Email</q-item-label>
          <q-item-label class="text-subtitle1" caption>gym@qq.cm</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>

<script>
export default {
  name: "About"
}
</script>

<style scoped>

</style>
