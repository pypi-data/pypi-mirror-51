(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-2d0e502c"],{9351:function(e,t,r){"use strict";r.r(t);var n={name:"AxText",props:{name:null,dbName:null,tag:null,options:null,value:null,isRequired:null},data:function(){return{currentValue:null,errors:[]}},watch:{currentValue:function(e){this.$emit("update:value",e)},value:function(e){this.currentValue=e}},created:function(){this.currentValue=this.value},methods:{isValid:function(){return!!this.requiredIsValid()},requiredIsValid:function(){return!this.isRequired||(this.currentValue&&0!==this.currentValue.length?(this.errors=[],!0):(this.errors.push(this.options.required_text),!1))}}},u=r("2877"),a=r("6544"),l=r.n(a),i=r("a844"),s=Object(u.a)(n,function(){var e=this,t=e.$createElement;return(e._self._c||t)("v-textarea",{attrs:{"error-messages":e.errors,hint:e.options.hint,label:e.name,"auto-grow":""},on:{keyup:e.isValid},model:{value:e.currentValue,callback:function(t){e.currentValue=t},expression:"currentValue"}})},[],!1,null,"60767f83",null);t.default=s.exports,l()(s,{VTextarea:i.a})}}]);