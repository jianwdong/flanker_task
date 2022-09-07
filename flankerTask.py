#!/usr/bin/python

from pyepl.locals import *
import random


def prepare(exp, config) :
    state = exp.restoreState()
    exp.saveState(state,sessionNum=0)

def run(exp, config) :
    #Every time we run, restore the experiment state
    state = exp.restoreState()
    exp.setSession(state.sessionNum)
    vt = VideoTrack('video')
    kt = KeyTrack('key')
    at = AudioTrack('audio')
    jt = JoyTrack('joystick')
    log = LogTrack('session')
    clock = PresentationClock()
    bc = ButtonChooser(config.leftKey, config.rightKey)

    vt.clear('black')
    instruct(open(config.instructFile, 'r').read())
    vt.clear('black')
        
    log.logMessage('SESS_START\t%d'%(state.sessionNum))
    if state.sessionNum == 0 :
        flankerTask(config, vt, log, bc,clock, True)

    for i in range(0,config.numBlocks):
        waitForAnyKey(clock, Text("Press any key to begin session %d"% (i+1)))
        flankerTask(config, vt, log, bc,clock)


    state.sessionNum += 1
    exp.saveState(state)

    timestamp = flashStimulus(Text("Thank you!\nYou have completed the session."))
    log.logMessage('SESS_END', timestamp)
    print('Experiment ran successfully.')
    clock.wait()



def flankerTask(config, video, sess, bc, clock, practice=False) :
    highlow = [0]*config.numHigh + [1]*config.numLow
    random.shuffle(highlow)
    flanknum = [0]*config.numone +[1]*config.numthree +[2]*config.numfive
    random.shuffle(flanknum)
    print('practice is '+str(practice))
    if practice :
        highlow = [0]*config.numHighPractice + [1]*config.numLowPractice
        random.shuffle(highlow)
        flanknum = [0]*config.numonePractice +[1]*config.numthreePractice +[2]*config.numfivePractice
        random.shuffle(flanknum)
    else :
        sess.logMessage('BEGIN FLANKER TASK')
        sess.logMessage('DIRECTION\tRESPONSE\tHIGHLOW\tRT\tNumFlank')
    
    numIncorrect=0
    index=-1
    for i in highlow :
        index=index+1
        #Given that we know the conflict level, randomly pick one of
        #the two possible arrows from it.
        lr = random.randint(0,1)
        guide = CompoundStimulus([('guide',Text('.',size=0.175),'PROP',(.5,.52))])
        flanker = CompoundStimulus([('flanker',Text(config.flankHighLow[flanknum[index]][i][lr],size=0.15),'PROP',(.5, .5)),
                                    ('guide',Text('.',size=0.175),'PROP',(.5,.52))])
        arrows = CompoundStimulus([('flanker',Text(config.flankHighLow[flanknum[index]][i][lr],size=0.15),'PROP',(.5, .5)),
                                   ('arrow',Text(config.arrowHighLow[flanknum[index]][i][lr],size=0.15),'PROP',(.5, .5)),
                                   ('guide',Text('.',size=0.175),'PROP',(.5,.52))])
        #Show and get response and reaction time
        guide.present(clock, duration= config.guideDuration)
        flanker.present(clock, duration= config.flankerDuration)
        rt = arrows.present(clock, bc=bc, duration= config.arrowDuration)
        resp = 'RIGHT'
        direct = 'RIGHT'
        conflict = 'LOW'
        feedback = 'CORRECT!'
        if rt[1] == config.leftKey:
            resp = 'LEFT'
        #print rt[1]
        
        #When lr is 0, the target arrow is pointing left.
        if lr == 0 :
            direct = 'LEFT'
        #print direct
        #print resp
        if i == 0 :
            conflict = 'HIGH'

        respTime = rt[2][0] - rt[0][0]
        #yourTime = 'Your response time was %d ms.' %(respTime)
        if direct != resp :
            feedback = 'Incorrect.'
            numIncorrect=numIncorrect+1
        if not practice :
            numflanks=(1,3,5)
            sess.logMessage('%s\t%s\t%s\t%d\t%d' %(direct, resp, conflict, respTime, numflanks[flanknum[index]]), rt[0])
        #Wait after each time a set of arrows is displayed.
        #video.clear("black")
        #feedbackmess=CompoundStimulus([('feedback',Text(feedback),'PROP',(.5, .5)),('guide',Text('.',size=0.2),'PROP',(.5,.51))])
        Text("").present(clk=clock, duration=config.flankDelay, 
                                             jitter=config.flankJitter)
        #clock.delay(config.flankDelay, config.flankJitter)
    if not practice :    
        sess.logMessage('END FLANKER TASK')
    elif numIncorrect/(config.numHighPractice+config.numLowPractice) <= .2:
        Text("Please try to go faster.").present(clk=clock, duration=2000)
    elif numIncorrect/(config.numHighPractice+config.numLowPractice) > .2:
        Text("Please try to be more accurate.").present(clk=clock, duration=2000)


if __name__ == '__main__':

    exp = Experiment()
    config = exp.getConfig()

    exp.setBreak()
    if not exp.restoreState() :
        prepare(exp, config)

    run(exp, config)
