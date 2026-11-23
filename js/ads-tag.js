/* Blauweschild - Google Ads meting: tag, toestemming (Consent Mode v2) en conversies.
   Vul hieronder de tag-ID en de drie conversielabels in.
   Zolang er nog X'en staan, doet dit script niets. */
(function(){
  "use strict";
  var CONFIG={
    tagId:"AW-18590259177",
    conversies:{
      inspectie:"AW-18590259177/7K3PCJLC0b0dEOmvw6BF",
      spoed:"AW-18590259177/Cc9SCPf2z70dEOmvw6BF",
      telefoon:"AW-18590259177/8xCcCJ6Oy70dEOmvw6BF"
    }
  };
  if(!/^AW-\d{6,}$/.test(CONFIG.tagId))return;

  var KEY="bs-toestemming";
  var GRANTED={ad_storage:"granted",ad_user_data:"granted",ad_personalization:"granted",analytics_storage:"granted"};
  window.dataLayer=window.dataLayer||[];
  function gtag(){window.dataLayer.push(arguments);}
  window.gtag=window.gtag||gtag;
  function lezen(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function opslaan(v){try{localStorage.setItem(KEY,v);}catch(e){}}

  /* Toestemming: standaard geweigerd, pas aan na akkoord van de bezoeker. */
  gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"denied",wait_for_update:500});
  if(lezen()==="ja")gtag("consent","update",GRANTED);
  gtag("js",new Date());
  gtag("config",CONFIG.tagId);

  var s=document.createElement("script");
  s.async=true;
  s.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(CONFIG.tagId);
  document.head.appendChild(s);

  /* Conversie doorgeven. Met "klaar" wacht de pagina maximaal 0,8 s tot de melding is verstuurd. */
  function meld(naam,klaar){
    var label=CONFIG.conversies[naam];
    if(!label||/X{6}/.test(label)){if(klaar)klaar();return;}
    var gedaan=false;
    function fin(){if(gedaan)return;gedaan=true;if(klaar)klaar();}
    gtag("event","conversion",{send_to:label,event_callback:fin});
    if(klaar)setTimeout(fin,800);
  }

  /* Formulier verstuurd (Formspree gelukt): inspectie of spoed. Sollicitaties tellen niet mee. */
  var origFetch=window.fetch;
  if(origFetch){
    window.fetch=function(url,opts){
      var p=origFetch.apply(this,arguments);
      try{
        if(String(url).indexOf("formspree.io")===-1)return p;
        var soort=(opts&&opts.body&&typeof opts.body.get==="function"&&opts.body.get("Formulier"))||"";
        return p.then(function(r){
          if(!r.ok)return r;
          var naam=/spoed/i.test(soort)?"spoed":(/sollicitatie/i.test(soort)?null:"inspectie");
          if(!naam)return r;
          return new Promise(function(klaar){meld(naam,function(){klaar(r);});});
        });
      }catch(e){return p;}
    };
  }

  /* Klik op een telefoonnummer. */
  document.addEventListener("click",function(e){
    var a=e.target&&e.target.closest&&e.target.closest('a[href^="tel:"]');
    if(a)meld("telefoon");
  },true);

  /* Cookiemelding. */
  function banner(){
    if(lezen())return;
    var b=document.createElement("div");
    b.setAttribute("role","dialog");
    b.setAttribute("aria-label","Cookies");
    b.style.cssText="position:fixed;left:12px;right:12px;bottom:12px;z-index:2147483000;max-width:640px;margin:0 auto;padding:16px 18px;border-radius:14px;background:#0b1a3d;color:#e8eefc;border:1px solid #2a4a9a;box-shadow:0 10px 40px rgba(0,0,0,.5);font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif";
    var t=document.createElement("p");
    t.style.cssText="margin:0 0 12px";
    t.textContent="We gebruiken cookies van Google om te meten of onze advertenties werken. Dat doen we alleen met jouw toestemming.";
    var rij=document.createElement("div");
    rij.style.cssText="display:flex;gap:10px;flex-wrap:wrap";
    function knop(tekst,primair,fn){
      var k=document.createElement("button");
      k.type="button";
      k.textContent=tekst;
      k.style.cssText="cursor:pointer;border-radius:999px;padding:10px 18px;font:600 15px system-ui,sans-serif;color:#fff;border:1px solid "+(primair?"#3a74ff":"#5b6f9f")+";background:"+(primair?"#3a74ff":"transparent");
      k.addEventListener("click",fn);
      return k;
    }
    rij.appendChild(knop("Accepteren",true,function(){opslaan("ja");gtag("consent","update",GRANTED);b.remove();}));
    rij.appendChild(knop("Weigeren",false,function(){opslaan("nee");b.remove();}));
    b.appendChild(t);
    b.appendChild(rij);
    document.body.appendChild(b);
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",banner);else banner();
})();
