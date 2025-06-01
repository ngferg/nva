#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

import argparse
import queue
import sys
import sounddevice as sd
import json
import subprocess

from vosk import Model, KaldiRecognizer
from enum import Enum


q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

class Intent(Enum):
    UNKNOWN = 0
    NOTHING = 1
    EXIT = 2
    OPEN_PROGRAM = 3
    

class Ask:
    def __init__(self, utt: str):
        self.utt = utt.lower()
        self.intent = self.find_intent()
        self.sub_intent = self.find_subintent()

    def find_intent(self) -> Intent:
        words = self.utt.split()
        if words.__len__() == 0 or words[0].__len__() == 0:
            return Intent.NOTHING
        if words[0] == 'open':
            return Intent.OPEN_PROGRAM
        if words[0] == 'exit' or words[0] == 'cancel':
            return Intent.EXIT
        
        return Intent.UNKNOWN
    
    def find_subintent(self) -> str:
        words = self.utt.split()
        if self.intent == Intent.OPEN_PROGRAM:
            if words.__len__() > 1:
                words = words[1:]
                return " ".join(words).strip()
        return ""

    def debug_print(self):
        print(f"utterance: '{self.utt}'\nintent: {self.intent}\nsub-intent: {self.sub_intent}\n\n")


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
parser.add_argument(
    "-p", "--partials", type=bool, help="log partial recordings"
)
args = parser.parse_args(remaining)

def execute_action(ask):
    if ask.intent == Intent.OPEN_PROGRAM:
        app = find_app(ask.sub_intent)

        if app.__len__() > 0:
            subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a", app])
        else:
            app = find_app(ask.sub_intent.replace(" ", ""))
            if app.__len__() > 0:
                subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a", app])

def find_app(name: str) -> str:
    find = ["find", "/Applications", "-iname", "*" + name + "*.app", "-print"]
    
    result = subprocess.run(find, capture_output=True, text=True, check=True)
    return result.stdout.split('\n')[0]

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
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)
        
        stay_active = True

        rec = KaldiRecognizer(model, args.samplerate)
        while stay_active:
            data = q.get()
            if rec.AcceptWaveform(data):
                utt = json.loads(rec.Result())['text']
                if utt.__len__() > 0:
                    ask = Ask(utt)
                    ask.debug_print()

                    if ask.intent == Intent.EXIT:
                        stay_active = False
                    execute_action(ask)
            else:
                if partials: print(rec.PartialResult())
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
