import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            // Proxy /api requests to the backend during development
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                // We do NOT rewrite the path here because we updated the backend 
                // to listen on /api/analyze as well, or we can rewrite it.
                // Let's rewrite it so the backend doesn't need to change its clean routes?
                // Actually, Vercel passes the full path. It's safer if Backend handles /api/analyze.
            }
        }
    }
})
