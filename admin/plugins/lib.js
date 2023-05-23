import Vue from 'vue';

export default function ({store, redirect}) {
    Vue.prototype.$Lib = {
        UserRoles: [
            {
                'text': 'Student',
                'value': 1,
            },
            {
                'text': 'Supervisor',
                'value': 5,
            },
            {
                'text': 'Project Committee Member',
                'value': 10,
            },
            {
                'text': 'Head',
                'value': 15,
            },
            {
                'text': 'Super Admin',
                'value': 20,
            },
        ],
        Genders:[
            {
                text: 'Male',
                value: 0,
            },
            {
                text: 'Female',
                value: 1,
            },
            {
                text: 'Other',
                value: 2,
            }
        ],
        GetUserRole: (value) => {
            let type = this.UserRoles.find(t => t.value == value)

            if (type)
                return type.text;

            return ""
        },
        GetGender: (value) => {
            let type = this.Genders.find(t => t.value == value)

            if (type)
                return type.text;

            return ""
        },

    }
}



