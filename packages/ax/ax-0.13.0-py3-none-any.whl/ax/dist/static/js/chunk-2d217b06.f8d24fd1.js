(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-2d217b06"],{c894:function(e,r,u){"use strict";u.r(r);var n=u("6b54"),t={name:"AxInteger",props:{name:null,dbName:null,tag:null,options:null,value:null,isRequired:null},data:function(){return{currentValue:null,errors:[]}},watch:{currentValue:function(e){this.$emit("update:value",e)},value:function(e){this.currentValue=e}},created:function(){this.currentValue=this.value},methods:{isValid:function(){return!!this.requiredIsValid()},requiredIsValid:function(){if(this.isRequired){if(!this.currentValue||0===this.currentValue.length){var e=n.a.t("common.field-required");return this.errors.push(e),!1}return this.errors=[],!0}return!0}}},l=u("2877"),a=u("6544"),i=u.n(a),s=u("2677"),c=Object(l.a)(t,function(){var e=this,r=e.$createElement;return(e._self._c||r)("v-text-field",{attrs:{"error-messages":e.errors,label:e.name,type:"number"},on:{keyup:e.isValid},model:{value:e.currentValue,callback:function(r){e.currentValue=r},expression:"currentValue"}})},[],!1,null,"20add3f2",null);r.default=c.exports,i()(c,{VTextField:s.a})}}]);