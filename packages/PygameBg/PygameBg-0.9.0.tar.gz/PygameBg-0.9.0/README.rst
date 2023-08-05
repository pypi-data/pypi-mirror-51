PygameBg - Pygame Toolbox for Begginers by Petlja
=================================================

PygameBg is a small Python package aimed to reduces boilerplate code in simple Pygame programs, primarily initialization code and main loop.

PygamePg shoud make early Pygame learning curve more gradual for those without programming experience, but without losing focus from the pure Pygame API. 

When we comare Python with C-like programming languages, one of the positive features we usualy mention is a single line "Hellow World!" example::

    print('Hellow World!')

Pygame is not pythonish enough here. A proper "Draw circle" programm looks like::

    import pygame as pg

    pg.init()
    surface = pg.display.set_mode((400,400))
    pg.display.set_caption("Blue circle")

    pg.draw.circle(surface, pg.Color("blue"), (200,200), 100)

    pg.display.update()
    while pg.event.wait().type != pg.QUIT:
        pass
    pg.quit()


The central line of code in this example we would like to be focused on is::

    pg.draw.circle(surface, pg.Color("blue"), (200,200),100)

We could say that first three lines (excuding ``import``) opens a window, and last four lines waits for user to quit, but we would not like to bore with detais of those boilerplate lines.

Here is an equivalent example that use PatljaBg::

    import pygame as pg
    import pygamebg

    surface = pygamebg.open_window(400, 400, "Blue circle")

    pg.draw.circle(surface, pg.Color("blue"), (200,200), 100)

    pygamebg.wait_loop()

This is much more readable first example for begginers and easier to explain: We open window, then draw blue circe and wait for user to quit.

Beside ``wait_loop``, PygameBg supports ``frame_loop`` and ``event_loop``.

Here is example that use ``frame_loop``::

    import pygame as pg
    import pygamebg

    surface = pygamebg.open_window(300, 300, "Read keyboard state")

    x, y = 150, 150

    def update():
        global x, y
        surface.fill(pg.Color("white"))
        pressed = pg.key.get_pressed()
        if pressed[pg.K_RIGHT]:
            x += 1
        if pressed[pg.K_LEFT]:
            x -= 1
        if pressed[pg.K_DOWN]:
            y += 1
        if pressed[pg.K_UP]:
            y -= 1
        pg.draw.circle(surface , pg.Color("red"), (x, y), 30)

    pygamebg.frame_loop(30, update)

Frame loop calls ``update`` function once per frame and may optionaly call an event handler function::

    import pygame as pg
    import pygamebg

    width, height = 500, 300
    surface = pygamebg.open_window(width, width, "Increasing and decreasing speed")
    pg.key.set_repeat(10,10)

    fps = 30
    x, y = 150, 150
    vx, vy = 0, 0

    def update():
        global x,y
        x = (x + vx/fps) % width
        y = (y + vy/fps) % height

        surface.fill(pg.Color("white"))
        color = pg.Color("red")
        pg.draw.circle(surface, color, (int(x), int(y)), 30)

    def handle_event(d):
        global vx, vy
        if d.type == pg.KEYDOWN:
            if d.key == pg.K_RIGHT:
                vx += 1
            elif d.key == pg.K_LEFT:
                vx -= 1
            elif d.key == pg.K_DOWN:
                vy += 1
            elif d.key == pg.K_UP:
                vy -= 1

    pygamebg.frame_loop(fps, update, handle_event)

We can also use a dictionary agrument to specify event handlers for specific event types::

    def keydown(d):
        global vx, vy
        if d.key == pg.K_RIGHT:
            vx += 1
        elif d.key == pg.K_LEFT:
            vx -= 1
        elif d.key == pg.K_DOWN:
            vy += 1
        elif d.key == pg.K_UP:
            vy -= 1

    pygamebg.frame_loop(fps, update, {pg.KEYDOWN: keydown})

Frame loop can handle events, but it is allways frame driven: it updates on each frame and handles pending events before each update.

A pure event loop handles events immediately when they occurred and triggers repaint when needed (when an event handler returns ``True``)::

    import pygame as pg
    import pygamebg

    surface = pygamebg.open_window(500, 500, "Keboard and mouse events")
    pg.key.set_repeat(10,10)

    x, y = 150, 150

    def handle_event(d):
        global x, y
        if d.type == pg.MOUSEBUTTONDOWN:
            x,y = d.pos
            return True
        if d.type == pg.KEYDOWN:
            if d.key == pg.K_RIGHT:
                x += 1
            elif d.key == pg.K_LEFT:
                x -= 1
            elif d.key == pg.K_DOWN:
                y += 1
            elif d.key == pg.K_UP:
                y -= 1
            else:
                return False
            return True
        return False

    def paint():
        surface.fill(pg.Color("white"))
        pg.draw.circle(surface, pg.Color("blue"), (x, y), 50)

    pygamebg.event_loop(paint, handle_event)


A dictionary argument can also be used to specify event handlers for specific event types::

    import pygame as pg
    import pygamebg

    surface = pygamebg.open_window(500, 500, "Keyboard and mouse")
    pg.key.set_repeat(10,10)

    x, y = 150, 150

    def clicked(d):
        global x, y
        x,y = d.pos
        return True

    def keypressed(d):
        global x,y
        if d.key == pg.K_RIGHT:
            x += 1
        elif d.key == pg.K_LEFT:
            x -= 1
        elif d.key == pg.K_DOWN:
            y += 1
        elif d.key == pg.K_UP:
            y -= 1
        else:
            return False
        return True

    def paint():
        surface.fill(pg.Color("white"))
        pg.draw.circle(surface, pg.Color("blue"), (x, y), 50)

    pygamebg.event_loop(paint, {pg.MOUSEBUTTONDOWN:clicked, pg.KEYDOWN:keypressed})

Source files of all examples are avaiable `here 
<https://github.com/Petlja/PygameBg/tree/master/examples>`_.
