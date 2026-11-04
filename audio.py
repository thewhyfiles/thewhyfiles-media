import json,numpy as np,soundfile as sf
from scipy import signal
import os; S=os.environ["S"]
SR=48000
TL=json.load(open(f"{S}/work/timeline.json"));total=TL["total"];N=int(total*SR)
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
cuts=[s["t0"] for s in TL["scenes"][1:]]
for c in cuts:whoosh(max(0,c-.12),.4,.35)
for c in [1.2,4.85,8.10,9.10,10.88,14.93,16.83,19.60,21.50,24.97,27.53,33.50,34.30]:pop(c,.35)
for c in [6.62]:pop(c,.25)                                   # mastaba appears
for k in range(6):pop(22.37+.4+k*.38,.15)                    # terraces light up
for k in range(5):thud(10.53+.59+k*.5,.55,70+k*6,.45)        # tiers land
thud(20.90,.35,90,.3)                                        # weight on beam
thud(21.45,.8,55,.8);whoosh(21.40,.35,.4,down=True)          # beam cracks
whoosh(31.0,.9,.4)                                           # smoothing
sfx/=np.abs(sfx).max()
mix=vo*1.0+mus*0.11+sfx*0.16
mix=np.tanh(mix*1.0)
sf.write(f"{S}/work/out/audio.wav",mix,SR)
print("ok",total,len(mix)/SR)
