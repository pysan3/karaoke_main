<template>
  <div id="musiclist">
    <h3>music list</h3>
    {{ dataLists }}
    <v-client-table :column="columns" :data="dataLists">
    </v-client-table>
    <!-- <v-client-table v-if="loaded" :column="columns" :data="mList" :option="options" @row-click="onRowClick">
    </v-client-table> -->
    <br>
    <!-- <button @click="updateTable">here</button> -->
    <ul>
      <li v-for="item in mList" v-bind:key="item.id">
        <router-link v-bind:to="{name: 'singmusic', params: { song_id: item.song_id }}">{{ item.name }} {{ item.singer }}</router-link>
      </li>
    </ul>
    <button @click="debugFunctionforDebugging">here</button>
    <router-link to="/musicupload">music upload</router-link>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      columns: ['song_id', 'name', 'singer'],
      mList: [],
      dataLists: [{
        'song_id': 1,
        'name': 'sample1',
        'singer': 'sample1@example.com'
      }, {
        'song_id': 2,
        'name': 'sample2',
        'singer': 'sample2@example.com'
      }, {
        'song_id': 3,
        'name': 'sample3',
        'singer': 'sample3@example.com'
      }, {
        'song_id': 4,
        'name': 'sample4',
        'singer': 'sample4@example.com'
      }],
      options: {
        headings: {
          song_id: 'song id',
          name: 'song name',
          singer: 'singer'
        },
        sortable: ['song_id']
      }
    }
  },
  methods: {
    onRowClick (event) {
      window.location.href = `/#/sing/${event.row.id}`
    },
    updateTable () {
      axios.get('http://localhost:5042/api/musiclist')
        .then(response => {
          this.mList = []
          const list = JSON.parse(response.data)
          for (var i = 0, l = list.length; i < l; ++i) {
            const jsonData = {
              'song_id': list[i][0],
              'name': list[i][1],
              'singer': list[i][2]
            }
            this.mList.push(jsonData)
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    debugFunctionforDebugging () {
      console.log(this.mList)
      console.log(this.dataLists)
    }
  },
  created () {
    this.updateTable()
    this.debugFunctionforDebugging()
  }
}
</script>

<style>
#musiclist {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
  margin: 20px auto 0;
  /* width: 800px; */
}
</style>
