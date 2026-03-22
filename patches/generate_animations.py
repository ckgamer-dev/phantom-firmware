from PIL import Image, ImageDraw
import os, math

def ghost(img, cx, ty, size=36, fg=0, bg=1, blink=False, wink=False):
    d = ImageDraw.Draw(img)
    hw = size//2
    d.ellipse([cx-hw,ty,cx+hw,ty+size], fill=fg)
    d.rectangle([cx-hw,ty+size//2,cx+hw,ty+size//2+size//2], fill=fg)
    bw=size//5; by=ty+size+size//2-size//4
    for i in range(5):
        x0=cx-hw+i*bw
        d.ellipse([x0,by-bw//2,x0+bw,by+bw//2], fill=bg if i%2==0 else fg)
    ew=max(size//9,2); ey=ty+size//3
    if blink:
        d.line([cx-hw//2-ew,ey,cx-hw//2+ew,ey],fill=bg)
        d.line([cx+hw//2-ew,ey,cx+hw//2+ew,ey],fill=bg)
    else:
        d.ellipse([cx-hw//2-ew,ey-ew,cx-hw//2+ew,ey+ew],fill=bg)
        if not wink: d.ellipse([cx+hw//2-ew,ey-ew,cx+hw//2+ew,ey+ew],fill=bg)

def tc(img,y,text,fg=0):
    d=ImageDraw.Draw(img); w=len(text)*6
    d.text(((128-w)//2,y),text,fill=fg)

def save_anim(folder,fn,n,fps=4):
    os.makedirs(folder,exist_ok=True)
    for i in range(n):
        img=Image.new("1",(128,64),1); fn(img,i,n)
        img.save(f"{folder}/frame_{i}.png")
    with open(f"{folder}/meta.txt","w") as f:
        f.write(f"Filetype: Flipper Animation\nVersion: 1\n\n"
                f"Width: 128\nHeight: 64\nPassive frames: {n}\nActive frames: 0\n"
                f"Frames order: {' '.join(str(x) for x in range(n))}\n"
                f"Active cycles: 0\nFrame rate: {fps}\nDuration: 3600\n"
                f"Active cooldown: 0\n\nBubble slots: 0\n")

BASE="assets/dolphin/external"

# Boot Splash
FS="assets/slideshow/first_start"
os.makedirs(FS,exist_ok=True)
img=Image.new("1",(128,64),1); ImageDraw.Draw(img).ellipse([62,30,66,34],fill=0); img.save(f"{FS}/frame_00.png")
img=Image.new("1",(128,64),1); d=ImageDraw.Draw(img); d.ellipse([46,8,82,44],outline=0); d.rectangle([46,26,82,48],outline=0); img.save(f"{FS}/frame_01.png")
img=Image.new("1",(128,64),1); ghost(img,64,8,38,0,1,blink=True); img.save(f"{FS}/frame_02.png")
img=Image.new("1",(128,64),1); ghost(img,64,8,38); tc(img,54,"PHANTOM"); img.save(f"{FS}/frame_03.png")
img=Image.new("1",(128,64),0); ghost(img,64,6,38,1,0,wink=True); tc(img,50,"PHANTOM",1); tc(img,57,"Ghost in the Machine",1); img.save(f"{FS}/frame_04.png")
img=Image.new("1",(128,64),1); d=ImageDraw.Draw(img); d.rectangle([0,0,127,63],outline=0); d.rectangle([2,2,125,61],outline=0); ghost(img,64,7,34); tc(img,48,"PHANTOM"); tc(img,56,"v0.1.0-alpha"); img.save(f"{FS}/frame_05.png")
print("Splash: 6 Boot-Frames OK")

UD="assets/slideshow/update_default"
os.makedirs(UD,exist_ok=True)
for i,(bg,fg,t1,t2) in enumerate([(1,0,"PHANTOM","Updating.."),(0,1,"PHANTOM","Updating.."),(1,0,"PHANTOM","Installing.."),(0,1,"PHANTOM","Complete!")]):
    img=Image.new("1",(128,64),bg)
    if bg==0: ImageDraw.Draw(img).rectangle([0,0,127,63],outline=1)
    ghost(img,64,4,32,fg,bg,blink=(i%2==1)); tc(img,44,t1,fg); tc(img,54,t2,fg)
    img.save(f"{UD}/frame_0{i}.png")
print("Update: 4 Frames OK")

def idle(img,i,n):
    bob=int(math.sin(i/n*2*math.pi)*3)
    ghost(img,64,8+bob,36,blink=(i in(7,8))); tc(img,55,"PHANTOM")
save_anim(f"{BASE}/L1_PHANTOM_Idle_128x64",idle,20,4)
print("Anim 1: Ghost Idle OK")

def hacker(img,i,n):
    ghost(img,26,8,26)
    d=ImageDraw.Draw(img)
    d.rectangle([56,8,118,40],outline=0); d.rectangle([57,9,117,39],fill=1)
    d.rectangle([58,41,120,50],outline=0)
    for kx in range(61,117,8): d.rectangle([kx,42,kx+5,49],outline=0)
    lines=["PHANTOM v0.1","SubGHz scan..","NFC read OK","IR fuzz 0xFF"]
    li=min(i//4,3); ci=(i%4+1)*4
    for l in range(li+1):
        t=lines[l]
        if l==li: t=t[:ci]
        d.text((59,11+l*7),t[:18],fill=0)
    if i%2==0:
        cx2=59+len(lines[min(li,3)][:ci])*6
        d.rectangle([cx2,11+min(li,3)*7,cx2+2,17+min(li,3)*7],fill=0)
save_anim(f"{BASE}/L2_PHANTOM_Hacker_128x64",hacker,16,3)
print("Anim 2: Ghost Hacker OK")

def rf(img,i,n):
    ghost(img,26,10,28)
    d=ImageDraw.Draw(img); ph=i%6
    for w in range(3):
        r=(ph+w*6)%18*3+6
        if r<48: d.arc([44,22-r//3,44+r,22+r//3],-60,60,fill=0)
    d.text((70,16),"Sub-GHz",fill=0); d.text((70,26),"433.92 MHz",fill=0)
    d.text((70,38),f"RSSI:-{55+i%8}dBm",fill=0)
save_anim(f"{BASE}/L1_PHANTOM_RF_128x64",rf,18,4)
print("Anim 3: Ghost RF OK")

def reveal(img,i,n):
    d=ImageDraw.Draw(img)
    if i<6:
        sz=int(8+(i/6)*32); ghost(img,64,32-sz//2,sz,blink=(i%2==0))
    elif i<12:
        ghost(img,64,16,32)
        for sy in range(0,(i-6)*9,4):
            for sx in range(0,128,3): d.point((sx,sy),fill=0)
    elif i<18:
        ghost(img,48,12,30); chars=(i-12)*2
        d.text((84,18),"PHANTOM"[:chars],fill=0)
        if i>=15: d.text((84,28),"Ghost in"[:chars-4],fill=0)
        if i>=17: d.text((84,40),"the Machine",fill=0)
    else:
        ghost(img,48,12,30,blink=(i%2==1))
        d.text((84,18),"PHANTOM",fill=0); d.text((84,28),"Ghost in",fill=0)
        d.text((84,40),"the Machine",fill=0); d.text((84,52),"v0.1.0",fill=0)
save_anim(f"{BASE}/L3_PHANTOM_Ghost_128x64",reveal,24,3)
print("Anim 4: Ghost Reveal OK")

def nfc(img,i,n):
    ghost(img,24,10,26)
    d=ImageDraw.Draw(img)
    d.rectangle([60,14,118,42],outline=0); d.rectangle([61,15,117,41],fill=1)
    cx5,cy5=89,28
    for r in range(1,4): d.rectangle([cx5-r*5,cy5-r*3,cx5+r*5,cy5+r*3],outline=0)
    sx=62+(i*4%54); d.line([sx,15,sx,41],fill=0)
    sts=["Scanning..","MIFARE 1K","UID:A2B3C4","Reading..","Key A: OK","Saved! OK"]
    d.text((60,45),sts[min(i//2,len(sts)-1)],fill=0)
save_anim(f"{BASE}/L2_PHANTOM_NFC_128x64",nfc,14,3)
print("Anim 5: Ghost NFC OK")

MANIFEST="""Filetype: Flipper Animation Manifest\nVersion: 1\n\nName: L1_PHANTOM_Idle_128x64\nMin butthurt: 0\nMax butthurt: 14\nMin level: 1\nMax level: 3\nWeight: 10\n\nName: L2_PHANTOM_Hacker_128x64\nMin butthurt: 0\nMax butthurt: 14\nMin level: 1\nMax level: 3\nWeight: 10\n\nName: L1_PHANTOM_RF_128x64\nMin butthurt: 0\nMax butthurt: 14\nMin level: 1\nMax level: 3\nWeight: 8\n\nName: L3_PHANTOM_Ghost_128x64\nMin butthurt: 0\nMax butthurt: 14\nMin level: 1\nMax level: 3\nWeight: 8\n\nName: L2_PHANTOM_NFC_128x64\nMin butthurt: 0\nMax butthurt: 14\nMin level: 1\nMax level: 3\nWeight: 8\n\n"""
with open(f"{BASE}/manifest.txt","r") as f: old=f.read()
with open(f"{BASE}/manifest.txt","w") as f:
    f.write(MANIFEST.replace("\\n","\n") + old.replace("Filetype: Flipper Animation Manifest\nVersion: 1\n\n",""))
print("Manifest updated OK")
