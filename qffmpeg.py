import argparse
import os
from subprocess import run


def executeFFmpeg(arglist):
    try:
        run(arglist, check=False)
    except FileNotFoundError:
        print("\033[91mERROR:\033[0m FFmpeg is not installed or added to PATH")


def avc(file):
    ffmpeg = [
        "ffmpeg",
        "-i",
        file,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-strict",
        "-2",
        os.path.splitext(file)[0] + "_AVC.mp4",
    ]
    executeFFmpeg(ffmpeg)


def mp3(file):
    ffmpeg = [
        "ffmpeg",
        "-i",
        file,
        "-vn",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-b:a",
        "192k",
        os.path.splitext(file)[0] + "_AUDIO.mp3",
    ]
    executeFFmpeg(ffmpeg)


def trim(file, start, end):
    ffmpeg = [
        "ffmpeg",
        "-ss",
        start,
        "-to",
        end,
        "-i",
        file,
        "-c",
        "copy",
        os.path.splitext(file)[0] + "_TRIM.mp4",
    ]
    executeFFmpeg(ffmpeg)


def speedup(file, mult):
    ffmpeg = [
        "ffmpeg",
        "-i",
        file,
        "-filter:v",
        "setpts=PTS/" + mult,
        "-an",
        os.path.splitext(file)[0] + "_X" + mult + ".mp4",
    ]
    executeFFmpeg(ffmpeg)


parser = argparse.ArgumentParser(
    prog="qffmpeg", description="Quick FFmpeg - Frequently used FFmpeg functions"
)

parser.add_argument("file", metavar="FILE", type=str, help="video/audio file")

subparsers = parser.add_subparsers(
    title="commands", dest="command", required=True, help="Available functions to run"
)

parser_greet = subparsers.add_parser(
    "convert-to-avc", help="Convert video to h264 (AVC)"
)
parser_greet.set_defaults(func=lambda args: avc(args.file))

parser_greet = subparsers.add_parser("convert-to-mp3", help="Convert video to mp3")
parser_greet.set_defaults(func=lambda args: mp3(args.file))

parser_greet = subparsers.add_parser("trim", help="Trim video between two timestamps")
parser_greet.add_argument("start", type=str, help="Start of the clip")
parser_greet.add_argument("end", type=str, help="End of the clip")
parser_greet.set_defaults(func=lambda args: trim(args.file, args.start, args.end))

parser_greet = subparsers.add_parser(
    "speedup", help="Speed up video by some multiplier (no audio)"
)
parser_greet.add_argument("mult", type=str, help="Multiplier")
parser_greet.set_defaults(func=lambda args: speedup(args.file, args.mult))

args = parser.parse_args()
args.func(args)
