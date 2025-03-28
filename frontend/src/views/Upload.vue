<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="text-h5">
        <v-icon left class="mr-2">mdi-upload</v-icon>
        Upload de Arquivos
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="file-upload-card">
              <v-card-text class="text-center">
                <div
                  class="drop-zone pa-8"
                  :class="{ 'drop-zone-active': isDragging }"
                  @dragover.prevent="isDragging = true"
                  @dragleave.prevent="isDragging = false"
                  @drop.prevent="onFileDrop"
                  @click="$refs.fileInput.click()"
                >
                  <v-icon size="64" color="primary" class="mb-4">
                    {{ selectedFile ? 'mdi-file-check' : 'mdi-cloud-upload' }}
                  </v-icon>
                  
                  <h3 class="text-h6 mb-2">
                    {{ selectedFile ? selectedFile.name : 'Arraste e solte seu arquivo aqui' }}
                  </h3>
                  
                  <p class="text-body-2 text-medium-emphasis" v-if="!selectedFile">
                    ou clique para selecionar
                  </p>
                  
                  <p class="text-body-2" v-if="selectedFile">
                    {{ formatFileSize(selectedFile.size) }}
                  </p>
                  
                  <input
                    type="file"
                    ref="fileInput"
                    style="display: none"
                    @change="onFileChange"
                    :accept="fileType === 'image' ? 'image/*' : 'video/*'"
                  >
                </div>
              </v-card-text>
              
              <v-card-actions v-if="selectedFile" class="justify-center">
                <v-btn color="error" variant="text" @click="clearSelectedFile">
                  <v-icon left>mdi-delete</v-icon>
                  Remover
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" height="100%">
              <v-card-text>
                <h3 class="text-h6 mb-4">Configurações</h3>
                
                <v-radio-group v-model="fileType" label="Tipo de Arquivo" class="mb-4">
                  <v-radio value="image" label="Imagem"></v-radio>
                  <v-radio value="video" label="Vídeo"></v-radio>
                </v-radio-group>
                
                <v-divider class="mb-4"></v-divider>
                
                <v-alert
                  v-if="fileType === 'image'"
                  type="info"
                  variant="tonal"
                  class="mb-4"
                >
                  Formatos suportados: JPG, PNG, BMP, GIF
                </v-alert>
                
                <v-alert
                  v-else
                  type="info"
                  variant="tonal"
                  class="mb-4"
                >
                  Formatos suportados: MP4, AVI, MOV
                </v-alert>
                
                <v-btn
                  block
                  color="primary"
                  size="large"
                  :disabled="!selectedFile"
                  :loading="loading"
                  @click="uploadFile"
                >
                  <v-icon left class="mr-2">mdi-cloud-upload</v-icon>
                  Fazer Upload
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <v-card v-if="recentUploads.length > 0">
      <v-card-title class="text-h5">
        <v-icon left class="mr-2">mdi-history</v-icon>
        Uploads Recentes
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col
            v-for="file in recentUploads"
            :key="file.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card
              class="file-card"
              @click="openEditor(file)"
              variant="outlined"
              hover
            >
              <v-img
                v-if="file.file_type === 'image'"
                :src="getFileUrl(file.original_file)"
                height="180"
                cover
                class="align-end"
              >
                <v-card-title class="text-white bg-black bg-opacity-50">
                  {{ getFileName(file.original_file) }}
                </v-card-title>
              </v-img>
              
              <v-img
                v-else
                src="@/assets/video-thumbnail.jpg"
                height="180"
                cover
                class="align-end"
              >
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
                  @click.stop="openEditor(file)"
                >
                  Editar
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  variant="text"
                  color="error"
                  @click.stop="confirmDelete(file)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <!-- Diálogo de confirmação de exclusão -->
    <v-dialog v-model="deleteDialog.show" max-width="400">
      <v-card>
        <v-card-title class="text-h5">
          Confirmar exclusão
        </v-card-title>
        
        <v-card-text>
          Tem certeza que deseja excluir este arquivo? Esta ação não pode ser desfeita.
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="deleteDialog.show = false">
            Cancelar
          </v-btn>
          <v-btn color="error" @click="deleteFile">
            Excluir
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { eventBus } from '../plugins/eventBus'
import api from '../plugins/api'

