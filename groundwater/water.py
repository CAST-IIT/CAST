import json
import math
import os
import shutil

import matplotlib
import pandas as pd
from flask import jsonify
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from groundwater import app, db, bcrypt, mail
from groundwater.NumericalModel.numericalModel import numerical_model
from groundwater.bioScreenFormula import bio
from groundwater.assignParameterValue import assign_parameter_value
from groundwater.dataStorage import user_database, data_liedl, data_chu, data_ham, data_Bio, data_birla, data_maiergrathwohl, \
    data_liedl3d
from groundwater.databasePlots import create_bargraph, create_histogram, create_boxplot
from groundwater.dispersivity_graphs import dispersivity_graphs
from groundwater.file_checkers import allowed_file, check_file_for_liedl_equation, check_file_for_chu_equation, \
    check_file_for_ham_equation, check_file_for_liedl3d_equation, check_file_for_maier_and_grathwohl_equation, \
    check_file_for_birla_equation, check_file_for_database
from groundwater.form import RegistrationForm, LoginForm, UpdateAccountForm, LiedlForm, ChuForm, HamForm, Liedl3DForm, \
    BirlaForm, MaierGrathwohlForm, UserDatabaseForm, NumericalForm, RequestResetForm, ResetPasswordForm
from groundwater.liedl3D import create_liedl3DPlot
from groundwater.models import User, Liedl, Chu, Ham, Liedl3D, Birla, MaierGrathwohl, User_Database, Bio
from groundwater.parameters import Parameters
from groundwater.scatterplot import create_scatterplot
from groundwater.scatterplotAnalyticalModel import create_liedlPlotMultiple, create_chuEtAlPlotMultiple, \
    create_HamPlotMultiple, create_Liedl3DMultiple
from groundwater.scatterplotSingleMode import create_singlePlot
from groundwater.scatterplotsEmpiricalModel import create_MaierAndGrathwohlPlotMultiple, create_BirlaEtAlPlotMultiple

matplotlib.use('Agg')

app.secret_key = 'many random bytes'
df = pd.read_csv('groundwater/static/original.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about_groundwater', methods=['GET', 'POST'])
def about_groundwater():
    return render_template('IndexDocumentation/groundwater.html')


@app.route('/about_plume', methods=['GET', 'POST'])
def about_plume():
    return render_template('IndexDocumentation/contaminant_plume.html')


@app.route('/user_guide', methods=['GET', 'POST'])
def user_guide():
    return render_template('IndexDocumentation/users_guide.html')


@app.route('/complete_documentation', methods=['GET', 'POST'])
def complete_documentation():
    return render_template('IndexDocumentation/complete_documentation.html')


