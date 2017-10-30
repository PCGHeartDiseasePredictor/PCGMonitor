import matlab.engine
import pandas as pd
import numpy as np
import scipy.stats
import pickle
from PCGAPI.app import app
import os

class HeartbeatHandler:

	def heartbeat_analysis(self,heartbeat_data):
		file_data = heartbeat_data.read()
		f = open('/home/risav/PCG/pcg.wav', 'wb')
		f.write(file_data)
		f.close()
		eng = matlab.engine.start_matlab()
		var = eng.ssa10('pcg.wav')
		x = []
		for item in var:
			x.append(item)
		def postrapz(y, x=None, dx=1.0):
			y = np.asanyarray(y)
			if x is None:
				d = dx
			else:
				x = np.asanyarray(x)
				d = np.diff(x)
			ret = (d * (y[1:] +y[:-1]) / 2.0)
			return ret[ret>0].sum()
		def negtrapz(y, x=None, dx=1.0):
			y = np.asanyarray(y)
			if x is None:
				d = dx
			else:
				x = np.asanyarray(x)
				d = np.diff(x)
			ret = (d * (y[1:] +y[:-1]) / 2.0)
			return ret[ret<0].sum()
		maxValue = max(x)
		varValue = abs(np.var(x))
		posArea = abs(postrapz(x))
		negArea = abs(negtrapz(x))
		Kurtosis = abs(scipy.stats.kurtosis(x))
		Energy = scipy.stats.entropy(x)

		features = [maxValue[0],varValue,posArea,negArea,Kurtosis[0]]
		columns = ["maxValue" ,"varValue","posArea","negArea","kurtosis"]
		features = np.array(features).reshape((1,5))
		inputTest = pd.DataFrame(features,columns=columns)

		inputTest['area'] = abs(inputTest['posArea'] - inputTest['negArea'])
		inputTest  = inputTest.drop('posArea',1)
		inputTest  = inputTest.drop('negArea',1)

		filename = '/home/risav/finalized_model.sav'
		loaded_model = pickle.load(open(filename, 'rb'))
		predicted = loaded_model.predict(inputTest)
		return predicted[0]