export default {
  name: 'UploadView',
  data() {
    return {
      selectedFile: null,
      fileType: 'image',
      isDragging: false,
      deleteDialog: {
        show: false,
        fileId: null
      }
    }
  },
  computed: {
    ...mapState(['files', 'loading', 'error']),
    
    recentUploads() {
      return this.files.slice(0, 8)
    }
  },
  methods: {
    ...mapActions(['fetchFiles', 'uploadFile']),
    
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    
    onFileDrop(event) {
      this.isDragging = false
      const file = event.dataTransfer.files[0]
      if (file) {
        // Verificar se o tipo de arquivo corresponde à seleção
        const isImage = file.type.startsWith('image/')
        const isVideo = file.type.startsWith('video/')
        
        if ((this.fileType === 'image' && isImage) || (this.fileType === 'video' && isVideo)) {
          this.selectedFile = file
        } else {
          // Mostrar erro de tipo de arquivo incompatível
          this.$parent.showSnackbar(
            `Tipo de arquivo incompatível. Selecione um arquivo ${this.fileType === 'image' ? 'de imagem' : 'de vídeo'}.`,
            'error'
          )
        }
      }
    },
    
    clearSelectedFile() {
      this.selectedFile = null
      this.$refs.fileInput.value = null
    },
    
    async uploadFile() {
      if (!this.selectedFile) return
      
      try {
        const result = await this.$store.dispatch('uploadFile', {
          file: this.selectedFile,
          fileType: this.fileType
        })
        
        if (result) {
          this.clearSelectedFile()
          eventBus.emit('showSnackbar', 'Arquivo enviado com sucesso!', 'success')
          this.fetchFiles()
        }
      } catch (error) {
        console.error('Erro ao fazer upload:', error)
        eventBus.emit('showSnackbar', 'Erro ao fazer upload do arquivo.', 'error')
      }
    },
    
    formatFileSize(size) {
      if (size < 1024) {
        return size + ' bytes'
      } else if (size < 1024 * 1024) {
        return (size / 1024).toFixed(2) + ' KB'
      } else {
        return (size / (1024 * 1024)).toFixed(2) + ' MB'
      }
    },
    
    getFileName(path) {
      if (!path) return ''
      return path.split('/').pop()
    },
    
    getFileUrl(path) {
      if (!path) return ''
      return `http://localhost:8000${path}`
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    },
    
    openEditor(file) {
      if (file.file_type === 'image') {
        this.$router.push({ name: 'ImageEditor', params: { id: file.id } })
      } else {
        this.$router.push({ name: 'VideoEditor', params: { id: file.id } })
      }
    },
    
    confirmDelete(file) {
      this.deleteDialog = {
        show: true,
        fileId: file.id
      }
    },
    
    async deleteFile() {
      try {
        await api.delete(`files/${this.deleteDialog.fileId}/`)
        this.fetchFiles()
        eventBus.emit('showSnackbar', 'Arquivo excluído com sucesso!', 'success')
      } catch (error) {
        console.error('Erro ao excluir arquivo:', error)
        eventBus.emit('showSnackbar', 'Erro ao excluir arquivo.', 'error')
      } finally {
        this.deleteDialog.show = false
      }
    }
  },
  created() {
    this.fetchFiles()
  }
}
</script>

<style scoped>
.drop-zone {
  border: 2px dashed rgba(var(--v-theme-primary), 0.5);
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.drop-zone:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.drop-zone-active {
  border-color: var(--v-theme-primary);
  background-color: rgba(var(--v-theme-primary), 0.1);
}

.file-upload-card {
  height: 100%;
}
</style>
