import colors from 'vuetify/es5/util/colors'

const env = require('dotenv').config()

export default {
    mode: 'spa',
    /*
    ** Headers of the page
    */
    head: {
        titleTemplate: '%s',
        title: process.env.npm_package_name || '',
        meta: [
            {charset: 'utf-8'},
            {name: 'viewport', content: 'width=device-width, initial-scale=1'},
            {hid: 'description', name: 'description', content: process.env.npm_package_description || ''}
        ],
        link: [
            {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'},
            {rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Lato:300,300i,400,400i,700,700i&display=swap'}
        ],
        script: [
            {
                src: "https://www.2checkout.com/checkout/api/2co.min.js",
                type: "text/javascript"
            }
        ]
    },
    /*
    ** Customize the progress-bar color
    */
    loading: false,
    /*
    ** Global CSS
    */
    css: [
        '~/assets/line-awesome/css/line-awesome.css',
        '~/assets/css/style.scss',
    ],
    /*
    ** Plugins to load before mounting the App
    */
    plugins: [
        '@/plugins/IonValidate',
        '@/plugins/lib',
        '@/plugins/api',
    ],
    /*
    ** Nuxt.js dev-modules
    */
    devModules: [
        '@nuxtjs/vuetify',
    ],
    /*
    ** Nuxt.js modules
    */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios',
        '@nuxtjs/pwa',
        '@nuxtjs/dotenv',
        '@nuxtjs/auth',
    ],
    /*
    ** Axios module configuration
    ** See https://axios.nuxtjs.org/options
    */
    axios: {
        baseURL: env.parsed.APP_API
    },

    auth:{
        strategies: {
            local: {
                endpoints: {
                    login: { url: '/users/auth', method: 'post', propertyName: 'token' },
                    user: { url: '/users/', method: 'get', propertyName: 'data'},
                    logout: false,
                },

                tokenRequired: true,
                tokenType: "JWT"
            }
        },
        redirect: {
            login: '/login',
            logout: '/',
            user: '/profile',
            home: '/',
        }
    },

    /*
    ** vuetify module configuration
    ** https://github.com/nuxt-community/vuetify-module
    */
    vuetify: {
        customVariables: ['~/assets/variables.scss'],
        theme: {
            dark: false,
            themes: {
                light: {
                    primary: colors.teal.darken1,
                    accent: colors.teal.darken4,
                    secondary: colors.amber.darken3,
                    info: colors.blue .darken2,
                    warning: colors.amber.base,
                }
            }
        }
    },
    /*
    ** Build configuration
    */
    build: {
        extractCSS: true,
        /*
        ** You can extend webpack config here
        */
        extend(config, ctx) {
        }
    }
}
