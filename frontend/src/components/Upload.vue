<template>
  <div>
  <!-- <div v-if="!music"> -->
    <h2>Select an music</h2>
      <input @change="onFileChange" type="file" name="file" accept="audio/*" capture="microphone">
      <audio id="player" controls></audio>
    <div id="byte_content"></div>
  <!-- </div>
  <div v-else> -->
    <h2>data of music</h2>
    <h3>music name</h3>
    <input type="text" placeholder="music name" v-model="song_name">
    <h3>singer name</h3>
    <input type="text" placeholder="name of singer" v-model="singer">
    <button id="btn" @click="upload">upload music</button>
  <!-- </div> -->
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_id: 100,
      song_name: 'hoge',
      singer: 'hoge',
      uploadFile: null,
      resp: 0
    }
  },
  methods: {
    onFileChange (e) {
      e.preventDefault()
      const file = e.target.files[0]
      const player = document.getElementById('player')
      player.src = URL.createObjectURL(file)
      this.uploadFile = file
    },
    upload () {
      let formData = new FormData()
      formData.append('user_id', this.user_id)
      formData.append('song_name', this.song_name)
      formData.append('singer', this.singer)
      formData.append('music', this.uploadFile)
      let config = {
        headers: {
          'context-type': 'multipart/form-data'
        }
      }
      console.log(...formData.entries())
      axios.post('http://localhost:5042/api/upload', formData, config)
        .then(response => {
          console.log('got response')
          this.resp = response.data.success
          console.log(this.resp)
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
