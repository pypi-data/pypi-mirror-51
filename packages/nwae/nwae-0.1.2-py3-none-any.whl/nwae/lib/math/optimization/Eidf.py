# -*- coding: utf-8 -*-

import nwae.utils.Log as lg
from inspect import currentframe, getframeinfo
import numpy as np
import pandas as pd
import nwae.lib.math.NumpyUtil as nputil
import random as rd
import nwae.lib.math.Cluster as cl


#
# Enhanced IDF (EIDF)
#
# Given a set of vectors v1, v2, ..., vn with features f1, f2, ..., fn
# We try to find weights w1, w2, ..., wn or in NLP notation known as IDF,
# such that the separation (default we are using angle) between the vectors
# v1, v2, ... vn by some metric (default metric is the 61.8% quantile) is
# maximum when projected onto a unit hypersphere.
#
class Eidf:

    # General number precision required
    ROUND_PRECISION = 6

    #
    # We maximize by the 50% quantile, so that given all distance pairs
    # in the vector set, the 50% quantile is optimized at maximum
    #
    MAXIMIZE_QUANTILE = 2/(1+5**0.5)
    #
    MAXIMUM_IDF_W_MOVEMENT = 1.0
    # Don't set to 0.0 as this might cause vectors to become 0.0
    MINIMUM_WEIGHT_IDF = 0.01
    # delta % of target function start value
    DELTA_PERCENT_OF_TARGET_FUNCTION_START_VALUE = 0.01

    #
    # Monte Carlo start points
    #
    MONTE_CARLO_SAMPLES_N = 100

    #
    # This is the fast closed formula calculation of target function value
    # otherwise the double looping exact calculation is unusable
    #
    TARGET_FUNCTION_AS_SUM_COSINE = True

    #
    # If too many rows in the array, the normalize() function will be too slow
    # so we cluster them
    #
    MAX_X_ROWS_BEFORE_CLUSTER = 500

    #
    # Given our training data x, we get the IDF of the columns x_name.
    # TODO Generalize this into a NN Layer instead
    # TODO Optimal values are when "separation" (by distance in space or angle in space) is maximum
    #
    @staticmethod
    def get_feature_weight_idf_default(
            x,
            # Class label, if None then all vectors are different class
            y,
            # Feature name, if None then we use default numbers with 0 index
            x_name,
            feature_presence_only_in_label_training_data = False
    ):
        if feature_presence_only_in_label_training_data:
            df_tmp = pd.DataFrame(data=x, index=y)
            # Group by the labels y, as they are not unique
            df_agg_sum = df_tmp.groupby(df_tmp.index).sum()
            # No need a copy, the dataframe will create a new copy already from original x
            np_agg_sum = df_agg_sum.values
        else:
            # No need to group, each row is it's own document
            np_agg_sum = x.copy()

        # Just overwrite inline, don't copy
        np.nan_to_num(np_agg_sum, copy=False)

        # Get presence only by cell, then sum up by columns to get total presence by document
        np_feature_presence = (np_agg_sum > 0) * 1
        # Sum by column axis=0
        np_idf = np.sum(np_feature_presence, axis=0)

        lg.Log.debugdebug(
            str(Eidf.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + '\n\r\tAggregated sum by labels (' + str(np_agg_sum.shape[0]) + ' rows):\n\r' + str(np_agg_sum)
            + '\n\r\tPresence array (' + str(np_feature_presence.shape[0]) + ' rows):\n\r' + str(np_feature_presence)
            + '\n\r\tArray for IDF presence/normalized sum (' + str(np_idf) + ' rows):\n\r' + str(np_idf)
            + '\n\r\tx_names: ' + str(x_name) + '.'
        )

        # Total document count
        n_documents = np_agg_sum.shape[0]
        lg.Log.important(
            str(Eidf.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Total unique documents/intents to calculate IDF = ' + str(n_documents)
        )

        # If using outdated np.matrix, this IDF will be a (1,n) array, but if using np.array, this will be 1-dimensional vector
        # TODO RuntimeWarning: divide by zero encountered in true_divide
        idf = np.log(n_documents / np_idf)
        # Replace infinity with 1 count or log(n_documents)
        idf[idf==np.inf] = np.log(n_documents)
        # If only 1 document, all IDF will be zero, we will handle below
        if n_documents <= 1:
            lg.Log.warning(
                str(Eidf.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Only ' + str(n_documents) + ' document in IDF calculation. Setting IDF to 1.'
            )
            idf = np.array([1]*x.shape[1])
        lg.Log.debugdebug(
            str(Eidf.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + '\n\r\tWeight IDF:\n\r' + str(idf)
        )
        return idf

    def __init__(
            self,
            # numpy array 2 dimensions
            x,
            # Class label, if None then all vectors are different class
            y = None,
            # Feature name, if None then we use default numbers with 0 index
            x_name = None,
            feature_presence_only_in_label_training_data = False
    ):
        if type(x) is not np.ndarray:
            raise Exception(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Wrong type "' + str(type(x)) + '". Must be numpy ndarray type.'
            )

        if x.ndim != 2:
            raise Exception(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Wrong dimensions "' + str(x.shape) + '". Must be 2 dimensions.'
            )

        self.x = x
        self.y = y
        self.x_name = x_name
        self.feature_presence_only_in_label_training_data = feature_presence_only_in_label_training_data

        if self.y is None:
            # Default to all vectors are different class
            self.y = np.array(range(0, x.shape[0], 1), dtype=int)

        if self.x_name is None:
            self.x_name = np.array(range(0, x.shape[1], 1), dtype=int)

        lg.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Normalizing x..'
        )
        # TODO This is unusable in production, too slow!
        # Normalized version of vectors on the hypersphere
        self.xh = nputil.NumpyUtil.normalize(x=self.x)

        #
        # Start with default 1 weights
        #
        self.w_start = np.array([1.0]*self.x.shape[1], dtype=float)
        # We want to opimize these weights to make the separation of angles
        # between vectors maximum
        self.w = self.w_start.copy()

        lg.Log.debugdebug(
            str(Eidf.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + '\n\r\tIDF Initialization, x:\n\r' + str(self.x)
            + '\n\r\ty:\n\r' + str(self.y)
            + '\n\r\tx_name:\n\r' + str(self.x_name)
        )
        return

    def get_w(self):
        return self.w.copy()

    #
    # This is the target function to maximize the predetermined quantile MAXIMIZE_QUANTILE
    # TODO Unusable in production too slow. Optimize!
    #
    def target_ml_function(
            self,
            x_input
    ):
        #
        # TODO
        #  This normalize is unusable when x has too many rows,
        #  This is why we should cluster x first, then only optimize.
        #
        x_n = nputil.NumpyUtil.normalize(x = x_input)

        #
        # Fast calculation closed formula, compared to double-looping below that cannot be used in most cases
        #
        if Eidf.TARGET_FUNCTION_AS_SUM_COSINE:
            #
            # If already normalized, then a concise formula for sum of cosine of angles are just:
            #
            # 0.5 * [ (x_11 + x_21 +... + x_n1)^2 - (x_11^2 + x_21^2 + ... x_n1^2)
            #         (x_12 + x_22 +... + x_n2)^2 - (x_12^2 + x_22^2 + ... x_n2^2)
            #         ...
            #         (x_1n + x_2n +... + x_nn)^2 - (x_1n^2 + x_2n^2 + ... x_nn^2)
            #       ]
            #
            # Can be seen that the above formula takes care of all pairs = n_row*(n_row-1)/2.
            #
            # All vectors we assume are positive values only thus cosine values are in the range [0,1]
            #
            n_els = x_n.shape[0]
            n_pairs = n_els*(n_els-1)/2
            sum_cols = np.sum(x_n, axis=0)
            lg.Log.debugdebug('************** Sum Cols (' + str(n_els)  + 'rows ):\n\r' + str(sum_cols))
            sum_cols_square = np.sum(sum_cols**2)
            lg.Log.debugdebug('************** Sum Cols Square: ' + str(sum_cols_square))
            sum_els_square = np.sum(x_n**2)
            lg.Log.debugdebug('************** Sum Elements Square: ' + str(sum_els_square))
            sum_cosine = 0.5 * (sum_cols_square - sum_els_square)
            lg.Log.debugdebug('************** Sum Cosine: ' + str(sum_cosine))
            # Average of the cosine sum
            avg_cosine_sum = sum_cosine/n_pairs
            lg.Log.debugdebug('************** Avg Cosine Sum (of ' + str(n_pairs) + ' pairs): ' + str(avg_cosine_sum))
            avg_cosine_sum = max(0.0, min(1.0, avg_cosine_sum))
            lg.Log.debugdebug('************** Avg Cosine Sum (of ' + str(n_pairs) + ' pairs): ' + str(avg_cosine_sum))
            # Return average angle as this has meaning when troubleshooting or analyzing
            angle = np.arccos(avg_cosine_sum)*180/np.pi
            lg.Log.debugdebug('************** Angle: ' + str(angle))
            return angle

        # Get total angle squared between all points on the hypersphere
        quantile_angle_x = 0
        angle_list = []
        #
        # TODO
        #  The code below is quite unusable as it is super slow.
        #  This double looping must be eliminated to no loops.
        #
        for i in range(0, x_n.shape[0], 1):
            for j in range(i+1, x_n.shape[0], 1):
                if i == j:
                    continue
                # Get
                v1 = x_n[i]
                v2 = x_n[j]
                # It is possible after iterations that vectors become 0 due to the weights
                if (np.linalg.norm(v1) == 0) or (np.linalg.norm(v2) == 0):
                    lg.Log.warning(
                        str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                        + ': Vector zerorized from iterations.'
                    )
                    continue
                #
                # The vectors are already normalized
                #
                cos_angle = np.dot(v1, v2)
                #
                # This value can be >1 due to computer roundings and after that everything will be nan
                #
                if np.isnan(cos_angle):
                    errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                             + ': Cosine Angle between v1=' + str(v1) + ' and v2=' + str(v2) + ' is nan!!'
                    lg.Log.critical(errmsg)
                    raise Exception(errmsg)
                if cos_angle > 1.0:
                    cos_angle = 1.0
                elif cos_angle < 0.0:
                    cos_angle = 0.0
                angle = abs(np.arcsin((1 - cos_angle**2)**0.5))
                if np.isnan(angle):
                    errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                             + ': Angle between v1=' + str(v1) + ' and v2=' + str(v2) + ' is nan!!'\
                             + ' Cosine of angle = ' + str(cos_angle) + '.'
                    lg.Log.critical(errmsg)
                    raise Exception(errmsg)
                lg.Log.debugdebug(
                    'Angle between v1=' + str(v1) + ' and v2=' + str(v2) + ' is ' + str(180 * angle / np.pi)
                )
                angle_list.append(angle)

        quantile_angle_x = np.quantile(a=angle_list, q=[Eidf.MAXIMIZE_QUANTILE])[0]
        values_in_quantile = np.array(angle_list)
        values_in_quantile = values_in_quantile[values_in_quantile<=quantile_angle_x]
        sum_square_values_in_q = np.sum(values_in_quantile**2)
        if np.isnan(quantile_angle_x):
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Final quantile angle =' + str(quantile_angle_x)\
                     + ' for x_input:\n\r' + str(x_input) + '.'
            lg.Log.error(errmsg)
            raise Exception(errmsg)

        lg.Log.debugdebug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Angle = ' + str(np.sort(angle_list))
            + '\n\rQuantile ' + str(100*Eidf.MAXIMIZE_QUANTILE) + '% = ' + str(quantile_angle_x)
            + '\n\rSum square values in quantile = ' + str(sum_square_values_in_q)
        )
        return sum_square_values_in_q

    #
    # Differentiation of target function with respect to weights.
    # Returns a vector same dimensions as w
    #
    def differentiate_dml_dw(
            self,
            x_input,
            w_vec,
            delta = 0.000001
    ):
        # Take dw
        l = w_vec.shape[0]
        dw_diag = np.diag(np.array([delta]*l, dtype=float))
        # The return value
        dml_dw = np.zeros(l, dtype=float)
        for i in range(l):
            dw_i = dw_diag[i]
            dm_dwi = self.target_ml_function(x_input = np.multiply(x_input, w_vec + dw_i)) -\
                self.target_ml_function(x_input = np.multiply(x_input, w_vec))
            dm_dwi = dm_dwi / delta
            lg.Log.debugdebug(
                'Differentiation with respect to w' + str(i) + ' = ' + str(dm_dwi)
            )
            dml_dw[i] = dm_dwi

        lg.Log.debugdebug(
            'Differentiation with respect to w = ' + str(dml_dw)
        )

        return dml_dw

    #
    # Opimize by gradient ascent, on predetermined quantile MAXIMIZE_QUANTILE
    #
    def optimize(
            self,
            # If we don't start with standard IDF=log(present_in_how_many_documents/total_documents),
            # then we Monte Carlo some start points and choose the best one
            initial_w_as_standard_idf = False,
            max_iter = 10
    ):
        x_vecs = self.xh.copy()
        y_vecs = self.y.copy()

        #
        # If too many rows, we will have problem calculating normalize() after weighing vectors
        #
        if x_vecs.shape[0] > Eidf.MAX_X_ROWS_BEFORE_CLUSTER:
            lg.Log.info(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Too many rows ' + str(x_vecs.shape[0]) + ' > ' + str(Eidf.MAX_X_ROWS_BEFORE_CLUSTER)
                + '. Clustering to ' + str(Eidf.MAX_X_ROWS_BEFORE_CLUSTER) + ' rows..'
            )
            cl_result = cl.Cluster.cluster(
                matx = x_vecs,
                ncenters = Eidf.MAX_X_ROWS_BEFORE_CLUSTER
            )
            x_vecs = cl_result.np_cluster_centers
            lg.Log.debug(
                'New x after clustering:\n\r' + str(x_vecs)
            )
            y_vecs = np.array(range(x_vecs.shape[0]))

        ml_start = self.target_ml_function(x_input = x_vecs)
        ml_final = ml_start
        # The delta of limit increase in target function to stop iteration
        delta = ml_start * Eidf.DELTA_PERCENT_OF_TARGET_FUNCTION_START_VALUE

        lg.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Start target function value = ' + str(ml_start) + ', using delta = ' + str(delta)
            + ', quantile used = ' + str(Eidf.MAXIMIZE_QUANTILE)
        )
        iter = 1

        ml_prev = ml_start

        #
        # Find best initial start weights for iteration, either using standard IDF or via MC
        #
        if initial_w_as_standard_idf:
            # Start with standard IDF values
            self.w_start = Eidf.get_feature_weight_idf_default(
                x = x_vecs,
                y = y_vecs,
                x_name = self.x_name,
                feature_presence_only_in_label_training_data = self.feature_presence_only_in_label_training_data
            )
        else:
            # Monte Carlo the weights for some start points to see which is best
            tf_val_best = -np.inf
            for i in range(Eidf.MONTE_CARLO_SAMPLES_N):
                rd_vec = np.array([rd.uniform(-0.5, 0.5) for i in range(self.w.shape[0])])
                w_mc = self.w + rd_vec
                lg.Log.debugdebug(
                    'MC random w = ' + str(w_mc)
                )
                x_weighted = nputil.NumpyUtil.normalize(x=np.multiply(x_vecs, w_mc))
                tf_val = self.target_ml_function(x_input=x_weighted)
                if tf_val > tf_val_best:
                    tf_val_best = tf_val
                    self.w_start = w_mc
                    lg.Log.debugdebug(
                        'Update best MC w to ' + str(self.w_start)
                        + ', target function value = ' + str(tf_val_best)
                    )
            lg.Log.debugdebug(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + 'Best MC w: ' + str(self.w_start) + ', target function value = ' + str(tf_val_best)
            )
        lg.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Start weights:\n\r' + str(self.w_start)
        )

        w_iter_test = self.w_start.copy()
        while True:
            lg.Log.debugdebug(
                'ITERATION #' + str(iter) + ', using test weights:\n\r' + str(w_iter_test)
                + '\n\rexisting old weights:\n\r' + str(self.w)
            )

            # Get new vectors after weightage
            x_weighted = nputil.NumpyUtil.normalize(x=np.multiply(x_vecs, w_iter_test))
            # Get new separation we are trying to maximize (if using sum cosine is minimize)
            ml_cur = self.target_ml_function(x_input = x_weighted)
            ml_increase = ml_cur - ml_prev
            if ml_cur - ml_prev > 0:
                ml_final = ml_cur
                self.w = w_iter_test.copy()
            # Update old ML value to current
            ml_prev = ml_cur

            lg.Log.debug(
                ': ITERATION #' + str(iter) + '. ML Increase = ' + str(ml_increase)
                + ', delta =' + str(delta) + ', ML = ' + str(ml_cur)
                + ', updated weights:\n\r' + str(self.w)
            )
            if ml_increase < delta:
                # Gradient ascent done, max local optimal reached
                break
            if iter > max_iter:
                # Gradient ascent done, too many iterations already
                break
            iter += 1

            #
            # Find the dw we need to move to
            #
            # Get delta of target function d_ml
            dml_dw = self.differentiate_dml_dw(
                x_input = x_vecs,
                w_vec   = w_iter_test
            )

            lg.Log.debugdebug(
                'dml/dw = ' + str(dml_dw)
            )
            # Adjust weights
            l = w_iter_test.shape[0]
            max_movement_w = np.array([Eidf.MAXIMUM_IDF_W_MOVEMENT] * l)
            min_movement_w = -max_movement_w

            w_iter_test = w_iter_test + np.maximum(np.minimum(dml_dw*0.1, max_movement_w), min_movement_w)
            # Don't allow negative weights
            w_iter_test = np.maximum(w_iter_test, np.array([Eidf.MINIMUM_WEIGHT_IDF]*l))
            lg.Log.debugdebug(
                'Iter ' + str(iter) + ': New weights:\n\r' + str(w_iter_test)
            )

        lg.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': End target function value = ' + str(ml_final) + ' (started with ' + str(ml_start) + ')'
            + '\n\rStart weights:\n\r' + str(self.w_start)
            + '\n\rEnd weights:\n\r' + str(self.w)
        )
        return


if __name__ == '__main__':
    lg.Log.LOGLEVEL = lg.Log.LOG_LEVEL_DEBUG_1
    x = np.array([
        [1.0, 0.0, 1.0], #0
        [0.9, 0.8, 1.0], #0
        [0.5, 0.0, 0.0], #1
        [0.1, 1.0, 0.0], #2
        [0.0, 1.0, 0.0]  #3
    ])
    y = np.array([0, 0, 1, 2, 3])
    obj = Eidf(
        x = x,
        y = y,
        feature_presence_only_in_label_training_data = True
    )
    obj.optimize(
        initial_w_as_standard_idf=True
    )

    obj = Eidf(
        x = x,
        y = y,
        feature_presence_only_in_label_training_data = False
    )
    obj.optimize(
        initial_w_as_standard_idf = True
    )

    obj = Eidf(
        x = x,
        y = y,
        feature_presence_only_in_label_training_data = False
    )
    obj.optimize(
        initial_w_as_standard_idf = False
    )
