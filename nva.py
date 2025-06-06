#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

import queue
import sys
import pyttsx3
import sounddevice as sd
import json

from vosk import Model, KaldiRecognizer

from ask import Ask
from intents import Intent
import parser

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

args = parser.get_args()

try:
    partials = args.partials
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback) as stream:
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)
        
        stay_active = True


        tts = pyttsx3.init()
        stream.stop()
        tts.say("Howdy")
        tts.runAndWait()
        stream.start()

        rec = KaldiRecognizer(model, args.samplerate)

        while stay_active:
            data = q.get()
        
            if rec.AcceptWaveform(data):
                utt = json.loads(rec.Result())['text']
                if utt.__len__() > 0:
                    print(utt)
                    ask = Ask(utt)
                    ask.debug_print()

                    if ask.intent == Intent.EXIT:
                        stay_active = False
                    
                    ask.skill.execute_ask(ask)

                    if ask.talkback.__len__() > 0:
                        stream.stop()
                        tts.say(ask.talkback)
                        tts.runAndWait()
                        stream.start()
            else:
                if partials: print(rec.PartialResult())
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
