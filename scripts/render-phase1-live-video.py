#!/usr/bin/env python3
"""Render a genuine timed terminal capture plus recorded Wireshark UI frames.
Requires Pillow and ffmpeg. Supply the raw UI folder as the first argument.
"""
import json,re,sys,hashlib,tempfile,subprocess,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'video';UI=Path(sys.argv[1] if len(sys.argv)>1 else '/private/tmp/cn-live-ui')
TMP=Path(tempfile.mkdtemp(prefix='cn-live-render-'));W,H=2560,1720;FPS=24
mono=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',30)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',34)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24)
cues=[
(0,12,'Actual command session: Aryan DNS, Divyanshu nginx, Jatin Verma Backend A and Jatin Kumar Singh Backend B. Commands are automated and their real outputs are recorded.'),
(12,26,'Record the active interface, private IPv4 address, subnet mask and default gateway. These commands inspect Aryan’s Mac; remote inventories still require separate evidence.'),
(26,51,'Ping each service Mac to distinguish basic IP reachability from service availability. All three hosts responded in this recording; one edge response arrived outside the requested wait time.'),
(51,69,'Both private names resolve to the edge, 10.7.20.249, with TTL 30. A normal lookup also succeeds. DNS finds an address; it does not establish the later TCP connection.'),
(69,87,'Direct backend checks use known LAN ports. Backend A returned 200 in this run; Backend B timed out. These are actual current outputs, not the earlier healthy baseline.'),
(87,105,'Repeated domain requests test nginx distribution. The edge timed out in this fresh run, so these commands cannot currently demonstrate successful A/B balancing.'),
(105,122,'Verbose HTTPS keeps hostname and certificate checks enabled. This attempt times out before TLS, which means it does not provide a new certificate-validation result.'),
(122,140,'Check Cache-Control and conditional If-None-Match behavior. These live edge requests timed out. The earlier successful cache and 304 outputs remain in the evidence folder.'),
(140,162,'The public resolver returns NXDOMAIN for the private name. The wrong port and correct port both time out now; this is not a clean wrong-port recovery demonstration.'),
(162,185,'We now explicitly read the earlier successful TLS log and packet capture from 02:53 on 5 October. This is saved evidence, not a successful request from the current run.'),
(185,197,'In the real Wireshark window, the earlier capture shows a DNS query and its matching response. The answer contains the edge IP; local DNS runs on the same Mac as this client.'),
(197,210,'Selecting the response and expanding its details exposes the DNS transaction and UDP ports. Wireshark is being navigated, rather than shown as a presentation slide.'),
(210,223,'This edge TCP stream starts with SYN from client port 54008 to server port 443. The full capture’s frame 2 appears as frame 1 in this read-filtered view.'),
(223,236,'Select SYN-ACK from the edge, followed by the client ACK. Relative sequence and acknowledgement numbers become one. These three packets establish the connection before TLS.'),
(236,250,'The socket pair is 10.7.23.16:54008 to 10.7.20.249:443. ACKs, receive windows and retransmission support reliable delivery; the packet list preserves the actual recorded events.'),
(250,261,'Select ClientHello, then the server’s full TLS 1.2 handshake. The packet list identifies ServerHello, Certificate, ServerKeyExchange and ServerHelloDone.'),
(261,275,'Expand and scroll the selected packet details. A full TLS 1.2 capture can show its certificate; TLS 1.3 encrypts the certificate after ServerHello.'),
(275,288,'The client and server ChangeCipherSpec records are followed by encrypted handshake records. TLS protects the client-to-edge connection; the nginx-to-backend links use HTTP.'),
(288,300,'Application Data is encrypted, so inspect HTTP headers with curl. Controlled wrong-record and backend-stop failures remain unrecorded; today’s timeouts do not prove those deliberate tests.'),
]
def subtitle(im,text):
 d=ImageDraw.Draw(im);d.rectangle((0,1578,W,H),fill='#05090f');rows=[];line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if d.textlength(test,font=font)>2440 and line:rows.append(line);line=word
  else:line=test
 if line:rows.append(line)
 if len(rows)>3:raise ValueError('Subtitle overflow')
 for n,row in enumerate(rows):d.text(((W-d.textlength(row,font=font))/2,1590+n*40),row,font=font,fill='white')
 return im
