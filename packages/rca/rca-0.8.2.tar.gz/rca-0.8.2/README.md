# Recompress Audio (RCA)

**The Problem**: If you recompress lossless audio for use on
space-sensitive devices such as a cell phone or Raspberry Pi, then RCA
can help you re-compress those lossless tracks whenever improved
versions of your codec are released or when you change your desired
encoding settings.

It does this by keeping track of the encoder's version and flags used in
a simple text file that resides along-side the audio.

You can also characterize your tracks as speech or music, stereo or
mono, simple or complex (amung others), which RCA uses to tailor the
encoding flags and bitrates.

RCA is simple to use, command-line driven, and doesn't require any
changes to your directory layout or audio filenames.

## How it Works

You characterize a given directory audio tracks by populating a new
`properties.yml` file with something like the following:

```yaml
tracks:
  type: music
  complexity: moderate
  channels: stereo
```

The above tells RCA that all tracks are stereo music of moderate
complexity.

Here's a more complex example of a CDs having music, commentary, sound
effects, and two trailing filler track of dead-air:

```yaml
tracks:
  type: music
  complexity: simple
  channels: stereo

track03:
  type: effects
  complexity: moderate

speech:
  range: [4, -, 9, 12]
  complexity: complex
  channels: mono

filler:
  range: [13, 14]
```

The above tells RCA that:
- tracks 1, 2, 10, and 11 are *stereo music* of *simple* complexity
- track 3 is *stereo* sound *effects* of *moderate* complexity
- tracks 4, 5, 6, 7, 8, 9, and 12 are *mono speech* of *complex* complexity
- tracks 13 and 14 are filler

You then run RCA while specifying your desired output codec, such as
`rca opus`, which encodes the tracks according to the Ogg Opus profiles,
which can be customized.

## Getting Started

1. Install Python 3.5 or preferably the latest, which is currently 3.7.x
  - Windows users: enable the *Add Python to your PATH* option during install

2. Install RCA: open an command prompt as the Administrator (Windows) or
root on Linux/OSX) and run `pip3 install rca`










