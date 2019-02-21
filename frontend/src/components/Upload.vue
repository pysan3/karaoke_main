<template>
  <div>
    <h2>Select an music</h2>
      <input @change="onFileChange" type="file" name="file" accept="audio/*" capture="microphone">
      <audio id="player" controls></audio>
    <div id="byte_content"></div>
    <h2>data of music</h2>
    <h3>music name</h3>
    <button @click="getRandom">New random number</button>
    <br>
    <input type="text" placeholder="music name" v-model="song_title">
    <h3>singer name</h3>
    <input type="text" placeholder="name of singer" v-model="singer">
    <button id="btn" @click="upload">upload music</button>
    <br>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
export default {
  data () {
    return {
      song_title: 'hoge',
      singer: 'fhana',
      uploadFile: null
    }
  },
  computed: mapState([
    'user_id'
  ]),
  methods: {
    onFileChange (e) {
      e.preventDefault()
      const file = e.target.files[0]
      const player = document.getElementById('player')
      player.src = URL.createObjectURL(file)
      this.song_title = file.name
      this.uploadFile = file
    },
    upload () {
      if (this.song_title.length && this.singer.length) {
        alert('name should be longer than one letter')
        return
      }
      const formData = new FormData()
      formData.append('user_id', this.user_id)
      formData.append('song_title', this.song_title)
      formData.append('singer', this.singer)
      formData.append('music', this.uploadFile)
      const config = {
        headers: {
          'context-type': 'multipart/form-data'
        }
      }
      axios.post('http://localhost:5042/api/upload', formData, config)
        .then(response => {
          document.location = '/#/sing/' + response.data.song_id
        })
        .catch(error => {
          console.log(error)
        })
    },
    getRandom () {
      const path = 'http://localhost:5042/api/random'
      axios.get(path)
        .then(response => {
          this.song_title = response.data.randomNumber
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.$store.dispatch('loggedin')
  }
}
</script>
