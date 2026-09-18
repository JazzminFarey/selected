from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import subprocess,json,concurrent.futures
import os
ROOT=Path(__file__).resolve().parents[2]
S=Path(os.environ.get('REEL_SOURCES','/tmp/reel-source'));E=Path(os.environ.get('REEL_EDIT','/tmp/reel-edit-v2'));O=ROOT/'Assets';W,H=1280,720
E.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def img(n):return Image.open(S/n).convert('RGB')
def frame(names,name,mode='fill',label=None):
 canvas=Image.new('RGB',(W,H),'#fafaf8'); n=len(names)
 for i,src in enumerate(names):
  im=img(src);box=(W//n,H)
  if mode=='fit':
   im=ImageOps.contain(im,box); canvas.paste(im,(i*(W//n)+(box[0]-im.width)//2,(H-im.height)//2))
  else:canvas.paste(ImageOps.fit(im,box,centering=(.5,.45)),(i*(W//n),0))
 if label:
  d=ImageDraw.Draw(canvas);f=ImageFont.truetype(font,20);b=d.textbbox((0,0),label,font=f);d.rectangle((24,24,b[2]+48,64),fill='#0a0a0a');d.text((36,32),label,font=f,fill='white')
 p=E/(name+'.jpg');canvas.save(p,quality=94);return p

def card(name,lines):
 im=Image.new('RGB',(W,H),'#111111');d=ImageDraw.Draw(im)
 for txt,y,size in lines:
  f=ImageFont.truetype(bold if size>40 else font,size);d.text((64,y),txt,font=f,fill='#fafaf8')
 p=E/(name+'.jpg');im.save(p,quality=95);return p
shots=[]
def still(p,duration):shots.append({'source':str(p),'duration':duration,'type':'still'})
def motion(p,duration,start=0):shots.append({'source':str(p),'duration':duration,'type':'motion','start':start})
still(card('intro',[('JAZZ FAREY',260,100),('BRAND + CREATIVE',410,26)]),2)
still(frame(['money-hero.png','money-1.png'],'money-a','fill','ZIP'),1)
still(frame(['money-2.png','money-hero.png'],'money-b','fill'),1)
motion(S/'flex.mp4',1.5,0);motion(S/'flex.mp4',1.5,5)
still(frame(['feed-1.jpg','money-hero.png'],'social','fit'),1)
for i,n in enumerate(['allheartsecommerce-1.jpg','allheartsecommerce-0.jpg','allheartsecommerce-2.jpg']):still(frame([n],f'all-{i}',label='allHearts' if i==0 else None),1)
still(frame(['allheartsecommerce-0.jpg','allheartsecommerce-2.jpg'],'all-3'),1)
for i,n in enumerate(['barnardosbuddies-0.jpg','home-2.jpg','barnardosbuddies-1.jpg','barnardosbuddies-2.jpg']):still(frame([n],f'barn-{i}','fit' if i==0 else 'fill',label='Barnardos Buddies' if i==0 else None),1)
motion(S/'death-by-xoko-65a7m-0.gif',1.5,.5)
still(frame(['home-3.jpg'],'jump-1',label='Jump Rope for Heart'),.75)
still(frame(['death-by-xoko-65a7m-2.jpg'],'jump-2'),.75)
still(frame(['home-0.jpg'],'walk-0',label='Walk Your Way'),1)
still(frame(['walkyourway-1.jpg'],'walk-1','fill'),1.5)
still(frame(['home-0.jpg'],'walk-2'),.75)
still(frame(['walkyourway-1.jpg'],'walk-3'),.75)
still(frame(['home-4.jpg'],'give-0','fit','Give with Heart Day'),1)
still(frame(['integratedcampaigns-2.jpg'],'give-1'),1)
still(frame(['home-5.jpg'],'give-2',label='Heart Foundation / PR'),1)
still(frame(['home-4.jpg','home-6.jpg'],'give-3','fit'),1)
still(card('end',[('IDEAS.',170,80),('SYSTEMS.',270,80),('ECONOMICS.',370,80),('JAZZ FAREY',565,28)]),3)
assert sum(s['duration'] for s in shots)==30
elapsed=0
for shot in shots:
 shot['start_frame']=round(elapsed*30); elapsed+=shot['duration']; shot['frames']=round(elapsed*30)-shot['start_frame']

def render(pair):
 i,s=pair;dest=E/f'{i:02}.mp4';cmd=['ffmpeg','-v','error','-y']
 if s['type']=='still':cmd+=['-loop','1']
 elif s['source'].endswith('.gif'):cmd+=['-stream_loop','-1','-ss',str(s.get('start',0))]
 else:cmd+=['-ss',str(s['start'])]
 cmd+=['-i',s['source'],'-frames:v',str(s['frames']),'-an','-vf',f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0xe4e7ec,setsar=1,fps=30','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-threads','2',str(dest)]
 subprocess.run(cmd,check=True);return dest
paths=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(render,enumerate(shots)))
(E/'concat.txt').write_text('\n'.join(f"file '{p}'" for p in paths))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(E/'concat.txt'),'-c:v','libx264','-preset','slow','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(O/'reel/jazz-farey-showreel.mp4')],check=True)
# Web tiles: actual work only. No brand reconstruction.
tiles={'money-your-way':'money-hero.png','built-for-feed':'feed-1.jpg','allhearts':'allheartsecommerce-1.jpg','barnardos':'home-2.jpg','jump-rope':'home-3.jpg','walk-your-way':'home-0.jpg','give-with-heart':'home-4.jpg'}
for name,src in tiles.items():
 im=img(src);im.thumbnail((1200,1200));im.save(O/'work'/f'{name}.webp',quality=87)
Image.open(E/'money-a.jpg').save(O/'reel/poster.webp',quality=88)
Image.open(E/'social.jpg').save(O/'work/creative-system.webp',quality=87)
subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(S/'flex.mp4'),'-frames:v','1',str(O/'work/thats-a-flex.webp')],check=True)
(E/'timeline.json').write_text(json.dumps(shots,indent=2))
(ROOT/'docs/reel-timeline.json').write_text(json.dumps([{**s,'source':Path(s['source']).name} for s in shots],indent=2))
print('REEL COMPLETE', (O/'reel/jazz-farey-showreel.mp4').stat().st_size)
