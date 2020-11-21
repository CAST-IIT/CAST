import numpy as np
import scipy as sp
from scipy import special

def bio(thresholdConcentrationCthres,time,sourceThicknessH,sourceConcentrationc0,sourceWidthW,averageLinearGroundwaterVelocityv,
longitudinalDispersivityαx,horizontalTransverseDispersivityαy,verticalTransverseDispersivityαz,effectiveDiffusionCoefficientDf,
retardationFactorR,sourceDecayCoefficientγ,effectiveFirstOrderDecayCoefficientλeff,numberOfGaussPoints):    
    thresholdConcentrationCthres = thresholdConcentrationCthres  # threshhold concentration [mg/l]       Input Box (lower limit: >0, upper limit: <Co)
    # time
    time = time  # [y]          Input Box (Default = 20, if below 15, use: (1/la)+5,  upper limit 1000)
    # Geometry - centreline
    y = 0  # [m]          fixed (no Input)
    z_1 = 0  # [m]  BOTTOM OF SOURCE LOCATED AT        fixed (no input)
    sourceThicknessH = sourceThicknessH  # [m]   TOP OF SOURCE LOCATED AT        Input slider (lower limit: >0, upper limit:50)
    # Source term
    sourceConcentrationc0 = sourceConcentrationc0  # [mg/l]  INPUT CONCENTRATION      Input slider (lower limit: >0, upper limit:1000)
    z = (z_1 + sourceThicknessH) / 2  # [m]          fixed (no Input)
    sourceWidthW = sourceWidthW  # [m]  source width        Input slider (lower limit: >0, upper limit:1000)
    # hydraulic & mixing
    averageLinearGroundwaterVelocityv = averageLinearGroundwaterVelocityv  # [m/y]  AVERAGE LINEAR GROUNDWATER VELOCITY       Input Box (lower limit: 10, upper limit: 1000 -> for very high values we have to suggest: m=20)
    longitudinalDispersivityαx  = longitudinalDispersivityαx  # [m]  LONGITUDINAL DISPERSIVITY        Input slider (lower limit: 1, upper limit: 100, default: 10)
    horizontalTransverseDispersivityαy = horizontalTransverseDispersivityαy  # [m]  HORIZONTAL TRANSVERSE DISPERSIVITY        Input Box (lower limit: 0.1, upper limit: 10, default: 0.5)
    verticalTransverseDispersivityαz = verticalTransverseDispersivityαz  # [m]  VERTICAL TRANSVERSE DISPERSIVITY        Input Box (lower limit: 0.01, upper limit: 1, default: 0.05)
    effectiveDiffusionCoefficientDf  = effectiveDiffusionCoefficientDf  # [m^2/y]   EFFECTIVE DIFFUSION COEFFICIENT    Input Box (lower limit: 0 upper limit: 0.1, default: 0)
    # reaction terms
    retardationFactorR = retardationFactorR  # [-]          Input Box (lower limit: >0, upper limit:, default: 1)
    sourceDecayCoefficientγ = sourceDecayCoefficientγ  # [1/y]        Input Box (lower limit: 0, upper limit: 1, default: 0)
    effectiveFirstOrderDecayCoefficientλeff = effectiveFirstOrderDecayCoefficientλeff # [1/y]        Input slider (lower limit: 0, upper limit: 1, default: 0.1)
    # Gauss points: max 256
    numberOfGaussPoints = numberOfGaussPoints  # [-]    NUMBER OF GAUSS POINTS      Input Box (possible values: 4,5,6,10,15,20,60,104,256; default: 60)
    Dx = longitudinalDispersivityαx * averageLinearGroundwaterVelocityv + effectiveDiffusionCoefficientDf  # [m^2/y]
    Dy = horizontalTransverseDispersivityαy * averageLinearGroundwaterVelocityv + effectiveDiffusionCoefficientDf  # [m^2/y]
    Dz = verticalTransverseDispersivityαz * averageLinearGroundwaterVelocityv + effectiveDiffusionCoefficientDf  # [m^2/y]
    # used data
    vr = averageLinearGroundwaterVelocityv / retardationFactorR  # [m/y]
    Dyr = Dy / retardationFactorR  # [m^2/y]
    Dxr = Dx / retardationFactorR  # [m^2/y]
    Dyr = Dy / retardationFactorR  # [m^2/y]
    Dzr = Dz / retardationFactorR  # [m^2/y]

    def C(x):
        # Boundary Condition
        if x <= 1e-6:
            if y <= sourceWidthW / 2 and y >= -sourceWidthW / 2 and z <= sourceThicknessH and z >= z_1:
                C = sourceConcentrationc0 * np.exp(-sourceDecayCoefficientγ * time)
            else:
                C = 0
        else:
            a = sourceConcentrationc0 * np.exp(-sourceDecayCoefficientγ * time) * x / (8 * np.sqrt(np.pi * Dxr))
            roots = sp.special.roots_legendre(numberOfGaussPoints)[0]
            weights = sp.special.roots_legendre(numberOfGaussPoints)[1]
            # scaling
            bot = 0
            top = np.sqrt(np.sqrt(time))
            Tau = (roots * (top - bot) + top + bot) / 2
            Tau4 = Tau ** 4
            # calculation
            xTerm = (np.exp(-(((effectiveFirstOrderDecayCoefficientλeff - sourceDecayCoefficientγ) * Tau4) + ((x - vr * Tau4) ** 2) / (4 * Dxr * Tau4)))) / (Tau ** 3)
            yTerm = sp.special.erfc((y - sourceWidthW / 2) / (2 * np.sqrt(Dyr * Tau4))) - sp.special.erfc((y + sourceWidthW / 2) / (2 * np.sqrt(Dyr * Tau4)))
            zTerm = sp.special.erfc((z - sourceThicknessH) / (2 * np.sqrt(Dzr * Tau4))) - sp.special.erfc((z - z_1) / (2 * np.sqrt(Dzr * Tau4)))
            Term = xTerm * yTerm * zTerm
            Integrand = Term * (weights * (top - bot) / 2)
            C = a * 4 * sum(Integrand)
        return C

    x_array = np.array([0])
    c_array = np.array([C(0)])
    x = 0
    while C(x) >= thresholdConcentrationCthres:
        x = x + 1
        x_array = np.append(x_array, x)
        c_array = np.append(c_array, C(x))
    else:
        lMax = "%.2f" % x
    return lMax

