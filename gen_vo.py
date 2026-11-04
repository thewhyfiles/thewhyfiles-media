import json, sys, soundfile as sf
from kokoro_onnx import Kokoro
import os; S=os.environ["S"]
voice="am_michael"
k=Kokoro(f"{S}/tts/kokoro.onnx", f"{S}/tts/voices.bin")
lines=[
"Look closely at any QR code.",
"It has three big squares in its corners. Why?",
"These finder patterns show the camera where the code is.",
"Each has the same stripes: dark, light, thick core, light, dark.",
"From any angle through its center, the ratio stays one, one, three, one, one.",
"So a scanner spots them instantly, even when the code is tilted.",
"One corner is empty, so the scanner knows which way is up.",
"It straightens the grid, then reads the tiny squares as data.",
"Three simple squares, and any angle works.",
"Everything has a reason.",
]
out=[]
for i,t in enumerate(lines):
    a,sr=k.create(t,voice=voice,speed=0.97,lang="en-us")
    p=f"{S}/vo/{voice}_{i:02d}.wav"; sf.write(p,a,sr); out.append({"i":i,"text":t,"dur":len(a)/sr,"path":p})
json.dump(out,open(f"{S}/vo/{voice}.json","w"),indent=1)
print(voice,[round(o["dur"],2) for o in out], round(sum(o["dur"] for o in out),1))
