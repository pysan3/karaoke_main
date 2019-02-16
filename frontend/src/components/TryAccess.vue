<template>
  <div>
    <h2>{{ accessType }}</h2>
    <input type="text" placeholder="Username" v-model="user_name">
    <input type="password" placeholder="Password" v-model="user_password">
    <button @click="tryAccess">{{ accessType }}!!</button>
    <p>{{ msg }}
      <button @click="accessOpposite">{{ opposite }}</button>
    </p>
    <p>signup user_name {{ user_name }}</p>
    <p>signup password {{ user_password }}</p>
    <p>signup result {{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import * as types from '@/store/mutation-types'
import { mapState } from 'vuex'
export default {
  data () {
    return {
      accessType: this.$route.params.accessType,
      user_name: '',
      user_password: '',
      msg: '',
      opposite: ''
    }
  },
  computed: mapState([
    'user_id'
  ]),
  methods: {
    tryAccess () {
      if (this.user_name.length * this.user_password.length === 0) {
        alert('should not be zero charactors')
        return
      }
      axios.post('http://localhost:5042/api/' + this.accessType, {
        user_name: this.user_name,
        user_password: this.user_password
      })
        .then(response => {
          const responseId = response.data.user_id - 0
          if (responseId !== -1) {
            this.$store.commit(types.USER_ID, responseId)
            window.location.href = '/#/user'
          } else {
            alert(response.data.msg)
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    accessOpposite () {
      [this.accessType, this.opposite] = [this.opposite, this.accessType]
      window.location.href = '/#/tryaccess/' + this.accessType
    }
  },
  created () {
    if (this.accessType === 'login') {
      this.msg = 'make a new account'
      this.opposite = 'signup'
    } else if (this.accessType === 'signup') {
      this.msg = 'already have an account'
      this.opposite = 'login'
    } else {
      alert('url broken')
      window.location.href = '/'
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
