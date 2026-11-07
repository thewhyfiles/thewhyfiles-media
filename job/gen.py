import json, math, textwrap
T = json.load(open('out/timing.json'))
ID = ["Seseorang menguap, kamu ikut menguap.",
"Menguap itu menular, penyebabnya belum tuntas.",
"328 orang menonton video orang menguap.",
"222 orang menguap setidaknya sekali.",
"Studi 2018: ikut menguap, empati sedikit lebih tinggi.",
"Studi 2014: tak ada kaitan kuat dengan empati.",
"Usia berpengaruh: makin tua, makin jarang.",
"Tapi usia hanya menjelaskan 8%.",
"Sisanya masih misteri.",
"Setiap hal punya alasan."]
YEL, BLU, TXT, MUT = "#f4c430", "#4f66f5", "#efede9", "#a5a5a0"
SKY = lambda stars=60: {"type":"sky","stars":stars,"to":1300,"z":0}
def txt(x,y,s,size=30,fill=TXT,w=700,z=20,**k): d={"type":"text","x":x,"y":y,"text":s,"size":size,"fill":fill,"weight":w,"z":z}; d.update(k); return d
def pop(t, s1=1.0, dur=0.35):  # scale pop in
    return [{"t":0,"scale":0,"opacity":0},{"t":t,"scale":0,"opacity":0},{"t":t+dur,"scale":s1,"opacity":1,"ease":"back"}]
def fade(t, dur=0.35, dy=14, y=None):
    if y is None: return [{"t":0,"opacity":0},{"t":t,"opacity":0},{"t":t+dur,"opacity":1,"ease":"out"}]
    return [{"t":0,"opacity":0,"y":y+dy},{"t":t,"opacity":0,"y":y+dy},{"t":t+dur,"opacity":1,"y":y,"ease":"out"}]
def moon(x,y,r,z=10,phase="full",k=None):
    L=[]; base={"type":"circle","x":x,"y":y,"r":r,"fill":"#2a2f4a","stroke":"#8c92b5","sw":2,"z":z}
    full={"type":"circle","x":x,"y":y,"r":r,"fill":"#e9e6da","z":z}
    if phase=="new": L=[base]
    elif phase=="full": L=[{"type":"glow","x":x,"y":y,"r":r*2.4,"color":"#cfd6ff","z":z,"opacity":0.5},full]
    else:
        d = f"M0,{-r} A{r},{r} 0 0 1 0,{r} Z" if phase=="first" else f"M0,{-r} A{r},{r} 0 0 0 0,{r} Z"
        L=[base,{"type":"path","x":x,"y":y,"d":d,"fill":"#e9e6da","z":z}]
    if k: [l.__setitem__("keys",k) for l in L]
    return L
def sun(x,y,r,z=10,k=None):
    L=[{"type":"glow","x":x,"y":y,"r":r*2.6,"color":"#ffd36a","z":z},{"type":"circle","x":x,"y":y,"r":r,"fill":YEL,"z":z}]
    if k: [l.__setitem__("keys",k) for l in L]
    return L
def saturn(x,y,r,z=10,k=None):
    L=[{"type":"ellipse","x":x,"y":y,"rx":r*1.9,"ry":r*0.45,"fill":"none","stroke":"#d9c38a","sw":max(3,r*0.18),"rot":-18,"z":z},
       {"type":"circle","x":x,"y":y,"r":r,"fill":"#d8b86a","z":z}]
    if k: [l.__setitem__("keys",k) for l in L]
    return L
def subs(en):
    lines = textwrap.wrap(en, 36); n=len(lines); h=34+40*n
    L=[{"type":"rect","x":360,"y":985,"w":660,"h":h,"r":20,"fill":"#171717","fill_opacity":0.86,"z":60,
        "keys":[{"t":0,"opacity":0},{"t":0.1,"opacity":0},{"t":0.35,"opacity":1}]}]
    y0 = 985 - 20*(n-1) + 11
    for i,l in enumerate(lines):
        L.append(txt(360,y0+40*i,l,30,"#F2F0E9",700,61,keys=[{"t":0,"opacity":0},{"t":0.1,"opacity":0},{"t":0.35,"opacity":1}]))
    return L
def ground(y=930): return {"type":"rect","x":360,"y":y+200,"w":800,"h":400,"fill":{"grad":[[0,"#10132a"],[1,"#07080f"]]},"z":2}


