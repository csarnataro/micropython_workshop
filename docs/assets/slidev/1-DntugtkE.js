import{d as g,y as k,o as $,b as x,e as i,f as C,h as S,c as b,k as P,q as B,s as j,a6 as p}from"../modules/vue-IhCS570-.js";import{u,p as m,f as w}from"./context-BiSSNjCe.js";import{_ as h,a8 as f}from"../index-Cu5_GQ2r.js";import{_ as T}from"../arduino-friend-BTULsMmy.js";import"../modules/shiki-Dnhd8-fg.js";function v(e){return e.startsWith("/")?"/"+e.slice(1):e}function z(e,o=!1){const r=e&&["#","rgb","hsl"].some(s=>e.indexOf(s)===0),t={background:r?e:void 0,color:e&&!r?"white":void 0,backgroundImage:r?void 0:e?o?`linear-gradient(#0005, #0008), url(${v(e)})`:`url("${v(e)}")`:void 0,backgroundRepeat:"no-repeat",backgroundPosition:"center",backgroundSize:"cover"};return t.background||delete t.background,t}const I=g({__name:"cover",props:{background:{default:""}},setup(e,{expose:o}){o();const{$slidev:r,$nav:t,$clicksContext:s,$clicks:n,$page:c,$renderContext:l,$frontmatter:d}=u(),a=e,y=k(()=>z(a.background,!0)),_={$slidev:r,$nav:t,$clicksContext:s,$clicks:n,$page:c,$renderContext:l,$frontmatter:d,props:a,style:y};return Object.defineProperty(_,"__isScriptSetup",{enumerable:!1,value:!0}),_}}),M={class:"my-auto w-full"};function O(e,o,r,t,s,n){return $(),x("div",{class:"slidev-layout cover",style:S(t.style)},[i("div",M,[C(e.$slots,"default")])],4)}const A=h(I,[["render",O],["__file","/Users/christian/Private/csarnataro/micropython_workshop/slides/node_modules/@slidev/theme-default/layouts/cover.vue"]]),F={__name:"1",setup(e,{expose:o}){o(),m(f);const{$slidev:r,$nav:t,$clicksContext:s,$clicks:n,$page:c,$renderContext:l,$frontmatter:d}=u(),a={$slidev:r,$nav:t,$clicksContext:s,$clicks:n,$page:c,$renderContext:l,$frontmatter:d,InjectedLayout:A,get frontmatter(){return f},get useSlideContext(){return u},get _provideFrontmatter(){return m},get _frontmatterToProps(){return w}};return Object.defineProperty(a,"__isScriptSetup",{enumerable:!1,value:!0}),a}},L=i("h1",null,[p("Arduino "),i("img",{src:T,class:"ml-24 my-4 h-16 rounded"}),p(" Micropython")],-1),N=i("p",null,"Christian Sarnataro",-1),R=i("p",null,"WeMake Milan, Jun 22nd, 2024",-1);function U(e,o,r,t,s,n){return $(),b(t.InjectedLayout,B(j(t._frontmatterToProps(t.frontmatter,0))),{default:P(()=>[L,N,R]),_:1},16)}const D=h(F,[["render",U],["__file","/@slidev/slides/1.md"]]);export{D as default};