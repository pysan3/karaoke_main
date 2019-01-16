<template>
  <div>
    <p>LOGIN</p>
    <p>login succeeded {{ isFound }}</p>
    <p>login user_id {{ user_id }}</p>
    <p>login result {{ result }}</p>
    <!-- hogehoge -->
  </div>
</template>

<script>
import axios from 'axios'
export default {
  user () {
    return {
      user_name: 'master',
      user_password: 'hogehoge'
    }
  },
  data () {
    return {
      isFound: 0,
      user_id: 0,
      result: 0
    }
  },
  methods: {
    tryLogin () {
      axios.post('http://localhost:5042/api/signin', {
        user_name: 'takuto',
        user_password: '000'
      })
        .then(response => {
          this.isFound = response.data.succeed
          this.user_id = response.data.user_id
          this.result = response.data.msg
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.tryLogin()
  }
}
</script>
