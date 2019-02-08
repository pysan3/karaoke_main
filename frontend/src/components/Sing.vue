<template>
  <div>
    <button @click="sing">press here</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      song_id: 1,
      musicdata: null
    }
  },
  methods: {
    sleep (msec) {
      return new Promise(function (resolve) {
        setTimeout(function () {
          resolve()
        }, msec)
      })
    },
    sing () {
      const vm = this
      const handleSuccess = stream => {
        const context = new AudioContext()
        const input = context.createMediaStreamSource(stream)
        const processor = context.createScriptProcessor(1024, 1, 1)
        const connection = new WebSocket('ws://localhost:5042/ws')
        input.connect(processor)
        processor.connect(context.destination)
        processor.onaudioprocess = e => {
          let voice = e.inputBuffer.getChannelData(0)
          connection.send(voice.buffer)
        }
      }
      const p = navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      p.then(handleSuccess)
    },
    getMusic () {
      window.AudioContext = window.AudioContext || window.webkitAudioContext
      const vm = this
      const context = new AudioContext()
      const loadAudio = url => {
        const request = new XMLHttpRequest()
        request.open('GET', url, true)
        request.responseType = 'arraybuffer'
        request.onload = () => {
          context.decodeAudioData(request.response, function (buffer) {
            vm.musicdata = buffer
          }, onerror)
        }
        request.send()
      }
      loadAudio('http://localhost:5042/getmusic/' + this.song_id)
    },
    created () {
      this.getMusic()
    }
  }
}
</script>
