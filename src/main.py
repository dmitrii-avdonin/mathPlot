
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from math import sin, sqrt, fabs, exp
import matplotlib
matplotlib.__version__



class BaseChart:
    delta = 0.01
    def __init__(self, funcDef):
        defaultSliders = 1 # tangentPointSlider
        self.funcDef = funcDef
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.08 + 0.05 * (self.funcDef.slidersCount + defaultSliders) , right=0.9, top=0.95)
        self.funcDef.init()
        self.funcDef.setAxis()

        tanPointX = (self.funcDef.xMax + self.funcDef.xMin)/2
        self.tangDef = FunctionDef(self.tan, [tanPointX], color='blue')
        self.tangDef.addSliderDef(SliderDef('TanPoint', self.funcDef.xMin, self.funcDef.xMax))
        self.tangDef.init()
        self.funcDef.setOnChangeCallback(self.tangDef.onChange)

        addedSliders = 0
        addedSliders = self.tangDef.initSliders(addedSliders)
        addedSliders = self.funcDef.initSliders(addedSliders)

    def show(self):
        plt.show()


    def slope(self, x):
        xl = [x, x + self.delta]
        yl = self.funcDef.func(xl, self.funcDef.defaultParams)
        dx = (xl[1] - xl[0]) if (xl[1] - xl[0])>0 else None
        dy = (yl[1] - yl[0])
        return (dy/dx)


    def deriv(self, lst, params=None):
        return  [slope(x) for x in lst]


    def tan(self, lst, params):
        cx = params[0]
        xl = [cx, cx + self.delta]
        yl = self.funcDef.func(xl, self.funcDef.defaultParams)
        a = self.slope(cx)
        b = (yl[0] - a * xl[0]) if a != None else None
        return  [a*x+b for x in lst]



class FunctionDef:
    axcolor = 'lightgoldenrodyellow'
    

    def __init__(self, func, defaultParams, xRangeBounds = (-5, 5), xStep = 0.01, color='red'):
        self.func = func
        self.defaultParams = defaultParams
        if type(defaultParams) != list:
            raise Exception("defaultParams expected to be a list")
        self.xMin, self.xMax = xRangeBounds
        self.xStep = xStep
        self.color = color
        self
        self.xRange = np.arange(self.xMin, self.xMax, self.xStep)        
        self.yRange = self.func(self.xRange, defaultParams)
        self.onChangeCallback = None
        self.slidersCount = 0
        self.sliderDefs = []
        self.sliders = []        

    def setOnChangeCallback(self, value):
        self.onChangeCallback = value

    def init(self):        
        self.funcPlt, = plt.plot(self.xRange, self.yRange, lw=2, color=self.color)

    def setAxis(self):
        plt.axis([self.xMin-1, self.xMax+1, min(self.yRange)-1, max(self.yRange)+1])

    def addSliderDef(self, sliderDef):
        self.sliderDefs.append(sliderDef)
        self.slidersCount += 1

    def initSliders(self, existingSlidersCount):    
        for i in range(len(self.sliderDefs)):
            if(i<len(self.defaultParams)):
                self.sliderDefs[i].valinit = self.defaultParams[i]
            ax = plt.axes([0.25, 0.02 + 0.05 * (existingSlidersCount + i), 0.65, 0.03], facecolor=self.axcolor)
            sl = self.sliderDefs[i].getInstance(ax)
            sl.on_changed(self.onChange)
            self.sliders.append(sl)
        return existingSlidersCount + len(self.sliderDefs)

    def onChange(self, val_unused=None):
        for i in range(len(self.sliders)):
            if(i<len(self.defaultParams)):
                self.defaultParams[i] = self.sliders[i].val
        
        self.yRange = self.func(self.xRange, self.defaultParams)

        self.funcPlt.set_ydata(self.yRange)

        if self.onChangeCallback != None:
            self.onChangeCallback()


class SliderDef:
    label = None
    valmin = None
    valmax = None
    valinit = None
    valstep = None
    def __init__(self, label, valmin, valmax, valstep = None):
        self.label = label
        self.valmin = valmin
        self.valmax = valmax
        self.valinit = 0
        self.valstep = valstep

    def getInstance(self, ax):
        return Slider(ax, self.label, self.valmin, self.valmax, valinit=self.valinit, valstep=self.valstep)



def powx(lst, params):
    base = params[0]
    return [pow(base, x) for x in lst ]

def poly(lst, params):
    a = params[0]
    return [ a* pow(x, 2) for x in lst ]

def sinx(lst, params):
    a = params[0]
    return [ a*sin(x) for x in lst ]

def circle(lst, params):
    r = params[0]
    return [ sqrt(r*r - x*x) for x in lst ]

def sigmoid(x):
    return 1/(1+exp(-x))

def net(lst, params):
    w1 = params[0]
    b1 = params[1]
    w2 = params[2]
    b2 = params[3]
    return [ sigmoid(w1*x+b1)  for x in lst ]

funcDef = FunctionDef(net, [1, 0, 1, 0], xRangeBounds=[-10, 10])
funcDef.addSliderDef(SliderDef('w1', -10, 10))
funcDef.addSliderDef(SliderDef('b1', -10, 10))
funcDef.addSliderDef(SliderDef('w2', -10, 10))
funcDef.addSliderDef(SliderDef('b2', -10, 10))

baseChart = BaseChart(funcDef)



def main():
    baseChart.show()


if __name__ == "__main__":
    main()