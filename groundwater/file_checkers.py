import math

import pandas as pd
import matplotlib
import numpy as np
import scipy as sp
from flask import flash, redirect, request
from werkzeug.utils import secure_filename
from groundwater.liedl3D import create_liedl3DPlot

from groundwater.parameters import Parameters


def allowed_file(check_file, current_user, current_table, db):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part', category='danger')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file', category='danger')
        return redirect(request.url)
    if file and allowed_extension(file.filename):
        filename = secure_filename(file.filename)
        plume = pd.read_csv(file)
        check = check_file(plume, current_user, current_table, db)
        if check:
            flash(f'Successfully uploaded the file {filename}', category='success')
        # else:
        #     flash(f'Problem parsing the parameters.\n'
        #           f'Please check that parameter heading and values for parameters are matching'
        #           f' the permitted codes.\n'
        #           f'Kindly refer to the sample csv file for details.',
        #           category='danger')
    else:
        flash('Incorrect file type!', category='danger')
        return redirect(request.url)


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Parameters.Extensions.ALLOWED_EXTENSIONS


def convert_and_clean_inputs_database(plume, parameter_name):
    parameter = plume[parameter_name].values.tolist()
    parameter = [x for x in parameter if str(x) != 'nan']
    for idx, item in enumerate(parameter):
        if item == -1:
            parameter[idx] = None
    return parameter


def convert_and_clean_inputs(plume, parameter_name):
    parameter = plume[parameter_name].values.tolist()
    parameter = [x for x in parameter if str(x) != 'nan']
    return parameter


def check_file_for_database(plume, current_user, User_Database, db):
    try:
        lMax = convert_and_clean_inputs_database(plume, 'Plume length[m]')
        site = convert_and_clean_inputs_database(plume, 'Site Unit')
        compound = convert_and_clean_inputs_database(plume, 'Compound')
        atv = convert_and_clean_inputs_database(plume, 'Aquifer thickness[m]')
        w = convert_and_clean_inputs_database(plume, 'Plume Width[m]')
        hc = convert_and_clean_inputs_database(plume, 'Hydraulic conductivity[10-3 [m/s]]')
        ed = convert_and_clean_inputs_database(plume, 'Electron Donor[mg/l]')
        o2 = convert_and_clean_inputs_database(plume, 'Electron Acceptors : O2[mg/l]')
        no3 = convert_and_clean_inputs_database(plume, 'NO3[mg/l]')
        so4 = convert_and_clean_inputs_database(plume, 'SO4[mg/l]')
        fe = convert_and_clean_inputs_database(plume, 'Fe(II)[mg/l]')
        ps = convert_and_clean_inputs_database(plume, 'Plume state')
        cg = convert_and_clean_inputs_database(plume, 'Chem. Group')
        cy = convert_and_clean_inputs_database(plume, 'Country')
        ls = convert_and_clean_inputs_database(plume, 'Literature Source')
        plume_length = len(lMax)
        for i in range(plume_length):
            user_db = User_Database(
                Site_Unit=site[i], Aquifer_thickness=atv[i],
                Plume_length=lMax[i], Plume_Width=w[i],
                Hydraulic_conductivity=hc[i], Electron_Donor=ed[i],
                O2=o2[i], NO3=no3[i], SO4=so4[i], Fe=fe[i], Plume_state=ps[i],
                Chem_Group=cg[i], Country=cy[i], Literature_Source=ls[i],
                user_database=current_user, Compound=compound[i])
            db.session.add(user_db)
        db.session.commit()
    except Exception as e:
        return False
    return True


def check_file_for_liedl_equation(plume, current_user, Liedl, db):
    try:
        m = convert_and_clean_inputs(plume, 'Aquifer thickness')
        tv = convert_and_clean_inputs(plume, 'Transverse Dispersivity')
        a = convert_and_clean_inputs(plume, 'Reaction Stochiometric coefficient ')
        ca = convert_and_clean_inputs(plume, 'Contaminant Concentration')
        cd = convert_and_clean_inputs(plume, 'Reactant Concentration')
        plume_length = len(m)
        for i in range(plume_length):
            liedl = Liedl(
                Aquifer_thickness=m[i],
                Transverse_Dispersivity=tv[i], Stoichiometry_coefficient=a[i],
                Contaminant_Concentration=ca[i],
                Reactant_Concentration=cd[i],
                Model_Plume_Length=((4 * m[i] * m[i]) / (math.pi * math.pi * tv[i])) * math.log(
                    ((a[i] * cd[i] + ca[i]) / ca[i]) * (4 / math.pi)),
                liedl=current_user
            )
            db.session.add(liedl)
        db.session.commit()
    except Exception as e:
        return False
    return True


