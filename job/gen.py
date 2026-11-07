import json, math, textwrap
T = json.load(open('out/timing.json'))
ID = ["Bagaimana GPS tahu lokasimu?",
"Ponselmu tidak mengirim apa pun. Hanya mendengar.",
"Satelit setinggi 20.000 km menyiarkan waktu tepat.",
"Sinyal radio melaju secepat cahaya.",
"Ponsel mengukur lama tiap sinyal tiba.",
"Waktu dikali kecepatan menjadi jarak.",
"Satu jarak: kamu ada di lingkaran raksasa.",
"Tiga lingkaran berpotongan di satu titik.",
"Jam ponsel murah, satelit keempat memperbaikinya.",
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
B=[]
# 1 hook
D=T[0]["beat"]; L=[SKY(60)]+earth()
for x,y,s,t in [(170,460,0.9,0.2),(550,420,0.9,0.5),(360,360,1.0,0.8)]:
    L+=sat(x,y,s,k=pop(t))
L.append({"type":"person","x":360,"y":866,"h":230,"outfit":"hero","pose":"idle","faces":[{"t":0,"face":"neutral"},{"t":1.4,"face":"worry"}],"z":12})
L.append(txt(360,590,"?",190,YEL,800,12,keys=pop(1.2,1.0,0.45)))
B.append((L,{"zoom":[1,1.05]}))
# 2 phone only listens
D=T[1]["beat"]; L=[SKY(50)]+earth()
L+=sat(360,420,1.1,k=pop(0.1))
L.append({"type":"person","x":360,"y":850,"h":230,"outfit":"hero","pose":"idle","z":12})
for j in range(4):
    t0=0.5+j*0.55; ks=[{"t":0,"y":490,"opacity":0},{"t":t0,"y":490,"opacity":0},{"t":t0+0.1,"y":490,"opacity":1},{"t":t0+0.9,"y":700,"opacity":1,"ease":"linear"},{"t":t0+1.0,"y":700,"opacity":0}]
    L.append({"type":"circle","x":360,"r":8,"fill":YEL,"z":11,"keys":ks})
L+=chip(360,900,"HANYA MENERIMA",440,1.5)
B.append((L,{"zoom":[1,1.04]}))
# 3 orbit
D=T[2]["beat"]; L=[SKY(60)]
cx,cy,R=360,600,240
L.append({"type":"circle","x":cx,"y":cy,"r":R,"fill":"none","stroke":"#4a5390","sw":3,"opacity":0.8,"z":4})
L.append({"type":"circle","x":cx,"y":cy,"r":112,"fill":BLU,"opacity":0.25,"z":5})
L.append({"type":"circle","x":cx,"y":cy,"r":100,"fill":{"grad":[[0,"#1c2a66"],[1,"#0a0d22"]],"dir":"v"},"z":6})
L.append(txt(cx,cy-14,"Bumi",28,MUT,700,8))
for i in range(4):
    a0=i*math.pi/2+0.5; ks=[]
    for j in range(0,int(D*10)+1):
        a=a0+0.12*j/10*1.0; ks.append({"t":j/10,"x":round(cx+R*math.cos(a),1),"y":round(cy+R*math.sin(a),1),"ease":"linear"})
    ks[0]["opacity"]=0; ks[2+i*2]["opacity"]=0; ks[5+i*2]["opacity"]=1
    L.append({"type":"circle","r":15,"fill":YEL,"z":9,"keys":ks})
    L.append({"type":"glow","r":40,"color":YEL,"z":8,"opacity":0.5,"keys":[dict(k) for k in ks]})
L+=chip(360,870,"± 20.200 km di atas Bumi",440,1.0)
L.append(txt(360,1010,"",20,MUT))
B.append((L,{"zoom":[1,1.03]}))
# 4 speed of light
D=T[3]["beat"]; L=[SKY(50)]+earth()
L+=sat(200,430,1.0,k=pop(0.1))
L.append({"type":"person","x":520,"y":850,"h":230,"outfit":"hero","pose":"idle","z":12})
for j in range(3):
    t0=0.5+j*0.7; ks=[{"t":0,"x":215,"y":470,"opacity":0},{"t":t0,"x":215,"y":470,"opacity":0},{"t":t0+0.05,"x":215,"y":470,"opacity":1},{"t":t0+0.55,"x":510,"y":700,"opacity":1,"ease":"linear"},{"t":t0+0.6,"x":510,"y":700,"opacity":0}]
    L.append({"type":"glow","r":40,"color":"#ffe08a","z":10,"keys":[dict(k) for k in ks]})
    L.append({"type":"circle","r":9,"fill":"#fff4d0","z":11,"keys":ks})
L+=chip(360,900,"300.000 km / detik",460,1.2)
B.append((L,{"zoom":[1,1.04]}))
# 5 stopwatch
D=T[4]["beat"]; L=[SKY(50)]
L+=clock(360,600,170,YEL,0.2)
L.append({"type":"rect","x":360,"y":405,"w":40,"h":24,"r":4,"fill":YEL,"z":9})
L.append(txt(360,860,"± 0,07 detik",60,TXT,800,12,keys=fade(1.4,y=860)))
L.append(txt(360,925,"satelit tepat di atas kepala",24,MUT,600,12,keys=fade(2.0)))
B.append((L,{"zoom":[1,1.04]}))
# 6 equation
D=T[5]["beat"]; L=[SKY(50)]
L.append(txt(360,470,"waktu",60,TXT,800,12,keys=fade(0.3,y=470)))
L.append(txt(360,560,"×",70,YEL,800,12,keys=pop(0.9)))
L.append(txt(360,650,"kecepatan cahaya",50,TXT,800,12,keys=fade(1.3,y=650)))
L.append({"type":"rect","x":360,"y":735,"w":500,"h":5,"r":2,"fill":BLU,"z":10,"keys":[{"t":0,"sx":0},{"t":1.9,"sx":0},{"t":2.3,"sx":1,"ease":"out"}]})
L.append(txt(360,830,"= jarak",84,YEL,800,12,keys=pop(2.4,1.0,0.45)))
B.append((L,{"zoom":[1,1.04]}))
# 7 one circle
D=T[6]["beat"]; L=[SKY(50)]
cx,cy,R=360,590,240
L+=sat(cx,cy,1.0,k=pop(0.1),z=10)
L.append({"type":"circle","x":cx,"y":cy,"r":R,"fill":"none","stroke":BLU,"sw":5,"z":9,"keys":[{"t":0,"scale":0.1,"opacity":0},{"t":0.3,"scale":0.1,"opacity":0},{"t":1.2,"scale":1,"opacity":1,"ease":"out"}]})
ks=[]
for j in range(0,int(D*10)+1):
    a=math.pi/2+0.5*math.sin(j/10*1.3)*1.0+0.15*j/10; ks.append({"t":j/10,"x":round(cx+R*math.cos(a),1),"y":round(cy+R*math.sin(a),1),"ease":"linear"})
ks[0]["opacity"]=0; ks[11]["opacity"]=0; ks[14]["opacity"]=1
L.append({"type":"glow","r":46,"color":YEL,"z":10,"keys":[dict(k) for k in ks]})
L.append({"type":"circle","r":16,"fill":YEL,"z":11,"keys":ks})
L.append(txt(360,890,"kamu di mana saja di sini",28,MUT,600,12,keys=fade(2.0)))
B.append((L,{"zoom":[1,1.03]}))
# 8 three circles
D=T[7]["beat"]; L=[SKY(50)]
P=(360,650)
for i,((x,y),r,t) in enumerate([((240,530),170,0.2),((480,530),170,1.0),((360,780),130,1.8)]):
    L+=sat(x,y,0.55,k=pop(t),z=10)
    L.append({"type":"circle","x":x,"y":y,"r":r,"fill":"none","stroke":BLU,"sw":4,"z":9,"keys":[{"t":0,"scale":0.1,"opacity":0},{"t":t,"scale":0.1,"opacity":0},{"t":t+0.8,"scale":1,"opacity":1,"ease":"out"}]})
L.append({"type":"glow","x":P[0],"y":P[1],"r":90,"color":YEL,"z":11,"keys":[{"t":0,"opacity":0},{"t":2.8,"opacity":0},{"t":3.2,"opacity":1}]})
L.append({"type":"circle","x":P[0],"y":P[1],"r":15,"fill":YEL,"z":12,"keys":pop(2.8,1,0.35)})
B.append((L,{"zoom":[1,1.03]}))
# 9 clocks
D=T[8]["beat"]; L=[SKY(50)]
L+=clock(190,560,100,"#a5a5a0",0.2,wob=14)
L.append(txt(190,710,"jam ponsel",26,TXT,700,12,keys=fade(0.5)))
L.append(txt(190,745,"murah",22,MUT,600,12,keys=fade(0.7)))
L+=clock(530,560,100,YEL,0.8)
L.append(txt(530,710,"jam atom",26,TXT,700,12,keys=fade(1.1)))
L.append(txt(530,745,"di satelit",22,MUT,600,12,keys=fade(1.3)))
L+=sat(360,420,0.8,k=pop(2.0))
L.append({"type":"glow","x":360,"y":420,"r":90,"color":BLU,"z":5,"opacity":0.4,"keys":pop(2.0)})
L+=chip(360,860,"+1 SATELIT = KOREKSI",500,2.4)
B.append((L,{"zoom":[1,1.03]}))
# 10 end card
D=T[9]["beat"]; L=[{"type":"rect","x":360,"y":640,"w":1200,"h":1600,"fill":{"grad":[[0,"#05060d"],[1,"#141a3d"]]},"z":0}]
L.append({"type":"glow","x":360,"y":560,"r":360,"color":BLU,"z":1,"keys":[{"t":0,"opacity":0},{"t":1.0,"opacity":0.7}]})
L.append(txt(360,580,"The Why Files ID",64,TXT,800,10,keys=fade(0.15,0.6,20,580)))
L.append(txt(360,650,"Segala hal punya alasan.",30,"#cfd3e6",500,10,keys=fade(0.6,0.6)))
L.append(txt(360,1130,"Sumber: GPS.gov (Space Segment, Accuracy); Scientific American (Leick)",17,MUT,500,10,keys=fade(0.6)))
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
C=[SKY(80)]+earth(1760,760)
C+=sat(180,430,1.5)+sat(545,340,1.3)
C.append({"type":"circle","x":360,"y":600,"r":150,"fill":"none","stroke":BLU,"sw":6,"z":9,"opacity":0.8})
C.append({"type":"glow","x":360,"y":600,"r":150,"color":YEL,"z":10,"opacity":0.55})
C.append({"type":"circle","x":360,"y":600,"r":24,"fill":YEL,"z":11})
C.append({"type":"rect","x":360,"y":236,"w":250,"h":52,"r":26,"fill":BLU,"z":12})
C.append(txt(360,247,"TEKNOLOGI",26,TXT,800,13))
for i,(s_,c) in enumerate([("Bagaimana",TXT),("GPS tahu",YEL),("lokasimu?",TXT)]):
    C.append(txt(360,815+i*84,s_,72,c,800,13))
cb={"duration":2.0,"layers":C,"camera":{"zoom":[1,1]},"caption":None}
json.dump({"meta":{"size":[720,1280],"fps":30},"beats":[cb]},open("cover_story.json","w"),indent=0)
print(len(beats), sum(b["duration"] for b in beats))
