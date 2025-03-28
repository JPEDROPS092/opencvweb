import { createStore } from 'vuex'
import api from '../plugins/api'

export default createStore({
  state: {
    files: [],
    currentFile: null,
    loading: false,
    error: null
  },
  mutations: {
    SET_FILES(state, files) {
      state.files = files
    },
    SET_CURRENT_FILE(state, file) {
      state.currentFile = file
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    async fetchFiles({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.get('files/')
        commit('SET_FILES', response.data)
        return response.data
      } catch (error) {
        const errorMsg = 'Erro ao carregar arquivos: ' + (error.response?.data?.error || error.message || 'Erro desconhecido')
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async fetchFile({ commit }, id) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.get(`files/${id}/`)
        commit('SET_CURRENT_FILE', response.data)
        return response.data
      } catch (error) {
        const errorMsg = 'Erro ao carregar arquivo: ' + (error.response?.data?.error || error.message || 'Erro desconhecido')
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async uploadFile({ commit, dispatch }, { file, fileType }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('file_type', fileType)
        
        const response = await api.post('upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        await dispatch('fetchFiles')
        return response.data
      } catch (error) {
        const errorMsg = 'Erro ao fazer upload do arquivo: ' + (error.response?.data?.error || error.message || 'Erro desconhecido')
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async applyFilter({ commit, dispatch }, { fileId, filterType }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.post(`apply-filter/${fileId}/${filterType}/`)
        commit('SET_CURRENT_FILE', response.data)
        return response.data
      } catch (error) {
        const errorMsg = `Erro ao aplicar filtro ${filterType}: ` + (error.response?.data?.error || error.message || 'Erro desconhecido')
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async extractROI({ commit, dispatch }, { fileId, x1, y1, x2, y2 }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.post(`extract-roi/${fileId}/`, { x1, y1, x2, y2 })
        await dispatch('fetchFile', fileId)
        return response.data
      } catch (error) {
        const errorMsg = 'Erro ao extrair ROI: ' + (error.response?.data?.error || error.message || 'Erro desconhecido')
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    },
    async createVideoSegment({ commit, dispatch }, { fileId, startTime, endTime }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await api.post(`video-segment/${fileId}/`, { 
          start_time: startTime, 
          end_time: endTime 
        })
        await dispatch('fetchFile', fileId)
        return response.data
      } catch (error) {
        const errorMsg = 'Erro ao criar segmento de vídeo: ' + (error.response?.data?.error || error.message || 'Erro desconhecido')
        commit('SET_ERROR', errorMsg)
        console.error(errorMsg, error)
        return null
      } finally {
        commit('SET_LOADING', false)
      }
    }
  }
})
