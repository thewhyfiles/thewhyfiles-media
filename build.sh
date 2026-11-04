set -e
export S=$PWD/scratch
mkdir -p $S/tts $S/vo; ln -sfn $PWD $S/work
pip install -q kokoro-onnx soundfile scipy
curl -sSL -o $S/tts/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
curl -sSL -o $S/tts/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
npm init -y >/dev/null; npm i -s three @fontsource/sora @fontsource/inter @fontsource/dm-serif-display playwright
npx playwright install --with-deps chromium
python3 gen_vo.py; node build_timeline.cjs
CONC=$(nproc) node render.cjs scenes 4 7 0 1 2 8 9 3 5 6
node cover.cjs
python3 audio.py
cd out; ls scene_*.mp4 | sed "s/.*/file '&'/" > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy video.mp4
ffmpeg -v error -y -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af loudnorm=I=-15:TP=-1.5:LRA=11 -ar 48000 -shortest -movflags +faststart reel.mp4
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration,size -of compact reel.mp4
python3 -c "from PIL import Image; im=Image.open('cover.jpg'); print('cover', im.size)" 2>/dev/null || ls -l cover.jpg
