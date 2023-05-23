import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify, {
    options: {
        customProperties: true
    },
    theme: {
        primary: "#2c77f4",
        accent: "#5867dd",
        secondary: "#ffc107",
        info: "#1E88E5",
        warning: "#ffb822",
        error: "#fd397a",
        success: "#1dc9b7"

    }
});