@app.route('/credits', methods=['GET', 'POST'])
def credits():
    return render_template('IndexDocumentation/credits.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    organisation=form.organisation.data, country=form.organisation.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If the user is already logged in then redirect to home-page
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Check if user exist in the db and password entered by the user is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # User exist & password entered is valid, thereby log the user in
            # and redirect to the home-page
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            return redirect(url_for('index')) if next_page else redirect(url_for('index'))
        else:
            # User credentials are wrong or the user does not exist
            flash('Login Unsuccessful! Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                           form=form)


@app.route('/database', methods=['POST', 'GET'])
@login_required
def database():
    table_data = user_database(current_user.id)
    def check_null(data):
        if data == -1:
            data = None
        return data
    if "open" in request.form:
        if request.method == 'POST':
            Aquifer_thickness = check_null(float(request.form["aqui"]))
            Plume_length = check_null(float(request.form["length"]))
            Plume_Width = check_null(float(request.form["width"]))
            Hydraulic_conductivity = check_null(float(request.form["conduct"]))
            Electron_Donor = check_null(float(request.form["donor"]))
            O2 = check_null(float(request.form["o2"]))
            NO3 = check_null(float(request.form["no3"]))
            SO4 = check_null(float(request.form["so4"]))
            Fe = check_null(float(request.form["fe"]))
            Plume_state = check_null((request.form["state"]))
            Chem_Group = check_null((request.form["chem"]))
            Country = check_null((request.form["country"]))
            Literature_Source = check_null((request.form["source"]))
            user_entry = User_Database(Site_Unit=request.form["name"], Aquifer_thickness=Aquifer_thickness,
                                       Plume_length=Plume_length, Plume_Width=Plume_Width,
                                       Hydraulic_conductivity=Hydraulic_conductivity, Electron_Donor=Electron_Donor,
                                       O2=O2, NO3=NO3, SO4=SO4, Fe=Fe, Plume_state=Plume_state,
                                       Chem_Group=Chem_Group, Country=Country, Literature_Source=Literature_Source,
                                       user_database=current_user, Compound=request.form["compound"])
            db.session.add(user_entry)
            db.session.commit()
            flash('Your entry has been added!', 'success')
            return redirect('/database')
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_database, current_user, User_Database, db)
            return redirect('/database')
    elif "delete" in request.form:
        if request.method == 'POST':
            User_Database.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect('/database')
    return render_template('DatabaseManagement/database.html', table_data=table_data,
                           column_names=Parameters.User_data_columns)



@app.route('/dispersivityData', methods=['POST', 'GET'])
def dispersivity():
    x = dispersivity_graphs()
    return render_template('DispersivityData/dispersivityData.html', data=x.to_html())


@app.route('/allPlots', methods=['POST', 'GET'])
def allPlots():
    return render_template('DatabaseManagement/allPlots.html')


@app.route('/scatter', methods=['POST'])
def change_scatterplot():
    # begin
    data = request.json
    scatterplot_fits = data.get('scatterplot_fits', 'default')
    parameters = data.get('parameters', 'default')
    table_data = user_database(current_user.id)
    index = assign_parameter_value(parameters)
    # end
    graphJSON = create_scatterplot(
        scatterplot_fits, parameters, table_data, index)
    return graphJSON


@app.route('/hist', methods=['POST', 'GET'])
def change_feature1():
    data = request.json
    histogramFeature = data.get('histogramFeature', 'default')
    parameter = data.get('parameter', 'default')
    table_data = user_database(current_user.id)
    index = assign_parameter_value(parameter)
    graphJSON = create_histogram(
        histogramFeature, table_data, index, parameter)
    return graphJSON


@app.route('/box', methods=['POST', 'GET'])
def change_boxplot():
    boxplot = request.args['selected']
    table_data = user_database(current_user.id)
    index = assign_parameter_value(boxplot)
    graphJSON = create_boxplot(boxplot, table_data, index)
    return graphJSON


@app.route('/bargraph', methods=['POST', 'GET'])
def bargraph():
    table_data = user_database(current_user.id)
    plot = create_bargraph(table_data)
    return render_template('DatabaseManagement/bargraph.html', plot=plot)


@app.route('/boxplot', methods=['POST', 'GET'])
def boxplot():
    boxplot = 'Plume length[m]'
    table_data = user_database(current_user.id)
    index = assign_parameter_value(boxplot)
    plot = create_boxplot(boxplot, table_data, index)
    if request.method == 'POST':
        return redirect(url_for('DatabaseManagement/boxplot'))
    return render_template('DatabaseManagement/boxplot.html', plot=plot)


@app.route('/histogram', methods=['POST', 'GET'])
def histogram():
    histogramFeature = 'Gaussian'
    parameter = 'Plume length[m]'
    table_data = user_database(current_user.id)
    index = assign_parameter_value(parameter)
    plot = create_histogram(histogramFeature, table_data, index, parameter)
    if request.method == 'POST':
        return redirect(url_for('DatabaseManagement/histogram'))
    return render_template('DatabaseManagement/histogram.html', plot=plot)


@app.route('/scatterplot', methods=['POST', 'GET'])
def scatterplot():
    parameters = 'Aquifer thickness[m]'
    scatterplot_fits = 'Exponential'
    table_data = user_database(current_user.id)
    index = assign_parameter_value(parameters)
    plot = create_scatterplot(scatterplot_fits, parameters, table_data, index)
    if request.method == 'POST':
        return redirect(url_for('DatabaseManagement/scatterplot'))
    return render_template('DatabaseManagement/scatterplot.html', plot=plot)


@app.route('/statistics', methods=['POST', 'GET'])
def statistics():
    sa = pd.read_csv('groundwater/static/original.csv')
    sa = sa[sa['SO4[mg/l]'] != 'depleted']
    sa = sa[sa['NO3[mg/l]'] != 'depleted']
    sa_final = sa.drop(['Site No.', 'Site Unit', 'Compound', 'Plume state', 'Chem. Group', 'Country',
                        'Literature Source'], axis=1)
    data = sa_final.astype(float).describe()
    return render_template('DatabaseManagement/statistics.html', data=data)


@app.route('/analyticalModel', methods=['POST', 'GET'])
@login_required
def analyticalModel():
    return render_template('AnalyticalModel/analyticalModel.html')


@app.route('/documentationLiedl', methods=['GET', 'POST'])
def documentationLiedl():
    return render_template('AnalyticalModel/documentationLiedl.html')


@app.route('/liedlModelSingle', methods=['POST', 'GET'])
def liedlModelSingle():
    m = 2
    tv = 0.001
    a = 3.5
    ca = 8
    cd = 5
    lMax = ((4 * m * m) / (math.pi * math.pi * tv)) * \
        math.log(((a * cd + ca) / ca) * (4 / math.pi))
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return render_template('AnalyticalModel/liedlModelSingle.html', year_histogram=year_histogram)


@app.route('/random-name/', methods=['POST'])
def random_name():
    m = float(request.form['Thickness'])
    tv = float(request.form['Dispersivity'])
    a = float(request.form['Stoichiometric'])
    ca = float(request.form['Acceptor'])
    cd = float(request.form['Donor'])
    lMax = ((4 * m * m) / (math.pi * math.pi * tv)) * \
        math.log(((a * cd + ca) / ca) * (4 / math.pi))
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/liedlModelMultiple', methods=['POST', 'GET'])
def liedlModelMultiple():
    form = LiedlForm()
    table_data = data_liedl(current_user.id)
    if form.validate_on_submit():
        m = form.Aquifer_thickness.data
        tv = form.Transverse_Dispersivity.data
        a = form.Stoichiometry_coefficient.data
        ca = form.Contaminant_Concentration.data
        cd = form.Reactant_Concentration.data
        lMax = ((4 * m * m) / (math.pi * math.pi * tv)) * math.log(((a * cd + ca) / ca) * (4 / math.pi))
        lMax = "%.2f" % lMax
        liedl = Liedl(Aquifer_thickness=m, Transverse_Dispersivity=tv, Stoichiometry_coefficient=a,
                      Contaminant_Concentration=ca,
                      Reactant_Concentration=cd, Model_Plume_Length=lMax, liedl=current_user)
        db.session.add(liedl)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect('/liedlModelMultiple')

    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])

            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_liedlPlotMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            pass
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_liedl_equation, current_user, Liedl, db)
        return redirect('/liedlModelMultiple')
    elif "delete" in request.form:
        if request.method == 'POST':
            Liedl.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
        return redirect('/liedlModelMultiple')
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_liedlPlotMultiple(df['Site No.'].tolist(), table_data)
    x = df['Site Unit']
    y = df['Site No.']
    return render_template('AnalyticalModel/liedlModelMultiple.html', plot=para, siteData=zip(y, x),
                           form=form, table_data=table_data, column_names=Parameters.Liedl_data_columns)


