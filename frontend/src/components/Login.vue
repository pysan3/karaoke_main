<template>
  <div class="login">
    <p>LOGIN</p>
    <h2>log in</h2>
    <input type="text" placeholder="Username" v-model="user_name">
    <input type="password" placeholder="Password" v-model="user_password">
    <button @click="tryLogin">Register</button>
    <p>Do you have an account?
      <router-link to="/api/signup">sign up now!!</router-link>
    </p>
    <p>login succeeded {{ isFound }}</p>
    <p>login user_id {{ user_id }}</p>
    <p>login user_name {{ user_name }}</p>
    <p>login msg {{ msg }}</p>
    <!-- hogehoge -->
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_name: '',
      user_password: '',
      isFound: 0,
      user_id: 0,
      msg: ''
    }
  },
  methods: {
    tryLogin () {
      axios.post('http://localhost:5042/api/login', {
        user_name: this.user_name,
        user_password: this.user_password
      })
        .then(response => {
          this.isFound = response.data.isFound
          this.user_id = response.data.user_id
          this.msg = response.data.msg
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

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.login {
  margin-top: 20px;

  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  align-items: center
}
input {
  margin: 10px 0;
  padding: 10px;
}
</style>
