<template>
  <div class="login">
    <p>LOGIN</p>
    <h2>log in</h2>
    <input type="text" placeholder="Username" v-model="user_name">
    <input type="password" placeholder="Password" v-model="user_password">
    <button @click="tryLogin">Register</button>
    <p>Do you have an account?
      <router-link to="/signup">sign up now!!</router-link>
    </p>
    <p>login succeeded {{ isFound }}</p>
    <p>login user_id {{ user_id }}</p>
    <p>login user_name {{ user_name }}</p>
    <p>login msg {{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_name: '',
      user_password: '',
      user_id: -1
    }
  },
  methods: {
    tryLogin () {
      if (this.user_name.length * this.user_password.length === 0) {
        alert('should not be zero charactors')
        return
      }
      axios.post('http://localhost:5042/api/login', {
        user_name: this.user_name,
        user_password: this.user_password
      })
        .then(response => {
          if ((this.user_id = response.data.user_id) !== -1) {
            window.location.href = '/'
          } else if (this.user_name.length !== 0) {
            alert(response.data.msg)
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    if (this.user_name.length !== 0) {
      this.tryLogin()
    }
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
