from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, Float, ForeignKey, insert, text
import geopandas as gpd

metadata = MetaData()
metadata.reflect(bind=engine)  # récupère toutes les tables

for table_name in metadata.tables:
    print("Table:", table_name)
    table = metadata.tables[table_name]
    # for column in table.columns:
    #     print(" -", column.name, column.type)

with engine.connect() as conn:
    projections = pd.read_sql(f"SELECT * FROM projections", conn)
    stations = pd.read_sql(f"SELECT * FROM stations", conn)
    variables = pd.read_sql(f"SELECT * FROM variables", conn)

# Visualize a table as DataFrame
table_name = "delta_historical_rcp85_qa_h3"
table = metadata.tables[table_name]
for column in table.columns:
    print(" -", column.name, column.type)
with engine.connect() as conn:
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

# Format data
indicators = {'deltaQA': 'QA', 'deltaQJXA': 'QJXA', 'deltaVCN10': 'VCN10_summer'}

for indicator, indicator_name in indicators.items():
    print(indicator)
    data_path = f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/hydrological-projections_changes-by-warming-level_by-variable_filtered-fst/{indicator}.csv'

    data = pd.read_csv(data_path, sep=';', index_col=0)

    data = data.merge(stations[['code', 'n']], on='code', how='left')
    data = data.rename(columns={'EXP': 'exp', 'GCM': 'gcm', 'RCM': 'rcm', 'BC': 'bc', 'HM': 'hm', 'GWL': 'gwl',
                        f'delta{indicator_name}': 'value'})
    data['chain'] = data[['exp', 'gcm', 'rcm', 'bc', 'hm']].astype(str).agg('_'.join, axis=1)

    gwl = ['GWL-15', 'GWL-20', 'GWL-30']
    for current_gwl in gwl:
        print(current_gwl)
        # current_gwl = gwl[0]
        data['variable_en'] = f'{indicator_name}_{current_gwl}'

        current_data = data[data['gwl'] == current_gwl]
        current_data = current_data.reset_index(drop=True)
        current_data = current_data.rename_axis('id')

        table_name = f"delta_historical_rcp85_{indicator_name.lower()}_{''.join(current_gwl.lower().split('-'))}"

        with engine.connect() as conn:
            conn.execute(text(f'DROP TABLE IF EXISTS narratracc;'))
            conn.commit()

        current_data.to_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/{table_name}.csv', sep=';')

        current_data.to_sql(table_name, engine, index=True, if_exists="replace")  
 
# GeoDataframe for Regions
gdf = gpd.read_file("static/data/regions.geo.json")
gdf_proj = gdf.to_crs(epsg=3857) 

# 4. Calculer l'aire en km²
gdf["surface_km2"] = gdf_proj.area / 1e6 
gdf['name'] = gdf['name'].str.replace('-', '_', regex=False)

def find_matching_name(code, name_list):
    for name in name_list:
        fragments = name.split('_')  
        for frag in fragments:
            if code.startswith(frag):
                return name
    return None

name_list = gdf["name"].tolist()

explore2_stations = pd.read_csv('/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/stations_Explore2_louis.csv', sep=',')

explore2_stations["region_id"] = explore2_stations["code"].apply(lambda c: find_matching_name(c, name_list))

# Create Regions table
regions = gdf[['name', 'surface_km2']]
regions = regions.rename(columns={'name': 'region_id'})

region_n_points = explore2_stations.groupby(['region_id'])['n'].size().reset_index(name="region_n_points")
regions = regions.merge(region_n_points, on="region_id", how="left")
regions.columns = [col.lower() for col in regions.columns]
explore2_stations.columns = [col.lower() for col in explore2_stations.columns]

# Put Regions & Stations to DB
regions.to_sql('regions', engine, index=False, if_exists="replace") 
regions.to_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/regions.csv', sep=';')
explore2_stations.to_sql("stations", con=engine, if_exists="replace", index=False)
explore2_stations.to_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/explore2_stations.csv', sep=';')

