import math,wave,struct,random,subprocess
from pathlib import Path
rate=24000;duration=30;random.seed(4);a=[]
# Original restrained instrumental bed: soft harmonic tones, low pulse, no samples.
for i in range(rate*duration):
 t=i/rate;beat=t%0.5
 chord=[(130.81,196,293.66),(110,164.81,246.94),(146.83,220,329.63),(130.81,196,293.66)][int(t//4)%4]
 pad=sum(math.sin(2*math.pi*f*t) for f in chord)*.025*(.7+.3*math.sin(math.pi*t/4)**2)
 pulse=math.sin(2*math.pi*(48*beat+18*(1-math.exp(-24*beat))/24))*math.exp(-22*beat)*.15
 tick=(random.random()*2-1)*math.exp(-100*(t%.25))*.012
 fade=min(1,t/.2,max(0,(30-t)/2));v=(pad+pulse+tick)*fade
 a.append(struct.pack('<h',int(max(-1,min(1,v))*32767)))
with wave.open('/tmp/reel-edit-v2/original-bed.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b''.join(a))
p=Path(__file__).resolve().parents[2]/'Assets/reel/jazz-farey-showreel.mp4';tmp=p.with_name('temp.mp4')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-i','/tmp/reel-edit-v2/original-bed.wav','-t','30','-c:v','copy','-c:a','aac','-b:a','96k','-movflags','+faststart',str(tmp)],check=True);tmp.replace(p)