@app.route('/documentationChu', methods=['GET', 'POST'])
def documentationChu():
    return render_template('AnalyticalModel/documentationchuEtAl.html')


@app.route('/chuEtAlSingle', methods=['POST', 'GET'])
def chuEtAlSingle():
    W = 2
    Th = 0.01
    Ca = 8
    Cd = 5
    g = 1.5
    e = 0
    lMax = ((math.pi * W * W) / (16 * Th)) * (((g * Cd) / (Ca - e)) ** 2)
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return render_template('AnalyticalModel/chuEtAlSingle.html', year_histogram=year_histogram)


@app.route('/chuEtAlSinglePlot', methods=['POST'])
def chuEtAlSinglePlot():
    W = float(request.form['Thickness'])
    Th = float(request.form['Dispersivity'])
    g = float(request.form['Stoichiometric'])
    Ca = float(request.form['Acceptor'])
    Cd = float(request.form['Donor'])
    e = float(request.form['Epsilon'])
    lMax = ((math.pi * W * W) / (16 * Th)) * (((g * Cd) / (Ca - e)) ** 2)
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/chuEtAlModelMultiple', methods=['POST', 'GET'])
def chuEtAlModelMultiple():
    form = ChuForm()
    table_data = data_chu(current_user.id)
    if form.validate_on_submit():
        W = form.Width.data
        Th = form.Transverse_Horizontal_Dispersivity.data
        g = form.Reaction_Stoichiometric_Ratio.data
        Ca = form.Contaminant_Concentration.data
        Cd = form.Reactant_Concentration.data
        e = form.Biological_Factor.data
        lMax = ((math.pi * W * W) / (16 * Th)) * (((g * Cd) / (Ca - e)) ** 2)
        lMax = "%.2f" % lMax
        chu = Chu(Width=W, Transverse_Horizontal_Dispersivity=Th, Reaction_Stoichiometric_Ratio=g,
                  Contaminant_Concentration=Ca, Reactant_Concentration=Cd, Biological_Factor=e, Model_Plume_Length=lMax,
                  chu=current_user)
        db.session.add(chu)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect(url_for('chuEtAlModelMultiple'))
    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])
            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_chuEtAlPlotMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            pass
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_chu_equation, current_user, Chu, db)
        return redirect(url_for('chuEtAlModelMultiple'))
    elif "delete" in request.form:
        if request.method == 'POST':
            Chu.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect(url_for('chuEtAlModelMultiple'))
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_chuEtAlPlotMultiple(df['Site No.'].tolist(), table_data)
    y = df['Site No.']
    x = df['Site Unit']
    return render_template('AnalyticalModel/chuEtAlModelMultiple.html', plot=para, siteData=zip(y, x),
                           form=form, table_data=table_data, column_names=Parameters.Chu_data_columns)

