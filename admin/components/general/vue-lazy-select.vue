<template>
    <div>
        <div class="VueLazySelect" ref="VueLazySelect">
            <div class="VueLazyInput">
                <ul class="VueInputSelectedList" @click="RedirectFocus($event)">
                    <li v-for="item in selected" >
                        <slot name="selected" :item="item" :close="UnSelect">
                            <div class="SelectedItem">
                                <span>{{item.name}}</span>
                                <a class="UnSelectItem" @click="UnSelect(item)">X</a>
                            </div>
                        </slot>
                    </li>
                    <li>
                        <input @click="RedirectFocus($event)" :placeholder="GetPlaceholder" v-model="search" ref='LazyInput' class="LazyInput" type="text">
                    </li>
                </ul>

            </div>

            <div v-if="open" class="VueLazyResult">
                <div class="NoSearchText" v-if="!search.length">
                    Search by name, email or teacher initial
                </div>

                <div v-else-if="working" class="LazyResultWorking">
                    Working....
                </div>

                <div class="ResultList" v-else-if="items.length > 0">
                    <div v-for="(item, index) in items" @click="AddSelected(item)" class="ResultItem">
                        <slot name="item" :item="item">
                            <span>{{item.name}}</span>
                        </slot>
                    </div>
                </div>

                <div v-else class="NoResultText">
                    No Result
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { CancelToken } from 'axios'

    export default {
        name: "vue-lazy-select",
        mounted() {
            let ref = this.$refs.VueLazySelect
            let that = this

            window.addEventListener('click', function (e) {

                if (ref.contains(e.target) && e.target.className != "RemoveSelectedBtn") {
                    // that.open = true
                } else {
                    that.open = false
                    this.items = []

                }
            });



            this.CancelToken = CancelToken
            this.source = CancelToken.source()
        },
        created() {

        },
        data: () => {
            return {
                loading: false,
                open: false,
                search: "",
                items: [],
                working: false,
                selected: [],
                CancelRequest: null,
                CancelToken: null,
                source: null,
                timer: null,
            }
        },
        props: ["handle", "api", "placeholder"],
        computed: {
            GetPlaceholder() {
                return this.search.length == 0 && this.selected.length == 0 ? this.placeholder : ""
            }
        },
        watch: {
            search(value, old) {

                this.items = []
                let that = this


                if (value && value.length) {

                    this.working = true

                    if (this.timer && this.timer != null)
                        clearTimeout(this.timer)

                    this.timer = setTimeout(function () {
                        that.Fetch(value)
                    }, 250)

                }
            }
        },
        methods: {
            Fetch(keyword) {

                if (!keyword || keyword.length === 0) {
                    this.items = []
                    return
                }

                if (this.working && this.CancelRequest) {
                    this.CancelRequest()
                }

                this.working = true
                let $that = this;
                let url = this.api.replace("%1s", keyword)

                this.$axios.get(url, {
                    cancelToken: this.source.token
                })
                    .then((res) => {

                        this.items = res.data.results.filter((item) => {
                            return this.selected.findIndex(i => i[this.handle] == item[this.handle]) == -1
                        })

                    })
                    .catch(function (thrown) {

                    })
                    .finally(()=> {
                        this.working = false
                    })
            },
            RedirectFocus($event) {
                let cn = $event.target.className

                if (cn == "VueInputSelectedList" || cn == 'LazyInput') {
                    let input = this.$refs.LazyInput
                    input.focus()
                    this.open = true
                }
            },
            AddSelected(item) {
                this.selected.push(item)
                this.items = this.items.filter(i => i[this.handle] != item[this.handle])
                this.open = false
                this.search = ""
                this.$emit('input', this.selected)
            },
            UnSelect(item) {
                this.selected = this.selected.filter(x => x[this.handle] != item[this.handle])
                this.items.push(item)
                this.$emit('input', this.selected)
            }
        }
    }
</script>

<style scoped lang="scss">
    .VueLazyResult {
        box-shadow: 0 0 50px 0 rgba(82, 63, 105, .15);
        border: 1px solid #e2e5ec;
        position: absolute;
        width: 100%;
        background: #fff;
        top: 100%;
        z-index: 5;
        margin-top: 0;
    }

    .VueLazySelect {
        position: relative;
        background: #fff;
    }


    .VueLazyInput {
        border: 1px solid #ddd;
        width: 100%;
        padding: 0;
        outline: none;
        cursor: text;

        &:focus {
            border-color: rgba(44, 119, 244, .5);
        }
    }

    .ResultItem {
        padding: 8px 16px;
        cursor: pointer;
    }

    .ResultItem:hover {
        background: #f7f8fa;
    }

    .ResultList {
        max-height: 300px;
        overflow: hidden auto;
    }


    ul.VueInputSelectedList {
        list-style: none;
        padding: 3px 7px;
        overflow: hidden;
        margin: 0;
    }


    .VueInputSelectedList li {
        float: left;
        margin: 2px 5px 2px 0;

        .SelectedItem {
            float: left;
            background-color: #E9F1FE;
            padding: 3px 8px;
            border: 1px solid #e0e8f3;
            cursor: pointer;
            border-radius: 2px;
            color: #2c77f4;

            .UnSelectItem {
                margin-left: 3px;
                border-radius: 50px;
                width: 10px;
                height: 10px;
            }
        }


        &.SelectedItemInput {
            width: 3px;

            input {
                border: none;
                outline: none;
            }
        }
    }

    .LazyInput {
        background: transparent;
        border: none;
        outline: none;
        height: 33px;
        padding: 0 5px;
    }

    .NoSearchText {
        padding: 10px 20px;
    }
</style>
