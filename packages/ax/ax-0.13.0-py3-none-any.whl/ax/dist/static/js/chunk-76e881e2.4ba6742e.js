(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-76e881e2","chunk-0334c8c2"],{"0ece":function(e,t,i){(e.exports=i("24fb")(!1)).push([e.i,".card[data-v-6594593b]{padding:25px}.close[data-v-6594593b]{position:absolute;right:10px;top:10px}.close-ico[data-v-6594593b]{font-size:20px}",""])},"5ee1":function(e,t,i){"use strict";i.r(t);var s=i("f499"),l=i.n(s),a=(i("7f7f"),i("7514"),i("cebc")),n=i("6b54"),o=i("4360"),r={name:"AxFieldSettings",props:{guid:null,options:null,privateOptions:null,showHint:{type:Boolean,default:!0},showRequired:{type:Boolean,default:!0},showRequiredText:{type:Boolean,default:!0},showWholeRow:{type:Boolean,default:!0}},data:function(){return{isRequired:!1,isRequiredLocale:null,isWholeRow:!1,isWholeRowIsDisabled:!1,isWholeRowLocale:null,requiredTextLabel:null,reuiredText:null,hint:null,header:null,submit:null,field:null,valid:!0}},computed:{addedOptions:function(){var e=Object(a.a)({},this.options);return e.required_text=this.reuiredText,e.hint=this.hint,e},isNotVirtual:function(){return!(this.field&&this.field.fieldType.isVirtual||this.field&&this.field.fieldType.isReadonly)}},watch:{},mounted:function(){var e=this;this.field=o.a.state.form.fields.find(function(t){return t.guid===e.guid}),this.isRequired=this.field.isRequired,this.isWholeRow=this.field.isWholeRow,this.reuiredText=this.options.required_text,this.hint=this.options.hint,this.field.fieldType.isAlwaysWholeRow&&(this.isWholeRowIsDisabled=!0),this.header=n.a.t("form.field-settings-title",{name:this.field.name})},methods:{locale:function(e){return n.a.t(e)},updateSettings:function(){if(this.$refs.form.validate()){var e={};e.guid=this.field.guid,e.name=this.field.name,e.dbName=this.field.dbName,e.isRequired=this.isRequired,e.isWholeRow=this.isWholeRow,e.optionsJson=l()(this.addedOptions),e.privateOptionsJson=l()(this.privateOptions),o.a.dispatch("form/updateField",e),this.$emit("closed")}},closeModal:function(){this.$emit("closed")}}},d=(i("ea76"),i("2877")),u=i("6544"),c=i.n(u),h=i("8336"),f=i("0e8f"),p=i("4bd4"),b=i("a722"),m=i("b73d"),x=i("2677"),v=Object(d.a)(r,function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"card"},[i("v-form",{ref:"form",on:{submit:function(t){return t.preventDefault(),e.updateSettings(t)}},model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[i("h1",[e._v(e._s(e.header))]),i("v-btn",{staticClass:"close",attrs:{ripple:!1,color:"black",flat:"",icon:""},on:{click:e.closeModal}},[i("i",{staticClass:"fas fa-times close-ico"})]),i("br"),i("v-layout",{attrs:{"align-left":"",row:"",wrap:""}},[i("v-flex",{attrs:{xs5:""}},[e.showRequired?i("v-switch",{directives:[{name:"show",rawName:"v-show",value:e.isNotVirtual,expression:"isNotVirtual"}],attrs:{label:e.locale("form.is-required"),"cy-data":"is-required-input"},model:{value:e.isRequired,callback:function(t){e.isRequired=t},expression:"isRequired"}}):e._e()],1),i("v-flex",{attrs:{"offset-xs2":"",xs5:""}},[e.showWholeRow?i("v-switch",{attrs:{disabled:e.isWholeRowIsDisabled,label:e.locale("form.is-whole-row"),"cy-data":"whole-row"},model:{value:e.isWholeRow,callback:function(t){e.isWholeRow=t},expression:"isWholeRow"}}):e._e()],1),i("v-flex",{attrs:{xs12:""}},[e.showRequiredText?i("v-text-field",{directives:[{name:"show",rawName:"v-show",value:e.isNotVirtual,expression:"isNotVirtual"}],attrs:{label:e.locale("form.required-text-label"),"cy-data":"required"},model:{value:e.reuiredText,callback:function(t){e.reuiredText=t},expression:"reuiredText"}}):e._e()],1),i("v-flex",{attrs:{xs12:""}},[e.showHint?i("v-text-field",{directives:[{name:"show",rawName:"v-show",value:e.isNotVirtual,expression:"isNotVirtual"}],attrs:{label:e.locale("form.hint-setting-label"),"cy-data":"hint"},model:{value:e.hint,callback:function(t){e.hint=t},expression:"hint"}}):e._e()],1)],1),e._t("default"),i("v-btn",{attrs:{ripple:!1,"data-cy":"save-settings-btn",small:"",type:"submit"},on:{click:function(t){return t.preventDefault(),e.updateSettings(t)}}},[i("i",{staticClass:"fas fa-save"}),e._v("\n        "+e._s(e.locale("form.field-settings-submit"))+"\n    ")])],2)],1)},[],!1,null,"6594593b",null);t.default=v.exports,c()(v,{VBtn:h.a,VFlex:f.a,VForm:p.a,VLayout:b.a,VSwitch:m.a,VTextField:x.a})},6519:function(e,t,i){var s=i("0ece");"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals),(0,i("499e").default)("38323113",s,!0,{sourceMap:!1,shadowMode:!1})},6946:function(e,t,i){"use strict";i.r(t);var s=i("5ee1"),l=i("6b54"),a={name:"AxFilesSettings",components:{AxFieldSettings:s.default},props:{guid:null,options:null},data:function(){return{changedOptions:{}}},created:function(){this.changedOptions=this.options,null!=this.changedOptions.enableWebcam&&void 0!==this.changedOptions.enableWebcam||(this.changedOptions.enableWebcam=!0)},methods:{locale:function(e){return l.a.t(e)}}},n=i("2877"),o=i("6544"),r=i.n(o),d=i("0e8f"),u=i("a722"),c=i("b73d"),h=i("2677"),f=Object(n.a)(a,function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("AxFieldSettings",{attrs:{guid:e.guid,options:e.changedOptions},on:{closed:function(t){return e.$emit("closed")}}},[i("v-layout",{attrs:{row:"",wrap:""}},[i("v-flex",{attrs:{xs6:""}},[i("v-text-field",{attrs:{label:e.locale("types.AxFiles.settings-min-number-label"),type:"number"},model:{value:e.changedOptions.minNumberOfFiles,callback:function(t){e.$set(e.changedOptions,"minNumberOfFiles",t)},expression:"changedOptions.minNumberOfFiles"}})],1),i("v-flex",{attrs:{"offset-xs1":"",xs5:""}},[i("v-text-field",{attrs:{label:e.locale("types.AxFiles.settings-max-number-label"),type:"number"},model:{value:e.changedOptions.maxNumberOfFiles,callback:function(t){e.$set(e.changedOptions,"maxNumberOfFiles",t)},expression:"changedOptions.maxNumberOfFiles"}})],1),i("v-flex",{attrs:{xs6:""}},[i("v-text-field",{attrs:{hint:e.locale("types.AxFiles.settings-max-size-hint"),label:e.locale("types.AxFiles.settings-max-size-label"),"persistent-hint":"","settings-max-size-hint":"",type:"number"},model:{value:e.changedOptions.maxFileSize,callback:function(t){e.$set(e.changedOptions,"maxFileSize",t)},expression:"changedOptions.maxFileSize"}})],1),i("v-flex",{attrs:{"offset-xs1":"",xs5:""}},[i("v-switch",{attrs:{label:this.$t("types.AxFiles.settings-enable-webcam-label"),"cy-data":"settings-enableModal"},model:{value:e.changedOptions.enableWebcam,callback:function(t){e.$set(e.changedOptions,"enableWebcam",t)},expression:"changedOptions.enableWebcam"}})],1),i("br"),i("v-text-field",{attrs:{hint:e.locale("types.AxFiles.settings-types-hint"),label:e.locale("types.AxFiles.settings-types-label"),"persistent-hint":"",type:"number"},model:{value:e.changedOptions.allowedFileTypes,callback:function(t){e.$set(e.changedOptions,"allowedFileTypes",t)},expression:"changedOptions.allowedFileTypes"}})],1)],1)},[],!1,null,"075c4778",null);t.default=f.exports,r()(f,{VFlex:d.a,VLayout:u.a,VSwitch:c.a,VTextField:h.a})},ea76:function(e,t,i){"use strict";var s=i("6519");i.n(s).a}}]);