@app.route('/documentationBio', methods=['GET', 'POST'])
def documentationBio():
    return render_template('AnalyticalModel/documentationBio.html')


@app.route('/BioSingle', methods=['POST', 'GET'])
def BioSingle():
    Cthres = 5e-5  
    time = 20  
    H = 6.1  
    c0 = 106.35
    W = 20  
    v = 292  
    ax  = 10.7   
    ay = 1.1 
    az = 0.11  
    Df  = 0 
    R = 1  
    gamma = 0  
    lambda_eff = 4.45e-1 
    numberOfGaussPoints = 60 
    lMax = bio(Cthres,time,H,c0,W,v,ax,ay,az,Df,R,gamma,lambda_eff,numberOfGaussPoints)
    year_histogram = create_singlePlot(lMax)
    return render_template('AnalyticalModel/BioSingle.html', year_histogram=year_histogram)


@app.route('/BioSinglePlot', methods=['POST'])
def BioSinglePlot():
    Cthres = float(request.form['Threshold_Concentration'])
    time = float(request.form['Time'])
    H = float(request.form['Top_Of_Source'])
    c0 = float(request.form['Input_Concentration'])
    W = float(request.form['Width'])
    v = float(request.form['Velocity'])
    ax = float(request.form['Longitudinal'])
    ay = float(request.form['Horizontal'])
    az = float(request.form['Vertical'])
    Df = float(request.form['Diffusion'])
    R = float(request.form['R'])
    gamma = float(request.form['Ga'])
    lambda_eff = float(request.form['La'])
    numberOfGaussPoints = float(request.form['M'])
    lMax = bio(Cthres,time,H,c0,W,v,ax,ay,az,Df,R,gamma,lambda_eff,numberOfGaussPoints)
    year_histogram = create_singlePlot(lMax)
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/BioMultiple', methods=['POST', 'GET'])
def BioMultiple():
    form = BioForm()
    table_data = data_Bio(current_user.id)
    if form.validate_on_submit():
        Cthres = form.Threshold_Concentration.data
        time = form.Time.data
        H = form.Top_Source_Location.data
        c0 = form.Input_Concentration.data
        W = form.Source_Width.data
        v = form.Average_Linear_Groundwater_Velocity.data
        ax = form.Longitudinal_Dispersivity.data
        ay = form.Horizontal_Transverse_Dispersivity.data
        az = form.Vertical_Transverse_Dispersivity.data
        Df = form.Effective_Diffusion_Coefficient.data
        R = form.R.data
        gamma = form.Ga.data
        lambda_eff = form.La.data
        numberOfGaussPoints = form.M.data
        lMax = bio(Cthres,time,H,c0,W,v,ax,ay,az,Df,R,gamma,lambda_eff,numberOfGaussPoints)
        bio_screen = Bio(Threshold_Concentration=Cthres, Time=time, Top_Source_Location=H,
                  Input_Concentration=c0, Source_Width=W, Average_Linear_Groundwater_Velocity=v,
                  Longitudinal_Dispersivity=ax, Horizontal_Transverse_Dispersivity=ay,
                  Vertical_Transverse_Dispersivity=az, Effective_Diffusion_Coefficient=Df, R=R, Ga=gamma, La=lambda_eff, M=numberOfGaussPoints,
                  Model_Plume_Length=lMax, bio=current_user)

        db.session.add(bio_screen)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect(url_for('BioMultiple'))
    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])
            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_BioPlotMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            pass
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_bio_equation, current_user, Bio, db)
        return redirect(url_for('BioMultiple'))
    elif "delete" in request.form:
        if request.method == 'POST':
            Bio.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect(url_for('BioMultiple'))
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_BioPlotMultiple(df['Site No.'].tolist(), table_data)
    y = df['Site No.']
    x = df['Site Unit']
    return render_template('AnalyticalModel/BioMultiple.html', plot=para, siteData=zip(y, x),form=form,
                           table_data=table_data, column_names=Parameters.Bio_data_columns)

