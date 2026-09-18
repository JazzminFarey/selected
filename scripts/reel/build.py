"""30-second correction edit. Explicit compositions; every foreground asset is uncropped.
Only background colour fields extend beyond the frame. Source artwork is never redrawn.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter, ImageSequence
import subprocess, json, math
ROOT=Path(__file__).resolve().parents[2]; A=ROOT/'Assets'; OUT=A/'reel'; TMP=Path('/tmp/reel-correction');TMP.mkdir(exist_ok=True)
W,H,FPS=1280,720,30
sources={
 'money':A/'Money Your Way/Hero.png','money2':A/'Money Your Way/1000131099 (1).png','trust':A/'Money Your Way/1000131103.png',
 'flex1':A/"That's A Flex/Ad 1.jpg",'flex2':A/"That's A Flex/Ad 2.jpg",
 'creator':A/'Feed/1.jpg','creator2':A/'Feed/2.jpg','travel':A/'Feed/4.jpg',
 'shirt':A/'earlier/allheartsecommerce-0.webp','mugs':A/'earlier/allheartsecommerce-1.webp','tote':A/'earlier/allheartsecommerce-2.webp',
 'posters':A/'earlier/home-2.webp','social':A/'earlier/barnardosbuddies-1.webp','buddies':A/'earlier/barnardosbuddies-2.webp',
 'book':A/'earlier/home-3.webp','spread':A/'earlier/death-by-xoko-65a7m-2.webp',
 'walk':A/'earlier/home-0.webp','phones':A/'earlier/walkyourway-1.webp'}
ims={k:Image.open(p).convert('RGB') for k,p in sources.items()}
# Extract genuine motion unchanged; its entire source frame remains visible.
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'work/flex-campaign.mp4'),'-vf','fps=30',str(TMP/'flex-%03d.jpg')],check=True)
flex=[Image.open(p).convert('RGB') for p in sorted(TMP.glob('flex-*.jpg'))]
g=Image.open(A/'earlier/jump-rope.gif');jump=[f.convert('RGB') for f in ImageSequence.Iterator(g)]
# Each shot has a deliberately chosen composition, background and source grouping.
shots=[
 ('money-pair',0,2,'Money Your Way'),('flex-motion',2,4.5,'That’s A Flex'),('creator-triptych',4.5,7,'Built for Feed'),
 ('allhearts-pair',7,9,'allHearts'),('allhearts-product',9,11,'allHearts'),
 ('barn-posters',11,13,'Barnardos Buddies'),('barn-pair',13,15,'Barnardos Buddies'),
 ('jump-motion',15,17.5,'Jump Rope'),('jump-spread',17.5,19,'Jump Rope'),
 ('walk-phones',19,21,'Walk Your Way'),('walk-pair',21,23,'Walk Your Way'),
 ('money-trust',23,23.75,'Money Your Way'),('flex-print',23.75,24.5,'That’s A Flex'),
 ('allhearts-pair',24.5,25.25,'allHearts'),('barn-pair',25.25,26,'Barnardos Buddies'),
 ('jump-spread',26,26.75,'Jump Rope'),('walk-phones',26.75,27.5,'Walk Your Way'),
 ('creator-triptych',27.5,28.25,'Built for Feed'),('flex-motion-return',28.25,29.25,'That’s A Flex'),
 ('money-pair',29.25,30,'Money Your Way')]
# Full source images are fitted into explicit boxes; no universal centre-crop.
def place(c,key,box,im=None):
 x,y,w,h=box;src=im if im is not None else ims[key];s=ImageOps.contain(src,(int(w),int(h)),Image.Resampling.LANCZOS)
 c.paste(s,(int(x+(w-s.width)/2),int(y+(h-s.height)/2)))
def field(key):
 # A defocused colour field from that exact creative fills the canvas behind complete assets.
 return ImageOps.fit(ims[key],(W,H)).filter(ImageFilter.GaussianBlur(65))
def draw(kind,t):
 if kind.startswith('money'):
  c=field('money');place(c,'money',(22,42,620,636));place(c,'trust' if kind=='money-trust' else 'money2',(648,42,610,636))
 elif kind.startswith('flex-motion'):
  c=Image.new('RGB',(W,H),'#ab83f8');sec=(3.4+t if kind.endswith('return') else 3.6+t);im=flex[min(len(flex)-1,int(sec*30))]
  # Original grid complete, companion print execution complete at right.
  place(c,None,(0,0,1020,720),im);place(c,'flex2',(1030,188,240,344))
 elif kind=='flex-print':
  c=Image.new('RGB',(W,H),'#ae87f5');place(c,'flex1',(80,0,509,720));place(c,'flex2',(690,0,503,720))
 elif kind=='creator-triptych':
  c=Image.new('RGB',(W,H),'#d6d6c9');place(c,'creator',(0,0,426,720));place(c,'creator2',(427,0,426,720));place(c,'travel',(854,0,426,720))
 elif kind=='allhearts-pair':
  c=field('mugs');place(c,'mugs',(20,40,620,640));place(c,'shirt',(650,40,610,640))
 elif kind=='allhearts-product':
  c=field('tote');place(c,'tote',(50,0,720,720));place(c,'shirt',(832,10,400,345));place(c,'mugs',(832,365,400,345))
 elif kind=='barn-posters':
  c=Image.new('RGB',(W,H),'#a5cd45');place(c,'posters',(0,0,960,720));place(c,'social',(970,30,300,330));place(c,'buddies',(970,365,300,330))
 elif kind=='barn-pair':
  c=field('social');place(c,'social',(16,116,620,488));place(c,'buddies',(644,116,620,488))
 elif kind=='jump-motion':
  c=Image.new('RGB',(W,H),'#e4e7ee');im=jump[min(8,2+int(t*2))];place(c,None,(0,0,790,720),im);place(c,'spread',(790,150,480,420))
 elif kind=='jump-spread':
  c=Image.new('RGB',(W,H),'#d9dce2');place(c,'spread',(0,0,1000,720));place(c,'book',(1010,180,260,360))
 elif kind=='walk-phones':
  c=Image.new('RGB',(W,H),'#f7efe5');place(c,'phones',(0,0,1000,720));place(c,'walk',(1000,80,280,560))
 elif kind=='walk-pair':
  c=Image.new('RGB',(W,H),'#f7efe5');place(c,'walk',(0,120,640,480));place(c,'phones',(640,120,640,480))
 return c
# 900 exact frames, editorial cuts only. No title cards or voiceover.
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'jazz-farey-showreel.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for i in range(900):
 t=i/30;k,start,end,label=next(s for s in shots if s[1]<=t<s[2]);im=draw(k,t-start)
 if i<30:
  d=ImageDraw.Draw(im);d.rectangle((24,18,340,46),fill='#fafaf8');d.text((33,23),'JAZZ FAREY · SELECTED WORK',font=font,fill='#111111')
 p.stdin.write(im.tobytes())
 if i in [round(s[1]*30)+3 for s in shots]:im.save(TMP/f'qa-{i:03d}.jpg',quality=92)
p.stdin.close();assert p.wait()==0
# The poster is the same complete two-up creative, without the identification overlay.
draw('money-pair',0).save(OUT/'poster.webp',quality=91)
(ROOT/'docs/reel-timeline.json').write_text(json.dumps([{'composition':k,'start':a,'end':b,'project':n,'start_frame':round(a*30),'frames':round(b*30)-round(a*30)} for k,a,b,n in shots],indent=2))
print('Rendered 900 frames / 30 seconds')
