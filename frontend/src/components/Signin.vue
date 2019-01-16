<template>
  <div>
    <p>SIGNIN</p>
    <p>signin succeeded {{ succeed }}</p>
    <p>signin user_id {{ user_id }}</p>
    <p>signin user_name {{ user_name }}</p>
    <p>signin result {{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_name: 'takuto',
      user_password: '000',
      succeed: 0,
      user_id: 0,
      msg: 0
    }
  },
  methods: {
    trySignin () {
      axios.post('http://localhost:5042/api/signin', {
        user_name: 'takuto',
        user_password: '000'
      })
        .then(response => {
          this.succeed = response.data.succeed
          this.user_id = response.data.user_id
          this.msg = response.data.msg
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.trySignin()
  }
}
</script>
