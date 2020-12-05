from flask_login import current_user
from flask_wtf import FlaskForm
from math import e
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, NumberRange, Regexp, email_validator

from groundwater.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    organisation = StringField('Organisation',
                               validators=[DataRequired()])
    country = StringField('Country',
                          validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

#
# def less_than(FlaskForm, field):
#     if field.data
#         raise ValidationError('Field must be less than 5')


class UserDatabaseForm(FlaskForm):
    Site_Unit = StringField('Site Unit', validators=[InputRequired()])
    Compound = StringField('Compound', validators=[InputRequired()])
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[InputRequired()])
    Plume_length = FloatField('Plume Length', validators=[InputRequired()])
    Plume_Width = FloatField('Plume Width', validators=[InputRequired()])
    Hydraulic_conductivity = FloatField('Hydraulic Conductivity', validators=[InputRequired()])
    Electron_Donor = FloatField('Electron Donor', validators=[InputRequired()])
    O2 = FloatField('O2', validators=[InputRequired()])
    NO3 = FloatField('NO3', validators=[InputRequired()])
    SO4 = FloatField('SO4', validators=[InputRequired()])
    Fe = FloatField('Fe', validators=[InputRequired()])
    Plume_state = StringField('Plume State', validators=[InputRequired()])
    Chem_Group = StringField('Chemical Group', validators=[InputRequired()])
    Country = StringField('Country', validators=[InputRequired()])
    Literature_Source = StringField('Literature Source', validators=[InputRequired()])
    submit = SubmitField('Add Data')


