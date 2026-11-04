import json, sys, soundfile as sf
from kokoro_onnx import Kokoro
import os; S=os.environ["S"]
voice="am_michael"
k=Kokoro(f"{S}/tts/kokoro.onnx", f"{S}/tts/voices.bin")
lines=[
"Egypt's pyramids are more than four thousand years old.",
"But why the pyramid shape?",
"Early royal tombs were low, flat blocks called mastabas.",
"Then Imhotep stacked them, each one smaller than the last.",
"The result: Djoser's Step Pyramid, about sixty metres tall.",
"Stone is strong when squeezed, but weak when it bends.",
"In a pyramid, every block rests on a wider layer below it.",
"Most of the mass sits low, so the weight flows into the ground.",
"Smoothed out, the Great Pyramid was Earth's tallest structure for nearly four thousand years.",
"Everything has a reason.",
]
out=[]
for i,t in enumerate(lines):
    a,sr=k.create(t,voice=voice,speed=0.97,lang="en-us")
    p=f"{S}/vo/{voice}_{i:02d}.wav"; sf.write(p,a,sr); out.append({"i":i,"text":t,"dur":len(a)/sr,"path":p})
json.dump(out,open(f"{S}/vo/{voice}.json","w"),indent=1)
print(voice,[round(o["dur"],2) for o in out], round(sum(o["dur"] for o in out),1))
