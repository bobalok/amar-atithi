<template>
    <div class="manag-your-space">
        <v-container grid-list-lg>
            <div class="manage-space-inner" v-if="created">

                <v-form lazy-validation v-model="valid" ref="form" @submit.prevent="FormSubmit">
                    <div class="manage-space-header">
                        <v-layout wrap>
                            <v-flex xs9>
                                <h2 class="page-title">Your Listing: {{form.title}}</h2>
                            </v-flex>
                            <v-flex xs3 class="text-right">
                                <v-btn :working="working" :disabled="working" type="submit" color="primary right">Save
                                    Changes
                                </v-btn>
                            </v-flex>
                        </v-layout>
                    </div>

                    <div class="manage-space-form">
                        <div class="form-section">
                            <h2 class="section-title">About Your Place</h2>

                            <div class="section-data">
                                <v-layout wrap>
                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>What kind of places do you have?</label>
                                            <v-select
                                                    :rules="[rules.required]"
                                                    label="What kind of place do you have?"
                                                    solo
                                                    flat
                                                    :items="types"
                                                    item-text="name"
                                                    item-value="pk"
                                                    v-model="form.type"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>Shared Space</label>
                                            <v-select
                                                    :rules="[rules.required]"
                                                    label="What will your guests have?"
                                                    solo
                                                    flat
                                                    item-text="name"
                                                    item-value="pk"
                                                    :items="spaces"
                                                    v-model="form.space"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>How many guests can you serve?</label>
                                            <v-select
                                                    :rules="[rules.required]"
                                                    label="How many guests can you serve?"
                                                    solo
                                                    flat
                                                    item-text="text"
                                                    item-value="value"
                                                    :items="GuestsList"
                                                    v-model="form.max_guest"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Address Line One</label>
                                            <v-text-field
                                                    label="Street Address"
                                                    solo
                                                    flat
                                                    :rules="[rules.required]"
                                                    v-model="form.address_one"
                                            ></v-text-field>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Address Line Two</label>
                                            <v-text-field
                                                    label="Apt., suite, building access code"
                                                    solo
                                                    flat
                                                    :rules="[rules.required]"
                                                    v-model="form.address_two"
                                            ></v-text-field>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>City</label>
                                            <v-select
                                                    :rules="[rules.required]"
                                                    label="Where does your place located?"
                                                    solo
                                                    flat
                                                    item-text="name"
                                                    item-value="code"
                                                    :items="cities"
                                                    v-model="form.city"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>State</label>
                                            <v-text-field
                                                    label="State, Region or Province"
                                                    solo
                                                    flat
                                                    :rules="[rules.required]"
                                                    v-model="form.state"
                                            ></v-text-field>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Zip Code</label>
                                            <v-text-field
                                                    label="Zip code of your area"
                                                    solo
                                                    flat
                                                    :rules="[rules.required, rules.digit]"
                                                    v-model="form.zip"
                                            ></v-text-field>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </div>
                        </div>

                        <div class="form-section">
                            <h2 class="section-title">Title and description</h2>
                            <div class="section-subtitle">Add a title and description to help guests get an idea of what
                                it’ll be like to stay in your place.
                            </div>

                            <div class="section-data">
                                <v-layout wrap>
                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Listing Title</label>
                                            <v-text-field
                                                    label="Your listing title should highlight what makes your place special"
                                                    solo
                                                    flat
                                                    :counter="60"
                                                    clearable
                                                    :rules="[rules.required, rules.max(form.title, 60)]"
                                                    v-model="form.title"
                                                    class="with-counter"
                                            ></v-text-field>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Listing description</label>

                                            <v-textarea
                                                    label="Your listing description should help guests to imagine what it’s like to stay at your place."
                                                    solo
                                                    flat
                                                    :counter="1500"
                                                    rows="7"
                                                    :rules="[rules.required, rules.max(form.description, 1500)]"
                                                    v-model="form.description"
                                                    class="with-counter"
                                            ></v-textarea>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </div>
                        </div>

                        <div class="form-section">
                            <h2 class="section-title">Bed and Bath</h2>

                            <div class="section-data">
                                <v-layout wrap>
                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>How many bed your guests can use?</label>
                                            <v-select
                                                    label="Number of beds your guest can use"
                                                    :rules="[rules.required]"
                                                    solo
                                                    flat
                                                    item-text="text"
                                                    item-value="value"
                                                    :items="BedSelect"
                                                    v-model="form.beds"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>How many baths your guests can use?</label>
                                            <v-select
                                                    label="Number of baths your guest can use"
                                                    :rules="[rules.required]"
                                                    solo
                                                    flat
                                                    item-text="text"
                                                    item-value="value"
                                                    :items="BathSelect"
                                                    v-model="form.baths"
                                            ></v-select>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </div>
                        </div>

                        <div class="form-section">
                            <h2 class="section-title">Amenities</h2>
                            <div class="section-subtitle">List of amenities you will provide to your guests</div>

                            <div class="section-data">
                                <div class="form-check-list">
                                    <v-checkbox
                                            :input-value="form.amenities.indexOf(amenity.pk) >=0 "
                                            :label="amenity.name" color="primary"
                                            :key="`amn-${amenity.pk}`"
                                            v-for="amenity in amenities"
                                            @change="AmenitiesChange($event, amenity)"
                                    ></v-checkbox>
                                </div>

                                <!--                                <div class="additional-list-item">-->
                                <!--                                    <label>Additional amenities</label>-->
                                <!--                                    <div class="form-input">-->
                                <!--                                        <input type="text">-->
                                <!--                                        <v-btn>Add</v-btn>-->
                                <!--                                    </div>-->
                                <!--                                </div>-->
                            </div>
                        </div>

                        <div class="form-section">
                            <h2 class="section-title">Set the Scene</h2>
                            <div class="section-subtitle">
                                <div>Tips to get great photos of your space</div>

                                <ul class="pt-0 mt-3">
                                    <li>Include all spaces your guest will access, like bedrooms, bathrooms, the
                                        kitchen,
                                        and
                                        living room.
                                    </li>
                                    <li>Take photos in landscape mode to capture as much of your space as possible.
                                        Shoot
                                        from
                                        corners to add perspective.
                                    </li>
                                    <li>Spaces look best in natural light. If it’s nighttime, turn on your lights. Avoid
                                        using
                                        flash.
                                    </li>
                                </ul>
                            </div>

                            <div class="section-data">
                                <div class="upload-wrap">
                                    <input ref="FileSelector" @change="FileSelected"
                                           accept="image/x-png,image/jpg,image/jpeg" type="file">
                                    <div class="upload-selector">
                                        <i class="la la-cloud-upload"></i>
                                        <div>Select an image (1MB or less)</div>
                                    </div>
                                </div>

                                <div class="uploaded-images">
                                    <div class="image-wrap" v-for="image in form.images" :key="`image_${image.pk}`">
                                        <img :src="image.file">

                                        <div class="action-btn">
                                            <v-btn @click="RemoveImage(image)" color="error" class="table-btn">
                                                <i class="white--text la la-trash"></i>
                                            </v-btn>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-section">
                            <h2 class="section-title">House Rules</h2>
                            <div class="section-subtitle">List of amenities you will provide to your guests</div>

                            <div class="section-data">
                                <div class="form-check-list">
                                    <v-checkbox
                                            :input-value="form.rules.indexOf(rule.pk) >=0 "
                                            :label="rule.name" color="primary"
                                            :key="`rule-${rule.pk}`"
                                            v-for="rule in h_rules"
                                            @change="RulesChange($event, rule)"
                                    ></v-checkbox>
                                </div>

                                <!--                                <div class="additional-list-item">-->
                                <!--                                    <label>Additional amenities</label>-->
                                <!--                                    <div class="form-input">-->
                                <!--                                        <input type="text">-->
                                <!--                                        <v-btn>Add</v-btn>-->
                                <!--                                    </div>-->
                                <!--                                </div>-->
                            </div>
                        </div>

                        <!--                        <div class="form-section">-->
                        <!--                            <h2 class="section-title">Acknowledgements</h2>-->
                        <!--                            <div class="section-subtitle">List of amenities you will provide to your guests</div>-->

                        <!--                            <div class="section-data">-->
                        <!--                                <div class="form-check-list">-->
                        <!--                                    <v-checkbox label="Wifi" color="primary"></v-checkbox>-->
                        <!--                                    <v-checkbox label="Shampoo" color="primary"></v-checkbox>-->
                        <!--                                    <v-checkbox label="Television" color="primary"></v-checkbox>-->
                        <!--                                    <v-checkbox label="Air Conditioning" color="primary"></v-checkbox>-->
                        <!--                                </div>-->

                        <!--                                <div class="additional-list-item">-->
                        <!--                                    <label>Additional amenities</label>-->
                        <!--                                    <div class="form-input">-->
                        <!--                                        <input type="text">-->
                        <!--                                        <v-btn>Add</v-btn>-->
                        <!--                                    </div>-->
                        <!--                                </div>-->
                        <!--                            </div>-->
                        <!--                        </div>-->

                        <div class="form-section mb-7">
                            <h2 class="section-title">Booking Settings</h2>

                            <div class="section-data">
                                <v-layout wrap>
                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>When can guest check-in?</label>

                                            <div class="checkinout">
                                                <div class="checkin">
                                                    <span>From:</span>
                                                    <v-select
                                                            label="Check-in start time"
                                                            :rules="[rules.required]"
                                                            solo
                                                            flat
                                                            item-text="text"
                                                            item-value="value"
                                                            :items="times.in"
                                                            v-model="form.checkin_from"
                                                    ></v-select>
                                                </div>

                                                <div class="checkin">
                                                    <span>To:</span>
                                                    <v-select
                                                            label="Check-in end time"
                                                            :rules="[rules.required]"
                                                            solo
                                                            flat
                                                            item-text="text"
                                                            item-value="value"
                                                            :items="times.in"
                                                            v-model="form.checkin_to"
                                                    ></v-select>
                                                </div>
                                            </div>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Last time to checkout?</label>
                                            <v-select
                                                    label="Checkout time"
                                                    :rules="[rules.required]"
                                                    solo
                                                    flat
                                                    item-text="text"
                                                    item-value="value"
                                                    :items="times.out"
                                                    v-model="form.checkout"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>Minimum Stay?</label>
                                            <v-select
                                                    label="Minimum night guests have to stay"
                                                    :rules="[rules.required]"
                                                    solo
                                                    flat
                                                    item-text="text"
                                                    item-value="value"
                                                    :items="NightStay"
                                                    v-model="form.min_stay"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs6>
                                        <div class="form-group last-item">
                                            <label>Maximum Stay?</label>
                                            <v-select
                                                    label="Maximum night guests can stay"
                                                    :rules="[rules.required]"
                                                    solo
                                                    flat
                                                    item-text="text"
                                                    item-value="value"
                                                    :items="NightStay"
                                                    v-model="form.max_stay"
                                            ></v-select>
                                        </div>
                                    </v-flex>

                                    <v-flex xs12>
                                        <div class="form-group last-item">
                                            <label>Price per night (in BDT)</label>
                                            <v-text-field
                                                    label="How much will you charge for each night?"
                                                    solo
                                                    flat
                                                    :rules="[rules.required, rules.digit]"
                                                    v-model="form.price"
                                                    class="with-counter"
                                            ></v-text-field>
                                        </div>
                                    </v-flex>
                                </v-layout>
                            </div>
                        </div>

                        <!--                        <div class="form-section">-->

                        <!--                            <h2 class="section-title">Booking Calendar</h2>-->
                        <!--                            <div class="section-subtitle">Block or unblock a day to prevent booking</div>-->

                        <!--                            <div class="section-data">-->
                        <!--                                <v-layout fill-height>-->
                        <!--                                    <v-flex>-->
                        <!--                                        <v-sheet height="64">-->
                        <!--                                            <v-toolbar flat color="white">-->
                        <!--                                                &lt;!&ndash;                                        <v-btn outlined class="mr-4" @click="setToday">&ndash;&gt;-->
                        <!--                                                &lt;!&ndash;                                            Today&ndash;&gt;-->
                        <!--                                                &lt;!&ndash;                                        </v-btn>&ndash;&gt;-->
                        <!--                                                <v-btn color="primary" outlined fab class="mr-2 calendar-arrow" small-->
                        <!--                                                       @click="prev">-->
                        <!--                                                    <i class="la la-chevron-left"></i>-->
                        <!--                                                </v-btn>-->
                        <!--                                                <v-btn color="primary" outlined fab class="mr-2 calendar-arrow" small-->
                        <!--                                                       @click="next">-->
                        <!--                                                    <i class="la la-chevron-right"></i>-->
                        <!--                                                </v-btn>-->
                        <!--                                                <v-toolbar-title>{{ title }}</v-toolbar-title>-->
                        <!--                                                <v-spacer></v-spacer>-->
                        <!--                                                <v-btn color="primary" outlined @click="setToday">-->
                        <!--                                                    Block This Month-->
                        <!--                                                </v-btn>-->
                        <!--                                            </v-toolbar>-->
                        <!--                                        </v-sheet>-->
                        <!--                                        <v-sheet height="600">-->
                        <!--                                            <v-calendar-->
                        <!--                                                    ref="calendar"-->
                        <!--                                                    v-model="focus"-->
                        <!--                                                    color="primary"-->
                        <!--                                                    :now="today"-->
                        <!--                                                    type="month"-->
                        <!--                                                    :weekdays="[6,0,1,2,3,4,5]"-->
                        <!--                                            >-->
                        <!--                                                <template v-slot:day="{ present, past, date }">-->
                        <!--                                                    <v-layout-->
                        <!--                                                            fill-height-->
                        <!--                                                    >-->


                        <!--                                                        <template v-if="past || date == today || tracked[date]">-->
                        <!--                                                            <div class="blocked"></div>-->
                        <!--                                                        </template>-->
                        <!--                                                    </v-layout>-->
                        <!--                                                </template>-->
                        <!--                                            </v-calendar>-->
                        <!--                                        </v-sheet>-->
                        <!--                                    </v-flex>-->
                        <!--                                </v-layout>-->
                        <!--                            </div>-->
                        <!--                        </div>-->

                        <div class="form-footer">
                            <v-btn
                                    :working="working"
                                    :disabled="working"
                                    type="submit"
                                    color="primary">{{ form.published ? 'Save Changes' : 'Save & Publish'}}
                            </v-btn>
                        </div>
                    </div>
                </v-form>

            </div>
            <div v-else class="pt-12 pb-12">
                <IonLoading/>
            </div>
        </v-container>
    </div>