def sat(x,y,s=1.0,z=10,k=None,col="#d9d5c8"):
    L=[{"type":"rect","x":x,"y":y,"w":34*s,"h":34*s,"r":4,"fill":col,"z":z},
       {"type":"rect","x":x-40*s,"y":y,"w":40*s,"h":18*s,"fill":BLU,"stroke":"#8fa0ff","sw":2,"z":z},
       {"type":"rect","x":x+40*s,"y":y,"w":40*s,"h":18*s,"fill":BLU,"stroke":"#8fa0ff","sw":2,"z":z},
       {"type":"circle","x":x,"y":y-24*s,"r":4*s,"fill":YEL,"z":z}]
    if k: [l.__setitem__("keys",k) for l in L]
    return L
def earth(y=1560,r=700,z=3):
    return [{"type":"circle","x":360,"y":y,"r":r+14,"fill":BLU,"opacity":0.25,"z":z},
            {"type":"circle","x":360,"y":y,"r":r,"fill":{"grad":[[0,"#1c2a66"],[1,"#0a0d22"]],"dir":"v"},"z":z+1}]
def chip(x,y,s,w,t,col=BLU,tc=TXT,z=12):
    return [{"type":"rect","x":x,"y":y,"w":w,"h":52,"r":26,"fill":col,"z":z,"keys":pop(t)},
            txt(x,y+11,s,26,tc,800,z+1,keys=pop(t))]
def clock(x,y,r,col,t,wob=0,z=10):
    ks=[{"t":j/10,"rot":round(j*36+(wob*math.sin(j*1.7) if wob else 0),1),"ease":"linear"} for j in range(0,60)]
    return [{"type":"circle","x":x,"y":y,"r":r,"fill":"#10132a","stroke":col,"sw":5,"z":z,"keys":pop(t)},
            {"type":"path","x":x,"y":y,"d":f"M0,0 L0,{-r*0.72}","fill":"none","stroke":col,"sw":5,"z":z+1,"keys":ks},
            {"type":"circle","x":x,"y":y,"r":6,"fill":col,"z":z+2}]

import random
def P(x,y,h,outfit="gray",face="neutral",faces=None,z=12,**k):
    p={"type":"person","x":x,"y":y,"h":h,"outfit":outfit,"pose":"idle","z":z}
    if faces: p["faces"]=faces
    else: p["face"]=face
    p.update(k)
    return [{"type":"ellipse","x":x,"y":y+4,"rx":h*0.3,"ry":8,"fill":"#000000","opacity":0.4,"z":z-1},p]
def yawn(t0): return [{"t":0,"face":"neutral"},{"t":t0,"face":"shock"}]
def bubble(x,y,t,s="AAAH",size=44,col=YEL,z=15): return txt(x,y,s,size,col,800,z,keys=pop(t,1.0,0.3))
def heart(x,y,s,col,t,z=11,pulse=True):
    ks=pop(t,s,0.4)
    if pulse: ks+= [{"t":t+0.4+0.4*j,"scale":s*(1.12 if j%2==0 else 1.0),"ease":"inout"} for j in range(1,8)]
    return {"type":"path","x":x,"y":y,"d":"M0,30 C-60,-10 -45,-55 0,-25 C45,-55 60,-10 0,30 Z","fill":col,"z":z,"keys":ks}
