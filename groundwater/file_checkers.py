import math

import pandas as pd
from flask import flash, redirect, request
from werkzeug.utils import secure_filename
from groundwater.liedl3D import create_liedl3DPlot
from groundwater.bioScreenFormula import bio

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
        else:
            flash(f'Problem parsing the parameters.\n'
                  f'Please check that the heading and ranges/values for the parameters are matching'
                  f' the permitted codes.\n'
                  f'Kindly refer to the sample csv file for details.',
                  category='danger')
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
        print(e)
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
        print(e)
        return False
    return True


def check_file_for_bio_equation(plume, current_user, Bio, db):
    try:
        Cthres = convert_and_clean_inputs(plume, 'Threshold Concentration')
        time = convert_and_clean_inputs(plume, 'Time')
        H = convert_and_clean_inputs(plume, 'Source Thickness')
        c0 = convert_and_clean_inputs(plume, 'Source Concentration')
        W = convert_and_clean_inputs(plume, 'Source Width')
        v = convert_and_clean_inputs(plume, 'Average Linear Groundwater Velocity')
        ax = convert_and_clean_inputs(plume, 'Longitudinal Dispersivity')
        ay = convert_and_clean_inputs(plume, 'Horizontal Transverse Dispersivity')
        az = convert_and_clean_inputs(plume, 'Vertical Transverse Dispersivity')
        Df = convert_and_clean_inputs(plume, 'Effective Diffusion Coefficient')
        R = convert_and_clean_inputs(plume, 'Retardation Factor')
        gamma = convert_and_clean_inputs(plume, 'Source Decay Coefficient')
        lambda_eff = convert_and_clean_inputs(plume, 'Effective first-order Decay Coefficient')
        numberOfGaussPoints = convert_and_clean_inputs(plume, 'Number of Gauss points')
        plume_length = len(W)
        for i in range(plume_length):
            lMax = bio(Cthres[i],time[i],H[i],c0[i],W[i],v[i],ax[i],ay[i],az[i],Df[i],R[i],gamma[i],lambda_eff[i],
            numberOfGaussPoints[i])
            bio_screen = Bio(Threshold_Concentration=Cthres[i], Time=time[i], Top_Source_Location=H[i],
                  Input_Concentration=c0[i], Source_Width=W[i], Average_Linear_Groundwater_Velocity=v[i],
                  Longitudinal_Dispersivity=ax[i], Horizontal_Transverse_Dispersivity=ay[i],
                  Vertical_Transverse_Dispersivity=az[i], Effective_Diffusion_Coefficient=Df[i], R=R[i], Ga=gamma[i], La=lambda_eff[i],
                  M=numberOfGaussPoints[i],Model_Plume_Length=lMax, bio=current_user)
            db.session.add(bio_screen)
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
        print(e)
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
        print(e)
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
        print(e)
        return False
    return True
