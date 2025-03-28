<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="text-h4 font-weight-bold">
        <v-icon size="large" class="mr-2">mdi-information</v-icon>
        Sobre o EdTETI
      </v-card-title>
      
      <v-card-text>
        <p class="text-body-1 mb-4">
          O EdTETI é uma aplicação web para processamento de imagens e vídeos, desenvolvida como uma versão moderna e acessível 
          do processador original. Esta aplicação utiliza tecnologias modernas para oferecer uma experiência de usuário aprimorada 
          e recursos avançados de processamento.
        </p>
        
        <v-divider class="my-6"></v-divider>
        
        <h3 class="text-h5 mb-4">Tecnologias Utilizadas</h3>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="mb-4">
              <v-card-title>
                <v-icon color="primary" class="mr-2">mdi-server</v-icon>
                Backend
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Django
                    </v-list-item-title>
                    <v-list-item-subtitle>Framework web Python</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Django REST Framework
                    </v-list-item-title>
                    <v-list-item-subtitle>API RESTful</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      OpenCV
                    </v-list-item-title>
                    <v-list-item-subtitle>Processamento de imagens e vídeos</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      NumPy
                    </v-list-item-title>
                    <v-list-item-subtitle>Computação numérica</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      YOLO
                    </v-list-item-title>
                    <v-list-item-subtitle>Detecção de objetos</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="mb-4">
              <v-card-title>
                <v-icon color="primary" class="mr-2">mdi-monitor</v-icon>
                Frontend
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Vue.js 3
                    </v-list-item-title>
                    <v-list-item-subtitle>Framework JavaScript progressivo</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Vuetify
                    </v-list-item-title>
                    <v-list-item-subtitle>Biblioteca de componentes Material Design</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Vuex
                    </v-list-item-title>
                    <v-list-item-subtitle>Gerenciamento de estado</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Vue Router
                    </v-list-item-title>
                    <v-list-item-subtitle>Roteamento de páginas</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>
                      <v-icon color="green" class="mr-2">mdi-check-circle</v-icon>
                      Axios
                    </v-list-item-title>
                    <v-list-item-subtitle>Cliente HTTP</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-divider class="my-6"></v-divider>
        
        <h3 class="text-h5 mb-4">Funcionalidades</h3>
        
        <v-row>
          <v-col cols="12" md="4">
            <v-card variant="outlined" height="100%">
              <v-card-title>
                <v-icon color="primary" class="mr-2">mdi-image</v-icon>
                Processamento de Imagens
              </v-card-title>
              <v-card-text>
                <ul>
                  <li>Aplicação de filtros diversos</li>
                  <li>Conversão para escala de cinza</li>
                  <li>Binarização</li>
                  <li>Detecção de bordas</li>
                  <li>Extração de ROI</li>
                  <li>Detecção de objetos</li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-card variant="outlined" height="100%">
              <v-card-title>
                <v-icon color="primary" class="mr-2">mdi-video</v-icon>
                Processamento de Vídeos
              </v-card-title>
              <v-card-text>
                <ul>
                  <li>Aplicação de filtros em tempo real</li>
                  <li>Segmentação de vídeos</li>
                  <li>Controle de velocidade</li>
                  <li>Inversão de direção</li>
                  <li>Extração de frames</li>
                  <li>Detecção de objetos em vídeo</li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="4">
            <v-card variant="outlined" height="100%">
              <v-card-title>
                <v-icon color="primary" class="mr-2">mdi-web</v-icon>
                Interface Web
              </v-card-title>
              <v-card-text>
                <ul>
                  <li>Design responsivo</li>
                  <li>Tema claro/escuro</li>
                  <li>Upload por arrastar e soltar</li>
                  <li>Visualização em galeria</li>
                  <li>Edição interativa</li>
                  <li>Notificações em tempo real</li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
ul {
  padding-left: 20px;
}
</style>
