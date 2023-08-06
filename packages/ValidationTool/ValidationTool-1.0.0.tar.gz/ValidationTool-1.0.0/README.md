Function List:
    update_progress(job_title, progress):
        show status bar of long process. Operation purpose
        
    SummarizeDefault(raw_data,default_flag_column,by_vars,plot=False,continuous_var=False,n_bin=10):
        Summarize default data by different variables
        
        raw_data: pandas.DataFrame. The dataset contains the default column and groupby variable
        default_flag_column: String. column name of the default flag in dataset
        by_vars: String. Column name of the groupby variable
        continuous_var: Boolean. Default as False. If select as True, function will bucket the variable to do groupby.
        n_bin: int. If contunuous_var is set as True, function will bucket the variable into "n_bin" bins
        plot: Boolean. Default as False. If select True, function will generate graph
        
        return a DataFrame
    
    CalcROCPrep(s, default_flag_data):
        Preparation for ROC calculation. Not directly into result
        
    CalcROCStats(s,default_flag_data):
        Calculation of ROC stats
        s: pandas.DataFrame. Score generated from regression model
        default_flag_data: pandas.Dataframe. Default flag data from real transactions.
        
        return a dictionary of 3 stats
        
    CalcPredAccuracy(s,default_flag_data,n_bin=10,plot=False,is_default_rate=True):
        Compare the generated default probability with real default flag
        s: pandas.DataFrame. Score generated from regression model
        default_flag_data: pandas.Dataframe. Default flag data from real transactions.
        n_bin: int. default flag will be grouped into "n_bin" bins
        plot: Boolean. Default as False. If select True, function will generate graph
        is_default_rate. Boolean. Default as True. Select False only if this function is used to compare two series that are NOT between (0,1)
        
        return dataframe of bucket score VS actual default
        
                    CalcModelROC(raw_data,response_var,explanatory_var_1,explanatory_var_2="",explanatory_var_3="",explanatory_var_4="",explanatory_var_5="",explanatory_var_6="",explanatory_var_7="",explanatory_var_8="",explanatory_var_9="",explanatory_var_10=""):
        Directly generate ROC stats from a given model. Not suggested to use because of explanatory variable number limitation.
        raw_data: pandas.DataFrame. The dataset contains all variables used in model generation.
        response_var: string. Column name of response var.
        explanatory_var_1:string. Column name of response var.
        explanatory_var_2-10:string.Optional. Column name of response var.
        
        return dataframe
    
    CalcWOE_IV(data,default_flag_column,categorical_column,event_list=[1,"Yes"],continuous_variable=False,n_bucket=10):
        Calculate IV of each variable
        Calculation refer to: https://www.listendata.com/2015/03/weight-of-evidence-woe-and-information.html
        data: pandas.DataFrame. dataset that contains all variables
        default_flag_column: String. column name of the default flag in dataset
        categorical_column:String. column name of the categorical column
        continuous_var: Boolean. Default as False. If select as True, function will bucket the variable to do groupby.
        n_bin: int. If contunuous_var is set as True, function will bucket the variable into "n_bin" bins
        event_list: list. The list contains all possibility than can be considered as "event"
        
        return [IV value of certain variable, table of calculation]
    
    PerformRandomCV(data,response_var,explanatory_var_list=[],k=20,plot=True,sampling_as_default_percentage=False):
        Do Random Cross Validation of model to check model stability. 
        Return standard deviation of each coefficients.
        raw_data: pandas.DataFrame. The dataset contains all variables used in model generation.
        response_var: string. Column name of response var.
        explanatory_var_list: list. List of all names of explanatory variables
        k: int. 1/k samples will be eliminated as train set.
        plot: Boolean. Default as True. Plot std. dev of each coefficient.
        sampling_as_default_percentage: Boolean. Default as False. If selected as True, sampling will be done as the default rate.
        
        return std.dev of coefficients during k-time regression
        
    PerformK_Fold(data,response_var, explanatory_var_list=[],k=10):
        Perform k-fold cross validation
        data: pandas.DataFrame. dataset that contains all variables.
        response_var: string. column name of response variable
        explanatory_var_list: list of strings. list that contains all explanatory variables
        
        return array of each fold score
        
    BestSubsetSelection(data,response_var,explanatory_var_list=[],plot=True):
        Run best subset selection
        data: pandas.DataFrame. raw dataset
        response_var: string. Column name of response var
        explanatory_var_list: list of string. Names of columns of all explanatory candidates.
        plot: If selected as True, it will plot the selection steps graph.
        
        return all combinations' RSS and R_squared
        
    ForwardStepwiseSelection(data,response_var,explanatory_var_list=[],plot=True):
        Do forward stepwise selection
        data: pandas.DataFrame. raw dataset
        response_var: string. Column name of response var
        explanatory_var_list: list of string. Names of columns of all explanatory candidates.
        plot: if selected as True, it will plot the selection steps graph
        
        return dataframe with AIC,BIC,R_squared of each variable combination
        
    CalcSpearmanCorrelation(data,var_1,var_2):
        Calculate spearman Correlation
        data: pandas.DataFrame. Contains var_1 and var_2
        var_1,var_2: string. column name of var_1 and var_2
        
        return float

    CalcKendallTau(data,var_1,var_2):
        Calculate KendallTau
        data: pandas.DataFrame. Contains var_1 and var_2
        var_1,var_2: string. column name of var_1 and var_2
        
        return float
        
    CalcSamplingGoodmanKruskalGamma(data,var_1, var_2,n_sample=1000):
        Calculate GoodmanKruskalGamma estimator with sampling data. Not suggest to use into report as this is just an estimator.
        data: pandas.DataFrame. Contains var_1 and var_2
        var_1,var_2: string. column name of var_1 and var_2
        
        return float
    
    CalcSomersD(data,var_1,var_2):
        Calculate Somers' D
        data: pandas.DataFrame. Contains var_1 and var_2
        var_1,var_2: string. column name of var_1 and var_2
        
        return float
        
    GenerateRankCorrelation(data,var_1,var_2):
        Calculate all 4 ranked correlation.
        data: pandas.DataFrame. Contains var_1 and var_2
        var_1,var_2: string. column name of var_1 and var_2. The order of var_1 and var_2 can not change.
        
        return float
		
		
	OLSForwardStepwise(data,response_var,explanatory_var_list=[],plot=True):
		Perform forward stepwise selection for OLS regression