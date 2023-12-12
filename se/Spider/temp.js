webpackJsonp([5], {
    "2odu": function (t, e) {
    }, JYZw: function (t, e) {
    }, Wp4R: function (t, e) {
    }, f11U: function (t, e, n) {
        "use strict";
        var i = n("1lFP"), a = n("JwXo"), s = n("oFuF"), o = {
            updated: function () {
                var t = this;
                document.querySelectorAll("input").forEach(function (e) {
                    e.onblur = t.temporaryRepair
                }), document.querySelectorAll("select").forEach(function (e) {
                    e.onchange = t.temporaryRepair
                }), document.querySelectorAll("textarea").forEach(function (e) {
                    e.onblur = t.temporaryRepair
                })
            },
            props: {courseid: {type: String}, kpointId: {type: String}, hastext: {type: Boolean, default: !0}},
            data: function () {
                return {
                    giftId: "",
                    giftPirce: "",
                    changeIndex: 1e4,
                    pageStart: 1,
                    list: [],
                    value: "1份",
                    number: 1,
                    popupVisible: !1,
                    show: !1,
                    tableData: [{name: "1份", value: 1}, {name: "10份", value: 10}, {
                        name: "20份",
                        value: 20
                    }, {name: "66份", value: 66}, {name: "99份", value: 99}]
                }
            },
            computed: {
                BASE_URL: function () {
                    return this.$Http.defaults.staticURL
                }, STATIC_URL: function () {
                    return this.$Http.defaults.staticURL
                }
            },
            ready: function () {
            },
            mounted: function () {
                this.getGift()
            },
            methods: {
                checked: function (t, e, n) {
                    console.log(t), this.giftId = e, this.giftPirce = n, this.changeIndex = t
                }, getGift: function () {
                    var t = this;
                    Object(a.e)(this.pageStart).then(function (e) {
                        t.list = e.list
                    })
                }, openValue: function () {
                    this.show = !this.show
                }, getvalue: function (t, e) {
                    this.number = e.value, this.value = e.name, this.show = !1
                }, temporaryRepair: function () {
                    var t = window.innerHeight;
                    if (this.windowHeight !== t) {
                        var e = void 0;
                        e = document.documentElement.scrollTop || document.body.scrollTop, e -= 1, window.scrollTo(0, e), e += 1, window.scrollTo(0, e)
                    }
                }, blur: function () {
                    this.$emit("blur")
                }, commits: function () {
                    var t = this;
                    if (1e4 !== this.changeIndex) {
                        var e = Number(this.number * this.giftPirce).toFixed(2);
                        Object(i.n)(this.courseid, this.kpointId, e, this.giftId, this.number, this.giftPirce).then(function (e) {
                            t.$Http.post("/api/wxds/dounifiedorder", {
                                id: e,
                                openid: JSON.parse(s.cookie.getItem("newsinfo")).userInfo.wechatopenid
                            }).then(function (e) {
                                e.data.appId ? window.WeixinJSBridge.invoke("getBrandWCPayRequest", {
                                    appId: e.data.appId,
                                    timeStamp: e.data.timeStamp,
                                    nonceStr: e.data.nonceStr,
                                    package: e.data.package,
                                    signType: e.data.signType,
                                    paySign: e.data.paySign
                                }, function (t) {
                                    "get_brand_wcpay_request:ok" === t.err_msg ? this.changeIndex = 1e4 : t.err_msg
                                }) : t.$toast({message: "请先关注公众号", duration: 4e3})
                            }).catch(function (e) {
                                t.$toast({message: e})
                            })
                        }).catch(function () {
                            confirm("请勿重复下单，请在订单中付款或取消订单") && (t.$store.commit("common/change_ishow", {isshow: !1}), t.$router.push({path: "/rewardRecord"}))
                        })
                    } else this.$toast({message: "请选择礼物！"})
                }
            }
        }, c = {
            render: function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("div", {staticStyle: {"z-index": "100000!important"}}, [n("div", [n("i", {
                    staticClass: "iconfont icon-shang",
                    staticStyle: {opacity: "0.8"},
                    on: {
                        click: function (e) {
                            t.popupVisible = !0
                        }
                    }
                })]), t._v(" "), n("mt-popup", {
                    staticStyle: {width: "100%", "z-index": "100000!important"},
                    attrs: {position: "bottom"},
                    model: {
                        value: t.popupVisible, callback: function (e) {
                            t.popupVisible = e
                        }, expression: "popupVisible"
                    }
                }, [n("div", {
                    staticClass: "popbox",
                    staticStyle: {"z-index": "100000!important"}
                }, [n("div", {staticClass: "gift_suo"}, t._l(t.list, function (e, i) {
                    return n("div", {key: i, staticClass: "give_gift"}, [n("div", {
                        staticClass: "gift_img",
                        class: {active: i == t.changeIndex},
                        on: {
                            click: function (n) {
                                return t.checked(i, e.gid, e.price)
                            }
                        }
                    }, [n("img", {
                        directives: [{
                            name: "lazy",
                            rawName: "v-lazy",
                            value: t.STATIC_URL + e.image,
                            expression: "STATIC_URL+ item.image"
                        }], attrs: {alt: "礼物"}
                    })]), t._v(" "), n("div", {staticClass: "gi_name"}, [t._v(t._s(e.name))]), t._v(" "), n("div", {staticClass: "gi_price"}, [t._v(t._s(e.price))])])
                }), 0), t._v(" "), n("div", {staticClass: "give"}, [n("div", {staticClass: "divInput"}, [n("div", {
                    staticClass: "inputs",
                    on: {click: t.openValue}
                }, [n("div", {staticStyle: {"font-size": "14px"}}, [t._v(t._s(t.value))]), t._v(" "), n("i", {
                    class: {
                        iconfont: !0,
                        "icon-jiantou9": !t.show,
                        "icon-shangjiantou": t.show
                    }, staticStyle: {"font-size": "15px", "margin-right": "3px", "margin-left": "3px", color: "#1b1111"}
                })]), t._v(" "), n("div", {
                    staticClass: "give_btn",
                    on: {click: t.commits}
                }, [t._v("确定")])]), t._v(" "), n("div", {
                    directives: [{
                        name: "show",
                        rawName: "v-show",
                        value: t.show,
                        expression: "show"
                    }], staticClass: "list"
                }, [n("ul", t._l(t.tableData, function (e, i) {
                    return n("li", {
                        key: e.index, on: {
                            click: function (n) {
                                return t.getvalue(i, e)
                            }
                        }
                    }, [t._v(t._s(e.name))])
                }), 0)])])])]), t._v(" "), n("div")], 1)
            }, staticRenderFns: []
        };
        var r = n("C7Lr")(o, c, !1, function (t) {
            n("rTLC")
        }, "transdata-v-42396c62", null);
        e.a = r.exports
    }, qqwt: function (t, e, n) {
        "use strict";
        Object.defineProperty(e, "__esModule", {value: !0});
        var i = n("3cXf"), a = n.n(i), s = n("IHPB"), o = n.n(s), c = n("rVsN"), r = n.n(c), u = n("lC5x"), l = n.n(u),
            d = n("J0Oq"), h = n.n(d), p = n("4YfN"), m = n.n(p), v = n("1lFP"), f = {
                name: "mu-slider",
                props: {
                    name: {type: String},
                    value: {type: [Number, String], default: 0},
                    max: {type: Number, default: 100},
                    min: {type: Number, default: 0},
                    step: {type: Number, default: .1},
                    disabled: {type: Boolean, default: !1}
                },
                data: function () {
                    return {inputValue: this.value, active: !1, hover: !1, focused: !1, dragging: !1}
                },
                computed: {
                    percent: function () {
                        var t = (this.inputValue - this.min) / (this.max - this.min) * 100;
                        return t > 100 ? 100 : t < 0 ? 0 : t
                    }, fillStyle: function () {
                        return {width: this.percent + "%"}
                    }, thumbStyle: function () {
                        return {left: this.percent + "%"}
                    }, sliderClass: function () {
                        return {zero: this.inputValue <= this.min, active: this.active, disabled: this.disabled}
                    }
                },
                created: function () {
                    this.handleDragMouseMove = this.handleDragMouseMove.bind(this), this.handleMouseEnd = this.handleMouseEnd.bind(this), this.handleTouchMove = this.handleTouchMove.bind(this), this.handleTouchEnd = this.handleTouchEnd.bind(this)
                },
                methods: {
                    handleMouseDown: function (t) {
                        this.disabled || (this.setValue(t), t.preventDefault(), document.addEventListener("mousemove", this.handleDragMouseMove), document.addEventListener("mouseup", this.handleMouseEnd), this.$el.focus(), this.onDragStart(t))
                    }, handleMouseUp: function () {
                        this.disabled || (this.active = !1)
                    }, handleTouchStart: function (t) {
                        this.disabled || (this.setValue(t.touches[0]), document.addEventListener("touchmove", this.handleTouchMove), document.addEventListener("touchup", this.handleTouchEnd), document.addEventListener("touchend", this.handleTouchEnd), document.addEventListener("touchcancel", this.handleTouchEnd), t.preventDefault(), this.onDragStart(t))
                    }, handleTouchEnd: function (t) {
                        this.disabled || (document.removeEventListener("touchmove", this.handleTouchMove), document.removeEventListener("touchup", this.handleTouchEnd), document.removeEventListener("touchend", this.handleTouchEnd), document.removeEventListener("touchcancel", this.handleTouchEnd), this.onDragStop(t))
                    }, setValue: function (t) {
                        var e = this.$el, n = this.max, i = this.min, a = this.step,
                            s = (t.clientX - e.getBoundingClientRect().left) / e.offsetWidth * (n - i);
                        s = Math.round(s / a) * a + i, (s = parseFloat(s.toFixed(5))) > n ? s = n : s < i && (s = i), this.inputValue = s, this.$emit("change", s), console.log(s, "value")
                    }, onDragStart: function (t) {
                        this.dragging = !0, this.active = !0, this.$emit("dragStart", t), this.$emit("drag-start", t)
                    }, onDragUpdate: function (t) {
                        var e = this;
                        this.dragRunning || (this.dragRunning = !0, window.requestAnimationFrame(function () {
                            e.dragRunning = !1, e.disabled || e.setValue(t)
                        }))
                    }, onDragStop: function (t) {
                        this.dragging = !1, this.active = !1, this.$emit("dragStop", t), this.$emit("drag-stop", t)
                    }, handleDragMouseMove: function (t) {
                        this.onDragUpdate(t)
                    }, handleTouchMove: function (t) {
                        this.onDragUpdate(t.touches[0])
                    }, handleMouseEnd: function (t) {
                        document.removeEventListener("mousemove", this.handleDragMouseMove), document.removeEventListener("mouseup", this.handleMouseEnd), this.onDragStop(t)
                    }
                },
                watch: {
                    value: function (t) {
                        this.inputValue = t
                    }, inputValue: function (t) {
                        this.$emit("input", t)
                    }
                },
                components: {}
            }, b = {
                render: function () {
                    var t = this, e = t.$createElement, n = t._self._c || e;
                    return n("div", [n("div", {
                        staticClass: "mu-slider",
                        class: t.sliderClass,
                        attrs: {tabindex: "0"},
                        on: {
                            touchstart: t.handleTouchStart,
                            touchend: t.handleTouchEnd,
                            touchcancel: t.handleTouchEnd,
                            mousedown: t.handleMouseDown,
                            mouseup: t.handleMouseUp
                        }
                    }, [n("input", {
                        attrs: {type: "hidden", name: t.name},
                        domProps: {value: t.inputValue}
                    }), t._v(" "), n("div", {staticClass: "mu-slider-track"}), t._v(" "), n("div", {
                        staticClass: "mu-slider-fill",
                        style: t.fillStyle
                    }), t._v(" "), n("div", {staticClass: "mu-slider-thumb", style: t.thumbStyle})])])
                }, staticRenderFns: []
            };
        var g = n("C7Lr")(f, b, !1, function (t) {
            n("Wp4R")
        }, null, null).exports, y = n("oFuF"), _ = n("f11U"), x = n("dV/5"), w = n("bSIt"), S = {
            name: "audioSpeed",
            computed: m()({}, Object(w.d)({
                timeOutshow: function (t) {
                    return t.newAudio.TIME.timeOutshow
                }, timeOutIndex: function (t) {
                    return t.newAudio.TIME.index
                }
            })),
            mounted: function () {
            },
            methods: m()({}, Object(w.c)({
                close: "newAudio/CHANGETIMEOUTSHOW",
                changeSpeed: "newAudio/CHANGESPEED"
            }), Object(w.b)({A_CHANGETIME: "newAudio/A_CHANGETIME"}), {
                select: function (t, e) {
                    1 !== t.value ? this.A_CHANGETIME({value: t.value, index: e}) : this.timepickerisshow = !0
                }, sure: function () {
                    this.A_CHANGETIME({
                        value: this.$refs.picker.getValues().reduce(function (t, e) {
                            return t.value + e.value
                        }), index: 5
                    }), this.close(!1), this.timepickerisshow = !1
                }, cancel: function () {
                    this.timepickerisshow = !1
                }
            }),
            data: function () {
                return {
                    timepickerisshow: !1,
                    slots: [{
                        flex: 1,
                        values: [{name: "0小时", value: 0}, {name: "1小时", value: 36e5}, {
                            name: "2小时",
                            value: 72e5
                        }, {name: "3小时", value: 108e5}, {name: "4小时", value: 144e5}, {
                            name: "5小时",
                            value: 18e6
                        }, {name: "6小时", value: 216e5}, {name: "7小时", value: 252e5}, {
                            name: "8小时",
                            value: 288e5
                        }, {name: "9小时", value: 324e5}, {name: "10小时", value: 36e6}, {
                            name: "11小时",
                            value: 396e5
                        }, {name: "12小时", value: 432e5}, {name: "13小时", value: 468e5}, {
                            name: "14小时",
                            value: 504e5
                        }, {name: "15小时", value: 54e6}, {name: "16小时", value: 576e5}, {
                            name: "17小时",
                            value: 612e5
                        }, {name: "18小时", value: 648e5}, {name: "19小时", value: 684e5}, {
                            name: "20小时",
                            value: 72e6
                        }, {name: "21小时", value: 756e5}, {name: "22小时", value: 792e5}, {
                            name: "23小时",
                            value: 828e5
                        }, {name: "24小时", value: 864e5}],
                        className: "slot1",
                        textAlign: "center"
                    }, {divider: !0, content: "-", className: "slot2"}, {
                        flex: 1,
                        values: [{name: "5分钟", value: 3e5}, {name: "10分钟", value: 6e5}, {
                            name: "15分钟",
                            value: 9e5
                        }, {name: "20分钟", value: 12e5}, {name: "25分钟", value: 15e5}, {
                            name: "30分钟",
                            value: 18e5
                        }, {name: "35分钟", value: 21e5}, {name: "40分钟", value: 24e5}, {
                            name: "45分钟",
                            value: 27e5
                        }, {name: "50分钟", value: 3e6}, {name: "55分钟", value: 33e5}],
                        className: "slot3",
                        textAlign: "center"
                    }],
                    sheetVisible: !0,
                    actions: [{name: "不开启", value: -1}, {name: "3分钟", value: 18e4}, {
                        name: "6分钟",
                        value: 36e4
                    }, {name: "10分钟", value: 6e5}, {name: "20分钟", value: 12e5}, {name: "自定义", value: 1}]
                }
            }
        }, E = {
            render: function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("div", [n("mt-popup", {
                    staticClass: "pop",
                    attrs: {
                        value: t.timeOutshow,
                        closeOnClickModal: !1,
                        position: "bottom",
                        "popup-transition": "popup-fade"
                    }
                }, [n("div", {staticClass: "box"}, [n("ul", t._l(t.actions, function (e, i) {
                    return n("li", {
                        key: i, class: {active: t.timeOutIndex === i}, on: {
                            click: function (n) {
                                return t.select(e, i)
                            }
                        }
                    }, [t._v(t._s(e.name))])
                }), 0), t._v(" "), n("div", {
                    staticClass: "close", on: {
                        click: function (e) {
                            return t.close(!1)
                        }
                    }
                }, [t._v("\n        关闭\n      ")])])]), t._v(" "), n("mt-popup", {
                    staticClass: "pop",
                    attrs: {
                        value: t.timepickerisshow,
                        closeOnClickModal: !1,
                        position: "bottom",
                        "popup-transition": "popup-fade"
                    }
                }, [n("div", {staticClass: "buttonclass"}, [n("div", {on: {click: t.cancel}}, [t._v("取消")]), t._v(" "), n("div", {on: {click: t.sure}}, [t._v("确定")])]), t._v(" "), n("mt-picker", {
                    ref: "picker",
                    attrs: {"value-key": "name", slots: t.slots}
                })], 1)], 1)
            }, staticRenderFns: []
        };
        var C = n("C7Lr")(S, E, !1, function (t) {
            n("2odu")
        }, "transdata-v-626dd1f4", null).exports, O = n("QmSG"), k = {
            components: {kSlider: g, Appreciation: _.a, audioTimeout: C},
            data: function () {
                return {
                    SPEED: {index: 1, speed: 1, speedName: "正常速度", speedShow: !1},
                    TIME: {timeOutshow: !1, index: 0, runTiming: -1},
                    playVideo: {},
                    topStart: 1,
                    bottomStart: 1,
                    rangeValue: 0,
                    chapterList: [],
                    totallength: 1,
                    detail: {},
                    vidoeTime: 0,
                    nowchapter: {nowIndex: 0},
                    coverShow: !1,
                    rnum: 0
                }
            },
            computed: m()({
                BASE_URL: function () {
                    return this.$Http.defaults.staticURL
                }, listIndex: function () {
                    var t = this;
                    return this.chapterList.findIndex(function (e) {
                        return e.id === t.playObject.id
                    })
                }, timeNameFormate: function () {
                    return -1 === this.timeName ? "定时关闭" : Object(y.secondToDate)(this.timeName / 1e3)
                }
            }, Object(w.d)({
                speedName: function (t) {
                    return t.newAudio.SPEED.speedName
                }, playObject: function (t) {
                    return t.newAudio.playObject
                }, timeName: function (t) {
                    return t.newAudio.TIME.runTiming
                }
            })),
            watch: {
                rnum: function (t) {
                    this.CHANGE_PLAYOBJECT(m()({}, this.playObject, {rnum: t}))
                }, listIndex: function () {
                    this.CHANGE_PLAYOBJECT(m()({}, this.playObject, {listIndex: this.listIndex}))
                }, "playObject.nowtimes": {
                    immediate: !0, handler: function () {
                        this.rangeValue = this.playObject.nowtimes / this.playObject.seconds * 100
                    }
                }
            },
            mounted: function () {
                var t = this;
                x.a.$on("Bus_next", function () {
                    t.next()
                }), this.infoInit()
            },
            beforeDestroy: function () {
                var t = this;
                return h()(l.a.mark(function e() {
                    return l.a.wrap(function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2, t.saveStudyHistory();
                            case 2:
                            case"end":
                                return e.stop()
                        }
                    }, e, t)
                }))()
            },
            methods: m()({}, Object(w.c)({
                CHANGE_PLAYOBJECT: "newAudio/CHANGE_PLAYOBJECT",
                CHANGE_LIST: "newAudio/CHANGE_LIST",
                close: "newAudio/CHANGESPEEDSHOW",
                closeTime: "newAudio/CHANGETIMEOUTSHOW"
            }), Object(w.b)({NEXTSONG: "newAudio/NEXTSONG", PREVIOUS: "newAudio/PREVIOUS"}), {
                previous: function () {
                    var t = this;
                    return h()(l.a.mark(function e() {
                        return l.a.wrap(function (e) {
                            for (; ;) switch (e.prev = e.next) {
                                case 0:
                                    if (t.$store.commit("newAudio/CHANGESPEED", t.SPEED, "正常速度"), t.$store.commit("newAudio/CHANGETIMEINDEX", t.TIME, 0), !(t.playObject.listIndex <= 0 && t.rnum > O.a)) {
                                        e.next = 7;
                                        break
                                    }
                                    return e.next = 5, t.loadRefresh();
                                case 5:
                                    e.next = 9;
                                    break;
                                case 7:
                                    if (!(t.playObject.listIndex <= 0 && t.rnum <= 1)) {
                                        e.next = 9;
                                        break
                                    }
                                    return e.abrupt("return");
                                case 9:
                                    if (!(t.rnum > 0)) {
                                        e.next = 14;
                                        break
                                    }
                                    return e.next = 12, t.PREVIOUS();
                                case 12:
                                    setTimeout(function () {
                                        t.$myaudio.play()
                                    }, 1e3), t.rnum -= 1;
                                case 14:
                                case"end":
                                    return e.stop()
                            }
                        }, e, t)
                    }))()
                }, next: function () {
                    var t = this;
                    return h()(l.a.mark(function e() {
                        return l.a.wrap(function (e) {
                            for (; ;) switch (e.prev = e.next) {
                                case 0:
                                    if (t.$store.commit("newAudio/CHANGESPEED", t.SPEED, "正常速度"), t.$store.commit("newAudio/CHANGETIMEINDEX", t.TIME, 0), !(t.playObject.listIndex >= t.chapterList.length - 1 && Math.ceil(t.rnum / O.a) < Math.ceil(t.totallength / O.a))) {
                                        e.next = 7;
                                        break
                                    }
                                    return e.next = 5, t.loadMore();
                                case 5:
                                    e.next = 11;
                                    break;
                                case 7:
                                    if (!(t.playObject.listIndex >= t.chapterList.length - 1 && Math.ceil(t.rnum / O.a) === Math.ceil(t.totallength / O.a))) {
                                        e.next = 11;
                                        break
                                    }
                                    return console.log(t.playObject, t.chapterList, t.playObject.listIndex, t.chapterList.length, t.totallength, t.rnum, O.a, Math.ceil(t.rnum / O.a), "他们的下标"), t.$toast({message: "到底了！"}), e.abrupt("return");
                                case 11:
                                    if (!(t.rnum < t.totallength)) {
                                        e.next = 16;
                                        break
                                    }
                                    return e.next = 14, t.NEXTSONG();
                                case 14:
                                    setTimeout(function () {
                                        t.$myaudio.play()
                                    }, 1e3), t.rnum += 1;
                                case 16:
                                case"end":
                                    return e.stop()
                            }
                        }, e, t)
                    }))()
                }, getDetailByid: function () {
                    var t, e = this;
                    return new r.a((t = h()(l.a.mark(function t(n) {
                        var i, a, s, o, c, r, u, d, h, p, m, f;
                        return l.a.wrap(function (t) {
                            for (; ;) switch (t.prev = t.next) {
                                case 0:
                                    return t.next = 2, Object(v.g)(e.$route.params.kpointId);
                                case 2:
                                    if (e.playVideo = t.sent, i = e.playVideo, a = i.id, s = i.name, o = i.audioInfo, c = o.imageurl, r = o.url, u = o.seconds, d = i.rnum, h = i.update_time, p = i.courseid, m = i.isLock, f = 0, e.playVideo.history && (f = e.playVideo.history.along), e.rnum = d, e.topStart = Math.ceil(d / O.a), e.bottomStart = Math.ceil(d / O.a) - 1, !e.playObject.playState || e.playObject.id !== e.$route.params.kpointId) {
                                        t.next = 12;
                                        break
                                    }
                                    return n(), t.abrupt("return");
                                case 12:
                                    e.CHANGE_PLAYOBJECT({
                                        courseid: p,
                                        isLock: m,
                                        listIndex: e.listIndex,
                                        id: a,
                                        name: s,
                                        imageurl: c,
                                        url: r,
                                        playState: !1,
                                        seconds: u,
                                        update_time: h,
                                        nowtimes: f
                                    }), n();
                                case 14:
                                case"end":
                                    return t.stop()
                            }
                        }, t, e)
                    })), function (e) {
                        return t.apply(this, arguments)
                    }))
                }, getChapterByid: function (t) {
                    var e = this, n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : function () {
                    };
                    return new r.a(function (i) {
                        var a = 0;
                        a = t ? e.bottomStart : e.topStart, Object(v.h)(e.$route.params.courseid, a).then(function (s) {
                            e.chapterList = t ? [].concat(o()(e.chapterList), o()(s.list)) : [].concat(o()(s.list), o()(e.chapterList)), e.CHANGE_LIST(e.chapterList), e.totallength = s.total, a < Math.ceil(e.totallength / O.a) ? e.$nextTick(function () {
                                n()
                            }) : e.$nextTick(function () {
                                e.$refs.myscroller.finishInfinite(!0)
                            }), i()
                        })
                    })
                }, loadMore: function (t) {
                    var e = this;
                    return h()(l.a.mark(function n() {
                        return l.a.wrap(function (n) {
                            for (; ;) switch (n.prev = n.next) {
                                case 0:
                                    return n.abrupt("return", new r.a(function (n, i) {
                                        e.bottomStart = e.bottomStart + 1, e.chapterList.length >= e.totallength || e.$nextTick(h()(l.a.mark(function i() {
                                            return l.a.wrap(function (i) {
                                                for (; ;) switch (i.prev = i.next) {
                                                    case 0:
                                                        return i.next = 2, e.getChapterByid(!0, t);
                                                    case 2:
                                                        n();
                                                    case 3:
                                                    case"end":
                                                        return i.stop()
                                                }
                                            }, i, e)
                                        })))
                                    }));
                                case 1:
                                case"end":
                                    return n.stop()
                            }
                        }, n, e)
                    }))()
                }, loadRefresh: function () {
                    var t = this;
                    return new r.a(function (e) {
                        t.topStart <= 1 ? t.$refs.myscroller.finishPullToRefresh() : (t.topStart = t.topStart - 1, t.$nextTick(h()(l.a.mark(function n() {
                            return l.a.wrap(function (n) {
                                for (; ;) switch (n.prev = n.next) {
                                    case 0:
                                        return n.next = 2, t.getChapterByid(!1);
                                    case 2:
                                        t.$refs.myscroller.finishPullToRefresh(), e();
                                    case 4:
                                    case"end":
                                        return n.stop()
                                }
                            }, n, t)
                        }))))
                    })
                }, playOrpause: function () {
                    this.$myaudio.paused ? (this.$myaudio.currentTime = this.playObject.nowtimes, this.$myaudio.play()) : (this.$myaudio.pause(), this.$store.dispatch("newAudio/SAVEHISTORY"))
                }, blur: function () {
                    window.scroll(0, 2e3)
                }, saveStudyHistory: function () {
                    this.playObject.courseid && (y.cookie.setItem("playobject", a()(this.playObject)), Object(v.m)(this.playObject.courseid, this.playObject.id, this.playObject.nowtimes))
                }, jump: function (t) {
                    var e = this;
                    if (this.playObject.listIndex > t) this.rnum = this.rnum - (this.playObject.listIndex - t); else {
                        if (!(this.playObject.listIndex < t)) return;
                        this.rnum = this.rnum + (t - this.playObject.listIndex)
                    }
                    this.$store.dispatch("newAudio/SAVEHISTORY"), "1" !== this.chapterList[t].isLock ? this.$nextTick(function () {
                        var n = e.chapterList;
                        e.CHANGE_PLAYOBJECT(m()({}, e.playObject, {
                            isLock: n[t].isLock,
                            listIndex: t,
                            id: n[t].id,
                            name: n[t].name,
                            imageurl: n[t].audioInfo.imageurl,
                            url: n[t].audioInfo.url,
                            playState: !0,
                            seconds: n[t].audioInfo.seconds,
                            update_time: n[t].update_time,
                            nowtimes: 0
                        })), setTimeout(function () {
                            e.$myaudio.play()
                        }, 200)
                    }) : this.$toast({message: "未购买的章节"})
                }, onDemand: function (t) {
                }, seekmusic: function (t) {
                    this.$myaudio.currentTime = t * this.playObject.seconds / 100
                }, getChapterIndexByKid: function () {
                }, infoInit: function () {
                    var t = this;
                    return h()(l.a.mark(function e() {
                        return l.a.wrap(function (e) {
                            for (; ;) switch (e.prev = e.next) {
                                case 0:
                                    return e.next = 2, t.getDetailByid();
                                case 2:
                                    if (t.playVideo.history && (t.$myaudio.currentTime = t.playVideo.history.along), t.bottomStart = t.bottomStart + 1, !(t.chapterList.length >= t.totallength)) {
                                        e.next = 6;
                                        break
                                    }
                                    return e.abrupt("return");
                                case 6:
                                    t.$nextTick(h()(l.a.mark(function e() {
                                        return l.a.wrap(function (e) {
                                            for (; ;) switch (e.prev = e.next) {
                                                case 0:
                                                    return e.next = 2, t.getChapterByid(!0);
                                                case 2:
                                                case"end":
                                                    return e.stop()
                                            }
                                        }, e, t)
                                    }))), t.$store.commit("newAudio/CHANGEADDIOSHOW", !0);
                                case 8:
                                case"end":
                                    return e.stop()
                            }
                        }, e, t)
                    }))()
                }, collect: function (t) {
                    var e = this;
                    return h()(l.a.mark(function n() {
                        var i;
                        return l.a.wrap(function (n) {
                            for (; ;) switch (n.prev = n.next) {
                                case 0:
                                    if (i = 0, 0 !== t) {
                                        n.next = 7;
                                        break
                                    }
                                    return i = 1, n.next = 5, Object(v.d)(e.playObject.id, 6);
                                case 5:
                                    n.next = 10;
                                    break;
                                case 7:
                                    return i = 0, n.next = 10, Object(v.c)(e.playObject.id, 6);
                                case 10:
                                    e.chapterList[e.listIndex].isFavorites = i, e.CHANGE_LIST(e.chapterList);
                                case 12:
                                case"end":
                                    return n.stop()
                            }
                        }, n, e)
                    }))()
                }, secondToDate: function (t) {
                    return Object(y.secondToDate)(Math.floor(t))
                }
            })
        }, T = {
            render: function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return t.playVideo.audioInfo ? n("div", {staticClass: "audio"}, [n("div", [n("div", {
                    staticClass: "banner",
                    style: {backgroundImage: "url(" + (t.BASE_URL + t.playObject.imageurl) + ")"}
                }), t._v(" "), n("div", {staticClass: "content"}, [n("div", {staticClass: "title"}, [t._v("\n        " + t._s(t.playObject.name) + "\n      ")]), t._v(" "), n("div", {
                    directives: [{
                        name: "momentL",
                        rawName: "v-momentL",
                        value: t.playObject.update_time,
                        expression: "playObject.update_time"
                    }], staticClass: "time"
                }), t._v(" "), n("div", {
                    staticClass: "header",
                    staticStyle: {position: "relative", "z-index": "1000"}
                }, [t.BASE_URL + t.playObject.imageurl ? n("img", {
                    directives: [{
                        name: "lazy",
                        rawName: "v-lazy",
                        value: t.BASE_URL + t.playObject.imageurl,
                        expression: "BASE_URL+playObject.imageurl"
                    }]
                }) : t._e(), t._v(" "), n("Appreciation", {
                    staticStyle: {
                        "margin-right": "0.4rem",
                        position: "absolute",
                        top: "-1.8rem",
                        right: "-2.8rem"
                    }, attrs: {courseid: t.$route.params.courseid, kpointId: t.playObject.id}, on: {blur: t.blur}
                })], 1)]), t._v(" "), n("div", {staticClass: " "}, [n("kSlider", {
                    attrs: {min: 0, max: 100},
                    on: {change: t.seekmusic},
                    model: {
                        value: t.rangeValue, callback: function (e) {
                            t.rangeValue = e
                        }, expression: "rangeValue"
                    }
                }), t._v(" "), n("div", {staticClass: "timesbox"}, [n("span", [t._v(t._s(t.secondToDate(t.playObject.nowtimes)))]), t._v(" "), n("span", [t._v(t._s(t.secondToDate(t.playObject.seconds)))])]), t._v(" "), n("div", {staticClass: "control"}, [n("span", {
                    class: {
                        iconfont: !0,
                        "icon-48shangyishou": !0
                    }, on: {
                        click: function (e) {
                            return t.previous()
                        }
                    }
                }), t._v(" "), n("span", {
                    class: {
                        iconfont: !0,
                        "icon-zanting1": t.playObject.playState,
                        "icon-qidong": !t.playObject.playState,
                        play: !0
                    }, on: {click: t.playOrpause}
                }), t._v(" "), n("span", {
                    class: {iconfont: !0, "icon-49xiayishou": !0}, on: {
                        click: function (e) {
                            return t.next()
                        }
                    }
                })]), t._v(" "), n("div", {staticClass: "bottombanner"}, [n("div", {
                    staticClass: "bottombanner-box",
                    on: {
                        click: function (e) {
                            t.coverShow = !t.coverShow
                        }
                    }
                }, [n("span", {staticClass: "iconfont icon-liebiaoshouqi"}), t._v(" "), n("span", [t._v(t._s(t.rnum) + "/" + t._s(t.totallength))])]), t._v(" "), t.chapterList.length > 0 ? n("div", {staticClass: "bottombanner-box"}, [n("span", {
                    class: {
                        iconfont: !0,
                        "icon-shoucang": 0 == t.chapterList[t.listIndex].isFavorites,
                        "icon-shoucang-not11": 1 == t.chapterList[t.listIndex].isFavorites,
                        shoucang: !0
                    }, on: {
                        click: function (e) {
                            return t.collect(t.chapterList[t.listIndex].isFavorites)
                        }
                    }
                }), t._v(" "), n("span", [t._v("收藏")])]) : t._e(), t._v(" "), n("div", {staticClass: "bottombanner-box"}, [n("span", {
                    staticClass: "iconfont iconfont icon-zengsong-copy-copy-copy-copy icon_t",
                    on: {
                        click: function (e) {
                            return t.$router.push({name: "rewardList", params: {kpointid: t.playObject.id}})
                        }
                    }
                }), t._v(" "), n("span", [t._v("打赏榜单")])]), t._v(" "), n("div", {staticClass: "bottombanner-box"}, [n("span", {
                    staticClass: "iconfont icon-huojian",
                    on: {
                        click: function (e) {
                            return t.close(!0)
                        }
                    }
                }), t._v(" "), n("span", [t._v(t._s(t.speedName))])]), t._v(" "), n("div", {staticClass: "bottombanner-box"}, [n("span", {
                    staticClass: "iconfont icon-timer",
                    on: {
                        click: function (e) {
                            return t.closeTime(!0)
                        }
                    }
                }), t._v(" "), n("span", [t._v(t._s(t.timeNameFormate))])])])], 1)]), t._v(" "), n("div", {
                    directives: [{
                        name: "show",
                        rawName: "v-show",
                        value: t.coverShow,
                        expression: "coverShow"
                    }], staticClass: "cover"
                }, [n("div", {staticClass: "playercontent"}, [n("div", {staticClass: "player-title"}, [n("span", [t._v("播放列表")]), t._v(" "), n("span", {
                    staticClass: "iconfont icon-shanchu",
                    on: {
                        click: function (e) {
                            t.coverShow = !t.coverShow
                        }
                    }
                })]), t._v(" "), n("div", {staticClass: "listen-list"}, [n("scroller", {
                    ref: "myscroller",
                    attrs: {refreshText: "下拉加载更多", "on-refresh": t.loadRefresh, "on-infinite": t.loadMore}
                }, t._l(t.chapterList, function (e, i) {
                    return n("div", {
                        key: i, staticClass: 'list-iteam active"', on: {
                            click: function (e) {
                                return t.jump(i)
                            }
                        }
                    }, [n("div", {staticClass: "list-iteam-left"}, [n("span", {
                        class: {
                            iconfont: !0,
                            "icon-zanting1": t.playObject.playState && t.playObject.id == e.id,
                            "icon-qidong": !(t.playObject.playState && t.playObject.id == e.id)
                        }
                    }), t._v(" "), n("span", {
                        class: {
                            name: !0,
                            active: t.playObject.playState && t.playObject.id == e.id
                        }
                    }, [t._v(t._s(e.name) + " "), 0 != e.isLock ? n("i", {
                        staticClass: "iconfont icon-suo",
                        staticStyle: {"font-size": "14px"}
                    }) : t._e()])]), t._v(" "), n("span", {staticClass: "times"}, [t._v(t._s(t.secondToDate(e.audioInfo.seconds)))])])
                }), 0)], 1)])]), t._v(" "), n("audioTimeout")], 1) : t._e()
            }, staticRenderFns: []
        };
        var I = n("C7Lr")(k, T, !1, function (t) {
            n("JYZw")
        }, "transdata-v-1c069eae", null);
        e.default = I.exports
    }, rTLC: function (t, e) {
    }
});

var ρ = getRR(测定值1);

// var v1 =getRR(定容体积);
//
// var v2 =getRR(提取液体积);

var d = getRR(稀释倍数);

// var m = getRR(称样量);
//
// var wdm = getRR(干物质含量);
//
// var v3 =getRR(净化体积);

// var w = ρ * v1 * v2 * d * 100 / (m * wdm * v3);

var w = ρ * d;

w;