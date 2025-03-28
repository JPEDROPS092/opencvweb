<template>
  <v-card class="file-card" variant="outlined" hover>
    <v-img
      v-if="file.file_type === 'image'"
      :src="file.processed_file_url || file.original_file_url"
      height="180"
      cover
      class="align-end"
      @click="$emit('edit', file)"
    >
      <v-card-title class="text-white bg-black bg-opacity-50">
        {{ getFileName(file.original_file) }}
      </v-card-title>
    </v-img>
    
    <v-img
      v-else
      class="align-end"
      height="180"
      cover
      @click="$emit('edit', file)"
    >
      <video 
        :src="file.processed_file_url || file.original_file_url" 
        style="width: 100%; height: 180px; object-fit: cover;"
        muted
        @mouseover="playVideo"
        @mouseout="pauseVideo"
        ref="videoElement"
      ></video>
      <v-card-title class="text-white bg-black bg-opacity-50">
        {{ getFileName(file.original_file) }}
      </v-card-title>
    </v-img>
    
    <v-card-text>
      <div class="d-flex align-center">
        <v-icon
          :color="file.file_type === 'image' ? 'blue' : 'red'"
          class="mr-2"
        >
          {{ file.file_type === 'image' ? 'mdi-image' : 'mdi-video' }}
        </v-icon>
        <span>{{ file.file_type === 'image' ? 'Imagem' : 'Vídeo' }}</span>
        <v-spacer></v-spacer>
        <span class="text-caption text-medium-emphasis">
          {{ formatDate(file.created_at) }}
        </span>
      </div>
    </v-card-text>
    
    <v-card-actions>
      <v-btn
        variant="text"
        color="primary"
        @click="$emit('edit', file)"
      >
        <v-icon class="mr-1">mdi-pencil</v-icon>
        Editar
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        variant="text"
        color="error"
        @click="$emit('delete', file)"
      >
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'FileCard',
  props: {
    file: {
      type: Object,
      required: true
    }
  },
  methods: {
    getFileName(path) {
      if (!path) return ''
      return path.split('/').pop()
    },
    
    // This method is kept for backward compatibility
    getFileUrl(path) {
      if (!path) return ''
      // Check if it's already a full URL
      if (path.startsWith('http')) return path
      return `http://localhost:8000${path}`
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    },
    
    playVideo() {
      if (this.$refs.videoElement) {
        this.$refs.videoElement.play()
      }
    },
    
    pauseVideo() {
      if (this.$refs.videoElement) {
        this.$refs.videoElement.pause()
      }
    }
  }
}
</script>

<style scoped>
.file-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.file-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2) !important;
}
</style>
