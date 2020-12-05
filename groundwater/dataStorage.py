from groundwater.models import Liedl, Chu, Ham, Liedl3D, Birla, MaierGrathwohl, User_Database


def user_database(user_id):
    user_entry = User_Database.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in user_entry:
        table_data.append([
            data.id,
            data.Site_Unit,
            data.Compound,
            data.Aquifer_thickness,
            data.Plume_length,
            data.Plume_Width,
            data.Hydraulic_conductivity,
            data.Electron_Donor,
            data.O2,
            data.NO3,
            data.SO4,
            data.Fe,
            data.Plume_state,
            data.Chem_Group,
            data.Country,
            data.Literature_Source
        ])
    return table_data


def data_liedl(user_id):
    liedl = Liedl.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in liedl:
        table_data.append([
            data.id,
            data.Aquifer_thickness,
            data.Transverse_Dispersivity,
            data.Stoichiometry_coefficient,
            data.Contaminant_Concentration,
            data.Reactant_Concentration,
            data.Model_Plume_Length
        ])
    return table_data


def data_chu(user_id):
    chu = Chu.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in chu:
        table_data.append([
            data.id,
            data.Width,
            data.Transverse_Horizontal_Dispersivity,
            data.Reaction_Stoichiometric_Ratio,
            data.Contaminant_Concentration,
            data.Reactant_Concentration,
            data.Biological_Factor,
            data.Model_Plume_Length
        ])
    return table_data

def data_Bio(user_id):
    bio = Bio.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in bio:
        table_data.append([
            data.id,
            data.Threshold_Concentration,
            data.Time,
            data.Top_Source_Location,
            data.Input_Concentration,
            data.Source_Width,
            data.Average_Linear_Groundwater_Velocity,
            data.Longitudinal_Dispersivity,
            data.Horizontal_Transverse_Dispersivity,
            data.Vertical_Transverse_Dispersivity,
            data.Effective_Diffusion_Coefficient,
            data.R,
            data.Ga,
            data.La,
            data.M,
            data.Model_Plume_Length
        ])
    return table_data

def data_ham(user_id):
    ham = Ham.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in ham:
        table_data.append([
            data.id,
            data.Width,
            data.Horizontal_Transverse_Dispersivity,
            data.Contaminant_Concentration,
            data.Reactant_Concentration,
            data.Gamma,
            data.Model_Plume_Length
        ])
    return table_data


def data_liedl3d(user_id):
    liedl3d = Liedl3D.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in liedl3d:
        table_data.append([
            data.id,
            data.Source_Thickness,
            data.Vertical_Transverse_Dispersivity,
            data.Source_Width,
            data.Horizontal_Transverse_Dispersivity,
            data.Stoichiometric_Ratio,
            data.Partner_Reactant_Concentration,
            data.Contaminant_Concentration,
            data.Threshold_Contaminant_Concentration,
            data.Model_Plume_Length
        ])
    return table_data


def data_birla(user_id):
    birla = Birla.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in birla:
        table_data.append([
            data.id,
            data.Aquifer_thickness,
            data.Vertical_Transverse_Dispersivity,
            data.Stoichiometry_coefficient,
            data.Contaminant_Concentration,
            data.Reactant_Concentration,
            data.Recharge_Rate,
            data.Model_Plume_Length
        ])
    return table_data


def data_maiergrathwohl(user_id):
    maier = MaierGrathwohl.query.filter_by(user_id=user_id).all()
    table_data = []
    for data in maier:
        table_data.append([
            data.id,
            data.Aquifer_thickness,
            data.Vertical_Transverse_Dispersivity,
            data.Stoichiometry_coefficient,
            data.Contaminant_Concentration,
            data.Reactant_Concentration,
            data.Model_Plume_Length
        ])
    return table_data
