"use strict";

document.addEventListener("DOMContentLoaded",()=>{
  const i18n=window.Q_I18N||{};
  const languages=i18n.names||{de:"Deutsch","en-US":"English (US)"};
  const sel=document.getElementById("locale");
  if(!sel)return;

  for(const [key,name] of Object.entries(languages))sel.add(new Option(name,key));

  let locale="de";
  try{
    const saved=localStorage.getItem("q_download_language");
    if(saved&&languages[saved])locale=saved;
  }catch(_){}

  const nav={
    de:{catalog:"Downloads",guide:"Anleitung",about:"Über Q",development:"Entwicklung",history:"Geschichte",feedback:"Feedback"},
    en:{catalog:"Downloads",guide:"Guide",about:"About Q",development:"Development",history:"History",feedback:"Feedback"}
  };

  function apply(){
    const contentLanguage=locale.startsWith("de")?"de":"en";
    document.documentElement.lang=contentLanguage;
    sel.value=locale;

    document.querySelectorAll("[data-language]").forEach(node=>{
      node.hidden=node.dataset.language!==contentLanguage;
    });

    const labels=nav[contentLanguage];
    document.querySelectorAll("[data-nav]").forEach(a=>{
      if(labels[a.dataset.nav])a.textContent=labels[a.dataset.nav];
    });

    const fallback=document.getElementById("translationFallback");
    if(fallback){
      const exact=locale.startsWith("de")||locale.startsWith("en");
      fallback.hidden=exact;
      fallback.textContent="This editorial page is currently available in German and English. English is shown for the selected interface language.";
    }
  }

  sel.addEventListener("change",()=>{
    locale=sel.value;
    try{localStorage.setItem("q_download_language",locale)}catch(_){}
    apply();
  });

  apply();
});
