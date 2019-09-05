<template>
  <div>
    <p>Home page</p>
    <p>Random number from backend:{{randomNumber}}</p>
    <button @click="getRandom">New random number</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0
    }
  },

  methods: {
    getRandomInt (min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },

    getRandonFromBackend () {
      const path = [`http://localhost:5000/api/random`]

      axios.get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber
          console.log(this.randomNumber)
        })
        .catch(error => {
          console.log('----------')
          console.log(error)
        })
    },
    getRandom () {
      /**
      this.randomNumber = this.getRandomInt(1, 100)
       */
      this.randomNumber = this.getRandonFromBackend()
    }
  },
  created () {
    this.getRandom()
  }
}
</script>

<style scoped>

</style>
