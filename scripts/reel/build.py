"""Director edit: exact frame cuts; explicit artwork panels, no generated campaign art."""
from pathlib import Path
from PIL import Image,ImageOps,ImageSequence,ImageDraw
import subprocess,json,math
R=Path(__file__).resolve().parents[2]; A=R/'Assets'; T=R/'.recovery-qa/reel';T.mkdir(parents=True,exist_ok=True)
W,H,FPS=1280,720,30
paths={'money':'Money Your Way/Hero.png','money2':'Money Your Way/1000131099 (1).png','creator':'Feed/cover.png','creator2':'Feed/2.jpg','travel':'Feed/4.jpg','shirt':'earlier/allheartsecommerce-0.webp','mugs':'earlier/allheartsecommerce-1.webp','tote':'earlier/allheartsecommerce-2.webp','posters':'earlier/home-2.webp','social':'earlier/barnardosbuddies-1.webp','buddies':'earlier/barnardosbuddies-2.webp','book':'earlier/home-3.webp','spread':'earlier/death-by-xoko-65a7m-2.webp','walk':'earlier/home-0.webp','phones':'earlier/walkyourway-1.webp','ooh':'sources/taylor-flex-ooh.webp'}
paths.update({'money':'drive/money-0.webp','money2':'drive/money-2.webp','money-man':'drive/money-1.webp','flex-master':'drive/flex-master.webp','flex-boss':'drive/flex-boss.webp'})
ims={k:Image.open(A/p).convert('RGB') for k,p in paths.items()}
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'work/flex-campaign.mp4'),'-vf','fps=30',str(T/'flex-%03d.jpg')],check=True)
flex=[Image.open(p).convert('RGB') for p in sorted(T.glob('flex-*.jpg'))]
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'drive/money-motion.mp4'),'-vf','fps=30',str(T/'money-%03d.jpg')],check=True)
money_motion=[Image.open(p).convert('RGB') for p in sorted(T.glob('money-*.jpg'))]
gif=Image.open(A/'earlier/jump-rope.gif');jump=[];ends=[];total=0
for f in ImageSequence.Iterator(gif):
 jump.append(f.convert('RGB'));total+=f.info.get('duration',100)/1000;ends.append(total)
# Frame-exact edit: campaign motion intercut with complete source executions.
# Earlier work receives 16.3 seconds; Zip receives 13.7 seconds. No added captions.
shots=[
 ('money-motion',0,1.4,'Money Your Way'),
 ('money-single',1.4,2,'Money Your Way'),
 ('flex-open',2,3.1,'That’s A Flex'),
 ('flex-pair',3.1,3.7,'That’s A Flex'),
 ('creator',3.7,4.6,'Built for Feed'),
 ('mugs',4.6,5.6,'allHearts'),
 ('shirt',5.6,6.2,'allHearts'),
 ('tote',6.2,6.8,'allHearts'),
 ('products',6.8,8,'allHearts'),
 ('posters',8,9.3,'Barnardos Buddies'),
 ('buddies',9.3,10.2,'Barnardos Buddies'),
 ('social',10.2,11.3,'Barnardos Buddies'),
 ('jump',11.3,12.9,'Jump Rope'),
 ('book',12.9,13.5,'Jump Rope'),
 ('spread',13.5,14.3,'Jump Rope'),
 ('walk',14.3,15.5,'Walk Your Way'),
 ('walk-grid',15.5,16.5,'Walk Your Way'),
 ('money-motion-return',16.5,17.4,'Money Your Way'),
 ('flex-build',17.4,18.5,'That’s A Flex'),
 ('creator-single',18.5,19.3,'Built for Feed'),
 ('creator',19.3,20.2,'Built for Feed'),
 ('social',20.2,21.3,'Barnardos Buddies'),
 ('products',21.3,22.4,'allHearts'),
 ('jump',22.4,23.5,'Jump Rope'),
 ('walk',23.5,24.6,'Walk Your Way'),
 ('money-man',24.6,25.3,'Money Your Way'),
 ('ooh-city',25.3,26,'That’s A Flex'),
 ('money-single',26,26.7,'Money Your Way'),
 ('flex-finish',26.7,28.6,'That’s A Flex'),
 ('money-motion',28.6,30,'Money Your Way')]

def put(c,im,box):
 x,y,w,h=map(round,box);im=ims[im] if isinstance(im,str) else im;im=ImageOps.contain(im,(max(1,w),max(1,h)),Image.Resampling.LANCZOS);c.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
