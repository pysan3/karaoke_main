<template>
  <div id="app">
    <div v-if="!music">
      <h2>Select an music</h2>
      <input type="file" accept="audio/*" capture="microphone" id="recorder">
      <audio id="player" controls></audio>
    </div>
    <div v-else>
      <h2>data of music</h2>
      <h3>music name</h3>
      <input type="text" placeholder="music name" v-model="song_name">
      <h3>singer name</h3>
      <input type="text" placeholder="name of singer" v-model="singer">
      <img :src="music" />
      <button @click="upload">upload music</button>
      <button @click="removeImage">Remove music</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user_id: 100,
      song_name: '',
      singer: '',
      music: '',
      resp: 0
    }
  },
  methods: {
    onFileChange (e) {
      var recorder = document.getElementById('recorder')
      var player = document.getElementById('player')
      var vm = this
      recorder.addEventListener('change', function (e) {
        var file = e.target.files[0]
        vm.createImage(file)
        player.src = URL.createObjectURL(file)
      })
    },
    createImage (file) {
      var reader = new FileReader()
      reader.onload = (e) => {
        this.music = e.target.result
      }
      reader.readAsDataURL(file)
    },
    upload () {
      axios
        .post('http://localhost:5042/api/upload', {
          user_id: this.user_id,
          song_name: this.song_name,
          singer: this.singer,
          music: this.music
        })
        .then(response => {
          this.resp = response.data.success
        })
        .catch(error => {
          console.log(error)
        })
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
<script>
  var recorder = document.getElementById('recorder');
  var player = document.getElementById('player')

  recorder.addEventListener('change', function(e) {
    var file = e.target.files[0];
    // Do something with the audio file.
    player.src =  URL.createObjectURL(file);
  });
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
