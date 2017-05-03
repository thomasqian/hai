import sys, json, re, os
import nltk
from nltk.tag import StanfordPOSTagger
nltk.data.path.append('nltk_data')
_path_to_model = 'stanford-postagger/models/english-bidirectional-distsim.tagger'
_path_to_jar = 'stanford-postagger/stanford-postagger.jar'

def authorize(sid):
	'''
		Returns true if senderID has administrative privileges.
	'''
	return sid == os.environ['ADMIN_ID'] or sid == os.environ['ADMIN_ID2']; 


def sendResponse(sid, msg, cmd=''):
	res = {}
	res["sid"] = sid
	res["msg"] = msg
	res["cmd"] = cmd
	print json.dumps(res, ensure_ascii=False)

def handleCommand(sid, txt):
	if authorize(sid):
		if txt == 'whoami':
			sendResponse(sid, '', 'whoami')
		else:
			sendResponse(sid, 'Unknown Command')
	else:
		sendResponse(sid, "Sorry, you don't have admnistrative privileges! :(");

def handleMessage(sid, txt):
	tagger = StanfordPOSTagger(_path_to_model, path_to_jar=_path_to_jar, java_options='-mx4096m')
	tagged = tagger.tag(nltk.word_tokenize(txt))
	responseMessage = str(tagged)
	sendResponse(sid, responseMessage)

def main():
	if len(sys.argv) != 3:
		exit()

	sid = sys.argv[1]
	receivedMessage = sys.argv[2]

	if receivedMessage and receivedMessage[0] == '/':
		handleCommand(sid, receivedMessage[1:])
	else:
		handleMessage(sid, receivedMessage)

	'''
	tokens = nltk.word_tokenize(receivedMessage)
	tagged = nltk.pos_tag(tokens)

	chunkGram = r"""Action Phrase: {<VB\w?><DT>*<NN\w?>}"""
	chunkParser = nltk.RegexpParser(chunkGram)

	chunked = chunkParser.parse(tagged)

	responseMessage = str(chunked)
	'''

if __name__ == '__main__':
	main()