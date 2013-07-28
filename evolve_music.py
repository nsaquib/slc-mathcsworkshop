'''
Evolve a music piece with a simple evolutionary algorithm
Author: Saquib
Email: nzm.saquib@gmail.com
7/27/13
Note: you can get pygame libraries from http://www.pygame.org/download.shtml
'''

import pygame
import pygame.midi
from time import sleep
import random

def fitness(source, target):
   fitval = 0
   for i in range(0, len(source)):
      fitval += (ord(target[i]) - ord(source[i])) ** 2
   return(fitval)

def mutate(source):
   charpos = random.randint(0, len(source) - 1)
   parts = list(source)
   parts[charpos] = chr(ord(parts[charpos]) + random.randint(-1,1))
   return(''.join(parts))

def midiEvolve(source, target, iterthr):
    
    src = source
    
    GRAND_PIANO = 0
    CHURCH_ORGAN = 19
    DIST_GUITAR = 31
    rain = 97
    crystal = 99
    newage = 89
    
    instrument = newage
    #instrument = GRAND_PIANO
    
    pygame.init()
    pygame.midi.init()

    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    midi_out = pygame.midi.Output(port, 0)
    try:
        midi_out.set_instrument(instrument)

        fitval = fitness(source, target)
        i = 0

        while i < iterthr:
           i += 1
           m = mutate(source)
           fitval_m = fitness(m, target)
           if fitval_m < fitval:
              fitval = fitval_m
              source = m
              print "%5i %5i %14s" % (i, fitval_m, m)
              if fitval == 0:
                  break

        # play source and evolved music
        for n in range(0, len(src)):
            if n%2 == 0:
                currnote = src[n]
                midi_out.note_on(ord(currnote),127) # 74 is middle C, 127 is "how loud" - max is 127
            else:
                sleep(ord(src[n])**2/5000)
                #sleep(ord(src[n])/100)
                midi_out.note_off(ord(currnote),127)

        # just so the last note won't keep playing
        if len(src)%2 != 0:
            midi_out.note_off(ord(currnote),127)

        # take a pause before playing the evolved piece
        sleep(2)
        
        for n in range(0, len(source)):
            if n%2 == 0:
                currnote = source[n]
                midi_out.note_on(ord(currnote),127) # 74 is middle C, 127 is "how loud" - max is 127
            else:
                sleep(ord(source[n])**2/5000)
                #sleep(ord(source[n])/100)
                midi_out.note_off(ord(currnote),127)

        sleep(0.5)
        
    finally:
        del midi_out
        pygame.midi.quit()

#-----------------------------------------------------------

# examples

# midiEvolve("hello world",";wql* opqlq", 500)
        
# C on 6th scale is 72 on MIDI, B is 83. So, Choose from 'H' to 'S' for a full range of scale
# C-72  C#-73	D-74	D#-75	E-76	F-77	F#-78	G-79	G#-80	A-81	A#82	B83
# H     I       J       K       L       M       N       O       P       Q       R       S

# For the middle octave
# C-48	C#-49	D-50	D#-51	E-52	F-53	F#-54	G-55	G#-56	A-57	A#58	B59
# 0     1       2       3       4       5       6       7       8       9       :       ;

# small intervals symbols: ! # $
# larger intervals symbols: { | ~

# evolve a C D E progression towards a B F# A
#midiEvolve("H~J~L~","S~N~Q~", 500)

# evolve a longer progression with different intervals
midiEvolve("7~2~0~2~7~2~0~2~","4$1~;!9#5~7{9#2~", 1000)
#midiEvolve("7~2~0~2~7~2~0~2~","4$1~;!9#5~7{9#2~", 10000)
