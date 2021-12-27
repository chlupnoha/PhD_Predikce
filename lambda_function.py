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

    mix_design = {'CemType': event['CemType'],
                  'CemAmt': event['CemAmt'],
                  'FlyAsh': event['FlyAsh'],
                  'Limestone': event['Limestone'],
                  'Microsil': event['Microsil'],
                  'MicrosilSuspen': event['MicrosilSuspen'],
                  'CleanWater': event['CleanWater'],
                  'SludgeWater': event['SludgeWater'],
                  'Plast': event['Plast'],
                  'Superplast': event['Superplast'],
                  'AirEntrainer': event['AirEntrainer'],
                  'Retarder': event['Retarder'],
                  'Accelerator': event['Accelerator'],
                  'ShrinkageReducer': event['ShrinkageReducer'],
                  'Stabilizer': event['Stabilizer'],
                  'Crystalizer': event['Crystalizer'],
                  'SlumpRetention': event['SlumpRetention'],
                  'Agg_0_1': event['Agg_0_1'],
                  'Agg_0_2': event['Agg_0_2'],
                  'Agg_0_4': event['Agg_0_4'],
                  'Agg_4_6': event['Agg_4_6'],
                  'Agg_4_8': event['Agg_4_8'],
                  'Agg_8_16': event['Agg_8_16'],
                  'Agg_16_22': event['Agg_16_22'],
                  'PPFibres': event['PPFibres'],
                  'GlassFibres': event['GlassFibres'],
                  "Age": event['Age']
                  }

    df = pd.DataFrame(mix_design, index=[0])

    df = trans.DataTransformerPipeline.sum_water_agg_admix_add_fibres_microsil(df)
    df = trans.DataTransformerPipeline.drop_insignificant_variables(df)
    df = trans.DataTransformerPipeline.make_log_columns(df, ["CemAmt", "TotalWater"])
    df = trans.DataTransformerPipeline.make_interactions(df, "Age", ["CemType", "Age"])

    df.columns = [x for x in list(model_data.columns) if x not in ["ID", "fc_log"]]

    prediction = np.exp(trained_model.predict(df))[0].round(2)
    age = int(mix_design["Age"])
    predicton_RMSE = subRMSE[age]

    strengthMessage = f"Predicted compressive strength for given mix design: {prediction} MPa"
    errorMessage = f"Root mean squared error on the given day on model testing set was: {predicton_RMSE} MPa"

    return {
        'statusCode': 200,
        'body': predicton_RMSE,
        'strengthMessage': strengthMessage,
        'errorMessage': errorMessage,
        'event': event
    }