</template>

<script>
    import IonLoading from "../../../components/general/IonLoading";

    export default {
        name: "ManageYourPlace",
        components: {IonLoading},
        layout: 'hosting',

        data: () => ({
            checkbox: true,
            rules: [],
            types: [],
            spaces: [],
            cities: [],
            amenities: [],
            h_rules: [],
            times: {
                in: [],
                out: []
            },
            valid: false,
            working: false,
            created: false,
            form: {
                title: "",
                description: "",
                type: "",
                space: "",
                max_guest: "",
                address_one: "",
                address_two: "",
                city: "",
                state: "",
                zip: "",
                beds: "",
                baths: "",
                checkin_from: "",
                checkin_to: "",
                checkout: "",
                min_stay: "",
                max_stay: "",
                price: "",
                images: [],
                amenities: [],
                rules: [],
            },
            hints: {
                title: "",
                description: "",
                type: "",
                space: "",
                max_guest: "",
                address_one: "",
                address_two: "",
                city: "",
                state: "",
                zip: "",
                beds: "",
                baths: "",
                checkin_from: "",
                checkin_to: "",
                checkout: "",
                min_stay: "",
                max_stay: "",
                price: "",
            },

            today: '2019-08-12',
            focus: '2019-08-12',
            type: 'month',
            tracked: {
                '2019-08-20': [23, 45, 10],
                '2019-08-16': [10],
                '2019-08-15': [0, 78, 5],
                '2019-08-13': [0, 0, 50],
                '2019-08-12': [0, 10, 23],
                '2019-08-09': [2, 90],
                '2019-08-08': [10, 32],
                '2019-08-07': [80, 10, 10],
                '2019-08-05': [20, 25, 10],
            },
            start: null,
            end: null,

        }),
        mounted() {
            this.rules = this.$validator.rules
            this.$axios.get(this.$api.Place.Type.List).then(r => this.types = r.data)
            this.$axios.get(this.$api.Place.Space.List).then(r => this.spaces = r.data)
            this.$axios.get(this.$api.Place.Cities.List).then(r => this.cities = r.data)
            this.$axios.get(this.$api.Place.Amenities.List).then(r => this.amenities = r.data)
            this.$axios.get(this.$api.Place.Rules.List).then(r => this.h_rules = r.data)
            this.$axios.get(this.$api.Place.Times).then(r => this.times = r.data)

            let code = this.$route.params.code
            let api = this.$api.Place.Update(code)

            this.$axios.get(api).then((r) => {
                this.form = r.data
                this.created = true
            })
        },
        computed: {
            title() {
                return this.focus
            },
            monthFormatter() {
                return this.$refs.calendar.getFormatter({
                    timeZone: 'UTC', month: 'long',
                })
            },
            GuestsList() {
                let items = []

                for (let i = 1; i <= 40; i++) {
                    items.push({
                        text: i > 1 ? `for ${i} guests` : `for ${i} guest`,
                        value: i
                    })
                }

                return items
            },
            BedSelect() {
                let items = []

                for (let i = 1; i <= 40; i++) {
                    items.push({
                        text: i > 1 ? `${i} beds` : `${i} bed`,
                        value: i
                    })
                }

                return items
            },
            BathSelect() {
                let items = []

                for (let i = 1; i <= 40; i++) {
                    items.push({
                        text: i > 1 ? `${i} baths` : `${i} bath`,
                        value: i
                    })
                }

                return items
            },
            NightStay() {
                let items = []

                for (let i = 1; i <= 40; i++) {
                    items.push({
                        text: i > 1 ? `${i} nights` : `${i} night`,
                        value: i
                    })
                }

                return items
            }
        },
        methods: {
            setToday() {
                this.focus = this.today
            },
            prev() {
                this.$refs.calendar.prev()
            },
            next() {
                this.$refs.calendar.next()
            },
            AmenitiesChange(event, amenity) {

                if (event) {
                    this.form.amenities.push(amenity.pk)
                } else {
                    this.form.amenities.splice(this.form.amenities.indexOf(amenity.pk), 1)
                }
            },
            RulesChange(event, rule) {
                event ? this.form.rules.push(rule.pk) : this.form.rules.splice(this.form.rules.indexOf(rule.pk), 1)
            },
            FormSubmit() {
                console.log(111)
                new Promise((resolve, reject) => {
                    this.$refs.form.validate();
                    resolve();
                })
                    .then(() => this.valid ? this.Save() : '')
            },
            Save() {
                let code = this.$route.params.code
                let url = this.$api.Place.Update(code)

                this.working = true

                this.$axios.put(url, this.form)
                    .then((r) => {
                        if (!this.form.published) {
                            this.$store.dispatch("alert/Snack", "Listing Published")
                            this.form.published = true
                        } else {
                            this.$store.dispatch("alert/Snack", "Listing Updated")
                        }
                    })
                    .finally(() => this.working = false)
            },
            FileSelected(event) {


                let file = event.target.files[0]
                let filename = file.name
                let filesize = file.size
                let filext = filename.split('.').pop().toLowerCase();
                const allowed_ext = ['jpg', 'jpeg', 'png']
                let file_error = undefined

                this.$refs.FileSelector.value = ""

                if (!allowed_ext.includes(filext))
                    file_error = {
                        title: 'File format not allowed',
                        'desc': 'The file you selected cannot be uploaded. Please select a valid file. Allowed extensions are ' + allowed_ext.join(", ")
                    }

                if (filesize > 104857600)
                    file_error = {
                        title: 'File is too big',
                        'desc': 'The file you selected is too big. Maximum allowed size is 100 MB. Please consider optimizing the file or split it into pieces.'
                    }

                if (file_error) {
                    this.$store.commit("alert/SetIonDialogue", {
                        show: true,
                        title: file_error.title,
                        NoCancel: true,
                        content: file_error.desc,
                        buttons: [
                            {
                                text: "I understand",
                                action: () => {
                                    this.$store.commit("alert/CloseIonDialogue")
                                }
                            }
                        ]
                    });

                    return
                }


                let formData = new FormData();
                formData.append("place", this.$route.params.code);
                formData.append("file", file);

                let heads = {
                    headers: {'Content-Type': 'multipart/form-data'},
                    onUploadProgress: progressEvent => {
                        let uploadPercentage = parseInt(Math.round((progressEvent.loaded * 100) / progressEvent.total))
                    }
                }


                this.$axios.post(this.$api.Place.Image.Add, formData, heads).then((response) => {
                    this.form.images.push(response.data)
                }).catch((error) => {

                })


            },
            RemoveImage(image) {
                let url = this.$api.Place.Image.Remove(image.pk)

                this.$axios.delete(url)
                    .then(() => {
                        let filtered = this.form.images.filter(item => item.pk != image.pk)
                        this.form.images = filtered
                    })
            }
        },

    }
