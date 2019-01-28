<template>
  <div id="app">
  <!-- <div v-if="!music"> -->
    <h2>Select an music</h2>
    <input type="file" accept="audio/*" capture="microphone" id="recorder">
    <audio id="player" controls></audio>
    <button @click="onFileChange">preview</button>
  <!-- </div>
  <div v-else> -->
    <h2>data of music</h2>
    <h3>music name</h3>
    <input type="text" placeholder="music name" v-model="song_name">
    <h3>singer name</h3>
    <input type="text" placeholder="name of singer" v-model="singer">
    <button @click="upload">upload music</button>
    <button @click="removeImage">Remove music</button>
    <h1>{{ music }}</h1>
  <!-- </div> -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      user_id: 100,
      song_name: '',
      singer: '',
      resp: 0,
      file: new MediaStream()
    }
  },
  methods: {
    onFileChange () {
      var recorder = document.getElementById('recorder')
      var player = document.getElementById('player')
      var vm = this
      recorder.addEventListener('change', function (e) {
        vm.file = e.target.files[0]
        player.src = URL.createObjectURL(vm.file)
      })
    },
    upload () {
      console.log(this.file)
      var context = new AudioContext()
      var input = context.createMediaStreamSource(this.file)
      var processor = context.createScriptProcessor(1024, 1, 1)

      var connection = new WebSocket('http://localhost:5024:ws/upload')
      input.connect(processor)
      processor.connect(context.destination)
      processor.onaudioprocess = function (e) {
        var voice = e.inputBuffer.getChannelData(0)
        var data = {
          user_id: this.user_id,
          song_name: this.song_name,
          singer: this.singer,
          music: voice.buffer
        }
        connection.send(JSON.stringify(data))
      }
      if (this.resp !== -1) {
        document.location = '/'
      }
    },
    removeImage: function (e) {
      this.music = ''
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
