import pandas as pd
import matplotlib.pyplot as plt
from scipy import fftpack as fft
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class DataMining():
    def __init__(self, glucose):
        self.dataF = glucose

    def preprocess(self):
        nan_row = self.dataF.isna().sum(axis=1)
        rowNaN_list = list()
        for i in range(len(nan_row)):
            if nan_row[i] > 0.4 * len(self.dataF.loc[0]):
                rowNaN_list.append(i)
        self.dataF.drop(rowNaN_list, inplace=True)
        self.dataF.reset_index(inplace=True, drop=True)
        self.dataF.interpolate(method='quadratic', order=2, inplace=True)
        self.dataF = self.dataF.iloc[:,:30]
        plots = plt.figure()
        plots.suptitle('______CGM Time Series Plot______', fontsize=22)
        plt.plot(self.dataF.T.values)
        plt.show()


class Features():

    def __init__(self, glucose, dim):
        self.dataF = glucose
        self.dim = dim

    def FFT(self):
        fftG = fft.rfft(self.dataF, n=5, axis=1)
        fftGr = pd.DataFrame(data=fftG)
        print("\n\n-------Fast Fourier Transform-------")
        print(fftGr)
        fig = plt.figure()
        fig.suptitle('______Fast Fourier Transform______', fontsize=22)
        plt.plot(fftGr.values[:, 1:])
        plt.show()
        return fftGr

    def movAvg(self):
        count = 0
        avg = pd.DataFrame(index=range(len(self.dataF)))
        while count < len(self.dataF.loc[0]) // 5 - 1:
            avg = pd.concat([avg, self.dataF.iloc[:, 0 + (4 * count):10 + (4 * count)].mean(axis=1)], axis=1, ignore_index=True)
            count += 1
        print("\n\n-------Moving Average of window size 10 and 40% overlapping-------")
        print(avg)
        fig = plt.figure()
        fig.suptitle('______Moving Average______', fontsize=22)
        plt.plot(avg.values)
        plt.show()
        return avg

    def movStdError(self):
        count = 0
        stdErr = pd.DataFrame(index=range(len(self.dataF)))
        while count < len(self.dataF.loc[0]) // 5 - 1:
            stdErr = pd.concat([stdErr, self.dataF.iloc[:, 0 + (4 * count):10 + (4 * count)].sem(axis=1)], axis=1, ignore_index=True)
            count += 1
        print("\n\n-------Moving Standard Error of Mean of window size 10 and 40% overlapping-------")
        print(stdErr)
        fig = plt.figure()
        fig.suptitle('______Moving Standard Error of Mean______', fontsize=22)
        plt.plot(stdErr.values)
        plt.show()
        return stdErr

    def movKurtosis(self):
        count = 0
        kurto = pd.DataFrame(index=range(len(self.dataF)))
        while count < len(self.dataF.loc[0]) // 5 - 1:
            kurto = pd.concat([kurto, self.dataF.iloc[:, 0 + (4 * count):10 + (4 * count)].kurtosis(axis=1)], axis=1, ignore_index=True)
            count += 1
        print("\n\n-------Moving Kurtosis of window size 10 and 40% overlapping-------")
        print(kurto)
        fig = plt.figure()
        fig.suptitle('______Moving Kurtosis______', fontsize=22)
        plt.plot(kurto.values)
        plt.show()
        return kurto

    def matrix(self):
        feature_matrix = pd.concat([self.FFT(), self.movAvg(), self.movStdError(), self.movKurtosis()], axis=1,ignore_index=True)
        print("\n\n-------Feature Matrix-------")
        print(feature_matrix)
        feature_matrix.to_csv(r'feature_matrix.csv', index=None, header=False)
        return feature_matrix

    def Principal_Component_Analysis(self):
        fMatrix = self.matrix()
        matrix = StandardScaler().fit_transform(fMatrix.T)
        pca = PCA(n_components=self.dim)
        trans = pca.fit_transform(matrix)
        imp_features = pd.DataFrame(pca.components_)
        print("\n\n-------Top 5 PCA Features-------")
        for i in imp_features.values:
            rows = dict(enumerate(i))
            print(sorted(rows, key=rows.get, reverse=True)[:5])
        print("\n\n-------Time Series Data-------")
        print(pd.DataFrame(trans))
        print("\n\n-------Features-------")
        print(imp_features)
        fig = plt.figure()
        fig.suptitle('PCA Top 5 Features', fontsize=22)
        plt.plot(imp_features.iloc[0].values, 'ro', label='Feature 1')
        plt.legend()
        plt.show()
        plt.plot(imp_features.iloc[1].values, 'bo', label='Feature 2')
        plt.legend()
        plt.show()
        plt.plot(imp_features.iloc[2].values, 'co', label='Feature 3')
        plt.legend()
        plt.show()
        plt.plot(imp_features.iloc[3].values, 'ko', label='Feature 4')
        plt.legend()
        plt.show()
        plt.plot(imp_features.iloc[4].values, 'mo', label='Feature 5')
        plt.legend()
        plt.show()


print("Choose the Patient Number: ")
print("1. Patient 1")
print("2. Patient 2")
print("3. Patient 3")
print("4. Patient 4")
print("5. Patient 5")
pno = int(input())

if pno == 1:
    file = "CGMSeriesLunchPat1.csv"
elif pno == 2:
    file = "CGMSeriesLunchPat2.csv"
elif pno == 3:
    file = "CGMSeriesLunchPat3.csv"
elif pno == 4:
    file = "CGMSeriesLunchPat4.csv"
elif pno == 5:
    file = "CGMSeriesLunchPat5.csv"
else:
    file = "CGMSeriesLunchPat1.csv"
    print("Invalid Input: Default set to Patient 1")

csv = pd.read_csv(file)
cgm = DataMining(csv)
cgm.preprocess()
feature = Features(csv, 5)
feature.Principal_Component_Analysis()
