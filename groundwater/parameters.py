class Parameters:
    User_data_columns = [
        'ID',
        'Site Unit',
        'Compound',
        'Aquifer Thickness',
        'Plume Length',
        'Plume Width',
        'Hydraulic Conductivity',
        'Electron Donor',
        'Electron Acceptors : O2[mg/l]',
        'NO3',
        'SO4',
        'Fe',
        'Plume State',
        'Chemical Group',
        'Country',
        'Literature Source'
    ]
    Liedl_data_columns = [
        'ID',
        'Aquifer Thickness',
        'Transverse Dispersivity',
        'Stoichiometry coefficient',
        'Contaminant Concentration',
        'Reactant Concentration',
        'Model Plume Length'
    ]
    Chu_data_columns = [
        'ID',
        'Width',
        'Transverse Horizontal Dispersivity',
        'Reaction Stoichiometric Ratio',
        'Contaminant Concentration',
        'Reactant Concentration',
        'Biological Factor',
        'Model Plume Length'
    ]
    Bio_data_columns = [
        'ID',
        'Threshold Concentration',
        'Time',
        'Source Thickness',
        'Source Concentration',
        'Source Width',
        'Average Linear Groundwater Velocity',
        'Longitudinal Dispersivity',
        'Horizontal Transverse Dispersivity',
        'Vertical Transverse Dispersivity',
        'Effective Diffusion Coefficient',
        'Retardation Factor',
        'Source Decay Coefficient',
        'Effective first-order Decay Coefficient',
        'Number of Gauss points',
        'Model Plume Length'
    ]
    Ham_data_columns = [
        'ID',
        'Width',
        'Horizontal Transverse Dispersivity',
        'Contaminant Concentration',
        'Gamma',
        'Reactant Concentration',
        'Model Plume Length'
    ]
    Liedl3d_data_columns = [
        'ID',
        'Source Thickness',
        'Vertical Transverse Dispersivity',
        'Source Width',
        'Horizontal Transverse Dispersivity',
        'Stoichiometric Ratio',
        'Partner Reactant Concentration',
        'Contaminant Concentration',
        'Threshold Contaminant Concentration',
        'Model Plume Length'
    ]
    Birla_data_columns = [
        'ID',
        'Aquifer Thickness',
        'Vertical Transverse Dispersivity',
        'Stoichiometry coefficient',
        'Contaminant Concentration',
        'Reactant Concentration',
        'Recharge Rate',
        'Model Plume Length'
    ]
    Maiergrathwohl_data_columns = [
        'ID',
        'Aquifer Thickness',
        'Vertical Transverse Dispersivity',
        'Stoichiometry coefficient',
        'Contaminant Concentration',
        'Reactant Concentration',
        'Model Plume Length'
    ]

    class Extensions:
        ALLOWED_EXTENSIONS = ['csv']
