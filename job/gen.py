import json, math, textwrap
T = json.load(open('out/timing.json'))
ID = ["Kenapa seminggu ada tujuh hari?",
"Hari, bulan, tahun dari langit. Seminggu tidak.",
"Dulu, pengamat langit Babilonia rajin mengamati Bulan.",
"Satu bulan lunar sekitar 29,5 hari.",
"Dibagi empat fase, tiap fase sekitar tujuh hari.",
"Mereka juga melihat tujuh benda langit berkelana.",
"Matahari, Bulan, dan lima planet yang terlihat.",
"Tujuh jadi angka istimewa, minggu menyebar ke barat.",
"Tahun 321 M, Roma meresmikan minggu tujuh hari.",
"Itulah asal nama Sunday, Monday, dan Saturday.",
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

B=[]
# 1 hook: calendar row of 7
D=T[0]["beat"]; L=[SKY(50)]
days="SMTWTFS"
for i,c in enumerate(days):
    x=79+35+i*82; t=0.3+i*0.22
    col = BLU if i in (0,6) else "#262b45"
    L.append({"type":"rect","x":x,"y":470,"w":70,"h":86,"r":10,"fill":col,"stroke":"#5a6290","sw":2,"z":10,"keys":pop(t)})
    L.append(txt(x,483,c,34,TXT,800,11,keys=pop(t)))
L.append(txt(360,660,"7",150,YEL,800,11,keys=pop(1.9,1.0,0.45)))
L.append({"type":"person","x":360,"y":930,"h":220,"outfit":"hero","pose":"hands_up","faces":[{"t":0,"face":"neutral"},{"t":1.9,"face":"shock"}],"z":12})
B.append((L,{"zoom":[1,1.05]}))
# 2 sky gives days months years
D=T[1]["beat"]; L=[SKY(60)]
L+=sun(150,470,52,k=pop(0.3)); L.append(txt(150,575,"Hari",30,TXT,700,12,keys=fade(0.5)))
L+=moon(360,470,46,k=pop(0.8)); L.append(txt(360,575,"Bulan",30,TXT,700,12,keys=fade(1.0)))
L.append({"type":"circle","x":570,"y":470,"r":58,"fill":"none","stroke":"#6b739c","sw":3,"z":10,"keys":pop(1.3)})
L.append({"type":"circle","x":570,"y":470,"r":16,"fill":YEL,"z":10,"keys":pop(1.3)})
L.append({"type":"circle","x":628,"y":470,"r":9,"fill":"#5aa0ff","z":11,"keys":[{"t":0,"opacity":0},{"t":1.3,"opacity":0},{"t":1.6,"opacity":1}]})
L.append(txt(570,575,"Tahun",30,TXT,700,12,keys=fade(1.5)))
L.append({"type":"rect","x":360,"y":760,"w":300,"h":130,"r":18,"fill":"none","stroke":BLU,"sw":4,"z":10,"keys":pop(2.3)})
L.append(txt(360,750,"Minggu",40,TXT,800,11,keys=pop(2.3)))
L.append(txt(360,800,"tanpa penanda langit",22,MUT,600,11,keys=fade(2.7)))
B.append((L,{"zoom":[1,1.04]}))
# 3 babylonian ziggurat + moon
D=T[2]["beat"]; L=[SKY(90)]
L+=moon(540,430,62)
for i,(w,h) in enumerate([(460,70),(340,70),(220,70)]):
    L.append({"type":"rect","x":300,"y":930-35-70*i,"w":w,"h":h,"fill":["#3a3326","#4a4130","#5a4f3a"][i],"z":5})
L.append({"type":"rect","x":300,"y":745,"w":60,"h":20,"fill":"#5a4f3a","z":5})
L.append(ground())
L.append({"type":"person","x":300,"y":720,"h":130,"outfit":"hero","pose":"point_r","looky":-1,"lookx":1,"z":8,
          "keys":[{"t":0,"aR":-60},{"t":1.2,"aR":-140,"ease":"out"}]})
L.append({"type":"person","x":130,"y":930,"h":120,"outfit":"gray","pose":"idle","looky":-1,"z":8})
L.append({"type":"person","x":610,"y":930,"h":130,"outfit":"gray","pose":"hands_up","z":8})
B.append((L,{"zoom":[1.08,1.0]}))
# 4 lunar month ring of 30 dots
D=T[3]["beat"]; L=[SKY(40)]
cx,cy,R=360,620,230
L+=moon(cx,cy-30,60)
L.append(txt(cx,cy+90,"± 29,5 hari",44,YEL,800,12,keys=fade(D-1.4)))
for i in range(30):
    a=-math.pi/2+2*math.pi*i/30; t=0.3+i*(D-1.6)/30
    r=10 if i<29 else 7
    L.append({"type":"circle","x":round(cx+R*math.cos(a),1),"y":round(cy+R*math.sin(a),1),"r":r,"fill":"#2a2f4a","z":9})
    L.append({"type":"circle","x":round(cx+R*math.cos(a),1),"y":round(cy+R*math.sin(a),1),"r":r,"fill":BLU,"z":10,
              "keys":[{"t":0,"opacity":0},{"t":t,"opacity":0},{"t":t+0.12,"opacity":1}]})
B.append((L,{"zoom":[1,1.03]}))
# 5 four phases
D=T[4]["beat"]; L=[SKY(40)]
ph=["new","first","full","last"]; names=["Bulan baru","Kuartal 1","Purnama","Kuartal 3"]
for i in range(4):
    x=105+i*170; t=0.3+i*0.55
    L+=moon(x,520,52,phase=ph[i],k=pop(t))
    L.append(txt(x,612,names[i],22,MUT,600,12,keys=fade(t+0.1)))
    L.append(txt(x,672,"±7 hari",28,YEL,800,12,keys=fade(t+0.25)))
L.append({"type":"rect","x":360,"y":720,"w":620,"h":6,"r":3,"fill":BLU,"z":10,"keys":[{"t":0,"sx":0},{"t":2.6,"sx":0},{"t":3.1,"sx":1,"ease":"out"}]})
L.append(txt(360,810,"29,5 ÷ 4 ≈ 7,4",52,TXT,800,12,keys=fade(3.0,y=810)))
B.append((L,{"zoom":[1.03,1]}))
# 6 seven wanderers along arc
D=T[5]["beat"]; L=[SKY(120)]
L.append({"type":"path","d":"M-20,760 Q360,240 740,760","fill":"none","stroke":BLU,"sw":3,"opacity":0.6,"z":5})
bod=[(YEL,22),("#e9e6da",18),("#b0aaa0",7),("#fff4d0",9),("#e0603a",8),("#f0d9a8",12),("#d8b86a",11)]
def arc(u): # quadratic bezier
    x=(1-u)**2*-20+2*(1-u)*u*360+u*u*740; y=(1-u)**2*760+2*(1-u)*u*240+u*u*760; return round(x,1),round(y,1)
for i,(c,r) in enumerate(bod):
    u0=0.08+i*0.125; ks=[]
    for j in range(0,int(D*10)+1):
        t=j/10; x,y=arc(u0+0.035*t); ks.append({"t":t,"x":x,"y":y,"ease":"linear"})
    ks[0]["opacity"]=0; ks[3+i*2]["opacity"]=0; ks[6+i*2]["opacity"]=1
    L.append({"type":"glow","r":r*3.5,"color":c,"z":6,"keys":[dict(k) for k in ks]})
    L.append({"type":"circle","r":r,"fill":c,"z":7,"keys":[dict(k) for k in ks]})
L.append(ground(930))
L.append({"type":"person","x":360,"y":930,"h":170,"outfit":"hero","pose":"point_l","looky":-1,"z":8})
B.append((L,{"zoom":[1,1.05]}))
# 7 lineup sun moon + 5 planets
D=T[6]["beat"]; L=[SKY(50)]
L+=sun(250,450,60,k=pop(0.2)); L.append(txt(250,560,"Matahari",26,TXT,700,12,keys=fade(0.35)))
L+=moon(470,450,50,k=pop(0.5)); L.append(txt(470,560,"Bulan",26,TXT,700,12,keys=fade(0.65)))
pl=[("Merkurius","#b0aaa0",18),("Venus","#fff4d0",24),("Mars","#e0603a",21),("Jupiter","#e8c79a",34),("Saturnus","#d8b86a",26)]
for i,(n,c,r) in enumerate(pl):
    x=80+i*140; t=0.9+i*0.3
    if n=="Saturnus": L+=saturn(x,720,r,k=pop(t))
    else: L.append({"type":"circle","x":x,"y":720,"r":r,"fill":c,"z":10,"keys":pop(t)})
    L.append(txt(x,800,n,22,TXT,600,12,keys=fade(t+0.1)))
L.append({"type":"rect","x":360,"y":880,"w":160,"h":56,"r":28,"fill":BLU,"z":12,"keys":pop(2.6)})
L.append(txt(360,891,"= 7",32,TXT,800,13,keys=pop(2.6)))
B.append((L,{"zoom":[1,1.03]}))
# 8 spread west: Babylon -> Rome
D=T[7]["beat"]; L=[SKY(40)]
L.append(txt(360,470,"7",170,YEL,800,10,keys=pop(0.2,1,0.5)))
L.append({"type":"glow","x":360,"y":420,"r":200,"color":"#ffd36a","z":9,"opacity":0.35})
bx,by,rx,ry=580,760,140,680
L.append({"type":"line","x1":rx,"y1":ry,"x2":bx,"y2":by,"stroke":"#3b4270","sw":4,"z":8})
for (x,y,n) in [(bx,by,"Babilonia"),(rx,ry,"Roma")]:
    L.append({"type":"circle","x":x,"y":y,"r":14,"fill":BLU if n=="Babilonia" else "#2a2f4a","stroke":BLU,"sw":3,"z":10})
    L.append(txt(x,y+56,n,28,TXT,700,12))
for j in range(5):
    t0=1.0+j*0.25; ks=[{"t":0,"x":bx,"y":by,"opacity":0},{"t":t0,"x":bx,"y":by,"opacity":0},{"t":t0+0.1,"x":bx,"y":by,"opacity":1},{"t":t0+1.6,"x":rx,"y":ry,"opacity":1,"ease":"inout"},{"t":t0+1.8,"x":rx,"y":ry,"opacity":0}]
    L.append({"type":"circle","r":7,"fill":YEL,"z":11,"keys":ks})
L.append({"type":"circle","x":rx,"y":ry,"r":14,"fill":BLU,"z":10,"keys":[{"t":0,"opacity":0},{"t":2.7,"opacity":0},{"t":3.0,"opacity":1}]})
L.append(txt(360,880,"Persia · Yunani · Roma",24,MUT,600,12,keys=fade(2.6)))
B.append((L,{"zoom":[1,1.04]}))
# 9 Rome 321 AD temple + stamp
D=T[8]["beat"]; L=[SKY(40)]
L.append({"type":"poly","points":[[150,440],[360,360],[570,440]],"fill":"#d9d5c8","z":5})
L.append({"type":"rect","x":360,"y":455,"w":440,"h":30,"fill":"#c9c4b5","z":5})
for i in range(5): L.append({"type":"rect","x":190+i*85,"y":580,"w":36,"h":220,"fill":"#d9d5c8","z":5})
L.append({"type":"rect","x":360,"y":705,"w":480,"h":30,"fill":"#c9c4b5","z":5})
L.append({"type":"rect","x":360,"y":740,"w":520,"h":30,"fill":"#b8b3a4","z":5})
L.append(ground(755))
L.append(txt(360,860,"321 M",64,YEL,800,12,keys=fade(0.6,y=860)))
L.append({"type":"rect","x":360,"y":560,"w":300,"h":96,"r":12,"fill":"#10132a","fill_opacity":0.92,"stroke":BLU,"sw":7,"rot":-8,"z":14,"keys":[{"t":0,"opacity":0,"scale":1.8},{"t":2.2,"opacity":0,"scale":1.8},{"t":2.5,"opacity":1,"scale":1,"ease":"out"}]})
L.append(txt(360,578,"7 HARI",50,BLU,800,14,rot=-8,keys=[{"t":0,"opacity":0,"scale":1.8},{"t":2.2,"opacity":0,"scale":1.8},{"t":2.5,"opacity":1,"scale":1,"ease":"out"}]))
B.append((L,{"zoom":[1,1.04],"shake_at":2.5}))
# 10 Sunday Monday Saturday
D=T[9]["beat"]; L=[SKY(40)]
rows=[("Sunday","Matahari",lambda y,k:sun(170,y,36,k=k)),("Monday","Bulan",lambda y,k:moon(170,y,34,k=k)),("Saturday","Saturnus",lambda y,k:saturn(170,y,26,k=k))]
for i,(en,idn,f) in enumerate(rows):
    y=440+i*180; t=0.6+i*0.8
    L+=f(y,pop(t))
    L.append(txt(430,y+8,en,56,TXT,800,12,keys=fade(t+0.1)))
    L.append(txt(430,y+52,"← "+idn,24,YEL,600,12,keys=fade(t+0.3)))
B.append((L,{"zoom":[1,1.03]}))
# 11 end card
D=T[10]["beat"]; L=[{"type":"rect","x":360,"y":640,"w":1200,"h":1600,"fill":{"grad":[[0,"#05060d"],[1,"#141a3d"]]},"z":0}]
L.append({"type":"glow","x":360,"y":560,"r":360,"color":BLU,"z":1,"keys":[{"t":0,"opacity":0},{"t":1.0,"opacity":0.7}]})
L.append(txt(360,580,"The Why Files ID",64,TXT,800,10,keys=fade(0.15,0.6,20,580)))
L.append(txt(360,650,"Segala hal punya alasan.",30,"#cfd3e6",500,10,keys=fade(0.6,0.6)))
L.append(txt(360,1130,"Sumber: Britannica; Astronomy/The Conversation (2024); Merriam-Webster",17,MUT,500,10,keys=fade(0.6)))
B.append((L,{"zoom":[1,1.02],"end":True}))

beats=[]
for i,(L,cam) in enumerate(B):
    t=T[i]; L=L+subs(t["text"])
    b={"duration":t["beat"],"layers":L,"camera":{"zoom":cam["zoom"],"ease":"inout"},
       "caption":{"text":ID[i],"from":t["start"],"to":round(t["start"]+t["dur"],3)}}
    if "shake_at" in cam: b["camera"]["keys"]=None; b["camera"].pop("keys"); b["camera"]["shake"]=0
    if i==0: b["fade_in"]=0.2
    if cam.get("end"): b["fade_out"]=0.4; b["fade_in"]=0.2
    beats.append(b)
json.dump({"meta":{"size":[720,1280],"fps":30},"beats":beats},open("story.json","w"),indent=0)
print(len(beats), sum(b["duration"] for b in beats))
