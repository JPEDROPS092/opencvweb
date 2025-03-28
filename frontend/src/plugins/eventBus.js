import { reactive } from 'vue'

export const eventBus = reactive({
  // Método para emitir eventos
  emit(event, ...args) {
    this[event]?.(...args)
  },
  
  // Método para registrar ouvintes de eventos
  on(event, callback) {
    this[event] = callback
  }
})

export default eventBus
