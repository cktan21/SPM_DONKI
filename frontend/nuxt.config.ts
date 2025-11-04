// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },

    modules: ['@nuxtjs/tailwindcss', 'shadcn-nuxt', 'vue-sonner/nuxt', '@vueuse/nuxt'],

    // Enable WebSockets for Socket.IO
    nitro: {
        experimental: {
            websocket: true
        }
    },
    //   vueSonner: {
    //     css: false // true by default to include css file
    //   },
    shadcn: {
        /**
         * Prefix for all the imported component
         */
        prefix: '',

        /**
         * Directory that the component lives in.
         * Keep it at root: components/ui
         */
        componentDir: './components/ui'
    },

    // Make sure Nuxt scans the root components folder
    components: [
        { path: '~/components', pathPrefix: false }
    ]
})