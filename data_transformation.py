import numpy as np

class DataTransformator:
    
    @classmethod
    def sum_columns(cls,df,new_col,col_list):
        df[new_col] = df[col_list].sum(axis=1)
        return df
    
    @classmethod
    def make_ratios(cls,df,col1,col2):
        if (col1+"/"+col2) not in list(df.columns):
            df[col1+"/"+col2] = (df[col1] / df[col2])
        return df
    
    @classmethod
    def make_product(cls,df,col1,col2):
        df[f"{col1}*{col2}"] = df[col1]*df[col2]
        
        return df

class DataTransformatorPipeline:
    
    water_cols = ["CleanWater","SludgeWater"]
    fineAgg_cols = ['Agg_0_1', 'Agg_0_2','Agg_0_4',"Agg_4_6",'Agg_4_8']
    coarseAgg_cols = ['Agg_8_16','Agg_16_22']
    admixtures_cols = ['Plast','Superplast','AirEntrainer',
                  'Retarder','Accelerator','ShrinkageReducer',
                  'Stabilizer','Crystalizer','SlumpRetention']
    additives_cols = ['FlyAsh','Limestone','Microsil','MicrosilSuspen']
    fibres_cols = ["PPFibres","GlassFibres"]
    microsil_cols = ["Microsil","MicrosilSuspen"]
    
    col_to_sum = {"TotalWater" : water_cols,
        "FineAgg" : fineAgg_cols,
        "CoarseAgg" : coarseAgg_cols,
        "Admixtures" : admixtures_cols,
        "Additives" : additives_cols,
        "Fibres" : fibres_cols,
        "Microsil_MicrosilSuspen" : microsil_cols}
    
    @classmethod
    def sum_water_agg_admix_add_fibres_microsil(cls,df):
        """Sums explanatory variables into aggregated variables.
            Parameters:
                df (DataFrame): DataFrame containing the data for modeling

            Returns:
                df (DataFrame): DataFrame with aggregated variables into water, fine aggregates, coarse aggregates, 
                admixtures, additives, fibres, and microsilica. 
                The original variables are droped from the DataFrame apart from admixtures and additives.
        """
        for k,v in DataTransformatorPipeline.col_to_sum.items():
            df = DataTransformator.sum_columns(df,k,v)
        cols_to_drop = (DataTransformatorPipeline.water_cols + DataTransformatorPipeline.fineAgg_cols +
        DataTransformatorPipeline.coarseAgg_cols + DataTransformatorPipeline.fibres_cols + DataTransformatorPipeline.microsil_cols)
        try:
            df.drop(columns=cols_to_drop,inplace=True)
        except KeyError:
            print("Some of the aggregating variables are not in the DataFrame.")
        else:
            print("Variables were aggregated and selected dropped.")
        finally:
            return df
    
    @classmethod
    def drop_insignificant_variables(cls,df):
        """Drops variables with insignificant impact on the compressive strength.
            Parameters:
                df (DataFrame): DataFrame containing the data for modeling

            Returns:
                df (DataFrame): DataFrame with droped addmixtures: 
                                shrinkage-reducing, stabilizating, slump retention, and crystalizing
        """
        try:
            df.drop(columns=['ShrinkageReducer','Stabilizer','SlumpRetention',"Crystalizer"],inplace=True)
        except KeyError:
            print("Insignificant variables are not in the DataFrame.")
        else:
            print("Insignificant variables ('ShrinkageReducer','Stabilizer','SlumpRetention','Crystalizer') were dropped.")
        finally:
            return df
        
    @classmethod
    def make_log_columns(cls,df,cols):
        """Makes logarithm of selected variables.
            Parameters:
                df (DataFrame): DataFrame containing the data for modeling

            Returns:
                df (DataFrame): DataFrame with log() selected columns: 
                                Original variables are dropped.                    
        """
        try:
            new_cols = [(col+"_log") for col in cols]
            df[new_cols] = df[cols].applymap(lambda x: np.log(x))
            df.drop(columns=cols,inplace=True)
        except KeyError:
            print("Variables are not in the DataFrame.")
        else:
            print(f"{cols} variables were logarithmized and original variables dropped.")
        finally:
            return df
    
        
    @classmethod
    def make_interactions(cls,df,inter_col,except_cols):
        """Makes interaction between selected variables and all variables apart from selected ones.
            Parameters:
                df (DataFrame): DataFrame containing the data for modeling

            Returns:
                df (DataFrame): DataFrame with new interaction variables.
                                Products of selected variable and all others expect selected ones.
                                Original variabels are dropped (only products remain).
        """
        try:
            product_variables = [col for col in df if col not in except_cols]
            for col in product_variables:
                df = DataTransformator.make_product(df,inter_col,col)
            df.drop(columns=(product_variables), inplace=True)
        except KeyError:
            print("Some of the variables are not in the DataFrame.")
        else:
            print(f"Interactions (product) of {inter_col} and all variables apart from {except_cols} were made and original variables dropped.")
        finally:
            return df

    