def check_file_for_chu_equation(plume, current_user, Chu, db):
    try:
        m = convert_and_clean_inputs(plume, 'Width')
        tv = convert_and_clean_inputs(plume, 'Transverse Dispersivity')
        a = convert_and_clean_inputs(plume, 'Reaction Stoichiometric Ratio')
        ca = convert_and_clean_inputs(plume, 'Contaminant Concentration')
        cd = convert_and_clean_inputs(plume, 'Reactant Concentration')
        e = convert_and_clean_inputs(plume, 'Biological Factor')
        plume_length = len(m)
        for i in range(plume_length):
            chu = Chu(
                Width=m[i], Transverse_Horizontal_Dispersivity=tv[i], Reaction_Stoichiometric_Ratio=a[i],
                Contaminant_Concentration=ca[i], Biological_Factor=e[i],
                Reactant_Concentration=cd[i],
                Model_Plume_Length=((math.pi * m[i] * m[i]) / (16 * tv[i])) * (((a[i] * cd[i]) / (ca[i] - e[i])) ** 2),
                chu=current_user
            )
            db.session.add(chu)
        db.session.commit()
    except Exception as e:
        return False
    return True


def check_file_for_bio_equation(plume, current_user, Bio, db):
    try:
        cthres = convert_and_clean_inputs(plume, 'Threshold Concentration')
        t = convert_and_clean_inputs(plume, 'Time')
        z_2 = convert_and_clean_inputs(plume, 'Top Source Location')
        co = convert_and_clean_inputs(plume, 'Input Concentration')
        w = convert_and_clean_inputs(plume, 'Source Width')
        v = convert_and_clean_inputs(plume, 'Average Linear Groundwater Velocity')
        al_x = convert_and_clean_inputs(plume, 'Longitudinal Dispersivity')
        al_y = convert_and_clean_inputs(plume, 'Horizontal Transverse Dispersivity')
        al_z = convert_and_clean_inputs(plume, 'Vertical Transverse Dispersivity')
        df = convert_and_clean_inputs(plume, 'Effective Diffusion Coefficient')
        r = convert_and_clean_inputs(plume, 'R')
        ga = convert_and_clean_inputs(plume, 'Ga')
        la = convert_and_clean_inputs(plume, 'La')
        m = convert_and_clean_inputs(plume, 'M')

        plume_length = len(w)
        for i in range(plume_length):
            y = 0
            z_1 = 0
            z = (z_1 + z_2[i]) / 2
            Dx = al_x[i] * v[i] + df[i]  # [m^2/y]
            Dy = al_y[i] * v[i] + df[i]  # [m^2/y]
            Dz = Dy / 10 + df[i]  # [m^2/y]

            # used data
            vr = v[i] / r[i]  # [m/y]
            Dyr = Dy / r[i]  # [m^2/y]
            Dxr = Dx / r[i]  # [m^2/y]
            Dyr = Dy / r[i]  # [m^2/y]
            Dzr = Dz / r[i]  # [m^2/y]

            def C(x):
                # Boundary Condition
                if x <= 1e-6:
                    if y <= w[i] / 2 and y >= -w[i] / 2 and z <= z_2[i] and z >= z_1:
                        C = co[i] * np.exp(-ga[i] * t[i])
                    else:
                        C = 0
                else:
                    a = co[i] * np.exp(-ga[i] * t[i]) * x / (8 * np.sqrt(np.pi * Dxr))
                    roots = sp.special.roots_legendre(m[i])[0]
                    weights = sp.special.roots_legendre(m[i])[1]
                    # scaling
                    bot = 0
                    top = np.sqrt(np.sqrt(t[i]))
                    Tau = (roots * (top - bot) + top + bot) / 2
                    Tau4 = Tau ** 4
                    # calculation
                    xTerm = (np.exp(-(((la[i] - ga[i]) * Tau4) + ((x - vr * Tau4) ** 2) / (4 * Dxr * Tau4)))) / (Tau ** 3)
                    yTerm = sp.special.erfc((y - w[i] / 2) / (2 * np.sqrt(Dyr * Tau4))) - sp.special.erfc(
                        (y + w[i] / 2) / (2 * np.sqrt(Dyr * Tau4)))
                    zTerm = sp.special.erfc((z - z_2[i]) / (2 * np.sqrt(Dzr * Tau4))) - sp.special.erfc(
                        (z - z_1) / (2 * np.sqrt(Dzr * Tau4)))
                    Term = xTerm * yTerm * zTerm
                    Integrand = Term * (weights * (top - bot) / 2)
                    C = a * 4 * sum(Integrand)
                return C

            x_array = np.array([0])
            c_array = np.array([C(0)])
            x = 0
            while C(x) >= cthres[i]:
                x = x + 1
                x_array = np.append(x_array, x)
                c_array = np.append(c_array, C(x))
            else:
                lMax = "%.2f" % x

            bio = Bio(
                Threshold_Concentration=cthres[i], Time=t[i], Top_Source_Location=z_2[i], Input_Concentration=co[i],
                Source_Width=w[i], Average_Linear_Groundwater_Velocity=v[i], Longitudinal_Dispersivity=al_x[i],
                Horizontal_Transverse_Dispersivity=al_y[i], Vertical_Transverse_Dispersivity=al_z[i],
                Effective_Diffusion_Coefficient=df[i], R=r[i], Ga=ga[i], La=la[i], M=m[i], Model_Plume_Length=lMax,
                user_id=1
            )
            db.session.add(bio)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


