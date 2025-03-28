<template>
  <div>
    <v-container fluid v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-container>
    
    <v-container fluid v-else-if="error">
      <v-alert type="error" class="mb-4">
        {{ error }}
      </v-alert>
      <v-btn color="primary" to="/" prepend-icon="mdi-home">Voltar para Home</v-btn>
    </v-container>
    
    <v-container fluid v-else-if="!currentFile">
      <v-alert type="warning" class="mb-4">
        Imagem não encontrada
      </v-alert>
      <v-btn color="primary" to="/" prepend-icon="mdi-home">Voltar para Home</v-btn>
    </v-container>
    
    <div v-else>
      <v-card class="mb-4">
        <v-toolbar color="primary" dark>
          <v-btn icon @click="$router.push('/gallery')">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-toolbar-title>Editor de Imagem: {{ getFileName(currentFile.original_file) }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="resetImage" title="Restaurar Original">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
          <v-btn icon @click="downloadImage" title="Baixar Imagem">
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </v-toolbar>
        
        <v-row class="ma-0">
          <v-col cols="12" md="8" class="pa-0">
            <v-card flat class="image-editor-panel">
              <v-card-text class="text-center position-relative">
                <div class="image-wrapper">
                  <img 
                    :src="currentFile.processed_file_url || currentFile.original_file_url" 
                    alt="Imagem" 
                    @mousedown="startROI"
                    @mousemove="drawROI"
                    @mouseup="endROI"
                    ref="imageElement"
                    class="main-image"
                  />
                  <div 
                    v-if="isDrawingROI" 
                    class="roi-rectangle"
                    :style="{
                      left: `${Math.min(roiStart.x, roiEnd.x)}px`,
                      top: `${Math.min(roiStart.y, roiEnd.y)}px`,
                      width: `${Math.abs(roiEnd.x - roiStart.x)}px`,
                      height: `${Math.abs(roiEnd.y - roiStart.y)}px`
                    }"
                  ></div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="4" class="pa-0">
            <v-card flat class="controls-panel" height="100%">
              <v-tabs v-model="activeTab" bg-color="primary" align-tabs="center">
                <v-tab value="filters">Filtros</v-tab>
                <v-tab value="roi">ROI</v-tab>
                <v-tab value="info">Info</v-tab>
              </v-tabs>
              
              <v-window v-model="activeTab">
                <!-- Aba de Filtros -->
                <v-window-item value="filters">
                  <v-card-text>
                    <v-row>
                      <v-col cols="6" v-for="(filter, index) in availableFilters" :key="index">
                        <v-btn 
                          block 
                          :color="activeFilter === filter.value ? 'primary' : undefined"
                          @click="applyFilter(filter.value)"
                          class="text-none mb-2"
                          :prepend-icon="filter.icon"
                        >
                          {{ filter.name }}
                        </v-btn>
                      </v-col>
                    </v-row>
                    
                    <v-divider class="my-4"></v-divider>
                    
                    <v-btn 
                      block 
                      color="secondary" 
                      @click="resetImage"
                      prepend-icon="mdi-refresh"
                      class="mt-2"
                    >
                      Restaurar Original
                    </v-btn>
                  </v-card-text>
                </v-window-item>
                
                <!-- Aba de ROI -->
                <v-window-item value="roi">
                  <v-card-text>
                    <v-alert type="info" variant="tonal" class="mb-4">
                      Selecione uma região na imagem para extrair uma ROI (Região de Interesse).
                    </v-alert>
                    
                    <v-btn 
                      block 
                      color="primary" 
                      :disabled="!canExtractROI"
                      @click="extractROI"
                      prepend-icon="mdi-crop"
                      class="mb-4"
                    >
                      Extrair ROI
                    </v-btn>
                    
                    <v-divider class="my-4" v-if="currentFile.rois && currentFile.rois.length > 0"></v-divider>
                    
                    <div v-if="currentFile.rois && currentFile.rois.length > 0">
                      <h3 class="text-h6 mb-3">ROIs Extraídas</h3>
                      
                      <v-row>
                        <v-col cols="6" v-for="roi in currentFile.rois" :key="roi.id">
                          <v-card variant="outlined" class="roi-card">
                            <v-img 
                              :src="roi.roi_image_url" 
                              :aspect-ratio="16/9"
                              cover
                              class="roi-image"
                            ></v-img>
                            
                            <v-card-actions>
                              <v-btn 
                                variant="text" 
                                density="compact" 
                                icon="mdi-download" 
                                @click="downloadROI(roi)"
                              ></v-btn>
                              <v-spacer></v-spacer>
                              <v-btn 
                                variant="text" 
                                density="compact" 
                                icon="mdi-magnify" 
                                @click="viewROI(roi)"
                              ></v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-col>
                      </v-row>
                    </div>
                  </v-card-text>
                </v-window-item>
                
                <!-- Aba de Informações -->
                <v-window-item value="info">
                  <v-card-text>
                    <h3 class="text-h6 mb-3">Informações da Imagem</h3>
                    
                    <v-list>
                      <v-list-item>
                        <v-list-item-title>Nome do Arquivo</v-list-item-title>
                        <v-list-item-subtitle>{{ getFileName(currentFile.original_file) }}</v-list-item-subtitle>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-title>Data de Upload</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDate(currentFile.created_at) }}</v-list-item-subtitle>
                      </v-list-item>
                      
                      <v-list-item v-if="imageInfo.width && imageInfo.height">
                        <v-list-item-title>Dimensões</v-list-item-title>
                        <v-list-item-subtitle>{{ imageInfo.width }} x {{ imageInfo.height }} pixels</v-list-item-subtitle>
                      </v-list-item>
                      
                      <v-list-item>
                        <v-list-item-title>ROIs Extraídas</v-list-item-title>
                        <v-list-item-subtitle>{{ currentFile.rois ? currentFile.rois.length : 0 }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-window-item>
              </v-window>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </div>
    
    <!-- Diálogo para visualizar ROI ampliada -->
    <v-dialog v-model="roiDialog.show" max-width="800">
      <v-card>
        <v-card-title class="text-h5">
          Região de Interesse
          <v-spacer></v-spacer>
          <v-btn icon @click="roiDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text class="text-center">
          <v-img 
            :src="roiDialog.url" 
            max-height="600"
            contain
          ></v-img>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { eventBus } from '../plugins/eventBus';
import api from '../plugins/api';

export default {
  name: 'ImageEditorView',
  data() {
    return {
      currentFile: null,
      loading: true,
      error: null,
      isDrawingROI: false,
      roiStart: { x: 0, y: 0 },
      roiEnd: { x: 0, y: 0 },
      canExtractROI: false,
      activeTab: 'filters',
      activeFilter: null,
      imageInfo: {
        width: 0,
        height: 0
      },
      roiDialog: {
        show: false,
        url: ''
      },
      availableFilters: [
        { name: 'Blur', value: 'blur', icon: 'mdi-blur' },
        { name: 'Sharpen', value: 'sharpen', icon: 'mdi-image-filter-center-focus' },
        { name: 'Emboss', value: 'emboss', icon: 'mdi-image-filter-vintage' },
        { name: 'Laplacian', value: 'laplacian', icon: 'mdi-image-filter-drama' },
        { name: 'Canny', value: 'canny', icon: 'mdi-image-filter-frames' },
        { name: 'Sobel', value: 'sobel', icon: 'mdi-image-filter-hdr' },
        { name: 'Escala de Cinza', value: 'grayscale', icon: 'mdi-image-filter-black-white' },
        { name: 'Binarização', value: 'binary', icon: 'mdi-contrast-box' },
        { name: 'Detectar Objetos', value: 'detect_objects', icon: 'mdi-magnify-scan' }
      ]
    };
  },
  mounted() {
    this.fetchFileData();
  },
  methods: {
    async fetchFileData() {
      try {
        this.loading = true;
        const response = await api.get(`files/${this.$route.params.id}/`);
        this.currentFile = response.data;
        this.loading = false;
        
        // Carregar informações da imagem após carregar o arquivo
        this.$nextTick(() => {
          this.loadImageInfo();
        });
      } catch (error) {
        console.error('Error fetching file data:', error);
        this.error = 'Erro ao carregar os dados da imagem';
        this.loading = false;
      }
    },
    loadImageInfo() {
      if (this.$refs.imageElement) {
        const img = this.$refs.imageElement;
        // Aguardar o carregamento da imagem
        if (img.complete) {
          this.imageInfo.width = img.naturalWidth;
          this.imageInfo.height = img.naturalHeight;
        } else {
          img.onload = () => {
            this.imageInfo.width = img.naturalWidth;
            this.imageInfo.height = img.naturalHeight;
          };
        }
      }
    },
    getFileName(path) {
      if (!path) return '';
      return path.split('/').pop();
    },
    getImageUrl(path) {
      if (!path) return '';
      // Check if it's already a full URL
      if (path.startsWith('http')) return path;
      // Otherwise, add the API URL prefix
      return `http://localhost:8000${path}`;
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    async applyFilter(filterType) {
      try {
        this.loading = true;
        this.activeFilter = filterType;
        const response = await api.post(
          `apply-filter/${this.currentFile.id}/${filterType}/`
        );
        this.currentFile = response.data;
        eventBus.emit('showSnackbar', `Filtro ${filterType} aplicado com sucesso!`, 'success');
        this.loading = false;
      } catch (error) {
        console.error('Error applying filter:', error);
        this.error = 'Erro ao aplicar o filtro';
        eventBus.emit('showSnackbar', 'Erro ao aplicar o filtro', 'error');
        this.loading = false;
      }
    },
    async resetImage() {
      try {
        this.loading = true;
        this.activeFilter = null;
        // Fetch the original file instead of using a reset endpoint
        const response = await api.get(
          `files/${this.currentFile.id}/`
        );
        this.currentFile = response.data;
        eventBus.emit('showSnackbar', 'Imagem restaurada com sucesso!', 'success');
        this.loading = false;
      } catch (error) {
        console.error('Error resetting image:', error);
        this.error = 'Erro ao restaurar a imagem original';
        eventBus.emit('showSnackbar', 'Erro ao restaurar a imagem original', 'error');
        this.loading = false;
      }
    },
    startROI(event) {
      const rect = this.$refs.imageElement.getBoundingClientRect();
      this.roiStart = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      };
      this.roiEnd = { ...this.roiStart };
      this.isDrawingROI = true;
      this.canExtractROI = false;
    },
    drawROI(event) {
      if (!this.isDrawingROI) return;
      
      const rect = this.$refs.imageElement.getBoundingClientRect();
      this.roiEnd = {
        x: Math.max(0, Math.min(event.clientX - rect.left, rect.width)),
        y: Math.max(0, Math.min(event.clientY - rect.top, rect.height))
      };
    },
    endROI() {
      this.isDrawingROI = false;
      
      const width = Math.abs(this.roiEnd.x - this.roiStart.x);
      const height = Math.abs(this.roiEnd.y - this.roiStart.y);
      
      // Verificar se a ROI tem tamanho mínimo
      if (width > 10 && height > 10) {
        this.canExtractROI = true;
        // Mudar para a aba ROI automaticamente
        this.activeTab = 'roi';
      }
    },
    async extractROI() {
      if (!this.canExtractROI) return;
      
      try {
        this.loading = true;
        
        const imageRect = this.$refs.imageElement.getBoundingClientRect();
        const imageWidth = this.$refs.imageElement.naturalWidth;
        const imageHeight = this.$refs.imageElement.naturalHeight;
        
        // Converter coordenadas de tela para coordenadas da imagem original
        const scaleX = imageWidth / imageRect.width;
        const scaleY = imageHeight / imageRect.height;
        
        const x = Math.min(this.roiStart.x, this.roiEnd.x) * scaleX;
        const y = Math.min(this.roiStart.y, this.roiEnd.y) * scaleY;
        const width = Math.abs(this.roiEnd.x - this.roiStart.x) * scaleX;
        const height = Math.abs(this.roiEnd.y - this.roiStart.y) * scaleY;
        
        const response = await api.post(
          `extract-roi/${this.currentFile.id}/`,
          { x1: Math.round(x), y1: Math.round(y), x2: Math.round(x + width), y2: Math.round(y + height) }
        );
        
        this.currentFile = response.data;
        this.canExtractROI = false;
        this.loading = false;
      } catch (error) {
        console.error('Error extracting ROI:', error);
        this.error = 'Erro ao extrair a região de interesse';
        this.loading = false;
      }
    },
    viewROI(roi) {
      this.roiDialog.url = this.getImageUrl(roi.roi_image);
      this.roiDialog.show = true;
    },
    downloadImage() {
      const imageUrl = this.getImageUrl(this.currentFile.processed_file || this.currentFile.original_file);
      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = this.getFileName(this.currentFile.original_file);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    downloadROI(roi) {
      const imageUrl = this.getImageUrl(roi.roi_image);
      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = `ROI_${this.getFileName(this.currentFile.original_file)}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
};
</script>

<style scoped>
.image-wrapper {
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.main-image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

.roi-rectangle {
  position: absolute;
  border: 2px dashed #1976d2;
  background-color: rgba(25, 118, 210, 0.1);
  pointer-events: none;
}

.controls-panel {
  border-left: 1px solid rgba(0, 0, 0, 0.12);
}

.roi-card {
  transition: transform 0.2s;
}

.roi-card:hover {
  transform: scale(1.05);
}

.position-relative {
  position: relative;
}
</style>
