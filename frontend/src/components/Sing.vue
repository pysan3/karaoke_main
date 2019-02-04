<template>
  <div id="app">
  <!-- <div v-if="!music"> -->
    <h2>Select an music</h2>
    <input type="file" accept="audio/*" capture="microphone" id="recorder" @click="onFileChange">
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
export default {
  data () {
    return {
      user_id: 100,
      song_name: '',
      singer: ''
    }
  },
  methods: {
    onFileChange () {
      var recorder = document.getElementById('recorder')
      var player = document.getElementById('player')
      recorder.addEventListener('change', function (e) {
        player.src = URL.createObjectURL(e.target.files[0])
      })
    },
    upload () {
      var file = document.getElementById('recorder').files[0]
      var vm = this
      var counter = 0
      var chunkSIZE = 1024
      var connection = new WebSocket('ws://localhost:8000/websocket')
      connection.onmessage = function (event) {
        var result = JSON.parse(event.data).success
        if (result === -1) {
          document.location = '/#/api/musicupload'
        } else if (result === parseInt(file.size / chunkSIZE)) {
          connection.close()
          document.location = '/#/api/musiclist'
        }
      }
      for (var start = 0; start < file.size; start += chunkSIZE) {
        var stop = Math.min(start + chunkSIZE, file.size)
        var reader = new FileReader()
        reader.onloadend = function (evt) {
          var numArr = new Uint8Array(evt.target.result)
          var charList = ''
          ++counter
          for (var j = 0; j < numArr.length; ++j) {
            // check if right digit
            charList += numArr[j]
          }
          if (evt.target.readyState === FileReader.DONE) {
            var data = {
              loaded_data: counter,
              user_id: vm.user_id,
              song_name: vm.song_name,
              singer: vm.singer,
              music: charList
            }
            connection.send(JSON.stringify(data))
          }
        }
        var blob = file.slice(start, stop)
        reader.readAsArrayBuffer(blob)
      }
    }
  }
}
</script>

<style scoped>
#app {
  text-align: center;
}
img {
  width: 30%;
  margin: auto;
  display: block;
  margin-bottom: 10px;
}
</style>
