// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        colors: {
          primary: '#6200EA',          // Deep purple
          secondary: '#03DAC6',        // Teal
          accent: '#FF4081',          // Pink
          error: '#CF6679',           // Soft red
          info: '#2196F3',            // Blue
          success: '#4CAF50',         // Green
          warning: '#FB8C00',         // Orange
          background: '#121212',      // Dark background
          surface: '#1E1E1E',         // Slightly lighter than background
          'on-surface': '#E0E0E0',    // Light text on dark surface
          'primary-darken-1': '#3700B3', // Darker primary for hover states
          'secondary-darken-1': '#018786' // Darker secondary for hover states
        }
      },
      light: {
        colors: {
          primary: '#6200EA',          // Deep purple
          secondary: '#03DAC6',        // Teal
          accent: '#FF4081',          // Pink
          error: '#B00020',           // Red
          info: '#2196F3',            // Blue
          success: '#4CAF50',         // Green
          warning: '#FB8C00',         // Orange
          background: '#F5F5F5',      // Light grey background
          surface: '#FFFFFF',         // White surface
          'on-surface': '#212121',    // Dark text on light surface
          'primary-darken-1': '#3700B3', // Darker primary for hover states
          'secondary-darken-1': '#018786' // Darker secondary for hover states
        }
      }
    }
  },
  defaults: {
    VCard: {
      elevation: 2,
      rounded: 'lg'
    },
    VBtn: {
      rounded: 'pill',
      elevation: 2
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable'
    },
    VAppBar: {
      elevation: 4
    },
    VNavigationDrawer: {
      width: 280
    }
  }
})
