leftKey = Key('2')|JoyButton(0,5)|JoyButton(0,7)
rightKey = Key('3')|JoyButton(0,4)|JoyButton(0,6)

numBlocks = 3
instructExit = leftKey&rightKey

instructFile = "instructions.txt"

#List of a list of high conflict and list of low conflict stims.
#High is 0, low is 1

flankHighLow = [[[u">  >",u"<  <"], [u"<  <", u">  >"]],[[u">>>  >>>",u"<<<  <<<"], [u"<<<  <<<", u">>>  >>>"]],[[u">>>>>  >>>>>",u"<<<<<  <<<<<"], [u"<<<<<  <<<<<", u">>>>>  >>>>>"]]]

arrowHighLow = [[[u"<", u">"], [u"<", u">"]],[[u"<", u">"], [u"<", u">"]], [[u"<", u">"], [u"<", u">"]]]

numHighPractice = 2  #NOTE: numHighPractice + numLowPractice = numonePractice + numthreePractice + numfivePractice
numLowPractice = 2
numonePractice = 0
numthreePractice = 4
numfivePractice = 0

numHigh = 2  #NOTE: numHigh + numLow = numone + numthree + numfive
numLow = 2 
numone=0
numthree=4
numfive=0

guideDuration = 1000
flankerDuration=100
arrowDuration=4000
flankDelay = 1000 #ms
flankJitter = 100
