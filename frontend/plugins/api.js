import Vue from 'vue';

const API_HOME = ""
const Home = process.env.APP_HOME;


const API = {
    Users: {
        Login: "users/auth",
        Register: "users/register",
        VerifyPhone: "users/verify-phone",
        VerifyEmail: "users/verify-email",
        SelfUpdate: "users/update",
        Details: userid => `users/details/${userid}`,
        Listings: userid => `users/listings/${userid}`,
        Bookings: 'users/bookings',
        RequestVerification : "users/request-verification",
        SubmittedDocuments: "users/verification-requests",
    },
    Place: {
        Create: "places/create",
        List: "places/list",
        Recent: "places/recent-places",
        Search: "places/search",
        Update: code => `places/update/${code}`,
        Details: code => `places/details/${code}`,
        Similar: code => `places/similar/${code}`,
        Image: {
            Add: "places/add-image",
            Remove: pk => `places/remove-image/${pk}`,
        },
        Type: {
            List: "places/types"
        },
        Space: {
            List: "places/spaces"
        },
        Cities: {
            List: "places/cities"
        },
        Amenities: {
            List: "places/amenities"
        },
        Rules: {
            List: "places/rules"
        },
        Times: "places/check-times"
    },
    Reservation: {
        List: "reservations",
        GetQuote: "reservations/get-a-quote",
        CreateDraft: "reservations/create",
        ReviewYourGuest: "reservations/review-your-guest",
        ReviewTrip: "reservations/review-your-trip",
        Confirm: ref => `reservations/confirm-reservation/${ref}`,
        Details: ref => `reservations/details/${ref}`,
        Accept: ref => `reservations/accept/${ref}`,
        Reject: ref => `reservations/reject/${ref}`,
        Cancel: ref => `reservations/cancel/${ref}`,
        PayWithCredit: ref => `reservations/pay-with-credit/${ref}`,
        Adjustments: {
            List: ref => `reservations/adjustments/${ref}`,
            Details: ref => `reservations/adjustments/${ref}/details`,
            PaymentURL: ref => `reservations/adjustments/${ref}/payment-url`,
            Cancel: ref => `reservations/adjustments/cancel/${ref}`,
            Accept: ref => `reservations/adjustments/accept/${ref}`,
            CanRequestForChanges : `reservations/can-request-adjustment`
        },
        Change: "reservations/get-adjustment-quote",
        ChangeRequest: "reservations/request-adjustment",
        Payment: {
            GetPaymentURL: "reservations/get-payment-url",
            RequestsList: "transactions/payment-requests",
            Request: "transactions/request-payment"
        }
    },
    JSONOption: {
        headers: {
            'Content-Type': 'application/json',
        }
    }
}

Vue.prototype.$api = API

export default API
