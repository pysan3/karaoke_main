<template>
  <div>
    <p>Music List</p>
    <ul>
      <li v-for="item in mList" v-bind:key="item.id">
        {{ item.song_id }}  {{ item.name }}  {{ item.singer }}
      </li>
    </ul>
    <router-link to="/musicupload"><a>music upload</a></router-link>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      mList: []
    }
  },
  methods: {
    getMusicList () {
      axios.get('http://localhost:5042/api/musiclist')
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
