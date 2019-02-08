<template>
  <div class="signup">
    <p>SIGNUP</p>
    <h2>Sign up</h2>
    <input type="text" placeholder="Username" v-model="user_name">
    <input type="password" placeholder="Password" v-model="user_password">
    <button @click="trySignup">Register</button>
    <p>Do you have an account?
      <router-link to="/login">log in now!!</router-link>
    </p>
    <p>signup succeeded {{ succeed }}</p>
    <p>signup user_id {{ user_id }}</p>
    <p>signup user_name {{ user_name }}</p>
    <p>signup result {{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_name: '',
      user_password: '',
      succeed: 0,
      user_id: 0,
      msg: 0
    }
  },
  methods: {
    trySignup () {
      axios.post('http://localhost:5042/api/signup', {
        user_name: this.user_name,
        user_password: this.user_password
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
    this.trySignup()
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
.signup {
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
