"use strict";

document.addEventListener("DOMContentLoaded",()=>{
  const sel=document.getElementById("locale");
  if(!sel)return;

  const languages={"de":"DE","en-US":"EN"};
  for(const [key,name] of Object.entries(languages))sel.add(new Option(name,key));

  let locale="de";
  try{
    const saved=localStorage.getItem("q_download_language");
    if(saved&&saved.startsWith("en"))locale="en-US";
    else if(saved&&saved.startsWith("de"))locale="de";
    else if(!saved&&!(navigator.language||"").startsWith("de"))locale="en-US";
  }catch(_){}

  const nav={
    de:{catalog:"Downloads",about:"Über Q",development:"Entwicklung",history:"Geschichte",feedback:"Feedback"},
    en:{catalog:"Downloads",about:"About Q",development:"Development",history:"History",feedback:"Feedback"}
  };

  function apply(){
    const lang=locale==="de"?"de":"en";
    document.documentElement.lang=lang;
    sel.value=locale;
    document.querySelectorAll("[data-language]").forEach(node=>{
      node.hidden=node.dataset.language!==lang;
    });
    document.querySelectorAll("[data-nav]").forEach(a=>{
      const label=nav[lang][a.dataset.nav];
      if(label)a.textContent=label;
    });
  }

  sel.addEventListener("change",()=>{
    locale=sel.value;
    try{localStorage.setItem("q_download_language",locale)}catch(_){}
    apply();
  });

  apply();
});