# Narratracc tables
narratracc = pd.read_csv('/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/families.csv', sep=';')
narratracc.columns = [col.lower() for col in narratracc.columns]
narratracc[['gcm', 'rcm']] = narratracc['gcm-rcm'].str.split('_', expand=True)

gwl_dict = {"horizon1": 'gwl15', "horizon2": 'gwl20', "horizon3": 'gwl30'}
narratracc['gwl'] = narratracc['horizon'].map(gwl_dict)

narratracc = narratracc[['gwl', 'region', 'gcm', 'rcm', 'bc', 'hm', 'sous-famille', 'sous-famille_description', 'narratif_id', 'narratif_description', 'narratif_couleur']]
narratracc = narratracc.rename(columns={'sous-famille': 'famille', 'sous-famille_description': 'famille_description'})
narratracc.to_sql("narratracc", con=engine, if_exists="replace", index=False)
narratracc.to_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/narratracc.csv', sep=';')


### Generate Tables
metadata = MetaData()

regions_table = Table(
    'regions', metadata,
    Column('region_id', String(255), primary_key=True),
    Column('surface_km2', Float, nullable=False),
    Column('region_n_points', Integer, nullable=False)
)

# Crée physiquement la table dans la base
metadata.create_all(engine)

regions = pd.read_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/regions.csv', sep=';', index_col=0)

regions.to_sql("regions", con=engine, if_exists="append", index=False)

explore2_stations = pd.read_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/explore2_stations.csv', sep=';', index_col=0)
explore2_stations = explore2_stations.set_index('code').loc[stations['code']].reset_index()
explore2_stations = explore2_stations.rename(columns={'name_regions': 'region_id'})

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE stations
        ADD COLUMN region_id VARCHAR(255);
    """))

for _, row in explore2_stations.iterrows():
    code = row["code"]
    region_id = row["region_id"]
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE stations
            SET region_id = :region_id
            WHERE code = :code;
        """), {"region_id": region_id, "code": code})