@app.route('/documentationHam', methods=['GET', 'POST'])
def documentationHam():
    return render_template('AnalyticalModel/documentationHam.html')


@app.route('/hamModelSingle', methods=['POST', 'GET'])
def hamModelSingle():
    Q = 5
    Ath = 0.01
    Ca = 8
    Cd = 5
    a = 3.5
    lMax = ((Q * Q) / (4 * math.pi * Ath)) * (((a*Cd) / Ca) ** 2)
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return render_template('AnalyticalModel/hamModelSingle.html', year_histogram=year_histogram)


@app.route('/hamEtAlSinglePlot', methods=['POST'])
def hamEtAlSinglePlot():
    Q = float(request.form['Thickness'])
    Ath = float(request.form['Dispersivity'])
    Ca = float(request.form['Acceptor'])
    Cd = float(request.form['Donor'])
    a = float(request.form['Stoichiometric'])
    lMax = ((Q * Q) / (4 * math.pi * Ath)) * (((a*Cd) / Ca) ** 2)
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/hamModelMultiple', methods=['POST', 'GET'])
def hamModelMultiple():
    form = HamForm()
    table_data = data_ham(current_user.id)
    if form.validate_on_submit():
        Q = form.Width.data
        Ath = form.Horizontal_Transverse_Dispersivity.data
        Ca = form.Contaminant_Concentration.data
        Cd = form.Reactant_Concentration.data
        a = form.Gamma.data
        lMax = ((Q * Q) / (4 * math.pi * Ath)) * (((a*Cd) / Ca) ** 2)
        lMax = "%.2f" % lMax
        ham = Ham(Width=Q, Horizontal_Transverse_Dispersivity=Ath,
                  Contaminant_Concentration=Ca, Reactant_Concentration=Cd, Gamma=a, Model_Plume_Length=lMax,
                  ham=current_user)
        db.session.add(ham)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect('/hamModelMultiple')

    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])

            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_HamPlotMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            print(e)
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_ham_equation, current_user, Ham, db)
            return redirect('/hamModelMultiple')
    elif "delete" in request.form:
        if request.method == 'POST':
            Ham.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect('/hamModelMultiple')
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_HamPlotMultiple(df['Site No.'].tolist(), table_data)
    x = df['Site Unit']
    y = df['Site No.']
    return render_template('AnalyticalModel/hamModelMultiple.html', plot=para, siteData=zip(y, x),
                           form=form, table_data=table_data, column_names=Parameters.Ham_data_columns)



