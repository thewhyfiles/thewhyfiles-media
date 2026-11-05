import json, sys, soundfile as sf
from kokoro_onnx import Kokoro
import os; S=os.environ["S"]
voice="am_michael"
k=Kokoro(f"{S}/tts/kokoro.onnx", f"{S}/tts/voices.bin")
lines=[
"Drop an ice cube into water.",
"It floats. But that's actually strange. Why?",
"For most substances, the solid is denser than the liquid, so it sinks.",
"Water is a rare exception.",
"In liquid water, molecules tumble and pack closely together.",
"When it freezes, hydrogen bonds lock them into an open, hexagonal lattice.",
"All that empty space makes ice about nine percent less dense.",
"So it floats, with about ninety percent hidden below the surface.",
"That's why lakes freeze from the top down, and fish survive underneath.",
"Everything has a reason.",
]
out=[]
for i,t in enumerate(lines):
    a,sr=k.create(t,voice=voice,speed=0.97,lang="en-us")
    p=f"{S}/vo/{voice}_{i:02d}.wav"; sf.write(p,a,sr); out.append({"i":i,"text":t,"dur":len(a)/sr,"path":p})
json.dump(out,open(f"{S}/vo/{voice}.json","w"),indent=1)
print(voice,[round(o["dur"],2) for o in out], round(sum(o["dur"] for o in out),1))
