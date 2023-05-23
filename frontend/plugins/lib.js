import Vue from 'vue';


export default function ({store, redirect}) {
    Vue.prototype.$Settings = {
        SiteName: "Amar Atithi",
        SiteTagline: "Rent Your Place",
        PageTitle: name => `${name} - ${this.SiteName}`,
        Genders: [
            {
                'text': 'Male',
                'value': 1,
            },
            {
                'text': 'Female',
                'value': 2,
            },
            {
                'text': 'Not to mention',
                'value': 0,
            }
        ],
        GetGender: (value) => {
            let type = this.Genders.find(t => t.value == value)

            if (type)
                return type.text;

            return ""
        },
        MySqlDate: "YYYY-MM-DD",
        Price(value) {
            return `${value} BDT`
        },
        CurrencyName: "BDT",

        GuestsList(limit) {
            let items = []

            for (let i = 1; i <= limit; i++) {
                items.push({
                    text: i > 1 ? `${i} guests` : `${i} guest`,
                    value: i
                })
            }

            return items
        },
        ReservationStatus: {
            DISCARDED : 0,
            DRAFT : 1,
            PAYMENT_FAILED : 2,
            PAYMENT_CANCELLED : 3,
            PAYMENT_COMPLETE : 4,
            PAYMENT_CONFIRMED : 5,
            PAYMENT_REJECTED : 6,
            PENDING : 7,
            ACCEPTED : 8,
            DECLINED : 9,
            EXPIRED : 10,
            CANCELLED : 11,
            CLOSED : 12,
            COMPLETE : 13
        }
    }
}



