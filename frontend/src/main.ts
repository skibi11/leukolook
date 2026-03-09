import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'   
import './style.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faBars, faTimes } from '@fortawesome/free-solid-svg-icons'


library.add(faBars, faTimes)

const app = createApp(App)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.use(router)                      
app.mount('#app')