def check_file_for_ham_equation(plume, current_user, Ham, db):
    try:
        m = convert_and_clean_inputs(plume, 'Discharge')
        tv = convert_and_clean_inputs(plume, 'Horizontal Transverse Dispersivity')
        ca = convert_and_clean_inputs(plume, 'Contaminant Concentration')
        a = convert_and_clean_inputs(plume, 'Gamma')
        cd = convert_and_clean_inputs(plume, 'Reactant Concentration')
        plume_length = len(m)
        for i in range(plume_length):
            ham = Ham(
                Width=m[i], Horizontal_Transverse_Dispersivity=tv[i],
                Contaminant_Concentration=ca[i],
                Reactant_Concentration=cd[i],
                Gamma=a[i],
                Model_Plume_Length=((m[i] * m[i]) / (4 * math.pi * tv[i])) * (((a[i]*cd[i]) / ca[i]) ** 2),
                ham=current_user
            )
            db.session.add(ham)
        db.session.commit()
    except Exception as e:
        return False
    return True


def check_file_for_liedl3d_equation(plume, current_user, Liedl3D, db):
    try:
        m = convert_and_clean_inputs(plume, 'Source Thickness')
        htv = convert_and_clean_inputs(plume, 'Horizontal Transverse Dispersivity')
        tv = convert_and_clean_inputs(plume, 'Vertical Transverse Dispersivity')
        w = convert_and_clean_inputs(plume, 'Source Width')
        ca = convert_and_clean_inputs(plume, 'Partner Reactant Concentration')
        cth = convert_and_clean_inputs(plume, 'Threshold Contaminant Concentration')
        a = convert_and_clean_inputs(plume, 'Reaction Stoichiometric Ratio')
        cd = convert_and_clean_inputs(plume, 'Contaminant Concentration')
        plume_length = len(m)
        for i in range(plume_length):
            input = ca[i], cd[i], cth[i], a[i], m[i], htv[i], tv[i], w[i]
            year_histogram, lMax = create_liedl3DPlot(input)
            liedl3d = Liedl3D(
                Source_Thickness=m[i], Horizontal_Transverse_Dispersivity=htv[i],
                Vertical_Transverse_Dispersivity=tv[i], Stoichiometric_Ratio=a[i],
                Contaminant_Concentration=ca[i], Source_Width=w[i], Threshold_Contaminant_Concentration=cth[i],
                Partner_Reactant_Concentration=cd[i],
                Model_Plume_Length=lMax, liedl3d=current_user
            )
            db.session.add(liedl3d)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


def check_file_for_maier_and_grathwohl_equation(plume, current_user, MaierGrathwohl, db):
    try:
        m = convert_and_clean_inputs(plume, 'Aquifer Thickness')
        tv = convert_and_clean_inputs(plume, 'Vertical Transverse Dispersivity')
        a = convert_and_clean_inputs(plume, 'Reaction Stoichiometric Ratio')
        cd = convert_and_clean_inputs(plume, 'Contaminant Concentration')
        ca = convert_and_clean_inputs(plume, 'Partner Reactant Concentration')
        plume_length = len(m)
        for i in range(plume_length):
            maiergrathwohl = MaierGrathwohl(
                Aquifer_thickness=m[i],
                Vertical_Transverse_Dispersivity=tv[i], Stoichiometry_coefficient=a[i],
                Contaminant_Concentration=ca[i],
                Reactant_Concentration=cd[i],
                Model_Plume_Length=0.5 * ((m[i] * m[i]) / tv[i]) * (((a[i] * cd[i]) / ca[i]) ** 0.3),
                maiergrathwohl=current_user
            )
            db.session.add(maiergrathwohl)
        db.session.commit()
    except Exception as e:
        return False
    return True


def check_file_for_birla_equation(plume, current_user, Birla, db):
    try:
        m = convert_and_clean_inputs(plume, 'Aquifer Thickness')
        tv = convert_and_clean_inputs(plume, 'Vertical Transverse Dispersivity')
        a = convert_and_clean_inputs(plume, 'Reaction Stoichiometric Ratio')
        ca = convert_and_clean_inputs(plume, 'Contaminant Concentration')
        cd = convert_and_clean_inputs(plume, 'Partner Reactant Concentration')
        r = convert_and_clean_inputs(plume, 'Recharge Rate')
        plume_length = len(m)
        for i in range(plume_length):
            birla = Birla(
                Aquifer_thickness=m[i],
                Vertical_Transverse_Dispersivity=tv[i], Stoichiometry_coefficient=a[i],
                Contaminant_Concentration=ca[i],
                Reactant_Concentration=cd[i], Recharge_Rate=r[i],
                Model_Plume_Length=(1 - (0.047 * (m[i] ** 0.404) * (r[i] ** 1.883))) * (
                            (4 * m[i] * m[i]) / (math.pi * math.pi * tv[i])) * math.log(
                    (((a[i] * cd[i]) + ca[i]) / ca[i]) * (4 / math.pi)),
                birla=current_user
            )
            db.session.add(birla)
        db.session.commit()
    except Exception as e:
        return False
    return True
