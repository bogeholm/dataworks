import numpy as np

def shuffle_predict(model, X_data, y_data):
    """ Shuffle columns of X_data one at a time, and predict with model
    """
    columns = X_data.columns.values
    n_columns = len(columns)
    
    # Prepare OrderedDict with return values
    resdict = OrderedDict()
    resdict['column'] = columns
    
    r2_vals = np.zeros(n_columns)
    rmse_vals = np.zeros(n_columns)
    X_shuffle = X_data.copy(deep=True)
    
    # Predict before and after to make sure we shuffled correctly
    pred_before = model.predict(X_shuffle)
    
    X_shuffle.head()
    
    for idx, colname in enumerate(columns[0:5]):
        # Pick out a column and shuffle it
        org_col = X_shuffle[colname]
        shuffle_col = np.copy(org_col)
        np.random.shuffle(shuffle_col)
        
        # Replace column temporarily
        X_shuffle[colname] = shuffle_col
        # Predict with one column shuffled 
        shuffle_predict = model.predict(X_shuffle)
        
        # R squared and RMSE
        r2_vals[idx] = r2_score(shuffle_predict, y_data)
        rmse_vals[idx] = rmse(shuffle_predict, y_data)
        
        # Put original column back!
        X_shuffle[colname] = org_col
        
    # Test our shuffling abilities
    pred_after = model.predict(X_shuffle)
    assert np.allclose(pred_before, pred_after), f'Before: {pred_before[0:5]}..., after: {pred_after[0:5]}...'
    
    resdict['r2'] = r2_vals
    resdict['rmse'] = rmse_vals
    return pd.DataFrame(resdict)
    