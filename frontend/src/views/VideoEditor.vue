<template>
  <div class="video-editor">
    <div v-if="loading" class="loading">
      <p>Carregando...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="!currentFile" class="not-found">
      <p>Vídeo não encontrado</p>
      <button @click="$router.push('/')">Voltar para Home</button>
    </div>
    
    <div v-else class="editor-container">
      <div class="editor-header">
        <h2>Editor de Vídeo: {{ getFileName(currentFile.original_file) }}</h2>
        <button @click="$router.push('/')">Voltar para Home</button>
      </div>
      
      <div class="editor-content">
        <div class="video-container card">
          <video 
            ref="videoElement" 
            controls 
            :src="getVideoUrl(currentFile.processed_file || currentFile.original_file)"
            @loadedmetadata="onVideoLoaded"
          ></video>
        </div>
        
        <div class="controls-container">
          <div class="filter-controls card">
            <h3>Filtros</h3>
            <div class="filter-buttons">
              <button @click="applyFilter('blur')">Blur</button>
              <button @click="applyFilter('sharpen')">Sharpen</button>
              <button @click="applyFilter('emboss')">Emboss</button>
              <button @click="applyFilter('laplacian')">Laplacian</button>
              <button @click="applyFilter('canny')">Canny</button>
              <button @click="applyFilter('sobel')">Sobel</button>
              <button @click="applyFilter('grayscale')">Escala de Cinza</button>
              <button @click="applyFilter('binary')">Binarização</button>
              <button @click="applyFilter('detect_objects')">Detectar Objetos</button>
              <button @click="resetVideo" class="reset-button">Restaurar Original</button>
            </div>
          </div>
          
          <div class="segment-controls card">
            <h3>Segmentação de Vídeo</h3>
            <div class="time-controls">
              <div class="time-input">
                <label>Tempo Inicial (s):</label>
                <input type="number" v-model.number="startTime" min="0" :max="videoDuration" step="0.1" />
                <button @click="setCurrentTimeAsStart">Usar Atual</button>
              </div>
              
              <div class="time-input">
                <label>Tempo Final (s):</label>
                <input type="number" v-model.number="endTime" :min="startTime" :max="videoDuration" step="0.1" />
                <button @click="setCurrentTimeAsEnd">Usar Atual</button>
              </div>
            </div>
            
            <button @click="createSegment" :disabled="!canCreateSegment" class="create-segment-btn">
              Criar Segmento
            </button>
            
            <div v-if="currentFile.segments && currentFile.segments.length > 0" class="segments-list">
              <h4>Segmentos Criados</h4>
              <div class="segment-items">
                <div v-for="segment in currentFile.segments" :key="segment.id" class="segment-item">
                  <p>{{ formatTime(segment.start_time) }} - {{ formatTime(segment.end_time) }}</p>
                  <video controls :src="getVideoUrl(segment.segment_file)"></video>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'VideoEditor',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      videoDuration: 0,
      startTime: 0,
      endTime: 0,
      currentTime: 0
    }
  },
  computed: {
    ...mapState(['currentFile', 'loading', 'error']),
    
    canCreateSegment() {
      return this.startTime < this.endTime && this.endTime <= this.videoDuration
    }
  },
  methods: {
    ...mapActions(['fetchFile', 'applyFilter']),
    
    getFileName(path) {
      if (!path) return ''
      return path.split('/').pop()
    },
    
    getVideoUrl(path) {
      if (!path) return ''
      // Assumindo que a API retorna caminhos relativos à URL base da API
      return `http://localhost:8000${path}`
    },
    
    onVideoLoaded() {
      const video = this.$refs.videoElement
      this.videoDuration = video.duration
      this.endTime = this.videoDuration
    },
    
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs.toString().padStart(2, '0')}`
    },
    
    setCurrentTimeAsStart() {
      const video = this.$refs.videoElement
      this.startTime = video.currentTime
      if (this.startTime >= this.endTime) {
        this.endTime = Math.min(this.startTime + 1, this.videoDuration)
      }
    },
    
    setCurrentTimeAsEnd() {
      const video = this.$refs.videoElement
      this.endTime = video.currentTime
      if (this.endTime <= this.startTime) {
        this.startTime = Math.max(0, this.endTime - 1)
      }
    },
    
    async applyFilter(filterType) {
      await this.applyFilter({
        fileId: this.id,
        filterType
      })
    },
    
    async resetVideo() {
      // Recarrega o vídeo original
      await this.fetchFile(this.id)
    },
    
    async createSegment() {
      if (!this.canCreateSegment) return
      
      await this.$store.dispatch('createVideoSegment', {
        fileId: this.id,
        startTime: this.startTime,
        endTime: this.endTime
      })
    }
  },
  created() {
    this.fetchFile(this.id)
  }
}
</script>

<style scoped>
.video-editor {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.editor-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 1rem;
}

.video-container {
  overflow: hidden;
  padding: 1rem;
}

.video-container video {
  width: 100%;
  max-height: 70vh;
  display: block;
}

.controls-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-controls, .segment-controls {
  padding: 1rem;
}

.filter-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.reset-button {
  grid-column: span 2;
  background-color: #3498db;
}

.reset-button:hover {
  background-color: #2980b9;
}

.time-controls {
  margin: 1rem 0;
}

.time-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.time-input label {
  min-width: 120px;
}

.time-input input {
  width: 70px;
  padding: 0.25rem;
  background-color: #333;
  color: white;
  border: 1px solid #555;
  border-radius: 4px;
}

.create-segment-btn {
  width: 100%;
  margin-top: 1rem;
  background-color: #2ecc71;
}

.create-segment-btn:hover {
  background-color: #27ae60;
}

.create-segment-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.segments-list {
  margin-top: 1rem;
}

.segment-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0.5rem;
}

.segment-item {
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.5rem;
}

.segment-item p {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.segment-item video {
  width: 100%;
  height: auto;
  border-radius: 4px;
}

.loading, .error, .not-found {
  text-align: center;
  padding: 2rem;
}

.error {
  color: #e74c3c;
}

@media (max-width: 900px) {
  .editor-content {
    grid-template-columns: 1fr;
  }
}
</style>
