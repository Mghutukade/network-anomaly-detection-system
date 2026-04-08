# Hybrid model 
final_pred = []

for rf_p, iso_p in zip(rf_pred, y_pred_iso):
    if rf_p == 1 or iso_p == 1:
        final_pred.append(1)
    else:
        final_pred.append(0)