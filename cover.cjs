// Cover Reels The Why Files: frame 3D terkuat + judul. Output out/cover.jpg 1080x1920.
// Pakai: node cover.cjs  (membaca cover.json: {"t":22.3,"title":"Kenapa tutup got <b>bulat</b>?","pillar":"SAINS"})
// Butuh baris `window.__r=renderer;` di index.html (sebelum window.READY=true).
const http=require('http'),fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const ROOT=__dirname,OUT=path.join(ROOT,'out');fs.mkdirSync(OUT,{recursive:true});
const C=JSON.parse(fs.readFileSync(path.join(ROOT,'cover.json')));
const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.woff2':'font/woff2'};
const server=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]).replace(/^\/+/,'')||'index.html');
  if(!p.startsWith(ROOT)||!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.statusCode=404;return r.end()}
  r.setHeader('Content-Type',MIME[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(r)});
const CSS=`
#capbox,#wm,#fade,#end,.chip{display:none!important}
#cov{position:absolute;inset:0;pointer-events:none}
#cov .shade{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(23,23,23,.55) 0%,rgba(23,23,23,0) 22%,rgba(23,23,23,0) 50%,rgba(23,23,23,.92) 70%,#171717 100%)}
#cov .eyebrow{position:absolute;top:196px;left:0;right:0;text-align:center;font:500 20px Inter;letter-spacing:.32em;color:#A7A7A2}
#cov .eyebrow i{font-style:normal;color:#536DFF;letter-spacing:.32em}
#cov .title{position:absolute;left:52px;right:52px;top:792px;text-align:center;font:800 76px/1.04 Sora;letter-spacing:-.02em;color:#F2F0E9;text-wrap:balance}
#cov .title b{color:#536DFF;font-weight:800}
#cov .tag{position:absolute;top:1012px;left:0;right:0;text-align:center;font:400 30px 'DM Serif Display';color:#D9D9D5}
#cov .handle{position:absolute;top:1068px;left:0;right:0;text-align:center;font:500 19px Inter;letter-spacing:.08em;color:#A7A7A2}`;
(async()=>{
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const pg=await b.newPage({viewport:{width:720,height:1280},deviceScaleFactor:1.5});
  pg.on('pageerror',e=>console.error('PAGEERR',e.message));
  await pg.goto(`http://127.0.0.1:${server.address().port}/index.html`);
  await pg.waitForFunction('window.READY===true',null,{timeout:60000});
  await pg.evaluate(({C,CSS})=>{
    if(window.__r){window.__r.setPixelRatio(1.5);window.__r.setSize(720,1280,false);}
    const st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
    const d=document.createElement('div');d.id='cov';
    d.innerHTML=`<div class="shade"></div><div class="eyebrow">THE WHY FILES <i>·</i> ${C.pillar||''}</div><div class="title">${C.title}</div><div class="tag">Setiap hal punya alasan.</div><div class="handle">@thewhyfiles.id</div>`;
    document.getElementById('ov').appendChild(d);
    window.setT(C.t);
  },{C,CSS});
  await pg.evaluate(()=>document.fonts.ready);
  fs.writeFileSync(path.join(OUT,'cover.jpg'),await pg.screenshot({type:'jpeg',quality:92}));
  console.log('cover ok');await b.close();server.close();
})();
