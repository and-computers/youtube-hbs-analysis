# youtube-hbs-analysis

## What is this?

I was curious to know how many times "case" and related concepts are mentioned within Harvard Business School's youtube videos. I was trying to prove a point that the school is almost comically insufferable about how great case-based discussions are. The script is quick and messy.

### Results

These are really imperfect because transcripts through this method aren't always accurate, a number of videos had no transcripts, and a great number of them were missing significant portions of the content of the video. And yet.. almost 1 and a half times a video over the past ~14 years :sweat-smile:

```
...
0 mentions in zAoH2JpcA9E-transcript.txt
1 mentions in zFDlIoD7UYo-transcript.txt
3 mentions in zGcCANuL6ks-transcript.txt
2 mentions in zJ9sbKBLn4U-transcript.txt
0 mentions in zKQg0idkIdU-transcript.txt
0 mentions in zLbDvQ5d0SE-transcript.txt
0 mentions in zR9qmpwiCvc-transcript.txt
30 mentions in zSirMOiEbpA-transcript.txt
0 mentions in zTUZ8KnkxT8-transcript.txt
0 mentions in zXIPg6lftW8-transcript.txt
0 mentions in zmQZPp2KY9E-transcript.txt
0 mentions in zmhwydIIh_Y-transcript.txt
0 mentions in zmsaO9dG2NM-transcript.txt
0 mentions in zoNL6ptkKag-transcript.txt
1 mentions in zoNT5V4Icw0-transcript.txt
1 mentions in zrhOmRhfvOs-transcript.txt
15 mentions in zsh7opE4QZE-transcript.txt
0 mentions in zuz1d6o_WTA-transcript.txt
0 mentions in zvoz-YHQQWg-transcript.txt
0 mentions in zw3d9dPFV28-transcript.txt
Total number of video transcripts reviewed: 1401
Total case mentions: 1910
Avg mentions per file: 1.363311920057102
Percent of videos with mention: 30.8%
```

### Setting up Local Environment

##### For Mac OS

- Install pyenv from [homebrew](https://formulae.brew.sh/formula/pyenv#default)

##### Install Appropriate Python Version (if not already installed)

- `pyenv install 3.11`

#### Create the environment

- `pyenv virtualenv 3.11 youtube-hbs-analysis`

#### Activate the environment

- To activate (on Mac) `source ~/.pyenv/versions/youtube-hbs-analysis/bin/activate`

### Configure to Run

- Place some keys in a file called `.keys` in the `src` folder. It should have the following format:

```
[configuration]
SCRAPING_BEE_API_KEY=my-key
CHANNEL_URL=channel-url
```
