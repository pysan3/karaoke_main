<template>
    <div>
        <p>LOGIN</p>
        <!-- hogehoge -->
    </div>
</template>

<script>
import vue from 'vue'
import axios from 'axios'
import vueaxios from 'vue-axios'

export default {
    user () {
        return {
            user_name: 'hogehoge',
            user_password: 'hogehoge',
        }
    },
    result () {
        return {
            user_found: 0,
            user_id: 0,
            result: 0}
    }
    methods: {
        tryLogin () {
            const path = 'http://localhost:5042/api/login'
            axios.post(path, user)
            .then(response => {
                this.isLogin = response.result.isLogin
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

vue.use(vue-axios, axios)

var token = 'csrf_token here'
const path = 'http://localhost:5042/api/login'

axios.post('')

import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0
    }
  },
  methods: {
    getRandom () {
      const path = 'http://localhost:5042/api/random'
      axios.get(path)
      .then(response => {
        this.randomNumber = response.data.randomNumber
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
  created () {
    this.getRandom()
  }
}
</script>