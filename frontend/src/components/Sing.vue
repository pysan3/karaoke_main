<template>
  <div>
    <button id='btn'>press here</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      song_id: 'trumpet'
    }
  },
  methods: {
    getMusic (context) {
      const request = new XMLHttpRequest()
      request.responseType = 'arraybuffer'
      request.onreadystatechange = () => {
        console.log(request.response)
        if (request.readyState === 4) {
          if (request.status === 0 || request.status === 200) {
            context.decodeAudioData(request.response).then(buffer => {
              const btn = document.getElementById('btn')
              btn.onclick = () => {
                playSound(buffer)
              }
            })
          }
        }
      }
      const playSound = buffer => {
        const p = navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        const src = context.createBufferSource()
        src.buffer = buffer
        src.connect(context.destination)
        src.start(0)
        p.then(stream => {
          src.onended = () => {
            stream.getAudioTracks()[0].stop()
            console.log('stream ended')
          }
          handleSuccess(stream)
        })
      }
      const handleSuccess = stream => {
        const wsContext = new AudioContext()
        const input = wsContext.createMediaStreamSource(stream)
        const processor = wsContext.createScriptProcessor(1024, 1, 1)
        const connection = new WebSocket('ws://localhost:5042/ws')
        input.connect(processor)
        processor.connect(wsContext.destination)
        processor.onaudioprocess = e => {
          const voice = e.inputBuffer.getChannelData(0)
          connection.send(voice.buffer)
        }
      }
      // const accessURL = 'http://localhost:5042/audio/load_music/' + this.song_id
      request.open('GET', './assets/4.wav', true)
      request.send()
    }
  },
  created () {
    window.AudioContext = window.AudioContext || window.webkitAudioContext
    const context = new AudioContext()
    this.getMusic(context)
  }
}
</script>
