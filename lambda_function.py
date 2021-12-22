import _pickle as cPickle
import data_transformation as trans
import pandas as pd
import numpy as np

with open(r"trained_model_metrics.pickle", "rb") as input_file:
    trained_model_metrics = cPickle.load(input_file)
        
def lambda_handler(event, context):
    trained_model = trained_model_metrics["model"]
    subMSE = trained_model_metrics["MSE"]
    subRMSE = trained_model_metrics["RMSE"]
    model_data = trained_model_metrics["data"]
    
    #Possible cement types
    model_data["CemType"].unique()
    
    #Possible age from casting
    model_data["Age"].unique()
    
    mix_design = {'CemType' : "CEM I 42,5 R",
              'CemAmt' : 400, 
              'FlyAsh' : 0,
              'Limestone' : 0, 
              'Microsil' : 0,
              'MicrosilSuspen' : 0, 
              'CleanWater' : 100, 
              'SludgeWater' : 80, 
              'Plast' : 0, 
              'Superplast' : 3.0,
              'AirEntrainer' : 0.6, 
              'Retarder' : 0, 
              'Accelerator' : 0, 
              'ShrinkageReducer' : 0,
              'Stabilizer': 0, 
              'Crystalizer': 0, 
              'SlumpRetention' : 0, 
              'Agg_0_1' : 0, 
              'Agg_0_2': 0,
              'Agg_0_4' : 780, 
              'Agg_4_6' : 0, 
              'Agg_4_8' : 0, 
              'Agg_8_16' : 1020, 
              'Agg_16_22' : 0, 
              'PPFibres' : 0,
              'GlassFibres' : 0, 
              "Age": 2
             }
             
    df = pd.DataFrame(mix_design,index=[0])
    
    df = trans.DataTransformerPipeline.sum_water_agg_admix_add_fibres_microsil(df)
    df = trans.DataTransformerPipeline.drop_insignificant_variables(df)
    df = trans.DataTransformerPipeline.make_log_columns(df,["CemAmt","TotalWater"])
    df = trans.DataTransformerPipeline.make_interactions(df,"Age",["CemType","Age"])
    
    df.columns = [x for x in list(model_data.columns) if x not in ["ID","fc_log"]]
    
    prediction = np.exp(trained_model.predict(df))[0].round(2)
    age = int(mix_design["Age"])
    predicton_RMSE = subRMSE[age]
    
    print(event)
    return {
        'statusCode': 200,
        'body': predicton_RMSE,
        'zkouska' : "karel"
    }

