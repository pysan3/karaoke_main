<template>
  <div>
    <p>LOGIN</p>
    <p>login succeeded {{ isLogin }}</p>
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
      user_password: '000'
    }
  },
  result () {
    return {
      isFound: 0,
      user_id: 0,
      result: 0
    }
  },
  methods: {
    tryLogin () {
      axios.post('http://localhost:5042/api/login', {
        article: { user_name: 'master', user_password: '000' },
        csrf_token: 'csrf-token here'
      })
        .then(response => {
          this.isLogin = response.result.isLogin
          this.user_id = response.result.user_id
          this.result = response.result.result
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
