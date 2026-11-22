/* Blauweschild – gedeeld script voor alle pagina's */
(function(){
  const ROOT=document.body.dataset.root||"";
  const TEL="085 060 5985",MAIL="blauweschildongedierte@gmail.com";

  /* ===== FORMSPREE =====
     Plak hieronder de code van je Formspree-formulier (het stukje na /f/ in je endpoint),
     bijvoorbeeld "xyzabcde". Zolang dit leeg is, verstuurt de site niets. */
  const FORMSPREE_ID="";

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
  async function verstuur(data,btn){
    if(!FORMSPREE_ID)return {ok:false,demo:true};
    const oud=btn.textContent;btn.disabled=true;btn.textContent="Bezig met versturen…";
    try{
      const r=await fetch("https://formspree.io/f/"+FORMSPREE_ID,{method:"POST",headers:{"Accept":"application/json","Content-Type":"application/json"},body:JSON.stringify(data)});
      return {ok:r.ok};
    }catch(err){return {ok:false};}
    finally{btn.disabled=false;btn.textContent=oud;}
  }
  const mislukt="Versturen lukte niet. Bel ons direct op "+TEL+" of mail naar "+MAIL+".";
  document.querySelectorAll("form[data-form]").forEach(form=>{
    const out=form.querySelector(".sent");
    form.addEventListener("submit",async e=>{
      e.preventDefault();
      if(form.querySelector(".hp input")&&form.querySelector(".hp input").value)return;
      const missing=[...form.querySelectorAll("[required]")].filter(f=>!f.value.trim());
      out.hidden=false;
      if(missing.length){
        const names=missing.map(f=>f.closest("label").firstElementChild.textContent.replace("*","").trim().toLowerCase());
        out.textContent="Vul nog in: "+names.join(", ")+".";missing[0].focus();return;
      }
      const data={type:form.dataset.form};
      new FormData(form).forEach((v,k)=>{if(k!=="_gotcha")data[k]=String(v).trim();});
      const naam=(data.naam||"").split(" ")[0];
      data._subject=(form.dataset.subject||"Bericht via website")+" – "+(data.naam||data.telefoon||"");
      const res=await verstuur(data,form.querySelector("button[type=submit]"));
      if(res.demo){out.textContent="Het formulier is nog niet gekoppeld. Bel ons op "+TEL+" of mail naar "+MAIL+".";return;}
      if(!res.ok){out.textContent=mislukt;return;}
      if(form.dataset.redirect){location.href=ROOT+"bedankt/index.html";return;}
      out.textContent="Bedankt"+(naam?", "+naam:"")+". We bellen je zo snel mogelijk terug.";form.reset();
    });
  });

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