with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE stations
        ADD CONSTRAINT fk_region
        FOREIGN KEY (region_id)
        REFERENCES regions(region_id);
    """))

df_narratracc = pd.read_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/narratracc.csv', sep=';', index_col=0)
df_narratracc["region"] = df_narratracc["region"].str.replace('-', '_', regex=False)
df_narratracc = df_narratracc.rename(columns={'region': 'region_id', 'famille': 'famille_id'})
df_narratracc = df_narratracc.reset_index()
df_narratracc.rename(columns={"index": "id"}, inplace=True)
df_narratracc['exp'] = 'historical-rcp85'
df_narratracc['chain'] = df_narratracc[['exp', 'gcm', 'rcm', 'bc', 'hm']].astype(str).agg('_'.join, axis=1)
df_narratracc.loc[:, 'id'] = range(1, len(df_narratracc) + 1)
df_narratracc = df_narratracc.reset_index(drop=True)

narratracc_table = Table(
    'narratracc', metadata,
    Column('id', Integer, primary_key=True),
    Column('region_id', String(255), ForeignKey('regions.region_id'), nullable=False),
    Column('gwl', String(255), nullable=False),
    Column('chain', String(255), ForeignKey('projections.chain'), nullable=False),
    Column('exp', String(255), nullable=False),
    Column('gcm', String(255), nullable=False),
    Column('rcm', String(255), nullable=False),
    Column('bc', String(255), nullable=False),
    Column('hm', String(255), nullable=False),
    Column('famille_id', String(255), nullable=False),
    Column('famille_description', String(255), nullable=False),
    Column('narratif_id', String(255), nullable=False),
    Column('narratif_description', String(255), nullable=False),
    Column('narratif_couleur', String(255), nullable=False),
)

metadata.create_all(engine)

df_narratracc.to_sql("narratracc", con=engine, if_exists="append", index=False)


# Data Tables
filter_data = pd.read_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/code_Chain_outliers_Explore2.csv')
filter_data = filter_data[(filter_data['EXP'] == 'historical-rcp85') & (filter_data['BC'] == 'ADAMONT')]
filter_data['chain'] = filter_data[['EXP', 'GCM', 'RCM', 'BC', 'HM']].astype(str).agg('_'.join, axis=1)
exclusions = set(zip(filter_data['code'], filter_data['chain']))

# df[(df['code'] == 'A107020001') & (df['chain'] == 'historical-rcp85_CNRM-CM5_ALADIN63_ADAMONT_CTRIP')]

for indicator, indicator_name in indicators.items():
    print(indicator)
    
    for current_gwl in gwl:
        print(current_gwl)

        variable_en = f"delta{indicator_name}_{''.join(current_gwl.lower().split('-'))}"

        variables = Table('variables', metadata, autoload_with=engine)
        with engine.connect() as conn:
            df_variables = pd.read_sql(f"SELECT * FROM variables", conn)
        temperature = f"{current_gwl.split('-')[-1][0]}.{current_gwl.split('-')[-1][-1]}"

        if variable_en not in df_variables['variable_en']:
            ref_variable = df_variables[df_variables['variable_en'] == f"delta{indicator_name}_H3"]
            
            new_row = {
                'variable_en': variable_en, 
                'unit_en': ref_variable['unit_en'].values[0], 
                'name_en': ref_variable['name_en'].iloc[0].replace("the distant horizon", f"France with a warming level of +{temperature}°C") ,
                'description_en': ref_variable['description_en'].values[0], 
                'method_en': ref_variable['method_en'].values[0],
                'sampling_period_en': ref_variable['sampling_period_en'].values[0], 
                'topic_en': ref_variable['topic_en'].values[0], 
                'variable_fr': ref_variable['variable_fr'].values[0], 
                'unit_fr': ref_variable['unit_fr'].values[0], 
                'name_fr': ref_variable['name_fr'].iloc[0].replace("l'horizon lointain", f"une France à +{temperature}°C"),
                'description_fr': ref_variable['description_fr'].values[0], 
                'method_fr': ref_variable['method_fr'].values[0], 
                'sampling_period_fr': ref_variable['sampling_period_fr'].values[0], 
                'topic_fr': ref_variable['topic_fr'].values[0],
                'is_date': ref_variable['is_date'].values[0], 
                'to_normalise': ref_variable['to_normalise'].values[0], 
                'palette': ref_variable['palette'].values[0]
            }
            stmt = insert(variables).values(new_row)
            with engine.begin() as conn:
                conn.execute(stmt)

        table_name = f"delta_historical_rcp85_{indicator_name.lower()}_{''.join(current_gwl.lower().split('-'))}"
        current_data = pd.read_csv(f'/media/bcalmel/One Touch/2_Travail/3_INRAE_EHCLO/20_data/Explore2/meandre_tables/{table_name}.csv', sep=';')
        current_data['variable_en'] = variable_en
        couples_data = pd.Series(list(zip(current_data['code'], current_data['chain'])))
        current_data = current_data[~couples_data.isin(exclusions)]
        current_data.loc[:, 'id'] = range(1, len(current_data) + 1)
        current_data = current_data.reset_index(drop=True)
        current_data["region_id"] = current_data["code"].apply(lambda c: find_matching_name(c, name_list))

        data_table = Table(
            table_name, metadata,
            Column('id', Integer, primary_key=True),
            Column('gwl', String(255), nullable=False),
            Column('chain', String(255), ForeignKey('projections.chain'), nullable=False),
            Column('exp', String(255), nullable=False),
            Column('gcm', String(255), nullable=False),
            Column('rcm', String(255), nullable=False),
            Column('bc', String(255), nullable=False),
            Column('hm', String(255), nullable=False),
            Column('code', String(255), nullable=False),
            Column('region_id', String(255), ForeignKey('regions.region_id'), nullable=False),
            Column('n', Integer, nullable=False),
            Column('value', Float, nullable=False),
            Column('variable_en', String(255), ForeignKey('variables.variable_en'), nullable=False),
            )

        metadata.create_all(engine)
        
        current_data.to_sql(table_name, con=engine, if_exists="append", index=False)


with engine.connect() as conn:
    df = pd.read_sql(f"SELECT * FROM variables", conn)

metadata = MetaData()
metadata.reflect(bind=engine) 
table = metadata.tables['narratracc']