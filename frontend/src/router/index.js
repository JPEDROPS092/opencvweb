import { createRouter, createWebHistory } from 'vue-router'

// Importação com lazy-loading para melhor performance
const Home = () => import('../views/Home.vue')
const Upload = () => import('../views/Upload.vue')
const Gallery = () => import('../views/Gallery.vue')
const ImageEditor = () => import('../views/ImageEditor.vue')
const VideoEditor = () => import('../views/VideoEditor.vue')
const About = () => import('../views/About.vue')
const NotFound = () => import('../views/NotFound.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Início' }
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload,
    meta: { title: 'Upload de Arquivos' }
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: Gallery,
    meta: { title: 'Galeria de Arquivos' }
  },
  {
    path: '/image/:id',
    name: 'ImageEditor',
    component: ImageEditor,
    props: true,
    meta: { title: 'Editor de Imagem' }
  },
  {
    path: '/video/:id',
    name: 'VideoEditor',
    component: VideoEditor,
    props: true,
    meta: { title: 'Editor de Vídeo' }
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: { title: 'Sobre' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Página Não Encontrada' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Atualiza o título da página com base na rota
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'EdTETI'} - Processador de Imagens e Vídeos`
  next()
})

export default router
