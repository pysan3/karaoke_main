<template>
  <div id="app">
    <p>Music List</p>
    <ul>
      <li v-for="item in mList" v-bind:key="item.id">
        {{ item.id }}  {{ item.name }}
      </li>
    </ul>
    <router-link to="/api/musicupload"><a>music upload</a></router-link>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_id: 100,
      mList: []
    }
  },
  methods: {
    getMusicList () {
      axios.post('http://localhost:5042/api/musiclist', {
        user_id: this.user_id
      })
        .then(response => {
          this.mList = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getMusicList()
  }
}
</script>
