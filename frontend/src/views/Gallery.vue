<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-image-multiple</v-icon>
        <span class="text-h5">Galeria de Arquivos</span>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Buscar"
          single-line
          hide-details
          density="compact"
          class="max-width-300"
        ></v-text-field>
      </v-card-title>
      
      <v-card-text>
        <v-tabs v-model="activeTab" bg-color="primary">
          <v-tab value="all">Todos</v-tab>
          <v-tab value="image">Imagens</v-tab>
          <v-tab value="video">Vídeos</v-tab>
        </v-tabs>
        
        <v-window v-model="activeTab" class="mt-4">
          <v-window-item value="all">
            <v-row v-if="filteredFiles.length > 0">
              <v-col
                v-for="file in filteredFiles"
                :key="file.id"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <file-card :file="file" @edit="openEditor" @delete="confirmDelete"></file-card>
              </v-col>
            </v-row>
            <v-alert v-else type="info" class="mt-4">
              Nenhum arquivo encontrado. Faça upload de uma imagem ou vídeo.
            </v-alert>
          </v-window-item>
          
          <v-window-item value="image">
            <v-row v-if="filteredImageFiles.length > 0">
              <v-col
                v-for="file in filteredImageFiles"
                :key="file.id"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <file-card :file="file" @edit="openEditor" @delete="confirmDelete"></file-card>
              </v-col>
            </v-row>
            <v-alert v-else type="info" class="mt-4">
              Nenhuma imagem encontrada. Faça upload de uma imagem.
            </v-alert>
          </v-window-item>
          
          <v-window-item value="video">
            <v-row v-if="filteredVideoFiles.length > 0">
              <v-col
                v-for="file in filteredVideoFiles"
                :key="file.id"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <file-card :file="file" @edit="openEditor" @delete="confirmDelete"></file-card>
              </v-col>
            </v-row>
            <v-alert v-else type="info" class="mt-4">
              Nenhum vídeo encontrado. Faça upload de um vídeo.
            </v-alert>
          </v-window-item>
        </v-window>
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
import FileCard from '@/components/FileCard.vue'
import { eventBus } from '../plugins/eventBus'
import api from '../plugins/api'

export default {
  name: 'GalleryView',
  components: {
    FileCard
  },
  data() {
    return {
      search: '',
      activeTab: 'all',
      deleteDialog: {
        show: false,
        fileId: null
      }
    }
  },
  computed: {
    ...mapState(['files', 'loading', 'error']),
    
    filteredFiles() {
      if (!this.search) return this.files
      
      const searchTerm = this.search.toLowerCase()
      return this.files.filter(file => {
        const fileName = this.getFileName(file.original_file).toLowerCase()
        return fileName.includes(searchTerm)
      })
    },
    
    filteredImageFiles() {
      return this.filteredFiles.filter(file => file.file_type === 'image')
    },
    
    filteredVideoFiles() {
      return this.filteredFiles.filter(file => file.file_type === 'video')
    }
  },
  methods: {
    ...mapActions(['fetchFiles']),
    
    getFileName(path) {
      if (!path) return ''
      return path.split('/').pop()
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
.max-width-300 {
  max-width: 300px;
}
</style>
