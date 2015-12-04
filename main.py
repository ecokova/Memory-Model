# -*- coding: utf-8 -*-
'''
main.py
Jen Hammelman, Naomi Zarrilli, and Elena Cokova
Created 11/22/2015
Edited 12/4/2015
'''

import memory
import action
import retrieval
import FlexQueue
import threading
import sys
from collections import namedtuple
import time
import argparse
import urllib2
import operator
import json
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np


Association = namedtuple("MyStruct", "association frequency")

traitNames = ['Extraversion','Introversion', \
              'Sensing','iNtuition', 'Thinking','Feeling',
              'Perceiving','Judging']
colors = ['r','b', 'g','y', 'k','w','m','c']

def analyzePersonality(memories):
    allTraits = [('attitude', 'Extraversion', 'Introversion'), \
                 ('perceiving-function', 'Sensing', 'iNtuition'), \
                 ('judging-function', 'Thinking', 'Feeling'), \
                 ('lifestyle', 'Perceiving', 'Judging')]
    MBTIlist= list()

    for i in range(len(memories)):
        mem = memories[i]
        assoc = [x[0] for x in mem.queue.queue]
        words = '+'.join(assoc) #reduce(operator.add, stmAssoc, '')
        for trait in allTraits:
            num = [0.5, 0.5]
            text = words.replace(' ', '+')
            text = text.replace('\n','')
            
            url = 'http://uclassify.com/browse/prfekt/myers-briggs-' + trait[0] + '/' + \
                    'ClassifyText?readkey=lt42BVovxems' + \
                    'text=' + text + '&version=1.01&output=json'
            try:
                result = urllib2.urlopen(url)
                MBTI = json.loads(result.read())['cls1']
                MBTIlist.append(MBTI[trait[1]])
		MBTIlist.append(MBTI[trait[2]])
            except urllib2.URLError, e:
                print e
                pass
           
            '''
            MBTIlist.append(num[0])
            MBTIlist.append(num[1])
            '''
    return MBTIlist

def getPersonality(personalityResults, memories, DONE):
    while not DONE[0]:
        personalityResults.append(analyzePersonality(memories))
        
def animateBarplot(fig, rects, personalityResults):
    half = len(rects)/2
    for results in personalityResults:
        time.sleep(0.3)
        for i in xrange(0,len(rects)):
            rects[i].set_height(results[i])
        fig.canvas.draw()
		
def parseQs(qfile):
    questions = []
    results = []
    with open(qfile) as f:
        lines = [line for line in f]
        for i in xrange(0,len(lines),5):
            try:
                wc = lines[i:i+5]
                questions.append("{}\n{}\n{}".format(wc[0],wc[1],wc[2]))
                results.append((wc[3],wc[4]))
            except:
                pass
    
    return questions, results

def main(argv):
    parser = argparse.ArgumentParser(description='MBTI Memory Model')
    parser.add_argument('-q','--numQs', type=int, help='number of questions')
    parser.add_argument('-qfile', '--qfile', help='question file', 
                        default='myers-briggs.csv')
    parser.add_argument('-uinput', '--input', help='user input',
                        default='stdin')
    opts = parser.parse_args()
    
    DONE = [False]
    [questions, results] = parseQs(opts.qfile)

    LTM = memory.MemoryThread(DONE, 0.2, 0)
    STM = memory.MemoryThread(DONE, 0.2, 7)
    SM  = memory.MemoryThread(DONE, 0.2, 5)

    RHS = action.Action(5,STM, LTM, 0.2, DONE)
    ATN = action.Action(0, SM, STM, 0.1, DONE)
    RTV = retrieval.Retrieval(STM.queue, LTM.queue, DONE, threading.Lock(), 0.2)
    personalityResults = []
    
    threads = [LTM, STM, SM, RHS, ATN, RTV]

    personalityAccumulator = threading.Thread(target =getPersonality,
                                              args=[personalityResults, [STM, LTM], DONE])
    personalityAccumulator.start()

    for thread in threads:
        thread.start()

    for i in range(opts.numQs):
        ans = raw_input(questions[i])
        if ans == 'A':
            result = results[i][0]
        else:
            result = results[i][1]
        SM.queue.put(Association(result,0))

    DONE[0] = True
    
    for thread in threads:
        thread.join()
    personalityAccumulator.join()

    if personalityResults:
        plt.ion()
        fig = plt.figure()
        win = fig.canvas.manager.window
        x = personalityResults[0]
        print x
        rects = plt.bar(range(len(x)), x, align='center', color=colors)
        plt.xticks(range(len(x)), traitNames+traitNames, rotation='vertical')
        plt.show()
        win.after(100, lambda: animateBarplot(fig, rects, personalityResults))

    else:
        print "We didn't get enough info to form your personality. Please try again!"
    
    print "Long Term Memory: ", list(LTM.queue.queue)
    print
    print "Short Term Memory: ", list(STM.queue.queue)
    print
    print "Sensory Memory: ", list(SM.queue.queue)
    
    done = raw_input("Done, ok?")
    
    exit(0)
    
if __name__ == '__main__':
    main(sys.argv)