def caption(t): return next((s for a,b,s in cues if a<=t<b),cues[-1][2])
parts=[];counter=0;dedup={}
def save(im,duration):
 global counter
 raw=im.tobytes();key=hashlib.sha256(raw).digest()
 if key not in dedup:
  f=TMP/f'f-{counter:05}.png';counter+=1;im.save(f,compress_level=1);dedup[key]=f
 else:f=dedup[key]
 parts.extend([f"file '{f}'",f'duration {duration:.6f}'])
# Replay actual .cast data through the terminal grid. No command output is invented.
cast=[json.loads(x) for x in (OUT/'phase1-live-terminal.cast').read_text().splitlines()]
events=cast[1:];grid=[[' ']*114 for _ in range(38)];row=col=0
ansi=re.compile(r'\x1b\[([0-9;?]*)([A-Za-z])')
def consume(s):
 global grid,row,col
 i=0
 while i<len(s):
  if s[i]=='\x1b':
   m=ansi.match(s,i)
   if m:
    if m[2]=='J' and m[1]=='2':grid=[[' ']*114 for _ in range(38)]
    elif m[2] in ('H','f'):row=col=0
    i=m.end();continue
  c=s[i];i+=1
  if c=='\r':col=0
  elif c=='\n':row+=1
  elif c=='\t':col=min(113,(col//8+1)*8)
  elif c=='\b':col=max(0,col-1)
  elif ord(c)>=32:
   if col>=114:col=0;row+=1
   if row>=38:grid.pop(0);grid.append([' ']*114);row=37
   grid[row][col]=c;col+=1
  if row>=38:grid.pop(0);grid.append([' ']*114);row=37
marks=sorted(set([0.,185.]+[float(e[0]) for e in events if e[0]<185]+[a for a,b,s in cues if a<185]))
ei=0
for a,b in zip(marks,marks[1:]):
 while ei<len(events) and events[ei][0]<=a:consume(events[ei][2]);ei+=1
 im=Image.new('RGB',(W,H),'#0b0e13');d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,46),fill='#1d2530');d.text((28,10),'Actual terminal recording playback • fresh project checks • 5 October 2026',font=small,fill='#c6d5e6')
 for n,line in enumerate(grid):
  value=''.join(line).rstrip();d.text((35,60+n*39),value,font=mono,fill='#8de2ae' if value.startswith('$') else '#edf1f5')
 save(subtitle(im,caption(a)),b-a)
# DNS UI clip comes from actual window captures; remove setup gap/failed initial frame.
dns=json.loads((UI/'frames.json').read_text())[1:]
live=json.loads((UI/'live-frames.json').read_text())
# Frames 0–83 belong to DNS before a recoverable capture error; frames 84–326 show the TCP handshake.
groups=[(dns[::2],185,25),(live[84:327:2],210,40),(live[327::2],250,50)]
for frames,start,target in groups:
 weights=[min(max(frames[i+1]['time']-f['time'],.02),.35) if i+1<len(frames) else .1 for i,f in enumerate(frames)]
 total=sum(weights);scale=target/total;elapsed=0
 for f,weight in zip(frames,weights):
  length=weight*scale;im=Image.new('RGB',(W,H),'#10151d');asset=Image.open(f['file']).convert('RGB');asset=ImageOps.contain(asset,(W,1578));im.paste(asset,((W-asset.width)//2,(1578-asset.height)//2))
  save(subtitle(im,caption(start+elapsed)),length);elapsed+=length
# Concatenated images form a true recording playback; no presentation cards are used.
parts.append(parts[-2]);(TMP/'frames.txt').write_text('\n'.join(parts))
print('Encoding 5:00 actual-command and Wireshark recording...',flush=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','concat','-safe','0','-i',str(TMP/'frames.txt'),'-t','300','-vf','fps=24','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(OUT/'phase1-live-demo.mp4')],check=True)
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
(OUT/'phase1-live-subtitles.srt').write_text('\n\n'.join(f'{n}\n{stamp(a)} --> {stamp(b)}\n{s}' for n,(a,b,s) in enumerate(cues,1)))
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(OUT/'phase1-live-demo.mp4')]))
assert float(meta['format']['duration'])==300
assert not any(s['codec_type']=='audio' for s in meta['streams'])
print('Verified: 300 seconds; no audio. Temporary QA images:',TMP,flush=True)
