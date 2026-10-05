#!/usr/bin/env python3
"""Record actual project commands and timings into an asciicast; requires live team services."""
import os,pty,select,subprocess,json,time,struct,fcntl,termios,signal
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'video'; out.mkdir(exist_ok=True)
chapters=[
('Team and services',12,['cat team/team.env.example']),
('LAN inventory',14,['ifconfig en0 | sed -n \'1,12p\'','route -n get default']),
('Ping all three service Macs',25,['ping -c 2 -W 1000 10.7.20.249','ping -c 2 -W 1000 10.7.16.92','ping -c 2 -W 1000 10.7.22.187']),
('Private DNS names',18,['dig @10.7.23.16 app.team.test +time=2 +tries=1 +noall +answer','dig @10.7.23.16 api.team.test +time=2 +tries=1 +noall +answer','dig app.team.test +time=2 +tries=1 +noall +answer']),
('Direct backend checks',18,['curl -sS -i --connect-timeout 2 --max-time 3 http://10.7.16.92:3001/api/status','curl -sS -i --connect-timeout 2 --max-time 3 http://10.7.22.187:3002/api/status']),
('Repeated requests through nginx',18,['for i in 1 2 3; do curl -sS -i --connect-timeout 2 --max-time 3 https://app.team.test/api/status; done']),
('TLS with certificate verification',17,['curl -v --connect-timeout 3 --max-time 5 https://app.team.test/api/status']),
('Cache headers and conditional response',18,['curl -sS -I --connect-timeout 2 --max-time 3 https://app.team.test/api/cache','curl -sS -i --connect-timeout 2 --max-time 3 -H \'If-None-Match: "cn-cache-v1"\' https://app.team.test/api/cache']),
('Failure probes: resolver and port',22,['dig @8.8.8.8 app.team.test +time=2 +tries=1 +noall +comments +answer','curl -v --connect-timeout 2 --max-time 3 https://app.team.test:65534/api/status','curl -sS -I --connect-timeout 2 --max-time 3 https://app.team.test/api/status']),
('Compare with the earlier successful TLS capture',23,["sed -n '/SSL certificate verify ok/,+25p' evidence/phase1/last-capture-requests-2026-10-05.md | head -30","/Applications/Wireshark.app/Contents/MacOS/tshark -r evidence/phase1/phase1-final-flow.pcapng -Y 'tcp.stream == 0 && (tcp.flags.syn == 1 || tls)' -T fields -e frame.number -e _ws.col.Info | head -12"]),
]
# 185-second real pseudo-terminal session. Child actually executes every displayed command.
script=[]
for title,duration,cmds in chapters:
 script += ["printf '\\033[2J\\033[H'",f"printf '%s\\n' {__import__('shlex').quote('PHASE I LIVE RUN — '+title)}", "printf '%s\\n\\n' 'Aryan Kinha | fresh commands; earlier saved output is labeled separately'",'cn_start=$SECONDS']
 for command in cmds:
  script += ['printf \'$ %s\\n\' '+__import__('shlex').quote(command),command,'cn_rc=$?','printf \'[exit %s]\\n\\n\' "$cn_rc"']
 script += [f'cn_left=$(({duration} - SECONDS + cn_start)); if [ "$cn_left" -gt 0 ]; then sleep "$cn_left"; fi']
path=Path('/private/tmp/cn-terminal-live.sh'); path.write_text('\n'.join(script))
master,slave=pty.openpty(); fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',38,114,0,0))
env=os.environ.copy();env['TERM']='xterm-256color';env['COLUMNS']='114';env['LINES']='38'
child=subprocess.Popen(['/bin/bash',str(path)],stdin=slave,stdout=slave,stderr=slave,cwd=root,env=env,start_new_session=True);os.close(slave)
started=time.monotonic(); events=[]
with (out/'phase1-live-terminal.cast').open('w') as f:
 f.write(json.dumps({'version':2,'width':114,'height':38,'timestamp':int(time.time()),'title':'Phase I actual command session','env':{'TERM':'xterm-256color'}})+'\n');f.flush()
 while True:
  ready,_,_=select.select([master],[],[],.2)
  if ready:
   try: b=os.read(master,65536)
   except OSError: break
   if not b:break
   event=[round(time.monotonic()-started,3),'o',b.decode(errors='replace')];events.append(event);f.write(json.dumps(event)+'\n');f.flush()
  if child.poll() is not None and not ready:break
os.close(master);child.wait();duration=time.monotonic()-started
(out/'phase1-live-terminal-timing.json').write_text(json.dumps({'duration':duration,'chapters':[{'title':a,'duration':b,'commands':c} for a,b,c in chapters]},indent=2))
(out/'phase1-live-command-output.txt').write_text(''.join(e[2] for e in events).replace('\x1b[2J\x1b[H','\n\n'))
print('Recorded actual terminal duration:',duration,flush=True)
