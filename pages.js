"use strict";
document.addEventListener("DOMContentLoaded",()=>{
 const languages=window.Q_I18N?.names||{de:"Deutsch","en-US":"English (US)"};
 const sel=document.getElementById("locale");
 if(!sel)return;
 for(const [key,name] of Object.entries(languages))sel.add(new Option(name,key));
 let locale="de";try{const saved=localStorage.getItem("q_download_language");if(saved&&languages[saved])locale=saved}catch(_){}
 function apply(){const de=locale.startsWith("de");document.documentElement.lang=de?"de":"en";sel.value=locale;document.querySelectorAll("[data-language]").forEach(n=>n.hidden=n.dataset.language!==(de?"de":"en"));const labels=de?["Downloads","Über Q","Geschichte","Qbot","Feedback"]:["Downloads","About Q","History","Qbot","Feedback"];document.querySelectorAll(".nav a").forEach((a,i)=>{if(labels[i])a.textContent=labels[i]})}
 sel.addEventListener("change",()=>{locale=sel.value;try{localStorage.setItem("q_download_language",locale)}catch(_){}apply()});
 apply();
});