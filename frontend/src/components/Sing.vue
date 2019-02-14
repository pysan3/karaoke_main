<template>
  <div>
    <button id='btn'>press here</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      song_id: 3,
      musicStop: 0,
      ready: 0
    }
  },
  methods: {
    getMusic () {
      window.AudioContext = window.AudioContext || window.webkitAudioContext
      const vm = this
      let context = null
      let connection = null
      const request = new XMLHttpRequest()
      request.responseType = 'arraybuffer'
      request.onreadystatechange = () => {
        if (request.readyState === 4) {
          if (request.status === 0 || request.status === 200) {
            vm.ready = 1
            const responseData = request.response
            const btn = document.getElementById('btn')
            btn.onclick = () => {
              context = new AudioContext()
              const p = context.decodeAudioData(responseData)
              connection = new WebSocket('ws://localhost:5042/ws')
              connection.onopen = e => {
                p.then(buffer => {
                  playSound(buffer)
                })
              }
            }
          }
        }
      }
      const playSound = buffer => {
        const p = navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        const src = context.createBufferSource()
        src.buffer = buffer
        src.connect(context.destination)
        p.then(stream => {
          src.onended = () => {
            stream.getTracks().forEach(track => {
              track.stop()
            })
            stream = null
            vm.musicStop = 1
          }
          src.start(0)
          handleSuccess(stream)
        })
      }
      const handleSuccess = stream => {
        const wsContext = new AudioContext()
        const input = wsContext.createMediaStreamSource(stream)
        const processor = wsContext.createScriptProcessor(1024, 1, 1)
        input.connect(processor)
        processor.connect(wsContext.destination)
        processor.onaudioprocess = e => {
          const voice = e.inputBuffer.getChannelData(0)
          if (connection !== null) {
            connection.send(voice.buffer)
          }
        }
        function disconnect () {
          clearInterval(interval)
          connection.close(1000, 'end of music')
          connection = null
        }
        function isDone () {
          if (vm.musicStop && connection.bufferedAmount === 0) {
            disconnect()
          }
        }
        let interval = setInterval(isDone, 1000)
      }
      request.open('GET', 'http://localhost:5042/audio/load_music/' + this.song_id, true)
      request.send()
    }
  },
  created () {
    this.getMusic()
  }
}
</script>