@app.route('/documentation3DLiedl', methods=['GET', 'POST'])
def documentation3DLiedl():
    return render_template('AnalyticalModel/documentationLiedl3D.html')


@app.route('/liedl3DModelSingle', methods=['POST', 'GET'])
def liedl3DModelSingle():
    Ca = 8
    Cd = 5
    Ct = 0.5
    g = 3
    M = 10
    Th = 0.01
    Tv = 0.01
    W = 7
    input = Ca, Cd, Ct, g, M, Th, Tv, W
    year_histogram, lMax = create_liedl3DPlot(input)
    lMax = "%.2f" % lMax
    return render_template('AnalyticalModel/liedl3DModelSingle.html', year_histogram=year_histogram)


@app.route('/liedl3DSinglePlot', methods=['POST'])
def liedl3DSinglePlot():
    M = float(request.form['Thickness'])
    Th = float(request.form['Dispersivity'])
    Tv = float(request.form['VDispersivity'])
    W = float(request.form['SourceWidth'])
    Ct = float(request.form['Threshold'])
    Ca = float(request.form['Acceptor'])
    Cd = float(request.form['Donor'])
    g = float(request.form['Stoichiometric'])
    input = Ca, Cd, Ct, g, M, Th, Tv, W
    year_histogram, lMax = create_liedl3DPlot(input)
    lMax = "%.2f" % lMax
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/liedl3DModelMultiple', methods=['POST', 'GET'])
def liedl3DModelMultiple():
    form = Liedl3DForm()
    table_data = data_liedl3d(current_user.id)
    if form.validate_on_submit():
        M = form.Source_Thickness.data
        Th = form.Horizontal_Transverse_Dispersivity.data
        Tv = form.Vertical_Transverse_Dispersivity.data
        W = form.Source_Width.data
        Ct = form.Threshold_Contaminant_Concentration.data
        Cd = form.Contaminant_Concentration.data
        Ca = form.Partner_Reactant_Concentration.data
        g = form.Stoichiometric_Ratio.data
        input = Ca, Cd, Ct, g, M, Th, Tv, W
        year_histogram, lMax = create_liedl3DPlot(input)
        lMax = "%.2f" % lMax
        liedl3d = Liedl3D(Source_Thickness=M, Horizontal_Transverse_Dispersivity=Th,
                          Vertical_Transverse_Dispersivity=Tv,
                          Source_Width=W, Threshold_Contaminant_Concentration=Ct, Contaminant_Concentration=Ca,
                          Partner_Reactant_Concentration=Cd, Stoichiometric_Ratio=g, Model_Plume_Length=lMax,
                          liedl3d=current_user)
        db.session.add(liedl3d)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect('/liedl3DModelMultiple')

    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])

            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_Liedl3DMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            print(e)
            pass
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_liedl3d_equation, current_user, Liedl3D, db)
            return redirect('/liedl3DModelMultiple')
    elif "delete" in request.form:
        if request.method == 'POST':
            Liedl3D.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect('/liedl3DModelMultiple')
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_Liedl3DMultiple(df['Site No.'].tolist(), table_data)
    y = df['Site No.']
    x = df['Site Unit']
    return render_template('AnalyticalModel/liedl3DModelMultiple.html', plot=para, siteData=zip(y, x),
                           form=form, table_data=table_data, column_names=Parameters.Liedl3d_data_columns)


@app.route('/empiricalModel', methods=['POST', 'GET'])
@login_required
def empiricalModel():
    return render_template('EmpiricalModel/empiricalModel.html')


@app.route('/documentationMaierAndGrathwohl', methods=['GET', 'POST'])
def documentationMaierAndGrathwohl():
    return render_template('EmpiricalModel/documentationMaierAndGrathwohl.html')


@app.route('/MaierAndGrathwohlSingle', methods=['POST', 'GET'])
def MaierAndGrathwohlSingle():
    M = 5
    tv = 0.01
    g = 3.5
    Ca = 8
    Cd = 5
    lMax = 0.5 * ((M * M) / tv) * (((g * Cd) / Ca) ** 0.3)
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return render_template('EmpiricalModel/MaierAndGrathwohlSingle.html', year_histogram=year_histogram)


