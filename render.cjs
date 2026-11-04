const http=require('http'),fs=require('fs'),path=require('path'),{spawn}=require('child_process');
const {chromium}=require('playwright');
const ROOT=__dirname,OUT=path.join(ROOT,'out');fs.mkdirSync(OUT,{recursive:true});
const TL=JSON.parse(fs.readFileSync(path.join(ROOT,'timeline.json')));
const MIME={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.woff2':'font/woff2','.css':'text/css'};
const server=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]).replace(/^\/+/,'')||'index.html');
  if(!p.startsWith(ROOT)||!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.statusCode=404;return r.end()}
  r.setHeader('Content-Type',MIME[path.extname(p)]||'application/octet-stream');fs.createReadStream(p).pipe(r)});
async function openPage(){
  const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const pg=await b.newPage({viewport:{width:720,height:1280},deviceScaleFactor:1});
  pg.on('pageerror',e=>console.error('PAGEERR',e.message));pg.on('console',m=>{if(m.type()==='error')console.error('CONSOLE',m.text())});
  await pg.goto(`http://127.0.0.1:${server.address().port}/index.html`);
  await pg.waitForFunction('window.READY===true',null,{timeout:60000});
  return {b,pg};}
async function shot(pg,t,q=92){await pg.evaluate(t=>window.setT(t),t);return pg.screenshot({type:'jpeg',quality:q});}
async function renderScene(i){
  const sc=TL.scenes[i],n=Math.round((sc.t1-sc.t0)*30);const fin=path.join(OUT,`scene_${String(i).padStart(2,'0')}.mp4`),tmp=fin.replace('.mp4','.tmp.mp4');
  const {b,pg}=await openPage();
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r','30',tmp],{stdio:['pipe','inherit','inherit']});
  const done=new Promise(res=>ff.on('close',res));const t0=Date.now();
  for(let f=0;f<n;f++){const buf=await shot(pg,sc.t0+f/30);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
    if(f%30==0)console.log(`scene ${i}: ${f}/${n} ${((Date.now()-t0)/1000).toFixed(0)}s`);}
  ff.stdin.end();const code=await done;await b.close();
  if(code===0){fs.renameSync(tmp,fin);console.log(`scene ${i} done (${n} frames, ${((Date.now()-t0)/1000).toFixed(0)}s)`)}else{console.error(`scene ${i} FAILED`);process.exitCode=1}}
(async()=>{
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const [mode,...args]=process.argv.slice(2);
  if(mode==='preview'){const {b,pg}=await openPage();for(const a of args){const t=parseFloat(a);const t0=Date.now();fs.writeFileSync(path.join(OUT,`prev_${a}.jpg`),await shot(pg,t));console.log('preview',a,Date.now()-t0,'ms')}await b.close()}
  else if(mode==='scenes'){const conc=parseInt(process.env.CONC||"2");const list=args.map(Number);let k=0;await Promise.all(Array.from({length:conc},async()=>{while(k<list.length){await renderScene(list[k++])}}))}
  server.close();})();
