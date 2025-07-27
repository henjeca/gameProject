
frame = 0  

def animate(hero, sprites):
    global frame
    frame += 0.1
    if frame >= len(sprites):
        frame = 0
    hero.image = sprites[int(frame)]

def animateDirection(speed,objectActor,sprites,sprites2,):
    global frame
    frame += 0.1
    if frame >= len(sprites):
        frame = 0
    
    if speed > 0:
        objectActor.image = sprites[int(frame)]
    else:
        objectActor.image = sprites2[int(frame)]