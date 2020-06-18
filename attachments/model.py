import tensorflow as tf
import pickle
import numpy as np
from nltk.corpus import stopwords

class SubjectPred:
	def model_pred(body_data):
		sw = stopwords.words('english')
		# print(sw)

		model = tf.keras.models.load_model('Conv1D.h5')

		body = "The Department of CSE and IT is conducting a Technical Talk on 'Competitive Programming’ on the 24th of January.The chief guest, also a speaker for the event is Mr. Gaurav Sen, ex-Uber SDE 2, ex-Directi, ex-Morgan Stanley employee, Youtuber. Therefore we require a felicitation kit that contains Shawl, Photoframe, and Pasaydan for the same.Kindly sanction the request as below for the felicitation of guests and judges."
		bow = pickle.load(open('bow.pickle','rb'))
		body = body.lower()
		body = list(body.split())
		for index,i in enumerate(body):
			if i in sw:
				body[index] = ''

		mail = ''
		for i in body:
			if i != '':
				mail += f'{i} '

		mail.replace('.','')
		mail = [mail]
		# print(mail)


		body = [bow.index(i) if i in bow else bow.index('NAN') for i in mail[0].split()]

		if len(body) < 199:
			for i in range(199-len(body)):
				body += [0]

		else:
			body = body[:199]


		stopwords = ['']

		# print(len(body))
		body = np.array(body)
		body = np.expand_dims(body,axis=0)
		pred = model.predict(body)
		pred = np.array(pred,dtype=np.int32)

		subject = ''
		for i in pred[0]:
			if i != 0:
				subject += f'{bow[i]} '

		print(subject)


		return subject



	def mode1_pred(body_data):
		body_data=body_data.lower()
		subject=""
		for word in body_data.split():
			print(word)
			if word=='felicitation':
				subject="Conduct Felicitation kit"
			if word=='persona':
				subject="Persona fest 2020" 
			if word=='Venue':
				subject="Grant venue event for"
		print(subject)
	s="i want felicitation kit"
	mode1_pred(s)


