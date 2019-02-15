<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'App',
  methods: {
    loggedin () {
      const request = new XMLHttpRequest()
      request.responseType = 'text'
      request.onload = () => {
        if (request.responseText === '0') {
          window.location.href = '/'
        }
      }
      request.open('GET', 'http://localhost:5042/api/loggedin/' + this.user_id, true)
      request.send()
    }
  },
  computed: mapState([
    'user_id'
  ]),
  created () {
    this.loggedin()
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