class LiedlForm(FlaskForm):
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[DataRequired()])
    Transverse_Dispersivity = FloatField('Transverse Dispersivity', validators=[InputRequired()])
    Stoichiometry_coefficient = FloatField('Stoichiometry coefficient', validators=[InputRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[InputRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[InputRequired()])
    submit = SubmitField('Generate Graph')


class ChuForm(FlaskForm):
    Width = FloatField('Width', validators=[InputRequired()])
    Transverse_Horizontal_Dispersivity = FloatField('Transverse Horizontal Dispersivity', validators=[InputRequired()])
    Reaction_Stoichiometric_Ratio = FloatField('Reaction Stoichiometric Ratio', validators=[InputRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[InputRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[InputRequired()])
    Biological_Factor = FloatField('Biological Factor', validators=[InputRequired("Please enter a valid value")])
    submit = SubmitField('Generate Graph')

class BioForm(FlaskForm):
    Threshold_Concentration = FloatField('Threshold Concentration', validators=[InputRequired()])
    Time = FloatField('Time', validators=[InputRequired()])
    Top_Source_Location = FloatField('Source Thickness', validators=[InputRequired()])
    Input_Concentration = FloatField('Source Concentration', validators=[InputRequired()])
    Source_Width = FloatField('Source Width', validators=[InputRequired()])
    Average_Linear_Groundwater_Velocity = FloatField('Average Linear Groundwater Velocity', validators=[InputRequired("Please enter a valid value")])
    Longitudinal_Dispersivity = FloatField('Longitudinal Dispersivity', validators=[InputRequired()])
    Horizontal_Transverse_Dispersivity = FloatField('Horizontal Transverse Dispersivity', validators=[InputRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[InputRequired()])
    Effective_Diffusion_Coefficient = FloatField('Effective Diffusion Coefficient', validators=[InputRequired()])
    R = FloatField('Retardation Factor', validators=[InputRequired()])
    Ga = FloatField('Source Decay Coefficient', validators=[InputRequired()])
    La = FloatField('Effective first-order Decay Coefficient', validators=[InputRequired()])
    M = FloatField('Number of Gauss points', validators=[InputRequired()])
    submit = SubmitField('Generate Graph')

class HamForm(FlaskForm):
    Width = FloatField('Width', validators=[InputRequired()])
    Horizontal_Transverse_Dispersivity = FloatField('Horizontal Transverse Dispersivity', validators=[InputRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[InputRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[InputRequired()])
    Gamma = FloatField('Gamma', validators=[InputRequired()])
    submit = SubmitField('Generate Graph')


class Liedl3DForm(FlaskForm):
    Source_Thickness = FloatField('Source Thickness', validators=[InputRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[InputRequired()])
    Source_Width = FloatField('Source Width', validators=[InputRequired()])
    Horizontal_Transverse_Dispersivity = FloatField('Horizontal Transverse Dispersivity', validators=[InputRequired()])
    Stoichiometric_Ratio = FloatField('Stoichiometric Ratio', validators=[InputRequired()])
    Partner_Reactant_Concentration = FloatField('Partner Reactant Concentration', validators=[InputRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[InputRequired()])
    Threshold_Contaminant_Concentration = FloatField('Threshold Contaminant Concentration', validators=[InputRequired()])
    submit = SubmitField('Generate Graph')


class BirlaForm(FlaskForm):
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[InputRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[InputRequired()])
    Stoichiometry_coefficient = FloatField('Stoichiometry coefficient', validators=[InputRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[InputRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[InputRequired()])
    Recharge_Rate = FloatField('Recharge Rate', validators=[InputRequired()])
    submit = SubmitField('Generate Graph')


class MaierGrathwohlForm(FlaskForm):
    Aquifer_thickness = FloatField('Aquifer Thickness', validators=[InputRequired()])
    Vertical_Transverse_Dispersivity = FloatField('Vertical Transverse Dispersivity', validators=[InputRequired()])
    Stoichiometry_coefficient = FloatField('Stoichiometry coefficient', validators=[InputRequired()])
    Contaminant_Concentration = FloatField('Contaminant Concentration', validators=[InputRequired()])
    Reactant_Concentration = FloatField('Reactant Concentration', validators=[InputRequired()])
    submit = SubmitField('Generate Graph')


def less_than(FlaskForm, field):
    if field.data >= 5:
        raise ValidationError('Field must be less than 5')


class NumericalForm(FlaskForm):
    # Domain
    Lx = FloatField('Length[m]', validators=[InputRequired(),
                                             NumberRange(min=2500, max=5000,
                                                         message='Please enter a value in '
                                                                 'the range of 2500-5000(inclusive)')])
    Ly = FloatField('Height[m]', validators=[InputRequired(), less_than])
    ncol = IntegerField('Number of columns', validators=[InputRequired(), NumberRange(min=2, max=250,
                                                                                      message='Please enter a value '
                                                                                              'in the range '
                                                                                              'of 2-250(inclusive)')])
    nrow = IntegerField('Number of rows', validators=[InputRequired(), NumberRange(min=2, max=250,
                                                                                   message='Please enter a '
                                                                                           'value in the range'
                                                                                           ' of 2-250(inclusive)')])
    # Parameters
    prsity = FloatField('Porosity',
                        validators=[InputRequired(),
                                    NumberRange(
                                        min=0, max=1,
                                        message='Please enter a value in the range of 0-1(inclusive)')])
    al = FloatField('Longitudinal Dispersivity[m]', validators=[InputRequired(),
                                                                NumberRange(
                                                                    min=1, max=10,
                                                                    message='Please enter a '
                                                                            'value in the range of 1-10(inclusive)')
                                                                ])
    trpt = FloatField('Transverse Vertical Dispersivity[m]', validators=[InputRequired(),
                                                                         NumberRange(
                                                                             min=0.01, max=0.1,
                                                                             message='Please enter a '
                                                                                     'value in the range '
                                                                                     'of 0.01-0.1(inclusive)')
                                                                         ])
    Gamma = FloatField('Stoichiometric Ratio', validators=[InputRequired(),
                                                           NumberRange(
                                                               min=1,
                                                               message='Please enter a '
                                                                       'more than or equal to 1')
                                                           ])

    Cd = FloatField('Contaminant Concentration[mg/l]', validators=[InputRequired()])
    Ca = FloatField('Partner Reactant Concentration[mg/l]', validators=[InputRequired()])
    h1 = FloatField('Head inlet[m]', validators=[InputRequired()])
    h2 = FloatField('Head outlet[m]', validators=[InputRequired()])
    hk = FloatField('Conductivity[m/d]', validators=[InputRequired(),
                                                     NumberRange(
                                                         min=8.64*pow(10, -5), max=864,
                                                         message='Please enter a '
                                                                 'value in the range of 8.64E-5 - 864(inclusive)')
                                                     ])
    submit = SubmitField('Run')
