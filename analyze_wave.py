#!/usr/bin/python

import wave, struct

def wavLoad (fname):
    wav = wave.open (fname, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
    frames = wav.readframes (nframes * nchannels)
    out = struct.unpack_from ("%dh" % nframes * nchannels, frames)

    # Convert 2 channles to numpy arrays
    if nchannels == 2:
        left = list (out[0::2])
        right = list (out[1::2])
    else:
        left = out
        right = left

    return left, right

def main():

    filename = "AKWF_0001.wav"
    left, right = wavLoad(filename)
    bins = 380
    step_size = len(left)/bins
    step_size = 22050

    i = 0
    for step in range(0,len(left),step_size):
        #print step, step, step+step_size
        #print len(left[step_size*step:(step_size+1)*step])
        #print step, sum(map(abs,left[step:step+step_size]))/step_size
        print step, abs(sum(left[step:step+step_size])/step_size)
        #print step, sum(right[step_size*step:(step_size+1)*step])/step_size

if __name__=="__main__":
    main()
