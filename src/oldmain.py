


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib
matplotlib.__version__

def powx(lst, args):
    base = args[0]
    return [pow(base, x) for x in lst]

def poly(lst, args):
    a = args[0]
    return [ a* pow(x, 2) for x in lst]

def xpm1(lst, args):
    return [ 1.0/x for x in lst]

func = xpm1

def slope(b, cx, d):
    xl = [cx, cx+d]
    yl = func(xl, [b])
    return (yl[1] - yl[0])/(xl[1] - xl[0])

def deriv(b, d, lst):
    return  [slope(b, x, d) for x in lst]

def tan(b, cx, d, lst):
    xl = [cx, cx+d]
    yl = func(xl, [b])
    a = (yl[1] - yl[0])/(xl[1] - xl[0])
    b = yl[0] - a * xl[0]
    return  [a*x+b for x in lst]


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
t = np.arange(-5, 5, 0.01)
a0 = 1.8
x0 = 3
d0 = 0.5


s = func(t, [a0])
l, = plt.plot(t, s, lw=2, color='red')
s2 = tan(a0, x0, d0, t)
l2, = plt.plot(t, s2, lw=2, color='green')
l2.set_visible(False)
s3 = deriv(a0, d0, t)
l3, = plt.plot(t, s3, lw=2, color='blue')
l3.set_visible(False)
plt.axis([-5, 5, -10, 10])


class SliderDef:
    label = None
    valmin = None
    valmax = None
    valinit = None
    valstep = None
    def __init__(self, label, valmin, valmax, valinit = 0, valstep = None):
        self.label = label
        self.valmin = valmin
        self.valmax = valmax
        self.valinit = valinit
        self.valstep = valstep

    def getInstance(self, ax):
        return Slider(ax, self.label, self.valmin, self.valmax, valinit=self.valinit, valstep=self.valstep)

sliderDefs = []
def addSliderDef(sliderDef):
    sliderDefs.append(sliderDef)

axcolor = 'lightgoldenrodyellow'

sliders = []
def initSliders():    
    for i in range(len(sliderDefs)):
        ax = plt.axes([0.25, 0.05 * (i+1), 0.65, 0.03], facecolor=axcolor)
        sl = sliderDefs[i].getInstance(ax)
        sliders.append(sl)


# axcolor = 'lightgoldenrodyellow'
# axDelta = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
# axCurrX = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
# axBase = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)


addSliderDef(SliderDef('delta', 0.001, 2, valinit=d0))
addSliderDef(SliderDef('x', -5, 5, valstep=0.001, valinit=x0))
addSliderDef(SliderDef('Base', 0.001, 5.0, valinit=a0))

initSliders()
sDelta = sliders[0]
sCurrX = sliders[1]
sBase = sliders[2]

# sDelta = Slider(axDelta, 'delta', 0.001, 2, valinit=d0)
# sCurrX = Slider(axCurrX, 'x', -5, 5, valstep=0.001, valinit=x0)
# sBase = Slider(axBase, 'Base', 0.01, 5.0, valinit=a0)


def update(val):
    base = sBase.val
    currX = sCurrX.val
    delta = sDelta.val
    l.set_ydata(func(t, [base]))
    l2.set_ydata(tan(base, currX, delta, t))
    l3.set_ydata(deriv(base, delta, t))
    fig.canvas.draw_idle()
sCurrX.on_changed(update)
sBase.on_changed(update)
sDelta.on_changed(update)

resetax = plt.axes([0.8, 0.005, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    sCurrX.reset()
    sBase.reset()
    sDelta.reset()
button.on_clicked(reset)

rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('f', 'f+t', 'f+t+d'), active=0)


def colorfunc(label):
    if(label == 'f'):   
        l.set_visible(True)
        l2.set_visible(False)
        l3.set_visible(False)
    if(label == 'f+t'):   
        l.set_visible(True)
        l2.set_visible(True)
        l3.set_visible(False)
    if(label == 'f+t+d'):   
        l.set_visible(True)
        l2.set_visible(True)
        l3.set_visible(True)

    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

def main():
    plt.show()


if __name__ == "__main__":
    main()