@app.route('/MaierAndGrathwohlSinglePlot', methods=['POST'])
def MaierAndGrathwohlSinglePlot():
    M = float(request.form['Thickness'])
    tv = float(request.form['Dispersivity'])
    g = float(request.form['Stoichiometric'])
    Ca = float(request.form['Acceptor'])
    Cd = float(request.form['Donor'])
    lMax = 0.5 * ((M * M) / tv) * (((g * Cd) / Ca) ** 0.3)
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/MaierAndGrathwohlModelMultiple', methods=['POST', 'GET'])
def MaierAndGrathwohlModelMultiple():
    form = MaierGrathwohlForm()
    table_data = data_maiergrathwohl(current_user.id)
    if form.validate_on_submit():
        M = form.Aquifer_thickness.data
        tv = form.Vertical_Transverse_Dispersivity.data
        g = form.Stoichiometry_coefficient.data
        Ca = form.Contaminant_Concentration.data
        Cd = form.Reactant_Concentration.data
        lMax = 0.5 * ((M * M) / tv) * (((g * Cd) / Ca) ** 0.3)
        lMax = "%.2f" % lMax
        maier = MaierGrathwohl(Aquifer_thickness=M, Vertical_Transverse_Dispersivity=tv, Stoichiometry_coefficient=g,
                               Contaminant_Concentration=Ca, Reactant_Concentration=Cd, Model_Plume_Length=lMax,
                               maiergrathwohl=current_user)
        db.session.add(maier)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect('/MaierAndGrathwohlModelMultiple')
    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])

            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_MaierAndGrathwohlPlotMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            pass
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_maier_and_grathwohl_equation, current_user,
                         MaierGrathwohl, db)
            return redirect('/MaierAndGrathwohlModelMultiple')
    elif "delete" in request.form:
        if request.method == 'POST':
            MaierGrathwohl.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect('/MaierAndGrathwohlModelMultiple')
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_MaierAndGrathwohlPlotMultiple(df['Site No.'].tolist(), table_data)
    y = df['Site No.']
    x = df['Site Unit']
    return render_template('EmpiricalModel/MaierAndGrathwohlModelMultiple.html', plot=para, siteData=zip(y, x),
                           form=form, table_data=table_data, column_names=Parameters.Maiergrathwohl_data_columns)


@app.route('/documentationBirlaEtAl', methods=['GET', 'POST'])
def documentationBirlaEtAl():
    return render_template('EmpiricalModel/documentationBirlaEtAl.html')


@app.route('/BirlaEtAlSingle', methods=['POST', 'GET'])
def BirlaEtAlSingle():
    M = 2
    tv = 0.001
    g = 3.5
    Ca = 8
    Cd = 5
    R = 1
    lMax = (1 - (0.047 * (M ** 0.404) * (R ** 1.883))) * ((4 * M * M) / (math.pi * math.pi * tv)) * math.log(
        (((g * Cd) + Ca) / Ca) * (4 / math.pi))
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return render_template('EmpiricalModel/BirlaEtAlSingle.html', year_histogram=year_histogram)


@app.route('/BirlaEtAlSinglePlot', methods=['POST'])
def BirlaEtAlSinglePlot():
    M = float(request.form['Thickness'])
    tv = float(request.form['Dispersivity'])
    g = float(request.form['Stoichiometric'])
    Ca = float(request.form['Acceptor'])
    Cd = float(request.form['Donor'])
    R = float(request.form['Recharge'])
    lMax = (1 - (0.047 * (M ** 0.404) * (R ** 1.883))) * ((4 * M * M) / (math.pi * math.pi * tv)) * math.log(
        (((g * Cd) + Ca) / Ca) * (4 / math.pi))
    lMax = "%.2f" % lMax
    year_histogram = create_singlePlot(lMax)
    return jsonify({'Result': lMax, 'data': render_template('graphSingleResult.html', year_histogram=year_histogram)})