def dots(y0,cols=20,sp=16,n=328,t0=0.2,pick=None,t1=None,x0=None):
    L=[]; x0 = 360-(cols-1)*sp/2 if x0 is None else x0
    for i in range(n):
        x=x0+(i%cols)*sp; y=y0+(i//cols)*sp
        d={"type":"circle","x":round(x,1),"y":round(y,1),"r":5.2,"fill":"#6c7090","z":10}
        ks=[{"t":0,"opacity":0},{"t":t0+i*0.004,"opacity":0},{"t":t0+i*0.004+0.12,"opacity":1}]
        if pick is not None and i in pick:
            tt=t1+pick[i]*0.006
            ks+= [{"t":tt,"scale":1.0},{"t":tt+0.15,"scale":1.5,"ease":"back"},{"t":tt+0.3,"scale":1.15}]
            d["fill_keys"]=None
            d2=dict(d); d2["fill"]=YEL; d2["z"]=11; d2["keys"]=[{"t":0,"opacity":0},{"t":tt,"opacity":0},{"t":tt+0.1,"opacity":1,"scale":1.4}]
            L.append(d); L.append(d2); d["keys"]=ks[:3]; continue
        d["keys"]=ks; L.append(d)
    return L
B=[]
# 0 hook
L=[SKY(60)]
L+=P(210,830,300,"gray",faces=yawn(0.5))
L+=P(510,830,300,"hero",faces=[{"t":0,"face":"neutral"},{"t":1.7,"face":"shock"}])
L.append(bubble(210,470,0.6)); L.append(bubble(510,470,1.8))
L.append({"type":"circle","x":360,"y":640,"r":10,"fill":BLU,"z":9,"keys":[{"t":0,"opacity":0},{"t":0.9,"opacity":0},{"t":1.0,"opacity":1,"x":290},{"t":1.8,"opacity":1,"x":430,"ease":"linear"},{"t":1.85,"opacity":0}]})
B.append((L,{"zoom":[1,1.05]}))
# 1 contagious chain
L=[SKY(50)]
xs=[90,225,360,495,630]
for i,x in enumerate(xs):
    L+=P(x,800,190,"hero" if i==4 else "gray",faces=yawn(0.3+0.55*i))
    L.append({"type":"circle","x":x,"y":690,"r":20,"fill":"none","stroke":BLU,"sw":3,"z":9,"keys":[{"t":0,"opacity":0,"scale":0.5},{"t":0.3+0.55*i,"opacity":0,"scale":0.5},{"t":0.35+0.55*i,"opacity":0.9,"scale":0.6},{"t":1.0+0.55*i,"opacity":0,"scale":3.2,"ease":"out"}]})
L.append(txt(360,500,"?",230,YEL,800,12,keys=pop(2.6,1.0,0.45)))
B.append((L,{"zoom":[1,1.04]}))
# 2 328 watch video
L=[SKY(50)]
L.append({"type":"rect","x":360,"y":430,"w":280,"h":150,"r":16,"fill":"#0b0e22","stroke":BLU,"sw":4,"z":10,"keys":pop(0.1)})
L.append({"type":"poly","points":[[345,400],[345,460],[395,430]],"fill":YEL,"z":11,"keys":pop(0.4)})
L+=chip(360,545,"328 PESERTA",300,0.7)
L+=dots(615,t0=1.0)
B.append((L,{"zoom":[1,1.03]}))
# 3 222 yawned
rng=random.Random(11); idx=list(range(328)); rng.shuffle(idx); pick={ix:r for r,ix in enumerate(idx[:222])}
L=[SKY(50)]
L.append(txt(360,430,"222",130,YEL,800,12,keys=pop(0.5,1.0,0.45)))
L.append(txt(360,500,"dari 328 menguap",32,TXT,700,12,keys=fade(0.9)))
L.append(txt(360,545,"setidaknya sekali",24,MUT,600,12,keys=fade(1.1)))
L+=dots(615,t0=0,pick=pick,t1=0.6)
B.append((L,{"zoom":[1,1.03]}))
# 4 2018 empathy
L=[SKY(50)]
L+=chip(360,400,"STUDI 2018",260,0.2)
L.append(heart(360,525,1.9,BLU,0.7))
L+=P(360,880,260,"hero",faces=yawn(0.5))
L.append(bubble(560,720,0.6))
B.append((L,{"zoom":[1,1.04]}))
# 5 2014 no strong link
L=[SKY(50)]
L+=chip(360,400,"STUDI 2014",260,0.2)
L.append(heart(360,525,1.9,"#5b5f7c",0.6,pulse=False))
L.append({"type":"rect","x":360,"y":525,"w":250,"h":14,"r":7,"fill":YEL,"rot":-40,"z":14,"keys":[{"t":0,"sx":0},{"t":1.2,"sx":0},{"t":1.6,"sx":1,"ease":"out"}]})
L+=P(360,880,260,"gray",faces=yawn(0.4))
B.append((L,{"zoom":[1,1.04]}))
# 6 age
L=[SKY(50)]
for x,o,fc,t,txtb,sz,kw in [(130,"hero",yawn(0.6),0.6,"AAAH",46,{}),(360,"gray",yawn(1.6),1.6,"aaah",30,{}),(590,"gray",[{"t":0,"face":"neutral"}],2.4,"...",34,{"glasses":True,"hair":None})]:
    kw={k:v for k,v in kw.items() if v is not None}
    L+=P(x,820,250,o,faces=fc,**kw)
    L.append(bubble(x,520,t,txtb,sz,YEL if x<500 else MUT))
L+=chip(130,880,"MUDA",160,0.3); L+=chip(590,880,"LEBIH TUA",220,0.3)
L.append({"type":"line","x1":210,"y1":880,"x2":470,"y2":880,"stroke":BLU,"sw":5,"z":10,"keys":[{"t":0,"opacity":0},{"t":1.0,"opacity":1}]})
B.append((L,{"zoom":[1,1.03]}))
# 7 8 percent
L=[SKY(50)]
L.append(txt(360,500,"USIA ≈ 8%",96,YEL,800,12,keys=pop(0.3,1.0,0.45)))
L.append({"type":"rect","x":360,"y":650,"w":560,"h":56,"r":14,"fill":"#2a2f4a","z":10})
L.append({"type":"rect","x":105,"y":650,"w":50,"h":56,"r":10,"fill":YEL,"z":11,"keys":[{"t":0,"sx":0},{"t":0.8,"sx":0},{"t":1.4,"sx":1,"ease":"out"}]})
L.append(txt(360,760,"sisanya belum terjelaskan",30,MUT,600,12,keys=fade(1.8)))
B.append((L,{"zoom":[1,1.03]}))
# 8 mystery
L=[SKY(80)]
L.append({"type":"glow","x":360,"y":520,"r":300,"color":BLU,"z":3,"opacity":0.35})
L.append(txt(360,560,"?",340,YEL,800,12,keys=pop(0.2,1.0,0.5)))
L+=P(360,860,230,"hero",faces=[{"t":0,"face":"neutral"},{"t":0.8,"face":"worry"}])
B.append((L,{"zoom":[1,1.04]}))
# 9 end card
L=[{"type":"rect","x":360,"y":640,"w":1200,"h":1600,"fill":{"grad":[[0,"#05060d"],[1,"#141a3d"]]},"z":0}]
L.append({"type":"glow","x":360,"y":560,"r":360,"color":BLU,"z":1,"keys":[{"t":0,"opacity":0},{"t":1.0,"opacity":0.7}]})
L.append(txt(360,580,"The Why Files ID",64,TXT,800,10,keys=fade(0.15,0.6,20,580)))
L.append(txt(360,650,"Segala hal punya alasan.",30,"#cfd3e6",500,10,keys=fade(0.6,0.6)))
L.append(txt(360,1112,"Sumber: Bartholomew & Cirulli, PLOS ONE (Mar 2014);",17,MUT,500,10,keys=fade(0.6)))
L.append(txt(360,1138,"Franzen dkk., J Exp Psychol Gen (Des 2018)",17,MUT,500,10,keys=fade(0.6)))
B.append((L,{"zoom":[1,1.02],"end":True}))

beats=[]
for i,(L,cam) in enumerate(B):
    t=T[i]; L=L+subs(t["text"])
    b={"duration":t["beat"],"layers":L,"camera":{"zoom":cam["zoom"],"ease":"inout"},
       "caption":{"text":ID[i],"from":t["start"],"to":round(t["start"]+t["dur"],3)}}
    if i==0: b["fade_in"]=0.2
    if cam.get("end"): b["fade_out"]=0.4; b["fade_in"]=0.2; b["caption"]=None
    beats.append(b)
json.dump({"meta":{"size":[720,1280],"fps":30},"beats":beats},open("story.json","w"),indent=0)
# cover
C=[SKY(80)]
C.append({"type":"glow","x":360,"y":520,"r":300,"color":BLU,"z":3,"opacity":0.3})
C+=P(230,720,380,"hero",face="shock",z=12)
C+=P(500,720,300,"gray",face="shock",z=12)
C.append(txt(230,330,"AAAH",56,YEL,800,15)); C.append(txt(500,400,"AAAH",44,YEL,800,15))
C.append({"type":"rect","x":360,"y":236,"w":330,"h":52,"r":26,"fill":BLU,"z":12})
C.append(txt(360,247,"PERILAKU MANUSIA",26,TXT,800,13))
for i,(s_,c) in enumerate([("Kenapa",TXT),("menguap",YEL),("menular?",TXT)]):
    C.append(txt(360,835+i*84,s_,72,c,800,13))
cb={"duration":2.0,"layers":C,"camera":{"zoom":[1,1]},"caption":None}
json.dump({"meta":{"size":[720,1280],"fps":30},"beats":[cb]},open("cover_story.json","w"),indent=0)
print(len(beats), sum(b["duration"] for b in beats))
