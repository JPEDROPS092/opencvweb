<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-6">
          <v-card-text class="text-center py-12">
            <v-row justify="center" align="center">
              <v-col cols="12" md="8" lg="6">
                <h1 class="text-h3 font-weight-bold mb-6">OpenCV-Web</h1>
                <h2 class="text-h5 mb-8">Processador de Imagens e Vídeos</h2>
                
                <p class="text-body-1 mb-8">
                  Uma ferramenta poderosa para processamento, edição e análise de imagens e vídeos.
                  Aplique filtros, extraia regiões de interesse, segmente vídeos e muito mais.
                </p>
                
                <v-row justify="center" class="mt-8">
                  <v-col cols="auto">
                    <v-btn
                      color="primary"
                      size="x-large"
                      to="/upload"
                      prepend-icon="mdi-upload"
                    >
                      Fazer Upload
                    </v-btn>
                  </v-col>
                  
                  <v-col cols="auto">
                    <v-btn
                      color="secondary"
                      size="x-large"
                      to="/gallery"
                      variant="outlined"
                      prepend-icon="mdi-image-multiple"
                    >
                      Ver Galeria
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h5">
            <v-icon left class="mr-2">mdi-star</v-icon>
            Funcionalidades
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <v-card variant="outlined" height="100%" class="feature-card">
                  <v-card-title>
                    <v-icon color="primary" size="large" class="mb-4">mdi-image-filter</v-icon>
                    <h3 class="text-h6">Filtros de Imagem</h3>
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Aplique diversos filtros como Blur, Sharpen, Emboss, Laplacian, Canny, Sobel e mais. Converta para escala de cinza ou binarize suas imagens.</p>
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-card variant="outlined" height="100%" class="feature-card">
                  <v-card-title>
                    <v-icon color="primary" size="large" class="mb-4">mdi-crop</v-icon>
                    <h3 class="text-h6">Extração de ROI</h3>
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Selecione e extraia regiões de interesse (ROI) de suas imagens para análise detalhada ou processamento específico.</p>
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-card variant="outlined" height="100%" class="feature-card">
                  <v-card-title>
                    <v-icon color="primary" size="large" class="mb-4">mdi-video</v-icon>
                    <h3 class="text-h6">Processamento de Vídeo</h3>
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Aplique filtros em vídeos, crie segmentos específicos, ajuste a velocidade de reprodução e extraia frames importantes.</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            
            <v-row class="mt-4">
              <v-col cols="12" md="4">
                <v-card variant="outlined" height="100%" class="feature-card">
                  <v-card-title>
                    <v-icon color="primary" size="large" class="mb-4">mdi-eye-scan</v-icon>
                    <h3 class="text-h6">Detecção de Objetos</h3>
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Utilize tecnologia de inteligência artificial para detectar e identificar objetos em imagens e vídeos automaticamente.</p>
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-card variant="outlined" height="100%" class="feature-card">
                  <v-card-title>
                    <v-icon color="primary" size="large" class="mb-4">mdi-content-save</v-icon>
                    <h3 class="text-h6">Exportação Flexível</h3>
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Salve seus resultados em diversos formatos. Exporte ROIs como imagens separadas ou segmentos de vídeo como novos arquivos.</p>
                  </v-card-text>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="4">
                <v-card variant="outlined" height="100%" class="feature-card">
                  <v-card-title>
                    <v-icon color="primary" size="large" class="mb-4">mdi-web</v-icon>
                    <h3 class="text-h6">Interface Web</h3>
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Acesse todas as funcionalidades através de uma interface web moderna, responsiva e fácil de usar, sem necessidade de instalação.</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-6" v-if="recentFiles.length > 0">
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h5">
            <v-icon left class="mr-2">mdi-history</v-icon>
            Arquivos Recentes
            <v-spacer></v-spacer>
            <v-btn
              variant="text"
              color="primary"
              to="/gallery"
              class="text-none"
            >
              Ver Todos
              <v-icon right>mdi-chevron-right</v-icon>
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col
                v-for="file in recentFiles"
                :key="file.id"
                cols="12"
                sm="6"
                md="3"
              >
                <file-card :file="file" @edit="openEditor" @delete="confirmDelete"></file-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
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
  name: 'HomeView',
  components: {
    FileCard
  },
  data() {
    return {
      deleteDialog: {
        show: false,
        fileId: null
      }
    }
  },
  computed: {
    ...mapState(['files', 'loading', 'error']),
    
    recentFiles() {
      return this.files.slice(0, 4)
    }
  },
  methods: {
    ...mapActions(['fetchFiles']),
    
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
.feature-card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
}
</style>