def full(im,bg='#eeece8',scale=1):
 c=Image.new('RGB',(W,H),bg);put(c,im,((W-W*scale)/2,(H-H*scale)/2,W*scale,H*scale));return c
# These rectangles isolate complete executions from a source montage, not arbitrary centre crops.
panels={'ooh-city':(755,10,1182,330),'ooh-retail':(22,370,446,689),'ooh-yellow':(495,370,818,689),'ooh-billboard':(846,370,1220,689)}
def draw(k,t,d):
 u=t/d;e=(1-math.cos(math.pi*u))/2
 if k in ['shirt','tote','book','spread','social']:return full(k,'#eeece8',.97+.03*e)
 if k=='walk-grid':return full('walk','#f7efe5',.97+.03*e)
 if k=='creator-single':return full('creator2','#d6d6c9')
 if k.startswith('money-motion'):
  c=Image.new('RGB',(W,H),'#b9765b');sec=(4.0 if k=='money-motion' else 6.1)+t
  im=money_motion[min(len(money_motion)-1,round(sec*30))]
  put(c,im,(0,40,640,640));put(c,'money-man' if k=='money-motion' else 'money2',(640,40,640,640));return c
 if k=='money-man':return full('money-man','#5f4739')
 if k=='flex-pair':
  c=Image.new('RGB',(W,H),'#190621');put(c,'flex-master',(80,0,510,720));put(c,'flex-boss',(690,0,510,720));return c
 if k.startswith('flex'):
  sec={'flex-open':.65,'flex-grid':1.6,'flex-build':2.0,'flex-finish':4.5}[k]+t
  f=flex[min(len(flex)-1,round(sec*30))]
  if k in ['flex-open','flex-finish']:
   return full(f.crop((10,10,665,379)),'#a883f5')
  if k=='flex-build':
   c=Image.new('RGB',(W,H),'#180521');put(c,f.crop((679,10,1072,710)),(840,0,405,720));put(c,f.crop((10,10,665,379)),(0,0,820,460));put(c,f.crop((10,389,332,710)),(90,450,255,255));put(c,f.crop((345,389,665,710)),(470,450,255,255));return c
  return full(f,'#190622')
 if k in panels:return full(ims['ooh'].crop(panels[k]),'#f4f1ec',.96+.04*e)
 if k=='ooh':return full('ooh','#fff')
 if k=='money-single':return full('money','#dc8c60',.98+.02*e)
 if k=='money-pair':
  c=Image.new('RGB',(W,H),'#ba7960');put(c,'money',(0,40-12*e,640,640));put(c,'money2',(640,40+12*e,640,640));return c
 if k=='creator':
  c=Image.new('RGB',(W,H),'#d6d6c9')
  for n,key in enumerate(['creator','creator2','travel']):put(c,key,(n*426,round(max(0,1-(t-n*.06)/.18)*90),426,720))
  return c
 if k=='mugs':return full('mugs','#ecebea',.92+.08*e)
 if k=='products':
  c=Image.new('RGB',(W,H),'#ecebea');put(c,'shirt',(0,0,640,720));put(c,'tote',(640,0,640,720));return c
 if k=='buddies':return full('buddies','#e5e6e4',.97+.03*e)
 if k=='posters':return full('posters','#a6cc48')
 if k=='jump':
  j=next((i for i,end in enumerate(ends) if (t+1)%total<end),len(jump)-1)
  return full(jump[j],'#e1e4ec')
 if k=='walk':return full('phones','#f7efe5',.95+.05*e)
 raise ValueError(k)
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(A/'reel/jazz-farey-showreel.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(900):
 t=i/30;k,a,b,proj=next(s for s in shots if round(s[1]*30)<=i<round(s[2]*30));im=draw(k,t-a,b-a);p.stdin.write(im.tobytes())
 if i in [round(a*30)+2 for _,a,_,_ in shots]:im.save(T/f'cut-{i:03}.jpg',quality=92)
p.stdin.close();assert p.wait()==0
# Creative poster, selected from actual animation; no labels or title cards.
draw('money-motion',.8,1.4).save(A/'reel/poster.webp',quality=93)
(R/'docs/reel-timeline.json').write_text(json.dumps([dict(composition=k,start=a,end=b,project=n,frames=round((b-a)*30)) for k,a,b,n in shots],indent=2))
print('900 frames / 30.000 seconds')
