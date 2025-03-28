<template>
  <v-app>
    <v-app-bar color="primary" elevation="4">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      
      <v-toolbar-title class="text-h5 font-weight-bold">
        Opencv Web - Processador de Imagens e Vídeos
      </v-toolbar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn icon @click="toggleTheme">
        <v-icon>{{ isDarkTheme ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>
    
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <v-list-item to="/" link>
          <template v-slot:prepend>
            <v-icon>mdi-home</v-icon>
          </template>
          <v-list-item-title>Início</v-list-item-title>
        </v-list-item>
        
        <v-divider></v-divider>
        
        <v-list-item to="/upload" link>
          <template v-slot:prepend>
            <v-icon>mdi-upload</v-icon>
          </template>
          <v-list-item-title>Upload</v-list-item-title>
        </v-list-item>
        
        <v-list-item to="/gallery" link>
          <template v-slot:prepend>
            <v-icon>mdi-image-multiple</v-icon>
          </template>
          <v-list-item-title>Galeria</v-list-item-title>
        </v-list-item>
      </v-list>
      
      <template v-slot:append>
        <div class="pa-4">
          <v-btn block color="primary" to="/about">
            Sobre
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
    
    <v-main>
      <v-container fluid class="pa-4">
        <router-view></router-view>
      </v-container>
    </v-main>
    
    <v-footer color="primary">
      <v-row justify="center" no-gutters>
        <span>&copy; {{ new Date().getFullYear() }} - EdTETI Web App</span>
      </v-row>
    </v-footer>
    
    <!-- Snackbar para notificações -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.text }}
      
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Fechar
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { eventBus } from './plugins/eventBus'

export default {
  name: 'App',
  data() {
    return {
      drawer: false,
      isDarkTheme: true,
      snackbar: {
        show: false,
        text: '',
        color: 'success',
        timeout: 3000
      }
    }
  },
  created() {
    // Escutar eventos de notificação do Vuex
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'SET_ERROR' && state.error) {
        this.showSnackbar(state.error, 'error');
      }
    });
    
    // Registrar o método showSnackbar no eventBus
    eventBus.on('showSnackbar', this.showSnackbar);
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      this.$vuetify.theme.global.name = this.isDarkTheme ? 'dark' : 'light';
    },
    showSnackbar(text, color = 'success', timeout = 3000) {
      this.snackbar = {
        show: true,
        text,
        color,
        timeout
      };
    }
  }
}
</script>

<style>
/* Estilos globais */
.v-application {
  font-family: 'Roboto', sans-serif;
  line-height: 1.5;
}

/* Transições de página */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}

/* Estilos para cards de arquivos */
.file-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.file-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2) !important;
}
</style>