</script>

<style lang="scss" scoped>
    h2.page-title {
        font-size: 26px;
        font-weight: 600;
    }

    .section-title {
        font-weight: 600;
        font-size: 18px;
        line-height: 26px;
        margin-bottom: 2px;
    }

    .form-section {
        margin-bottom: 40px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 45px;
        max-width: 900px;
    }

    .manage-space-header {
        margin-bottom: 50px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 15px;
    }

    .manag-your-space {
        margin: 50px 0;
    }

    .form-group label {
        margin-bottom: 5px;
        font-weight: 500;
    }


    .section-data {
        margin-top: 24px;
    }

    .section-subtitle {
    }

    .additional-list-item .form-input {
        border: 1px solid #ddd;
        position: relative;
        padding-right: 100px;
        height: 40px;
    }

    .additional-list-item .form-input button {
        position: absolute;
        right: -1px;
        top: -1px;
        background-color: rgb(249, 249, 249) !important;
        border-radius: 0 !important;
        width: 98px;
        text-align: center;
        height: 40px !important;
        margin: 0px;
        border: 1px solid #ddd;
    }

    .additional-list-item .form-input input {
        position: absolute;
        width: calc(100% - 100px);
        height: 38px;
        border: none;
        outline: none;
        padding: 0 16px;
        left: 0;
        top: 0;
        line-height: 14px;
    }

    .additional-list-item {
        margin-top: 12px;
    }

    .additional-list-item label {
        font-weight: 600;
    }

    .image-wrap {
        width: 270px;
        float: left;
        position: relative;
        margin: 0 10px 15px 10px;
        height: 270px;
        border: 2px dashed #ddd;
        padding: 5px;

        img {
            object-fit: cover;
            height: 100%;
            width: 100%;
        }
    }

    .image-wrap .action-btn {
        position: absolute;
        top: 0;
        right: 0;
        padding: 10px;
    }

    .uploaded-images {
        margin: 0 -10px;
        overflow: hidden;
    }

    .upload-wrap {
        height: 175px;
        margin: 0 0 24px 0;
        text-align: center;
        display: table;
        width: 100%;
        border: 2px dashed #d7d7d7;
        position: relative;

        input[type="file"] {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
            z-index: 5;
            font-size: 0;
            opacity: 0;
        }
    }

    .upload-selector {
        display: table-cell;
        vertical-align: middle;
        text-align: center;
        font-size: 15px;
        color: #444;

        i {
            font-size: 40px;
        }
    }


    .checkinout > div {
        width: 50%;
        float: left;
        padding: 0 4px;
    }

    .checkinout {
        overflow: hidden;
        margin: 0 -4px;
    }

    .checkinout > div > span {
        margin-bottom: 4px;
        display: block;
        color: #8a8a8a;
    }


    .blocked {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: #f3f3f3;
    }

    .calendar-arrow i {
        font-size: 16px;
    }

</style>