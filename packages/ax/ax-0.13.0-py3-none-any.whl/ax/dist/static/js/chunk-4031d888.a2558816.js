(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-4031d888"],{8088:function(i,t,e){(i.exports=e("24fb")(!1)).push([i.i,'.theme--light.v-chip{background:#e0e0e0;color:rgba(0,0,0,.87)}.theme--light.v-chip--disabled{color:rgba(0,0,0,.38)}.theme--dark.v-chip{background:#555;color:#fff}.theme--dark.v-chip--disabled{color:hsla(0,0%,100%,.5)}.application--is-rtl .v-chip__close{margin:0 8px 0 2px}.application--is-rtl .v-chip--removable .v-chip__content{padding:0 12px 0 4px}.application--is-rtl .v-chip--select-multi{margin:4px 0 4px 4px}.application--is-rtl .v-chip .v-avatar{margin-right:-12px;margin-left:8px}.application--is-rtl .v-chip .v-icon--right{margin-right:12px;margin-left:-8px}.application--is-rtl .v-chip .v-icon--left{margin-right:-8px;margin-left:12px}.v-chip{font-size:13px;margin:4px;outline:none;position:relative;-webkit-transition:.3s cubic-bezier(.25,.8,.5,1);transition:.3s cubic-bezier(.25,.8,.5,1)}.v-chip,.v-chip .v-chip__content{-webkit-box-align:center;-ms-flex-align:center;align-items:center;border-radius:28px;display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;vertical-align:middle}.v-chip .v-chip__content{cursor:default;height:32px;-webkit-box-pack:justify;-ms-flex-pack:justify;justify-content:space-between;padding:0 12px;white-space:nowrap;z-index:1}.v-chip--removable .v-chip__content{padding:0 4px 0 12px}.v-chip .v-avatar{height:32px!important;margin-left:-12px;margin-right:8px;min-width:32px;width:32px!important}.v-chip .v-avatar img{height:100%;width:100%}.v-chip--active,.v-chip--selected,.v-chip:focus:not(.v-chip--disabled){border-color:rgba(0,0,0,.13);-webkit-box-shadow:0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px 0 rgba(0,0,0,.14),0 1px 5px 0 rgba(0,0,0,.12);box-shadow:0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px 0 rgba(0,0,0,.14),0 1px 5px 0 rgba(0,0,0,.12)}.v-chip--active:after,.v-chip--selected:after,.v-chip:focus:not(.v-chip--disabled):after{background:currentColor;border-radius:inherit;content:"";height:100%;position:absolute;top:0;left:0;-webkit-transition:inherit;transition:inherit;width:100%;pointer-events:none;opacity:.13}.v-chip--label,.v-chip--label .v-chip__content{border-radius:2px}.v-chip.v-chip.v-chip--outline{background:transparent!important;border:1px solid currentColor;color:#9e9e9e;height:32px}.v-chip.v-chip.v-chip--outline .v-avatar{margin-left:-13px}.v-chip--small{height:24px!important}.v-chip--small .v-avatar{height:24px!important;min-width:24px;width:24px!important}.v-chip--small .v-icon{font-size:20px}.v-chip__close{-webkit-box-align:center;-ms-flex-align:center;align-items:center;color:inherit;display:-webkit-box;display:-ms-flexbox;display:flex;font-size:20px;margin:0 2px 0 8px;text-decoration:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.v-chip__close>.v-icon{color:inherit!important;font-size:20px;cursor:pointer;opacity:.5}.v-chip__close>.v-icon:hover{opacity:1}.v-chip--disabled .v-chip__close{pointer-events:none}.v-chip--select-multi{margin:4px 4px 4px 0}.v-chip .v-icon{color:inherit}.v-chip .v-icon--right{margin-left:12px;margin-right:-8px}.v-chip .v-icon--left{margin-left:-8px;margin-right:12px}',""])},8737:function(i,t,e){"use strict";e.r(t);var n=e("0a0d"),o=e.n(n),a=e("aede"),s=e("f499"),r=e.n(s),l=e("4c17"),c=e.n(l),p=e("9530"),h=e.n(p),u=e("287d");function d(){var i=Object(a.a)(["\n        query ($updateTime: String, $quicksearch: String, $guids: String, $dbName: String!) {\n          "," (\n            updateTime: $updateTime, \n            quicksearch: $quicksearch,\n            guids: $guids\n          ) {\n              guid\n              axLabel\n          }\n          form (dbName: $dbName) {\n              name\n              icon\n          }          \n        }\n      "]);return d=function(){return i},i}var v={name:"Ax1to1Column",props:{options_json:null},components:{AxForm:e("8697").default},data:function(){return{value:[],options:null,axItems:[],formIcon:null,modalGuid:null,activeItemGuid:null}},computed:{optionsForm:function(){return this.options?this.options.form:null},guidsString:function(){if(!this.value||0===this.value.length)return null;var i={items:this.value};return r()(i)},viewDbName:function(){return this.options.grid?this.options.form+this.options.grid:this.options.form}},mounted:function(){this.modalGuid=c()();var i=this.$slots.default[0].elm.innerText;i&&"null"!==i&&this.value.push(i),this.$slots.default[0].elm.innerText="",this.options_json&&(this.options=JSON.parse(this.options_json),this.loadData())},methods:{openFormModal:function(i){(this.options.enableFormModal||void 0===this.options.enableFormModal)&&(this.activeItemGuid=i.guid,this.$modal.show("tom-form-".concat(this.modalGuid)))},closeModal:function(){this.$modal.hide("tom-form-".concat(this.modalGuid))},loadData:function(){var i=this;if(!this.value||0===this.value.length)return!1;var t=h()(d(),this.viewDbName);return u.a.query({query:t,variables:{updateTime:o()(),quicksearch:null,guids:this.guidsString,dbName:this.options.form}}).then(function(t){i.axItems=t.data[i.viewDbName],i.formIcon=t.data.form.icon}).catch(function(t){i.$log.error("Error in Ax1to1Column => loadData apollo client => ".concat(t))}),!0}}},m=e("2877"),x=e("6544"),f=e.n(x),g=e("8212"),b=e("cc20"),w=Object(m.a)(v,function(){var i=this,t=i.$createElement,e=i._self._c||t;return e("span",[i._t("default"),i._l(i.axItems,function(t){return e("v-chip",{key:t.guid,staticClass:"chip"},[e("v-avatar",{staticClass:"grey"},[e("i",{class:"ax-chip-icon fas fa-"+i.formIcon})]),i._v("\n    "+i._s(t.axLabel)+"\n  ")],1)})],2)},[],!1,null,"0042aac6",null);t.default=w.exports,f()(w,{VAvatar:g.a,VChip:b.a})},bf5a:function(i,t,e){var n=e("8088");"string"==typeof n&&(n=[[i.i,n,""]]),n.locals&&(i.exports=n.locals),(0,e("499e").default)("4ea4a8e4",n,!0,{sourceMap:!1,shadowMode:!1})},cc20:function(i,t,e){"use strict";e("bf5a");var n=e("58df"),o=e("9d26"),a=e("b64a"),s=e("6a18"),r=e("98a1"),l=Object.assign||function(i){for(var t=1;t<arguments.length;t++){var e=arguments[t];for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&(i[n]=e[n])}return i};t.a=Object(n.a)(a.a,s.a,r.a).extend({name:"v-chip",props:{close:Boolean,disabled:Boolean,label:Boolean,outline:Boolean,selected:Boolean,small:Boolean,textColor:String,value:{type:Boolean,default:!0}},computed:{classes:function(){return l({"v-chip--disabled":this.disabled,"v-chip--selected":this.selected&&!this.disabled,"v-chip--label":this.label,"v-chip--outline":this.outline,"v-chip--small":this.small,"v-chip--removable":this.close},this.themeClasses)}},methods:{genClose:function(i){var t=this,e={staticClass:"v-chip__close",on:{click:function(i){i.stopPropagation(),t.$emit("input",!1)}}};return i("div",e,[i(o.a,"$vuetify.icons.delete")])},genContent:function(i){return i("span",{staticClass:"v-chip__content"},[this.$slots.default,this.close&&this.genClose(i)])}},render:function(i){var t=this.setBackgroundColor(this.color,{staticClass:"v-chip",class:this.classes,attrs:{tabindex:this.disabled?-1:0},directives:[{name:"show",value:this.isActive}],on:this.$listeners}),e=this.textColor||this.outline&&this.color;return i("span",this.setTextColor(e,t),[this.genContent(i)])}})}}]);