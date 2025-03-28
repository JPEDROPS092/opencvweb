<template>
  <div class="not-found-container">
    <v-card class="not-found-card">
      <v-card-text class="text-center pa-8">
        <v-icon size="100" color="error" class="mb-6">mdi-alert-circle</v-icon>
        
        <h1 class="text-h3 font-weight-bold mb-4">404</h1>
        <h2 class="text-h5 mb-6">Página Não Encontrada</h2>
        
        <p class="text-body-1 mb-8">
          A página que você está procurando não existe ou foi movida.
        </p>
        
        <v-btn
          color="primary"
          size="large"
          to="/"
          prepend-icon="mdi-home"
        >
          Voltar para a Página Inicial
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.not-found-card {
  max-width: 500px;
  width: 100%;
}
</style>
