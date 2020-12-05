from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from groundwater import db, login_manager, app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    organisation = db.Column(db.String(30), unique=False, nullable=False)
    country = db.Column(db.String(40), unique=False, nullable=False)
    user_database = db.relationship('User_Database', backref='user_database', lazy=True)
    liedl = db.relationship('Liedl', backref='liedl', lazy=True)
    chu = db.relationship('Chu', backref='chu', lazy=True)
    ham = db.relationship('Ham', backref='ham', lazy=True)
    liedl3d = db.relationship('Liedl3D', backref='liedl3d', lazy=True)
    birla = db.relationship('Birla', backref='birla', lazy=True)
    maiergrathwohl = db.relationship('MaierGrathwohl', backref='maiergrathwohl', lazy=True)
    bio = db.relationship('Bio', backref='bio', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __ref__(self):
        return f'User({self.id},{self.username},{self.email},{self.password},{self.organisation},{self.country})'


class User_Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Site_Unit = db.Column(db.String(60), nullable=True)
    Compound = db.Column(db.String(60), nullable=True)
    Aquifer_thickness = db.Column(db.Float, nullable=True)
    Plume_length = db.Column(db.Float, nullable=True)
    Plume_Width = db.Column(db.Float, nullable=True)
    Hydraulic_conductivity = db.Column(db.Float, nullable=True)
    Electron_Donor = db.Column(db.Float, nullable=True)
    O2 = db.Column(db.Float, nullable=True)
    NO3 = db.Column(db.Float, nullable=True)
    SO4 = db.Column(db.Float, nullable=True)
    Fe = db.Column(db.Float, nullable=True)
    Plume_state = db.Column(db.String(60), nullable=True)
    Chem_Group = db.Column(db.String(60), nullable=True)
    Country = db.Column(db.String(60), nullable=True)
    Literature_Source = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __ref__(self):
        return f'Database({self.id},{self.Site_Unit},{self.Aquifer_thickness},{self.Chem_Group},' \
               f'{self.Country},{self.Electron_Donor})'


class Liedl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Aquifer_thickness = db.Column(db.Float, nullable=False)
    Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Stoichiometry_coefficient = db.Column(db.Float, nullable=False)
    Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Reactant_Concentration = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'Liedl({self.id},{self.m},{self.tv},{self.a},{self.ca},{self.cd})'


class Chu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Width = db.Column(db.Float, nullable=False)
    Transverse_Horizontal_Dispersivity = db.Column(db.Float, nullable=False)
    Reaction_Stoichiometric_Ratio = db.Column(db.Float, nullable=False)
    Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Reactant_Concentration = db.Column(db.Float, nullable=False)
    Biological_Factor = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'Chu({self.id},{self.Width},{self.Transverse_Horizontal_Dispersivity},' \
               f'{self.Reaction_Stoichiometric_Ratio},{self.Contaminant_Concentration},' \
               f'{self.Reactant_Concentration},{self.Biological_Factor},{self.Model_Plume_Length},{self.user_id})'

class Bio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Threshold_Concentration = db.Column(db.Float, nullable=False)
    Time = db.Column(db.Float, nullable=False)
    Top_Source_Location = db.Column(db.Float, nullable=False)
    Input_Concentration = db.Column(db.Float, nullable=False)
    Source_Width = db.Column(db.Float, nullable=False)
    Average_Linear_Groundwater_Velocity = db.Column(db.Float, nullable=False)
    Longitudinal_Dispersivity = db.Column(db.Float, nullable=False)
    Horizontal_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Vertical_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Effective_Diffusion_Coefficient = db.Column(db.Float, nullable=False)
    R = db.Column(db.Float, nullable=False)
    Ga = db.Column(db.Float, nullable=False)
    La = db.Column(db.Float, nullable=False)
    M = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'Bio({self.id},{self.Threshold_Concentration},{self.Time},' \
               f'{self.Top_Source_Location},{self.Input_Concentration},{self.Source_Width}' \
               f'{self.Average_Linear_Groundwater_Velocity},{self.Longitudinal_Dispersivity},' \
               f'{self.Horizontal_Transverse_Dispersivity},{self.Vertical_Transverse_Dispersivity}' \
               f'{self.Effective_Diffusion_Coefficient},{self.R},{self.Ga},{self.La},{self.M})' \
               f'{self.Model_Plume_Length},{self.user_id})'



class Ham(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Width = db.Column(db.Float, nullable=False)
    Horizontal_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Reactant_Concentration = db.Column(db.Float, nullable=False)
    Gamma = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'Ham({self.id},{self.Width},{self.Horizontal_Transverse_Dispersivity},' \
               f'{self.Reaction_Stoichiometric_Ratio},' \
               f'{self.Contaminant_Concentration},{self.Reactant_Concentration})'


class Liedl3D(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Source_Thickness = db.Column(db.Float, nullable=False)
    Vertical_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Source_Width = db.Column(db.Float, nullable=False)
    Horizontal_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Stoichiometric_Ratio = db.Column(db.Float, nullable=False)
    Partner_Reactant_Concentration = db.Column(db.Float, nullable=False)
    Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Threshold_Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'Liedl3D({self.id},{self.Source_Thickness},{self.Vertical_Transverse_Dispersivity},' \
               f'{self.Horizontal_Transverse_Dispersivity},{self.Stoichiometric_Ratio},' \
               f'{self.Partner_Reactant_Concentration},{self.Contaminant_Concentration},' \
               f'{self.Threshold_Contaminant_Concentration})'


class Birla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Aquifer_thickness = db.Column(db.Float, nullable=False)
    Vertical_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Stoichiometry_coefficient = db.Column(db.Float, nullable=False)
    Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Reactant_Concentration = db.Column(db.Float, nullable=False)
    Recharge_Rate = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'Birla({self.id},{self.Aquifer_thickness},{self.Vertical_Transverse_Dispersivity},' \
               f'{self.Stoichiometry_coefficient},{self.Contaminant_Concentration},' \
               f'{self.Reactant_Concentration},{self.Recharge_Rate})'


class MaierGrathwohl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Aquifer_thickness = db.Column(db.Float, nullable=False)
    Vertical_Transverse_Dispersivity = db.Column(db.Float, nullable=False)
    Stoichiometry_coefficient = db.Column(db.Float, nullable=False)
    Contaminant_Concentration = db.Column(db.Float, nullable=False)
    Reactant_Concentration = db.Column(db.Float, nullable=False)
    Model_Plume_Length = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __ref__(self):
        return f'MaierGrathwohl({self.id},{self.Aquifer_thickness},{self.Vertical_Transverse_Dispersivity},' \
               f'{self.Stoichiometry_coefficient},{self.Contaminant_Concentration},{self.Reactant_Concentration})'

