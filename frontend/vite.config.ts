import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import fs from 'fs'
// import path from 'path'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,      // listen on 0.0.0.0
    port: 5173,
    strictPort: true,
    // https: {
    //   key: fs.readFileSync(path.resolve(__dirname, 'localhost+2-key.pem')),
    //   cert: fs.readFileSync(path.resolve(__dirname, 'localhost+2.pem')),
    // },
  },
})
