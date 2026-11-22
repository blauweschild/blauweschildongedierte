/* ---------- 3D: röntgenscan van een woning met looproutes, warmtebeeld en bloom ---------- */
(function(){
  const canvas=document.getElementById("scene");
  if(!canvas||!document.querySelector("[data-stage]"))return;
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  let renderer;
  try{ if(!window.THREE) throw 0; renderer=new THREE.WebGLRenderer({canvas,antialias:false,alpha:false,powerPreference:"high-performance"}); }
  catch(e){ document.documentElement.classList.add("no3d"); canvas.remove(); return; }
  const PR=Math.min(window.devicePixelRatio||1,1.75);
  renderer.setPixelRatio(PR);

  const INK=0x071029;
  const scene=new THREE.Scene();scene.background=new THREE.Color(INK);
  scene.fog=new THREE.Fog(INK,12,26);
  const camera=new THREE.PerspectiveCamera(32,1,0.1,100);camera.position.set(0,0,13);

  const COB=new THREE.Color(0x4f86ff),ICE=new THREE.Color(0xe4edff),AMB=new THREE.Color(0xffa83a),HOT=new THREE.Color(0xff5a1f);
  const root=new THREE.Group();scene.add(root);
  const house=new THREE.Group();house.position.y=-1.65;root.add(house);
  const U={scanY:{value:0},time:{value:0}};

  /* ---- materialen ---- */
  const xray=(op)=>new THREE.ShaderMaterial({
    uniforms:{uScanY:U.scanY,uCol:{value:COB},uScan:{value:ICE},uOp:{value:op}},
    vertexShader:`varying vec3 vW;varying vec3 vN;varying float vY;
      void main(){vY=position.y;vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;vN=normalize(mat3(modelMatrix)*normal);gl_Position=projectionMatrix*viewMatrix*w;}`,
    fragmentShader:`uniform float uScanY;uniform vec3 uCol;uniform vec3 uScan;uniform float uOp;
      varying vec3 vW;varying vec3 vN;varying float vY;
      void main(){vec3 V=normalize(cameraPosition-vW);float f=pow(1.-abs(dot(normalize(vN),V)),2.2);
        float d=vY-uScanY;float band=exp(-d*d/.004);float below=smoothstep(.0,-.9,d)*smoothstep(-1.6,-.9,d);
        vec3 c=uCol*(.025+f*.3)*uOp+uScan*band*.28+uCol*below*.03;
        gl_FragColor=vec4(c,1.);}`,
    transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide
  });
  const lineMat=(op,col)=>new THREE.ShaderMaterial({
    uniforms:{uScanY:U.scanY,uCol:{value:col||COB},uOp:{value:op}},
    vertexShader:`varying float vY;void main(){vY=position.y;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader:`uniform float uScanY;uniform vec3 uCol;uniform float uOp;varying float vY;
      void main(){float d=vY-uScanY;float band=exp(-d*d/.006);gl_FragColor=vec4(uCol*uOp+vec3(.85,.92,1.)*band*.7,1.);}`,
    transparent:true,depthWrite:false,blending:THREE.AdditiveBlending
  });
  const Lmain=lineMat(.6),Lsoft=lineMat(.22),Lfaint=lineMat(.08),Lice=lineMat(.38,ICE);
  const wallX=xray(1),furnX=xray(.6);

  const HW=2,HD=1.5,F1=1.4,F2=2.8,RT=4.15;
  function box(w,h,d,x,y,z,lm,face){
    const g=new THREE.BoxGeometry(w,h,d);g.translate(x,y+h/2,z);
    if(lm)house.add(new THREE.LineSegments(new THREE.EdgesGeometry(g),lm));
    if(face)house.add(new THREE.Mesh(g,face));
  }
  function poly(pts,m,closed){const g=new THREE.BufferGeometry().setFromPoints(pts.map(p=>new THREE.Vector3(...p)));house.add(closed?new THREE.LineLoop(g,m):new THREE.Line(g,m));}

  /* ---- woning ---- */
  box(HW*2,F2,HD*2,0,0,0,Lmain,wallX);
  box(HW*2-.24,F2,HD*2-.24,0,0,0,Lsoft,null);
  box(HW*2,.5,HD*2,0,-.5,0,Lfaint,null);
  const roof=new THREE.BufferGeometry();const o=.18;
  roof.setAttribute("position",new THREE.Float32BufferAttribute([-HW-o,F2,HD+o, HW+o,F2,HD+o, 0,RT,HD+o, -HW-o,F2,-HD-o, HW+o,F2,-HD-o, 0,RT,-HD-o],3));
  roof.setIndex([0,1,2, 3,5,4, 0,2,5, 0,5,3, 1,4,5, 1,5,2]);roof.computeVertexNormals();
  house.add(new THREE.LineSegments(new THREE.EdgesGeometry(roof),Lmain));house.add(new THREE.Mesh(roof,wallX));
  for(let i=1;i<6;i++){const u=i/6,y=F2+(RT-F2)*u,x=(HW+o)*(1-u);poly([[-x,y,HD+o],[-x,y,-HD-o]],Lsoft);poly([[x,y,HD+o],[x,y,-HD-o]],Lsoft);}
  box(.4,1.1,.4,-1.1,3.3,-.6,Lmain,wallX);
  [0,F1].forEach((y,i)=>{
    for(let x=-HW;x<=HW+.01;x+=.4)poly([[x,y,-HD],[x,y,HD]],Lfaint);
    for(let z=-HD;z<=HD+.01;z+=.4)poly([[-HW,y,z],[HW,y,z]],Lfaint);
    if(i)box(HW*2,.08,HD*2,0,y-.04,0,Lsoft,null);
  });
  const fz=HD+.003;
  const win=(x,y,w,h,z)=>{poly([[x-w,y,z],[x+w,y,z],[x+w,y+h,z],[x-w,y+h,z]],Lice,true);poly([[x,y,z],[x,y+h,z]],Lsoft);poly([[x-w,y+h*.55,z],[x+w,y+h*.55,z]],Lsoft);};
  win(-1.3,.45,.42,.65,fz);win(1.3,.45,.42,.65,fz);
  [-1.3,0,1.3].forEach(x=>win(x,1.8,.36,.6,fz));
  win(0,3.05,.25,.45,HD+o+.002);
  poly([[-.32,0,fz],[.32,0,fz],[.32,1.1,fz],[-.32,1.1,fz]],Lice,true);
  poly([[.6,0,-HD],[.6,0,.3],[.6,F1,.3],[.6,F1,-HD]],Lsoft,true);
  poly([[-.4,F1,-HD],[-.4,F1,HD*.1],[-.4,F2,HD*.1],[-.4,F2,-HD]],Lsoft,true);
  for(let i=0;i<9;i++){const y=i*F1/9,x=-1.75+i*.16;poly([[x,y,-HD+.08],[x,y,-HD+.75],[x+.16,y,-HD+.75]],Lfaint);}
  // meubels
  box(1.2,.45,.55,1.2,0,-1.15,Lsoft,furnX);        // keukenblok
  box(1.3,.38,.6,-1.0,0,.65,Lsoft,furnX);          // bank
  box(1.0,.35,1.4,1.2,F1,-.55,Lsoft,furnX);        // bed
  box(.5,.9,.4,-1.65,F1,.95,Lsoft,furnX);          // kast
  box(.22,F2+.5,.22,1.62,-.5,-1.1,Lice,null);      // leidingschacht

  /* ---- grondvlak ---- */
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(26,26),new THREE.ShaderMaterial({
    uniforms:{uCol:{value:COB}},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    vertexShader:`varying vec2 vP;void main(){vP=position.xy;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader:`uniform vec3 uCol;varying vec2 vP;
      float gl(vec2 p,float s){vec2 g=abs(fract(p*s-.5)-.5)/fwidth(p*s);return 1.-min(min(g.x,g.y),1.);}
      void main(){float r=length(vP);float fade=smoothstep(11.,1.5,r);
        float g=gl(vP,1.)*.35+gl(vP,4.)*.08;float glow=exp(-r*r/7.)*.18;
        gl_FragColor=vec4(uCol*(g*fade*.3+glow*.6),1.);}`
  }));
  ground.material.extensions={derivatives:true};
  ground.rotation.x=-Math.PI/2;ground.position.y=-.52;house.add(ground);

  /* ---- punten-shader ---- */
  const ptsMat=()=>new THREE.ShaderMaterial({
    uniforms:{uPR:{value:PR}},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,
    vertexShader:`attribute float size;attribute vec3 color;varying vec3 vC;
      void main(){vC=color;vec4 mv=modelViewMatrix*vec4(position,1.);gl_PointSize=size*${(300).toFixed(1)}/-mv.z;gl_Position=projectionMatrix*mv;}`,
    fragmentShader:`varying vec3 vC;void main(){float d=length(gl_PointCoord-.5)*2.;float a=exp(-d*d*4.);gl_FragColor=vec4(vC*a,1.);}`
  });

  /* ---- looproutes ---- */
  const routes=[
    [[-2.7,-.36,-2.0],[-1.8,-.32,-1.2],[-.8,-.34,-.6],[.6,-.32,-.4],[1.5,-.25,-1.0],[1.62,.6,-1.1],[1.62,1.6,-1.1],[1.45,2.45,-1.0],[.9,3.0,-.5],[.55,3.15,-.1]],
    [[-1.94,-.2,1.42],[-1.88,.5,1.42],[-1.72,1.3,1.42],[-1.2,2.1,1.42],[-.4,2.72,1.42],[.2,3.05,.9],[.55,3.15,.1]],
    [[.55,3.15,-.1],[1.1,3.05,.25],[.5,3.2,.55],[-.3,3.05,.1],[-.1,3.15,-.5],[.55,3.15,-.1]]
  ];
  const curves=routes.map((r,i)=>new THREE.CatmullRomCurve3(r.map(p=>new THREE.Vector3(...p)),i===2,"catmullrom",.5));
  const dash=new THREE.LineDashedMaterial({color:0xffa83a,dashSize:.07,gapSize:.07,transparent:true,opacity:.28,blending:THREE.AdditiveBlending,depthWrite:false});
  curves.forEach(c=>{const l=new THREE.Line(new THREE.BufferGeometry().setFromPoints(c.getPoints(200)),dash);l.computeLineDistances();house.add(l);});
  const runners=[];[4,3,2].forEach((n,ci)=>{for(let i=0;i<n;i++)runners.push({c:curves[ci],u:i/n+Math.random()*.05,sp:(.045+Math.random()*.02)*(ci===2?1.7:1),stop:Math.random()*6});});
  const TR=14,RN=runners.length*TR;
  const rGeo=new THREE.BufferGeometry();const rP=new Float32Array(RN*3),rC=new Float32Array(RN*3),rS=new Float32Array(RN);
  rGeo.setAttribute("position",new THREE.BufferAttribute(rP,3));rGeo.setAttribute("color",new THREE.BufferAttribute(rC,3));rGeo.setAttribute("size",new THREE.BufferAttribute(rS,1));
  const rPts=new THREE.Points(rGeo,ptsMat());rPts.frustumCulled=false;house.add(rPts);

  /* ---- warmtebeeld bij het nest ---- */
  const HN=40,hGeo=new THREE.BufferGeometry(),hP=new Float32Array(HN*3),hC=new Float32Array(HN*3),hS=new Float32Array(HN),hSeed=[];
  for(let i=0;i<HN;i++){const r=Math.random()*.42,a=Math.random()*6.28;hSeed.push([Math.cos(a)*r,Math.random()*.18,Math.sin(a)*r*.8,Math.random()*6.28]);}
  hGeo.setAttribute("position",new THREE.BufferAttribute(hP,3));hGeo.setAttribute("color",new THREE.BufferAttribute(hC,3));hGeo.setAttribute("size",new THREE.BufferAttribute(hS,1));
  const heat=new THREE.Points(hGeo,ptsMat());heat.position.set(.4,3.05,0);heat.frustumCulled=false;house.add(heat);

  /* ---- bevindingen ---- */
  const spots=[
    {p:[-2.45,-.34,-1.8],t:"Toegang",s:"Kier in kruipruimte"},
    {p:[-1.72,1.3,1.42],t:"Looproute",s:"Spouwmuur voorgevel"},
    {p:[.55,3.15,-.1],t:"Nest",s:"Isolatie zolder · 31 °C"}
  ];
  const tags=document.getElementById("tags3d");tags.innerHTML="";
  spots.forEach((s,i)=>{
    const m=new THREE.Mesh(new THREE.SphereGeometry(.06,16,12),new THREE.MeshBasicMaterial({color:0xffc070}));m.position.set(...s.p);house.add(m);
    const r=new THREE.Mesh(new THREE.RingGeometry(.12,.145,48),new THREE.MeshBasicMaterial({color:0xffa83a,transparent:true,side:THREE.DoubleSide,depthWrite:false,blending:THREE.AdditiveBlending}));r.position.copy(m.position);house.add(r);
    s.m=m;s.r=r;
    const d=document.createElement("div");d.className="tag3d";d.innerHTML="<b></b><span></span>";
    d.querySelector("b").textContent=String(i+1).padStart(2,"0")+" · "+s.t;d.querySelector("span").textContent=s.s;tags.appendChild(d);s.el=d;
  });
  const hud=document.createElement("div");hud.className="tag3d hud";hud.innerHTML="<b>Inspectiescan · tussenwoning</b><span id='hudline'>3 bevindingen · knaagdieren</span>";tags.appendChild(hud);
  const hudLine=hud.querySelector("span");

  /* ---- scanvlak ---- */
  const scanG=new THREE.Group();house.add(scanG);
  const sPlane=new THREE.Mesh(new THREE.PlaneGeometry(HW*2+.9,HD*2+.9),new THREE.ShaderMaterial({
    uniforms:{uCol:{value:COB}},transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,side:THREE.DoubleSide,
    vertexShader:`varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,
    fragmentShader:`uniform vec3 uCol;varying vec2 vU;void main(){vec2 e=min(vU,1.-vU);float edge=exp(-min(e.x,e.y)*40.);
      float lines=step(.92,fract(vU.y*24.))*.25;gl_FragColor=vec4(uCol*(.03+edge*.35+lines*.08),1.);}`
  }));
  sPlane.rotation.x=-Math.PI/2;scanG.add(sPlane);
  const sEdge=new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints([[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>new THREE.Vector3(a*(HW+.45),0,b*(HD+.45)))),new THREE.LineBasicMaterial({color:0x8fa9e6}));
  scanG.add(sEdge);
  [[-1,-1],[1,-1],[1,1],[-1,1]].forEach(([a,b])=>{
    const x=a*(HW+.45),z=b*(HD+.45);
    const g=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x-a*.3,0,z),new THREE.Vector3(x,0,z),new THREE.Vector3(x,0,z-b*.3)]);
    const l=new THREE.Line(g,new THREE.LineBasicMaterial({color:0xb8c9f0}));l.position.y=.002;scanG.add(l);
  });

  /* ---- stof ---- */
  const DN=300,dGeo=new THREE.BufferGeometry(),dP=new Float32Array(DN*3),dC=new Float32Array(DN*3),dS=new Float32Array(DN);
  for(let i=0;i<DN;i++){dP[i*3]=(Math.random()-.5)*28;dP[i*3+1]=(Math.random()-.5)*16;dP[i*3+2]=-10+Math.random()*11;const k=.15+Math.random()*.25;dC[i*3]=.35*k;dC[i*3+1]=.5*k;dC[i*3+2]=k;dS[i]=.05+Math.random()*.1;}
  dGeo.setAttribute("position",new THREE.BufferAttribute(dP,3));dGeo.setAttribute("color",new THREE.BufferAttribute(dC,3));dGeo.setAttribute("size",new THREE.BufferAttribute(dS,1));
  scene.add(new THREE.Points(dGeo,ptsMat()));

  /* ---- bloom-nabewerking ---- */
  const qCam=new THREE.OrthographicCamera(-1,1,1,-1,0,1),qScene=new THREE.Scene();
  const quad=new THREE.Mesh(new THREE.PlaneGeometry(2,2));qScene.add(quad);
  const vs=`varying vec2 vU;void main(){vU=uv;gl_Position=vec4(position.xy,0.,1.);}`;
  const brightM=new THREE.ShaderMaterial({uniforms:{t:{value:null}},vertexShader:vs,
    fragmentShader:`uniform sampler2D t;varying vec2 vU;void main(){vec3 c=texture2D(t,vU).rgb;float l=max(c.r,max(c.g,c.b));gl_FragColor=vec4(c*smoothstep(.3,.8,l),1.);}`});
  const blurM=new THREE.ShaderMaterial({uniforms:{t:{value:null},d:{value:new THREE.Vector2()}},vertexShader:vs,
    fragmentShader:`uniform sampler2D t;uniform vec2 d;varying vec2 vU;void main(){
      vec3 c=texture2D(t,vU).rgb*.227027;
      c+=(texture2D(t,vU+d*1.3846).rgb+texture2D(t,vU-d*1.3846).rgb)*.316216;
      c+=(texture2D(t,vU+d*3.2308).rgb+texture2D(t,vU-d*3.2308).rgb)*.070270;
      gl_FragColor=vec4(c,1.);}`});
  const compM=new THREE.ShaderMaterial({uniforms:{s:{value:null},b1:{value:null},b2:{value:null},time:U.time},vertexShader:vs,
    fragmentShader:`uniform sampler2D s;uniform sampler2D b1;uniform sampler2D b2;uniform float time;varying vec2 vU;
      float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
      void main(){vec3 c=texture2D(s,vU).rgb*.85+texture2D(b1,vU).rgb*.45+texture2D(b2,vU).rgb*.35;
        c=c/(1.+c*.18);
        float v=smoothstep(1.15,.35,length((vU-.5)*vec2(1.25,1.)));c=mix(vec3(.012,.03,.08),c,.55+.45*v);
        c+=(h(vU*1000.+time)-.5)*.018;
        gl_FragColor=vec4(c,1.);}`});
  const rtOpt={minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat,type:THREE.HalfFloatType};
  let rtS,rtA,rtB,rtC,rtD,post=true;
  try{
    rtS=renderer.capabilities.isWebGL2&&THREE.WebGLMultisampleRenderTarget?new THREE.WebGLMultisampleRenderTarget(4,4,rtOpt):new THREE.WebGLRenderTarget(4,4,rtOpt);
    if(rtS.samples!==undefined)rtS.samples=4;
    rtA=new THREE.WebGLRenderTarget(4,4,rtOpt);rtB=rtA.clone();rtC=rtA.clone();rtD=rtA.clone();
  }catch(e){post=false;}
  const pass=(m,target)=>{quad.material=m;renderer.setRenderTarget(target);renderer.render(qScene,qCam);};
  function blur(src,tmp,w,h,spread){
    blurM.uniforms.t.value=src.texture;blurM.uniforms.d.value.set(spread/w,0);pass(blurM,tmp);
    blurM.uniforms.t.value=tmp.texture;blurM.uniforms.d.value.set(0,spread/h);pass(blurM,src);
  }
  function draw(){
    if(!post){renderer.setRenderTarget(null);renderer.render(scene,camera);return;}
    try{
      renderer.setRenderTarget(rtS);renderer.render(scene,camera);
      brightM.uniforms.t.value=rtS.texture;pass(brightM,rtA);
      const w=rtA.width,h=rtA.height;
      blur(rtA,rtB,w,h,1);blur(rtA,rtB,w,h,2);
      blurM.uniforms.t.value=rtA.texture;blurM.uniforms.d.value.set(0,0);pass(blurM,rtC);
      blur(rtC,rtD,rtC.width,rtC.height,2.5);blur(rtC,rtD,rtC.width,rtC.height,4);
      compM.uniforms.s.value=rtS.texture;compM.uniforms.b1.value=rtA.texture;compM.uniforms.b2.value=rtC.texture;
      pass(compM,null);
    }catch(e){post=false;}
  }

  /* ---- plaatsing in de podium-vakken ---- */
  const stages=[...document.querySelectorAll("[data-stage]")];
  const target={x:0,y:0,s:1,vis:1},cur={x:0,y:0,s:1,init:false};
  const visH=()=>2*Math.tan(THREE.MathUtils.degToRad(camera.fov/2))*camera.position.z;
  function measure(){
    const vh=window.innerHeight,vw=window.innerWidth;let best=null,bestVis=-Infinity;
    stages.forEach(el=>{const r=el.getBoundingClientRect();const vis=Math.max(0,Math.min(r.bottom,vh)-Math.max(r.top,0));
      const score=vis>0?vis:-Math.min(Math.abs(r.top-vh),Math.abs(r.bottom));if(score>bestVis){bestVis=score;best=r;}});
    if(!best)return;
    const h=visH(),w=h*camera.aspect;
    target.x=((best.left+best.width/2)/vw-.5)*w;target.y=-((best.top+best.height/2)/vh-.5)*h;
    target.s=Math.min(best.width,best.height)/vh*h/6.2;target.vis=bestVis>40?1:0;
    if(!cur.init)Object.assign(cur,target,{init:true});
  }
  const dbs=new THREE.Vector2();
  function resize(){
    const w=window.innerWidth,h=window.innerHeight;
    renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
    renderer.getDrawingBufferSize(dbs);
    if(post){rtS.setSize(dbs.x,dbs.y);rtA.setSize(dbs.x>>1,dbs.y>>1);rtB.setSize(dbs.x>>1,dbs.y>>1);rtC.setSize(dbs.x>>2,dbs.y>>2);rtD.setSize(dbs.x>>2,dbs.y>>2);}
    measure();
  }
  window.addEventListener("resize",resize);window.addEventListener("scroll",measure,{passive:true});resize();

  const ptr={x:0,y:0,tx:0,ty:0};
  window.addEventListener("pointermove",e=>{ptr.tx=e.clientX/window.innerWidth*2-1;ptr.ty=e.clientY/window.innerHeight*2-1;},{passive:true});

  const clock=new THREE.Clock();let t=reduce?2.3:0,tagA=0;
  const v=new THREE.Vector3(),tmp=new THREE.Vector3(),c=new THREE.Color();
  function frame(){
    const dt=Math.min(clock.getDelta(),.033);
    if(!reduce)t+=dt;U.time.value=t;
    const k=reduce?1:1-Math.pow(.0015,dt);
    cur.x+=(target.x-cur.x)*k;cur.y+=(target.y-cur.y)*k;cur.s+=(target.s-cur.s)*k;
    root.position.set(cur.x,cur.y,0);root.scale.setScalar(cur.s);
    ptr.x+=(ptr.tx-ptr.x)*.04;ptr.y+=(ptr.ty-ptr.y)*.04;
    root.rotation.y=-0.6+Math.sin(t*.16)*.38+ptr.x*.32;
    root.rotation.x=.26+ptr.y*.08+Math.sin(t*.23)*.02;
    const sy=-0.55+(0.5-0.5*Math.cos(t*.62))*(RT+.75);
    scanG.position.y=sy;U.scanY.value=sy;
    // lopers met staart
    let i=0;
    runners.forEach(r=>{
      if(!reduce){const go=Math.sin(t*1.1+r.stop)>-.35?1:.08;r.u=(r.u+r.sp*go*dt)%1;}
      for(let j=0;j<TR;j++){
        let u=r.u-j*.0045;if(u<0)u+=1;
        r.c.getPointAt(u,tmp);rP[i*3]=tmp.x;rP[i*3+1]=tmp.y;rP[i*3+2]=tmp.z;
        const fall=1-j/TR,near=Math.exp(-Math.pow(tmp.y-sy,2)/.08);
        c.copy(AMB).lerp(ICE,near*.5*fall).multiplyScalar((.15+fall*.6)*(1+near*.6));
        rC[i*3]=c.r;rC[i*3+1]=c.g;rC[i*3+2]=c.b;rS[i]=(j===0?.42:.26*fall+.04)*(1+near*.6);i++;
      }
    });
    rGeo.attributes.position.needsUpdate=true;rGeo.attributes.color.needsUpdate=true;rGeo.attributes.size.needsUpdate=true;
    for(let n=0;n<HN;n++){
      const s=hSeed[n],p=.5+.5*Math.sin(t*1.8+s[3]);
      hP[n*3]=s[0]*(1+p*.15);hP[n*3+1]=s[1];hP[n*3+2]=s[2]*(1+p*.15);
      const r=Math.hypot(s[0],s[2])/.42;c.copy(HOT).lerp(AMB,r).multiplyScalar(.13*(1-r*.6)*(.7+p*.5));
      hC[n*3]=c.r;hC[n*3+1]=c.g;hC[n*3+2]=c.b;hS[n]=1.1-r*.6;
    }
    hGeo.attributes.position.needsUpdate=true;hGeo.attributes.color.needsUpdate=true;hGeo.attributes.size.needsUpdate=true;
    if(!reduce)for(let n=0;n<DN;n++){dP[n*3+1]+=dt*.06;if(dP[n*3+1]>8)dP[n*3+1]=-8;}
    dGeo.attributes.position.needsUpdate=true;
    // labels
    tagA+=((target.vis?1:0)-tagA)*.08;
    const W=window.innerWidth,H=window.innerHeight;
    spots.forEach((s,j)=>{
      const ph=(t*.8+j*.33)%1;s.r.scale.setScalar(1+ph*2.4);s.r.material.opacity=(1-ph);
      s.r.quaternion.copy(camera.quaternion);root.getWorldQuaternion(s.r.quaternion).invert().premultiply(camera.quaternion);
      s.m.getWorldPosition(v);v.project(camera);
      const x=(v.x+1)/2*W,y=(1-v.y)/2*H,on=x>0&&x<W&&y>60&&y<H;
      s.el.style.transform="translate("+x.toFixed(1)+"px,"+y.toFixed(1)+"px)";s.el.style.opacity=on?tagA:0;
    });
    v.set(0,-.6,HD+.5);house.localToWorld(v);v.project(camera);
    hud.style.transform="translate("+((v.x+1)/2*W).toFixed(1)+"px,"+((1-v.y)/2*H).toFixed(1)+"px)";hud.style.opacity=tagA*.95;
    hudLine.textContent="Scanhoogte "+Math.max(0,(sy+.5)*1.15).toFixed(2)+" m · 3 bevindingen";
    draw();
    requestAnimationFrame(frame);
  }
  frame();
})();
