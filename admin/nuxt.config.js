//import VuetifyLoaderPlugin from 'vuetify-loader/lib/plugin'


const env = require('dotenv').config()

export default {
    mode: 'spa',
    /*
    ** Headers of the page
    */
    head: {
        titleTemplate: '%s - ' + "Amar Atithi Admin",
        title: process.env.npm_package_name || '',
        meta: [
            {charset: 'utf-8'},
            {name: 'viewport', content: 'width=device-width, initial-scale=1'},
            {hid: 'description', name: 'description', content: process.env.npm_package_description || ''}
        ],
        link: [
            {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'}
            ,
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css?family=Poppins:300,300i,400,400i,500,500i,600,600i,700,700i&display=swap'
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
        '~/assets/font/_flaticon.scss',
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
    ** Nuxt.js modules
    */
    modules: [
        '@nuxtjs/vuetify',
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios',
        '@nuxtjs/dotenv',
        '@nuxtjs/pwa',
        '@nuxtjs/auth',
    ],

    auth:{
        strategies: {
            local: {
                endpoints: {
                    login: { url: '/users/admin-auth', method: 'post', propertyName: 'token' },
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
            user: '/',
            home: '/',
        }
    },

    /*
    ** Axios module configuration
    ** See https://axios.nuxtjs.org/options
    */
    axios: {
        baseURL: env.parsed.APP_API
    },
    /*
    ** vuetify module configuration
    ** https://github.com/nuxt-community/vuetify-module
    */
    vuetify: {
        // themes: {
        //     light: {
        //         primary: "#2c77f4",
        //         accent: "#5867dd",
        //         secondary: "#ffc107",
        //         info: "#1E88E5",
        //         warning: "#ffb822",
        //         error: "#fd397a",
        //         success: "#1dc9b7"
        //     }
        // },

        theme: {
            themes: {
                light: {
                    primary: "#2c77f4",
                    accent: "#5867dd",
                    secondary: "#ffc107",
                    info: "#1E88E5",
                    warning: "#ffb822",
                    error: "#fd397a",
                    success: "#1dc9b7"
                },
            },
        },

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
