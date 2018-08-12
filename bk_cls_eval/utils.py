# -*- coding: utf-8 -*-

import json
import numpy as np

def read_json(json_file,label_map_dict):
    """
    read ground truth
    Args:
        json_file        -- LabelX json file
        label_map_dict   -- label dict {'bloodiness':0,...}
    """
    gt_dict = dict()
    with open(json_file,'r') as f:
        for line in f:
            line = json.loads(line.strip())
            name = line['url'].split('/')[-1]
            label = line['label'][0]['data'][0]['class']
            # label == '' issue
            if label == '':
                continue
            gt_dict[name] = label_map_dict[label]
    return gt_dict

def read_log(log_file,label_map_dict):
    """
    bk class log file
    log syntax:
    image_name\tlabel
    image1.jpg\tbomb
    image2.jpg\tfight
    ...
    """
    pred_dict = dict()
    with open(log_file,'r') as f:
        for line in f:
            name,label = line.strip().split('\t')
            pred_dict[name] = label_map_dict[label]
    return pred_dict

def gen_yture_ypred(gt_dict,pred_dict):
    y_true = list()
    y_pred = list()
    for image in pred_dict:
        if image in gt_dict:
            y_true.append(gt_dict[image])
            y_pred.append(pred_dict[image])
    return y_true,y_pred

class Metrics(object):
    def __init__(self,y_true,y_pred,classes):
        self.__y_true = np.array(y_true)
        self.__y_pred = np.array(y_pred)
        n = len(classes)
        self.__cnf_matrix = np.zeros((n,n),dtype = int)
        for i in range(n):
            for j in range(n):
                self.__cnf_matrix[i][j] = np.where(self.__y_pred[np.where(self.__y_true == i)] == j)[0].shape[0]
        self.__classes = classes
        self.__eps = 1e-9
    
    @property
    def confusion_matrix(self):
        return self.__cnf_matrix

    def metrics_list(self):
        """
        return [bloodiness recall/precision,bomb,beheaded,march,fight,normal,accuracy]
        """
        met = list()
        diag = 0.0
        for i in range(self.__cnf_matrix.shape[0]):
            diag += self.__cnf_matrix[i][i]
            recall = self.__cnf_matrix[i][i]/(self.__eps + float(np.sum(self.__cnf_matrix,axis=1)[i]))
            precision = self.__cnf_matrix[i][i]/(self.__eps + float(np.sum(self.__cnf_matrix,axis=0)[i]))
            met.append(recall)
            met.append(precision)
        acc = diag / (self.__eps + float(np.sum(self.__cnf_matrix)))
        met.append(acc)
        return met

    def plot_confusion_matrix(self):
        # 避免服务器上import失败
        import matplotlib.pyplot as plt
        import itertools
        np.set_printoptions(precision = 2)
        plt.figure()
        plt.imshow(self.__cnf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.colorbar()
        tick_marks = np.arange(len(self.__classes))
        plt.xticks(tick_marks, self.__classes, rotation=45)
        plt.yticks(tick_marks, self.__classes)

        fmt = 'd'
        thresh = self.__cnf_matrix.max() / 2.
        for i, j in itertools.product(range(self.__cnf_matrix.shape[0]), range(self.__cnf_matrix.shape[1])):
            plt.text(j, i, format(self.__cnf_matrix[i, j], fmt),
                    horizontalalignment="center",
                    color="white" if self.__cnf_matrix[i, j] > thresh else "black")
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        plt.savefig('pic/confusion_matrix.png')
        #plt.show()

if __name__ == '__main__':
    pass
