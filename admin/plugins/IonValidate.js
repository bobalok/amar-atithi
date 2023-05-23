import Vue from 'vue';

const Validate = {


    rules: {
        required: (value) => {
            return value != undefined && value != null && value.toString().length > 0 || "Required"
        },

        name: value => !(/\d/g.test(value != undefined ? value.trim() : "") || /[১২৩৪৫৬৭৮৯০]/.test(value != undefined ? value.trim() : "")) || "Please write a valid name",
        digit: value =>  (/^\d*$/g.test( value ) ) || "Not a number",
        min: (v, l) => v != undefined && v.length >= l || `Please enter at least ${l} characters`,
        max: (v, l) => v != undefined && v.length <= l || `No more than ${l} characters`,
        match: (value1, value2, msg) => value1 == value2 || (msg || "Please enter the same value"),
        email: value => (/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(value != undefined ? value.trim() : "")) || "Please enter a valid email"
    }

}

Vue.prototype.$validator = Validate

export default Validate
