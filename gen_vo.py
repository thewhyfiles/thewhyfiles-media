import json, sys, soundfile as sf
from kokoro_onnx import Kokoro
import os; S=os.environ["S"]
voice="am_michael"
k=Kokoro(f"{S}/tts/kokoro.onnx", f"{S}/tts/voices.bin")
lines=[
"Why do clock hands turn this way?",
"Long before gears, people told time with shadows.",
"A sundial is a pointer that casts a shadow.",
"Up north, the sun rises in the east and crosses the southern sky.",
"So the shadow sweeps from west, through north, to east.",
"Seen from above, that turn is clockwise.",
"Our clocks took shape in medieval Europe, far up north.",
"Clockmakers likely copied that familiar motion.",
"Down south, a sundial's shadow turns the other way.",
"But by then, clockwise was already the standard.",
"Everything has a reason.",
]
out=[]
for i,t in enumerate(lines):
    a,sr=k.create(t,voice=voice,speed=0.97,lang="en-us")
    p=f"{S}/vo/{voice}_{i:02d}.wav"; sf.write(p,a,sr); out.append({"i":i,"text":t,"dur":len(a)/sr,"path":p})
json.dump(out,open(f"{S}/vo/{voice}.json","w"),indent=1)
print(voice,[round(o["dur"],2) for o in out], round(sum(o["dur"] for o in out),1))
