import logging
from Predictor import Predictor
from functools import partial
import numpy as np

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S', level=logging.DEBUG)

def abs_log(x):
    return np.abs(np.log(x))

def mult_abs_log(coeff):
    return np.abs(np.log(x))*coeff

def decorate_mult_abs_log(func,coeff):
    result = partial(func,coeff=coeff)
    result.__name__ = str(coeff) + func.__name__
    return result

contact_type = ["oe","contacts"]
suffix = ".gz.1000000.50001.500000.25000.txt"
training_file = "out/2018-09-24-trainingOrient.RandOnChr1."
validation_files = [
    "out/Interval_chr2_36000000_41000000validatingOrient.",
    "out/Interval_chr2_47900000_53900000validatingOrient.",
    "out/Interval_chr2_85000000_92500000validatingOrient."
            ]


#Some examples of predictors filtering:
#predictor.filter_predictors(".*CTCF.*|.*RNA.*", keep=False) #-- discard CTCF AND RNA
#predictor.filter_predictors(".*CTCF.*", keep=False) #-- discard CTCF
#predictor.filter_predictors(".*contact_dist.*|.*CTCF_W.*", keep=True) #-- keep only distance and CTCF in window

for contact_type,apply_log in zip(["contacts","oe"],[True,False]):
#for contact_type,apply_log in zip(["oe"],[False]):
    for (filter,keep),shortcut in zip(zip([".*","E1"],[True,False]),
                                           ["all","no E1"]):
        if contact_type == "oe":
            weightFuncs = [np.ones_like, np.array, abs_log, decorate_mult_abs_log(mult_abs_log,100),
                           decorate_mult_abs_log(mult_abs_log,10000)]
        else:
            weightFuncs = [np.ones_like]
        for weightFunc in weightFuncs:
            predictor = Predictor()
            predictor.read_data_predictors(training_file + contact_type + suffix)
            predictor.filter_predictors(filter, keep)
            trained_predictor = predictor.train(shortcut=shortcut, apply_log = apply_log,
                                                weightsFunc = weightFunc, show_plot=True)
            trained_predictor.out_dir = "out/models/"
            trained_predictor.draw_Feature_importances()
            #for validation_file in validation_files:
            #    trained_predictor.validate(validation_file + contact_type + suffix,
            #                               show_plot = False)

