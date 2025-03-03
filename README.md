# youtube-hbs-analysis

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
