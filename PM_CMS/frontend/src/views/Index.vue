<template>
<div class="index">
  <HeadNav></HeadNav>
  <LeftMenu></LeftMenu>
</div>
</template>

<script>
import HeadNav from '../components/HeadNav'
import LeftMenu from '../components/LeftMenu'
export default {
  name: 'Index',
  components: {
    LeftMenu,
    HeadNav
  }
}
</script>

<style scoped>
.index{
  width:100%;
  height: 100%;
  overflow: hidden;
}
</style>
