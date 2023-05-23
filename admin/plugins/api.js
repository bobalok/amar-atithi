import Vue from 'vue';

const API_HOME = ""
const Home = process.env.APP_HOME;
console.log(process.env)
console.log(111)

const API = {
    Documents: {
        List: "users/list-of-documents",
        Detail: pk => `users/documents/details/${pk}`,
        ChangeVerdict: "users/documents/change-verdict"
    },
    Payment: {
        List: "transactions/payment-requests-list",
        Detail : (pk) => `transactions/payment-requests/${pk}`,
        Update : (pk) => `transactions/update-payment-requests/${pk}`
    },
    JSONOption: {
        headers: {
            'Content-Type': 'application/json',
        }
    }
}

Vue.prototype.$api = API

export default API