@app.route('/BirlaEtAlModelMultiple', methods=['POST', 'GET'])
def BirlaEtAlModelMultiple():
    form = BirlaForm()
    table_data = data_birla(current_user.id)
    if form.validate_on_submit():
        M = form.Aquifer_thickness.data
        tv = form.Vertical_Transverse_Dispersivity.data
        g = form.Stoichiometry_coefficient.data
        Ca = form.Contaminant_Concentration.data
        Cd = form.Reactant_Concentration.data
        R = form.Recharge_Rate.data
        lMax = (1 - (0.047 * (M ** 0.404) * (R ** 1.883))) * ((4 * M * M) / (math.pi * math.pi * tv)) * math.log(
            (((g * Cd) + Ca) / Ca) * (4 / math.pi))
        lMax = "%.2f" % lMax
        birla = Birla(Aquifer_thickness=M, Recharge_Rate=R, Vertical_Transverse_Dispersivity=tv,
                      Stoichiometry_coefficient=g, Contaminant_Concentration=Ca, Reactant_Concentration=Cd,
                      Model_Plume_Length=lMax, birla=current_user)
        db.session.add(birla)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect('/BirlaEtAlModelMultiple')
    elif request.method == "GET":
        try:
            siteUnit = json.loads(request.args['siteUnits'])

            if len(siteUnit) is 0:
                siteUnit = df['Site No.'].tolist()

            siteUnit = [int(x) for x in siteUnit]
            para = create_BirlaEtAlPlotMultiple(siteUnit, table_data)
            return para
        except Exception as e:
            pass
    elif "upload" in request.form:
        if request.method == 'POST':
            allowed_file(check_file_for_birla_equation, current_user, Birla, db)
            return redirect('/BirlaEtAlModelMultiple')
    elif "delete" in request.form:
        if request.method == 'POST':
            Birla.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash(f'Successfully deleted all data', category='success')
            return redirect('/BirlaEtAlModelMultiple')
    elif not form.validate_on_submit():
        flash('Something went wrong with entering your data, please check form - your entries have not been erased', category='danger')
    para = create_BirlaEtAlPlotMultiple(df['Site No.'].tolist(), table_data)
    y = df['Site No.']
    x = df['Site Unit']
    return render_template('EmpiricalModel/BirlaEtAlModelMultiple.html', plot=para, siteData=zip(y, x),
                           form=form, table_data=table_data, column_names=Parameters.Birla_data_columns)


@app.route('/documentationNumerical', methods=['GET', 'POST'])
def documentationNumerical():
    return render_template('NumericalModel/documentationNumerical.html')


@app.route('/numericalModel', methods=['POST', 'GET'])
@login_required
def numericalModel():
    form = NumericalForm()
    bool = False
    if form.validate_on_submit():
        Lx = form.Lx.data
        Ly = form.Ly.data
        ncol = form.ncol.data
        nrow = form.nrow.data
        prsity = form.prsity.data
        al = form.al.data
        trpt = form.trpt.data
        Gamma = form.Gamma.data
        Cd = form.Cd.data
        Ca = form.Ca.data
        h1 = form.h1.data
        h2 = form.h2.data
        hk = form.hk.data
        id = str(current_user.id)
        # Replace this path with your path
        parent_dir = '/home/vedaanti/Water'
        path = os.path.join(parent_dir, id)
        if not (h1 > h2):
            flash(
                'Value of head inlet should be greater than value of head outlet', 'danger')
        else:
            try:
                id = str(current_user.id)
                lMax, plot_url = numerical_model(
                    Lx, Ly, ncol, nrow, prsity, al, trpt, Gamma, Cd, Ca, h1, h2, hk, id, path)
                lMax = "%.2f" % lMax
                bool = True
                string = 'Maximum Plume Length(LMax): ' + str(lMax)
                flash(string, 'success')
                return render_template('NumericalModel/numericalNew.html', form=form, bool=bool, plot_url=plot_url)
            except Exception as e:
                flash('No contour levels were found within the data range', 'danger')
        os.chdir("..")
        shutil.rmtree(path)
    return render_template('NumericalModel/numericalNew.html', form=form, bool=bool)
