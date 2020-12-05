import flopy
import matplotlib.pyplot as plt
import numpy as np
import glob
import io
import os
import base64
import shutil
from shutil import copy


def numerical_model(Lx, Ly, ncol, nrow, prsity, al, av, Gamma, Cd, Ca, h1, h2, hk, id, path):
    os.mkdir(path)
    os.chdir(path)
    # Domain

    Lx = Lx
    Ly = Ly
    ztop = 0
    zbot = -1
    ncol = ncol
    nrow = nrow
    nlay = 1
    delx = Lx / ncol
    dely = Ly / nrow
    delv = (ztop - zbot) / nlay

    # Parameter

    prsity = prsity
    al = al
    av = av
    Gamma = Gamma
    Cd = Cd
    Ca = Ca
    h1 = h1
    h2 = h2
    hk = hk
    perlen = 6000
    # Exe
    # Replace this path with your path
    exe_name_mf = copy('/home/vedaanti/Water/mf2005', path)
    exe_name_mt = copy('/home/vedaanti/Water/mt3dms', path)

    # Flow Calculation
    t0_mf = 'T02_mf' + id
    mf = flopy.modflow.Modflow(modelname=t0_mf, exe_name=exe_name_mf)
    dis = flopy.modflow.ModflowDis(mf, nlay=nlay, nrow=nrow, ncol=ncol, delr=delx, delc=dely, top=0, botm=[0 - delv],
                                   perlen=perlen)

    ibound = np.ones((nlay, nrow, ncol), dtype=np.int32)
    ibound[:, :, 0] = -1
    ibound[:, :, -1] = -1
    strt = np.ones((nlay, nrow, ncol), dtype=np.float32)
    strt[:, :, 0] = h1
    strt[:, :, -1] = h2

    bas = flopy.modflow.ModflowBas(mf, ibound=ibound, strt=strt)
    lpf = flopy.modflow.ModflowLpf(mf, hk=hk, laytyp=0)
    gmg = flopy.modflow.ModflowGmg(mf)
    lmt = flopy.modflow.ModflowLmt(mf)

    mf.write_input()
    mf.run_model(silent=True)

    # Transport Calculation
    t0_mt = 'T02_mt' + id
    mt = flopy.mt3d.Mt3dms(
        modelname=t0_mt, exe_name=exe_name_mt, modflowmodel=mf)

    icbund = np.ones((nlay, nrow, ncol), dtype=np.int32)
    icbund[:, 0, :] = -1  # first row
    icbund[:, :, 0] = -1  # first column
    icbund[:, :, -1] = -1  # last column

    sconc = np.zeros((nlay, nrow, ncol), dtype=np.float32)
    sconc[:, 0, :] = Ca
    sconc[:, :, 0] = (Gamma * Cd) + (2 * Ca)
    sconc[:, :, -1] = Ca

    btn = flopy.mt3d.Mt3dBtn(mt, icbund=icbund, prsity=prsity, sconc=sconc)
    adv = flopy.mt3d.Mt3dAdv(mt, mixelm=-1)
    dsp = flopy.mt3d.Mt3dDsp(mt, al=al, trpt=av / al)
    gcg = flopy.mt3d.Mt3dGcg(mt)
    ssm = flopy.mt3d.Mt3dSsm(mt)

    mt.write_input()
    mt.run_model(silent=True)

    ucnobj = flopy.utils.UcnFile('MT3D001.UCN')
    conc = ucnobj.get_alldata()
    mvt = mt.load_mas('MT3D001.MAS')

    C0 = 2 * Ca
    plt.figure(figsize=(11, 5))
    ax = plt.axes()
    mm = flopy.plot.map.PlotMapView(ax=ax, model=mf)
    mm.plot_grid(color='.5', alpha=0.2)
    conc = conc[0, 0, :]
    cs = mm.contour_array(conc, levels=[C0], colors=['k'])
    mm.plot_ibound()
    # plt.clabel(cs)
    plt.xlabel('Distance Lx [m]')
    plt.ylabel('Aquifer Thickness [m]')
    plt.title('Contaminant Plume')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    # Plume length
    p1 = cs.collections[0].get_paths()[0]
    coor_p1 = p1.vertices
    plume_length = np.max(coor_p1[:, 0])

    # clear up all memory
    ucnobj.close()
   # for filename in glob.glob('/home/vedaanti/Water/'+t0_mt+'*'):
    #   os.remove(filename)
   # for filename in glob.glob('/home/vedaanti/Water/'+t0_mf+'*'):
    #    os.remove(filename)
  # os.remove('/home/vedaanti/Water/MT3D.CNF')
  # os.remove('/home/vedaanti/Water/mt3d_link.ftl')
    os.chdir("..")
    return plume_length, '<img src="data:image/png;base64,{}">'.format(plot_url)
