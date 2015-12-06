# -*- coding: utf-8 -*-
'''
main.py
Jen Hammelman, Naomi Zarrilli, and Elena Cokova
Created 11/22/2015
Edited 12/4/2015
'''

import memory
import action
import retrieval_underscores as retrieval
import FlexQueue
import threading
import sys
import io
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

trait_names = ['Extraversion','Introversion', \
              'Sensing','iNtuition', 'Thinking','Feeling',
              'Perceiving','Judging']

'''
#Uncomment for shorter graph labels
trait_names = ['E','I', \
              'S','N', 'T','F',
              'P','J']
'''
colors = ['#818aa3','#a39081','#c5dca0','#dca0c5', '#f5f2b8','#efb8f5','#e8a994','#94e8e8',
          '#313873','#534031','#758c50','#8c5075', '#b5b268','#9f68a5','#985944','#449898']

# API Keys
#  qv7uGKYDBcSK
#  jHP7vqc5rX83

def analyze_personality(memories):
    all_traits = [('attitude', 'Extraversion', 'Introversion'), \
                 ('perceiving-function', 'Sensing', 'iNtuition'), \
                 ('judging-function', 'Thinking', 'Feeling'), \
                 ('lifestyle', 'Perceiving', 'Judging')]
    MBTI_list= list()

    for i in range(len(memories)):
        mem = memories[i]
        assoc = [x[0] for x in mem.queue.queue]
        words = '+'.join(assoc) #reduce(operator.add, stmAssoc, '')
        for trait in all_traits:
            num = [0.5, 0.5]
            text = words.replace(' ', '+')
            text = text.replace('\n','')
            
            url = 'http://uclassify.com/browse/prfekt/myers-briggs-' + trait[0] + '/' + \
                    'ClassifyText?readkey=jHP7vqc5rX83&' + \
                    'text=' + text + '&version=1.01&output=json'
            try:
                result = urllib2.urlopen(url)
                MBTI = json.loads(result.read())['cls1']
                MBTI_list.append(MBTI[trait[1]])
		MBTI_list.append(MBTI[trait[2]])
            except urllib2.URLError, e:
                print e
                pass
           
    return MBTI_list

def get_personality(personality_results, memories, DONE):
    while not DONE[0]:
        personality_results.append(analyze_personality(memories))
        
def animate_barplot(fig, rects, personality_results):
    half = len(rects)/2
    for results in personality_results:
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
    parser.add_argument('-afile', '--afile', help='answer file default stdin',
                        default='stdin')
    parser.add_argument('-t','--time', type=float, help='time for waiting',
                        default=0.2)
    opts = parser.parse_args()
    
    DONE = [False]
    [questions, results] = parseQs(opts.qfile)

    LTM = memory.MemoryThread(DONE, opts.time, 100, 0, "LTM")
    STM = memory.MemoryThread(DONE, opts.time, 1, 7, "STM")
    SM  = memory.MemoryThread(DONE, opts.time, 0.1, 5, "SM")

    RHS = action.Action(5, STM.queue, LTM.queue, opts.time, DONE, "RHS")
    ATN = action.Action(0, SM.queue, STM.queue, opts.time, DONE, "ATN")
    RTV = retrieval.Retrieval(STM.queue, LTM.queue, opts.time, DONE, "RTV")
    personality_results = []
    
    threads = [LTM, STM, SM, RHS, ATN, RTV]

    personality_accumulator = threading.Thread(target =get_personality,
                                              args=[personality_results, [STM, LTM], DONE])
    personality_accumulator.start()

    for thread in threads:
        thread.start()

    if opts.afile == 'stdin':
        for i in range(opts.numQs):
            ans = raw_input(questions[i])
            if ans == 'A':
                result = results[i][0]
            else:
                result = results[i][1]
            SM.queue.put(Association(result,0))
    else:
        i = 0
        for line in open(opts.afile):
            if i <= opts.numQs:
                ans = line.strip()
                if ans == 'A':
                    result = results[i][0]
                else:
                    result = results[i][1]
                SM.queue.put(Association(result,0))
            i += 1

    DONE[0] = True
    
    for thread in threads:
        thread.join()
    personality_accumulator.join()

    input = raw_input('press <ENTER> to see results')
    if personality_results:
        plt.ion()
        fig = plt.figure()
        win = fig.canvas.manager.window
        x = personality_results[0]
        rects = plt.bar(range(len(x)), x, align='center', color=colors)
        plt.xticks(range(len(x)), trait_names+trait_names, rotation=-90)
        plt.show()
        win.after(100, lambda: animate_barplot(fig, rects, personality_results))

    else:
        print "We didn't get enough info to form your personality. Please try again!"
    
    print "Long Term Memory: ", list(LTM.queue.queue)
    print
    print "Short Term Memory: ", list(STM.queue.queue)
    print
    print "Sensory Memory: ", list(SM.queue.queue)

    input = raw_input('press any key to exit')
    exit(0)
    
if __name__ == '__main__':
    main(sys.argv)
