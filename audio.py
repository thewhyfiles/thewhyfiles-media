import json,numpy as np,soundfile as sf
from scipy import signal
import os; S=os.environ["S"]
SR=48000
TL=json.load(open(f"{S}/work/timeline.json"));total=TL["total"];N=int(total*SR)
SC=[s["t0"] for s in TL["scenes"]]
rng=np.random.default_rng(3)
def place(buf,x,t,g=1.0):
    i=int(t*SR);j=min(len(buf),i+len(x));
    if i<len(buf):buf[i:j]+=x[:j-i]*g
# --- VO
vo=np.zeros(N)
for l in TL["lines"]:
    a,sr=sf.read(l["path"]);
    a=signal.resample_poly(a,SR,sr)
    place(vo,a,l["start"],1.0)
vo/=max(1e-9,np.abs(vo).max());vo*=0.9
# --- music pad: Am - F - C - G slow
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
mus=np.zeros(N);t=np.arange(N)/SR
seg=9.0
for k in range(int(total/seg)+2):
    ch=chords[k%4];t0=k*seg
    env=np.clip((t-t0)/3.0,0,1)*np.clip(1-(t-(t0+seg-3.0))/3.0,0,1)
    env=np.where((t>=t0)&(t<t0+seg),env,0)
    for m in ch:
        f=440*2**((m-69)/12)
        for det in (-0.3,0.0,0.3):
            mus+=env*np.sin(2*np.pi*(f+det)*t)*0.06
    f=440*2**((ch[0]-12-69)/12);mus+=env*np.sin(2*np.pi*f*t)*0.1
mus*=0.8+0.2*np.sin(2*np.pi*t/4.5)
b,a=signal.butter(2,1400/(SR/2));mus=signal.lfilter(b,a,mus)
mus*=np.clip(t/1.5,0,1)*np.clip((total-t)/2.5,0,1)
mus/=np.abs(mus).max()
# --- SFX
sfx=np.zeros(N)
def noise(d):return rng.standard_normal(int(d*SR))
def whoosh(t0,d=.45,g=.5,down=False):
    n=noise(d);L=len(n);tt=np.linspace(0,1,L)
    lo,hi=(2500,400) if down else (300,3500)
    fc=np.exp(np.linspace(np.log(lo),np.log(hi),L))
    out=np.zeros(L);blk=256
    for s in range(0,L,blk):
        c=fc[s]/(SR/2);c=min(.95,c);bb,aa=signal.butter(2,c);out[s:s+blk]=signal.lfilter(bb,aa,n[s:s+blk])
    env=np.sin(np.pi*tt)**2;place(sfx,out*env,t0,g/ max(1e-6,np.abs(out).max()))
def pop(t0,g=.5):
    d=.18;tt=np.arange(int(d*SR))/SR;x=np.sin(2*np.pi*(900+500*np.exp(-tt*40))*tt)*np.exp(-tt*28);place(sfx,x,t0,g)
def thud(t0,g=.9,f=60,d=.7):
    tt=np.arange(int(d*SR))/SR;x=np.sin(2*np.pi*(f+50*np.exp(-tt*25))*tt)*np.exp(-tt*7);x+=0.3*signal.lfilter(*signal.butter(2,500/(SR/2)),noise(d))*np.exp(-tt*30);place(sfx,x,t0,g)
def splash(t0,g=.7,d=.6):
    tt=np.arange(int(d*SR))/SR;n=signal.lfilter(*signal.butter(2,[300/(SR/2),3000/(SR/2)],btype='band'),noise(d))
    x=n*np.exp(-tt*9)/np.abs(n).max();x+=0.5*np.sin(2*np.pi*(180+400*np.exp(-tt*30))*tt)*np.exp(-tt*14);place(sfx,x,t0,g)
def chime(t0,g=.3,d=1.2):
    tt=np.arange(int(d*SR))/SR;x=sum(np.sin(2*np.pi*f*tt)*a for f,a in [(1568,1),(2349,.5),(3136,.3)])*np.exp(-tt*4);place(sfx,x,t0,g)
for c in SC[1:]:whoosh(max(0,c-.12),.4,.35)
CH={1:[.35,1.85],2:[.5,1.3,2.7],3:[.25,.55,1.0],4:[.5,2.5],5:[.4,2.9,3.3],6:[.9,2.4],7:[.7,2.0],8:[.4,2.3]}
for i,offs in CH.items():
    for o in offs:pop(SC[i]+o,.35)
whoosh(SC[0]+.25,.5,.4,down=True);splash(SC[0]+.74,.8);thud(SC[0]+.76,.4,70,.4)   # ice drops in
splash(SC[2]+.15,.45)                                                               # solid enters liquid
thud(SC[2]+2.8,.4,60,.5)                                                            # solid hits bottom
chime(SC[5]+2.2,.35)                                                                # lattice locks
sfx/=np.abs(sfx).max()
mix=vo*1.0+mus*0.11+sfx*0.16
mix=np.tanh(mix*1.0)
sf.write(f"{S}/work/out/audio.wav",mix,SR)
print("ok",total,len(mix)/SR)
