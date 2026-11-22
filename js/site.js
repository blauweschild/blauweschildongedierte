/* Blauweschild – gedeeld script voor alle pagina's */
(function(){
  const ROOT=document.body.dataset.root||"";
  const TEL="085 060 5985",MAIL="blauweschildongedierte@gmail.com";

  /* ===== FORMSPREE =====
     Alle formulieren versturen via dit endpoint (https://formspree.io/f/xbgoplzz).
     Het versturen gebeurt op de achtergrond; de bezoeker blijft op deze site
     en komt na verzending op de eigen bedankpagina. */
  const FORMSPREE_ID="xbgoplzz";

  /* ---------- menu: uitklappers ---------- */
  const dds=[...document.querySelectorAll(".menu [aria-expanded]")];
  const closeAll=except=>dds.forEach(b=>{if(b!==except){b.setAttribute("aria-expanded","false");b.nextElementSibling.hidden=true;}});
  dds.forEach(b=>{
    const panel=b.nextElementSibling,li=b.parentElement;let t;
    b.addEventListener("click",()=>{const open=b.getAttribute("aria-expanded")!=="true";closeAll(b);b.setAttribute("aria-expanded",open);panel.hidden=!open;});
    if(matchMedia("(hover:hover)").matches){
      li.addEventListener("mouseenter",()=>{clearTimeout(t);closeAll(b);b.setAttribute("aria-expanded","true");panel.hidden=false;});
      li.addEventListener("mouseleave",()=>{t=setTimeout(()=>{b.setAttribute("aria-expanded","false");panel.hidden=true;},180);});
    }
    li.addEventListener("focusout",e=>{if(!li.contains(e.relatedTarget)){b.setAttribute("aria-expanded","false");panel.hidden=true;}});
  });
  document.addEventListener("click",e=>{if(!e.target.closest(".menu"))closeAll();});

  /* ---------- mobiel menu ---------- */
  const mnav=document.getElementById("mnav"),burger=document.getElementById("burger");
  if(mnav&&burger){
    const openM=()=>{mnav.hidden=false;burger.setAttribute("aria-expanded","true");document.body.style.overflow="hidden";mnav.querySelector("button").focus();};
    const closeM=()=>{mnav.hidden=true;burger.setAttribute("aria-expanded","false");document.body.style.overflow="";burger.focus();};
    burger.addEventListener("click",openM);
    mnav.querySelector("[data-close]").addEventListener("click",closeM);
    mnav.addEventListener("click",e=>{if(e.target.closest("a"))closeM();});
    document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!mnav.hidden)closeM();});
  }

  /* ---------- spoedvenster ---------- */
  const sp=document.getElementById("spoed");let lastFocus=null;
  if(sp){
    const openS=()=>{lastFocus=document.activeElement;if(mnav&&!mnav.hidden){mnav.hidden=true;document.body.style.overflow="";}sp.hidden=false;document.getElementById("spoed-x").focus();};
    const closeS=()=>{sp.hidden=true;if(lastFocus)lastFocus.focus();};
    document.querySelectorAll("[data-spoed]").forEach(b=>b.addEventListener("click",openS));
    document.getElementById("spoed-x").addEventListener("click",closeS);
    sp.addEventListener("click",e=>{if(e.target===sp)closeS();});
    document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!sp.hidden)closeS();});
    document.getElementById("spoed-copy").addEventListener("click",e=>{
      const b=e.currentTarget,done=()=>{b.textContent="Gekopieerd";setTimeout(()=>b.textContent="Kopieer nummer",1800);};
      const sel=()=>{const r=document.createRange();r.selectNodeContents(document.getElementById("spoed-nr"));const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent="Geselecteerd";};
      try{navigator.clipboard.writeText(TEL.replace(/\s/g,"")).then(done,sel);}catch(err){sel();}
    });
  }

  /* ---------- formulieren ---------- */
  const ENDPOINT="https://formspree.io/f/"+FORMSPREE_ID;
  const holderOf=f=>f.closest(".field")||f.closest("label")||f.parentElement;
  const nameOf=f=>{const h=holderOf(f),l=h&&h.querySelector(".lbl");return (l?l.textContent:(f.name||"dit veld")).replace("*","").trim().toLowerCase();};
  function setErr(f,msg){
    f.setAttribute("aria-invalid","true");
    const h=holderOf(f);let e=h.querySelector(".field-err");
    if(!e){e=document.createElement("small");e.className="field-err";e.id=(f.id||f.name)+"-err";h.appendChild(e);f.setAttribute("aria-describedby",e.id);}
    e.textContent=msg;
  }
  function clearErr(f){
    f.removeAttribute("aria-invalid");
    const h=holderOf(f),e=h&&h.querySelector(".field-err");
    if(e){e.remove();f.removeAttribute("aria-describedby");}
  }
  function validate(form){
    const bad=[];
    form.querySelectorAll("input,select,textarea").forEach(f=>{
      if(f.closest(".hp")||f.type==="radio"||(f.type==="checkbox"&&!f.required))return;
      clearErr(f);
      const v=f.type==="checkbox"?f.checked:f.value.trim();
      if(f.required&&!v){setErr(f,f.type==="checkbox"?"Vink dit aan om je aanvraag te versturen.":"Vul je "+nameOf(f)+" in.");bad.push(f);return;}
      if(!v||f.type==="checkbox")return;
      if(f.type==="email"&&!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)){setErr(f,"Dit lijkt geen geldig e-mailadres.");bad.push(f);}
      else if(f.type==="tel"&&v.replace(/\D/g,"").length<10){setErr(f,"Vul een telefoonnummer van minimaal 10 cijfers in.");bad.push(f);}
    });
    return bad;
  }
  async function verstuur(data,btn){
    const oud=btn.innerHTML;btn.disabled=true;btn.classList.add("loading");
    btn.innerHTML='<span class="spin" aria-hidden="true"></span>Bezig met versturen…';
    btn.dataset.html=oud;
    const restore=()=>{btn.disabled=false;btn.classList.remove("loading");btn.innerHTML=oud;};
    /* Als gewone formuliergegevens versturen (zoals Formspree aanraadt): geen extra CORS-controle nodig. */
    const body=new URLSearchParams();Object.keys(data).forEach(k=>body.append(k,data[k]));
    try{
      const r=await fetch(ENDPOINT,{method:"POST",headers:{"Accept":"application/json"},body});
      if(r.ok)return {ok:true,restore};
      let j={};try{j=await r.json();}catch(e){}
      const msg=j.errors?j.errors.map(x=>x.message).join(" "):(j.error||"");
      console.error("Formspree antwoordde met status "+r.status,j);
      restore();return {ok:false,msg,status:r.status};
    }catch(err){
      console.error("Geen verbinding met Formspree:",err);
      restore();return {ok:false,network:true};
    }
  }
  /* Noodroute: als versturen mislukt, kan de bezoeker de aanvraag met één klik mailen. */
  function mailFallback(data){
    const lines=Object.keys(data).filter(k=>k.charAt(0)!=="_").map(k=>k+": "+data[k]);
    const body=lines.join("\n").slice(0,1800);
    return "mailto:"+MAIL+"?subject="+encodeURIComponent(data._subject||"Aanvraag via website")+"&body="+encodeURIComponent(body);
  }
  document.querySelectorAll("form[data-form]").forEach(form=>{
    const out=form.querySelector(".sent");
    form.addEventListener("input",e=>{if(e.target.getAttribute("aria-invalid"))clearErr(e.target);});
    form.addEventListener("change",e=>{if(e.target.type==="checkbox"&&e.target.getAttribute("aria-invalid"))clearErr(e.target);});
    form.querySelectorAll("textarea[maxlength]").forEach(t=>{
      const c=holderOf(t).querySelector(".counter");if(!c)return;
      const upd=()=>{c.textContent=t.value.length+" / "+t.maxLength;};t.addEventListener("input",upd);upd();
    });
    form.addEventListener("submit",async e=>{
      e.preventDefault();
      const hp=form.querySelector(".hp input");if(hp&&hp.value)return;
      out.hidden=true;out.classList.remove("bad");
      const bad=validate(form);
      if(bad.length){
        out.hidden=false;out.classList.add("bad");
        out.textContent=bad.length===1?"Er ontbreekt nog iets. Kijk even naar het gemarkeerde veld.":"Er ontbreken nog "+bad.length+" dingen. Kijk even naar de gemarkeerde velden.";
        bad[0].focus();return;
      }
      const data={};
      new FormData(form).forEach((v,k)=>{if(k==="_gotcha")return;v=String(v).trim();if(!v)return;data[k]=data[k]?data[k]+", "+v:v;});
      data.formulier=form.dataset.form;
      data.pagina=document.title;
      /* leesbare veldnamen in de e-mail; "email" blijft zo, zodat je direct kunt antwoorden */
      const mail={};
      Object.keys(data).forEach(k=>{const nk=k==="email"?"email":(k.charAt(0).toUpperCase()+k.slice(1)).replace(/_/g," ");mail[nk]=data[k];});
      const spoed=/spoed/i.test(data.urgentie||"")||form.dataset.form==="Spoed";
      mail._subject=(spoed?"SPOED – ":"")+(form.dataset.subject||"Bericht via website")+" – "+(data.naam||data.telefoon||"onbekend")+(data.plaagdier?" ("+data.plaagdier+")":"");
      const btn=form.querySelector("button[type=submit]");
      const res=await verstuur(mail,btn);
      if(!res.ok){
        out.hidden=false;out.classList.add("bad");out.textContent="";
        const p1=document.createElement("span");
        p1.textContent=(res.network?"Versturen lukte niet: er kon geen verbinding worden gemaakt.":"Versturen lukte niet"+(res.msg?": "+res.msg.replace(/[.!]?$/,"."):" (foutcode "+res.status+")."))+" Je kunt je aanvraag ook direct mailen, of bel ons op "+TEL+".";
        const a=document.createElement("a");a.className="btn btn-ghost";a.href=mailFallback(mail);a.textContent="Verstuur via e-mail";
        const wrap=document.createElement("span");wrap.style.cssText="display:grid;gap:10px";wrap.append(p1,a);out.append(wrap);
        return;
      }
      const naam=(data.naam||"").split(" ")[0];
      if(form.hasAttribute("data-redirect")){
        location.href=ROOT+"bedankt/index.html?n="+encodeURIComponent(naam)+"&t="+encodeURIComponent(form.dataset.form);
        return;
      }
      res.restore();out.hidden=false;out.textContent="Bedankt"+(naam?", "+naam:"")+"! We bellen je zo snel mogelijk terug.";form.reset();
    });
  });

  /* terug via de browser: knoppen niet laten hangen op "Bezig met versturen" */
  window.addEventListener("pageshow",()=>document.querySelectorAll("button.loading").forEach(b=>{b.disabled=false;b.classList.remove("loading");if(b.dataset.html)b.innerHTML=b.dataset.html;}));

  /* ---------- bedankpagina: persoonlijk maken ---------- */
  const thx=document.querySelector("[data-thanks]");
  if(thx){
    const q=new URLSearchParams(location.search),n=(q.get("n")||"").slice(0,40),t=q.get("t");
    if(n){thx.textContent="Bedankt, ";const em=document.createElement("em");em.textContent=n;thx.append(em,"!");}
    const lead=document.querySelector("[data-thanks-lead]");
    if(lead&&t==="Sollicitatie")lead.textContent="We hebben je sollicitatie goed ontvangen. Binnen een paar werkdagen nemen we contact met je op voor een eerste kennismaking.";
  }

  /* ---------- plaagcheck (alleen op de homepage) ---------- */
  const box=document.getElementById("signs");
  if(!box)return;
  const pests={
    muis:{name:"Muizen",url:"muizen",urg:"Binnen een week",hot:false,advice:"Zet voedsel in afgesloten bakken en kijk langs leidingdoorvoeren en plinten naar openingen. Een muis past door een gat zo groot als een potlood."},
    rat:{name:"Ratten",url:"ratten",urg:"Snel laten bekijken",hot:true,advice:"Ratten komen vaak via een kapotte rioolbuis. Laat dit snel inspecteren: ze kunnen ziektes overdragen en flinke schade doen."},
    wesp:{name:"Wespen",url:"wespen",urg:"Spoed mogelijk",hot:true,advice:"Blijf uit de buurt van de opening en sluit hem niet zelf af; de wespen zoeken dan een weg naar binnen. Wij behandelen het nest."},
    bedwants:{name:"Bedwantsen",url:"bedwantsen",urg:"Snel laten bekijken",hot:true,advice:"Was beddengoed op 60 °C en neem geen spullen mee naar andere kamers. Bedwantsen verspreiden zich snel via kleding en tassen."},
    vlo:{name:"Vlooien",url:"vlooien",urg:"Binnen een week",hot:false,advice:"Behandel je huisdier via de dierenarts en stofzuig dagelijks, ook naden en kieren. Gooi de stofzuigerzak direct weg."},
    mier:{name:"Mieren",url:"mieren",urg:"Geen haast",hot:false,advice:"Volg de mierenstraat naar binnen en maak het aanrecht schoon van suikerresten. Het nest zit vaak onder de bestrating of in de spouw."},
    kakkerlak:{name:"Kakkerlakken",url:"kakkerlakken",urg:"Snel laten bekijken",hot:true,advice:"Kakkerlakken zijn 's nachts actief en verstoppen zich bij warmte, zoals achter de koelkast. Een professionele aanpak is bijna altijd nodig."},
    zilvervis:{name:"Zilvervisjes",url:"zilvervisjes",urg:"Geen haast",hot:false,advice:"Zilvervisjes wijzen op vocht. Ventileer badkamer en kelder goed na het douchen of wassen en dicht naden en kieren."}
  };
  const signs=[
    ["Kleine zwarte keutels, zo groot als een rijstkorrel",{muis:3}],
    ["Keutels van 1 tot 2 cm",{rat:3}],
    ["Knaagsporen aan snoeren of verpakkingen",{muis:1,rat:1}],
    ["Geritsel in plafond of spouw, vooral 's nachts",{muis:2,rat:1}],
    ["Vette donkere vegen langs muren",{rat:2}],
    ["Veel wespen in en uit één opening bij de dakrand",{wesp:4}],
    ["Jeukende bultjes in een rij na het slapen",{bedwants:2,vlo:1}],
    ["Bloed- of zwarte stipjes op het matras",{bedwants:3}],
    ["Kleine springende insecten rond de enkels",{vlo:3}],
    ["Huisdier krabt zich opvallend vaak",{vlo:2}],
    ["Rij mieren langs plint of aanrecht",{mier:4}],
    ["Insecten die wegschieten als het licht aangaat",{kakkerlak:3,zilvervis:1}],
    ["Zilverkleurige insectjes in badkamer of kelder",{zilvervis:4}]
  ];
  const sel=new Set([0,2]);let touched=false;
  signs.forEach((s,i)=>{
    const b=document.createElement("button");
    b.type="button";b.className="sign";b.textContent=s[0];
    b.setAttribute("aria-pressed",sel.has(i));
    b.addEventListener("click",()=>{sel.has(i)?sel.delete(i):sel.add(i);b.setAttribute("aria-pressed",sel.has(i));touched=true;render();});
    box.appendChild(b);
  });
  const $=id=>document.getElementById(id);
  function render(){
    const score={};Object.keys(pests).forEach(k=>score[k]=0);
    sel.forEach(i=>{for(const k in signs[i][1])score[k]+=signs[i][1][k];});
    const ranked=Object.entries(score).filter(e=>e[1]>0).sort((a,b)=>b[1]-a[1]);
    const total=ranked.reduce((t,e)=>t+e[1],0);
    const name=$("r-name"),urg=$("r-urg"),adv=$("r-advice"),meter=$("r-meter"),note=$("r-note"),tag=$("r-tag"),more=$("r-more");
    meter.innerHTML="";
    if(!ranked.length){
      tag.textContent="Nog geen signalen";name.textContent="Kies wat je ziet";urg.hidden=true;more.hidden=true;
      adv.textContent="Tik één of meer signalen aan. Twijfel je? Vraag een inspectie aan, dan kijken we ter plekke.";
      note.textContent="";return;
    }
    const top=pests[ranked[0][0]];
    tag.textContent="Meest waarschijnlijk";name.textContent=top.name;urg.hidden=false;urg.textContent=top.urg;urg.className="urg"+(top.hot?" hot":"");
    adv.textContent=top.advice;
    more.hidden=false;more.href=ROOT+"ongedierte/"+top.url+"/index.html";more.textContent="Alles over "+top.name.toLowerCase()+" →";
    ranked.slice(0,3).forEach(([k,v])=>{
      const pct=Math.round(v/total*100);
      const d=document.createElement("div");
      d.innerHTML='<span></span><span class="bar"><i></i></span><b></b>';
      d.children[0].textContent=pests[k].name;d.querySelector("i").style.width=pct+"%";d.children[2].textContent=pct+"%";
      meter.appendChild(d);
    });
    note.textContent=touched?"Dit is een eerste inschatting, geen diagnose. Bij twijfel komen we kijken.":"Voorbeeld: twee signalen staan al aan. Pas ze aan naar jouw situatie.";
  }
  render();
})();
