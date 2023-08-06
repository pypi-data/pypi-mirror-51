
# MERIDIAN Acoustic Boat Detector

Using the [Ketos](https://docs.meridian.cs.dal.ca/ketos/) package we have created a little command-line tool for processing hydrophone data and searching for the acoustic signature of motorized vessels. In other words, a boat detector! 


# License

The MERIDIAN Acoustic Boat Detector is licensed under the [GNU GPLv3 licens](https://www.gnu.org/licenses/) and hence freely available for anyone to use and modify.


# Installation

```terminal
pip install -r requirements.txt
python setup sdist
pip install dist/boat_detector-1.0.0.tar.gz
```


# Windows users

See the [Step-by-step guide for Windows users](https://gitlab.meridian.cs.dal.ca/data_analytics_dal/projects/boat_detector/wikis/Step-by-step-guide-for-Windows-users).


# Usage example

To illustrate the usage of the boat detector, we have included an example data set in the 
`assets/` directory, which 
consists of 60 short audio recordings, each lasting no more than approximately 10 seconds. 
The recordings were made over the course of 1 hour using a broadband hydrophone with a sampling 
rate of 20 kHz. The hydrophone was deployed in a shallow bay that is busy with recreational 
boating. The data were kindly shared with us by Mitchell Rider from the Rosenstiel School 
of Marine & Atmospheric Science in the U.S. To save space the audio files have been 
downsampled to 4 kHz. The start time of each audio file is encoded into the file name using 
the format `HMS_%H_%M_%S__DMY_%d_%m_%y` where `%H` is the hour, `%M` is the minute, `%S` 
is the second, `%d` is the day, `%m` is the month, and `%y` is the year.

The boat detection program consists of two steps, data pre-processing and signal detection:

## Step I: Pre-processing

Pre-process the audio files in the `assets/` directory with the command
```terminal 
$ boat-preproc -c settings.json -i assets/ -v
```
This should produce the following output,
```terminal 
 Found 60 files
 Processing batch #1 ...
 Processing batch #2 ...
 Processing batch #3 ...
 Successfully processed 60 files
 Processed data saved to: output.csv
 Time table saved to: output_time_table.csv
 Elapsed time: 00:00:07
```

## Step II: Detection

Search for acoustic signatures of boats in the preprocessed data
```terminal
$ boat-detect -c settings.json -i output.csv -S
```
This should produce the following output,
```terminal 
 7 boats detected
 Detection report saved to: detections.csv
```
and this figure:

![](assets/figures/boat_detections.png)


# Options

## Pre-processing script
```terminal
$ boat-preprocess -h
usage: boat-preprocess [-h] [-c CONFIG_FILE] [-i INPUT] [-o OUTPUT_FILE] [-r]
                       [-v]

Split audio signal into frequency bands and produce a time series of the noise
magnitude in each band.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        path to json configuration file.
  -i INPUT, --input INPUT
                        path to the wav file to be analyzed or directory
                        containing multiple wav files.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        path to output csv file
  -r, --recursive_search
                        Include subdirectories in search for wav files
  -v, --verbose         Print progress updates during processing
```

## Detection script
```terminal
$ boat-detect -h
usage: boat-detect [-h] [-c CONFIG_FILE] [-i INPUT_FILE] [-o OUTPUT_FILE] [-S]

Perform outlier- and peak analysis of time-series data.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        path to json configuration file.
  -i INPUT_FILE, --input_file INPUT_FILE
                        .csv file containing time-series data to be analyzed.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        .csv file where analysis report will be outputted.
  -S, --show_graph      Show time-series data
```

# Configuration files

## General settings (settings.json)

The main configuration file informs the program about 1) the date-time filename 
labeling convetion, 2) the maximum amount of audio data to be processed in a single 
batch, and 3) the path to the detector configuration file.
```terminal
$ more settings.json 
{
    "date_time_format": "HMS_%H_%M_%S__DMY_%d_%m_%y",
    "batch_size": "5E6",
    "detector": "detectors/fav.json"
}
```

## Detectors

The `detectors/` folder contains two detector configuration files, [fav.json](detectors/fav.json) and [obi.json](detectors/obi.json), 
which implement two different detection strategies.

### fav.json

To detect the presence of a boat, the FAV (Frequency Amplitude Variation) detector takes advantage of the fact 
that the frequency spectrum of a boat often contains several narrow peaks, which occur at frequencies ranging 
from tens of Hz to several hundred Hz. More specifically, the FAV detector computes the Short-Time Fourier 
Transform (STFT) of the audio data, searches for narrow peaks, and reports a boat detection if a few such 
peaks are found. The peak search algorithm is similar, though not identical, to the one described in 
[this paper](https://doi.org/10.1111/2041-210X.13245). 

The performance of the FAV detector can be optimized by adjusting the parameters found in the [fav.json](detectors/fav.json) 
configuration file. While this file contains many parameters, the most relevant are the `threshold` parameter (found in 
the `fav_config` section) and the `height` parameter (found in the `detect_config` section). The former determines how sharp and tall 
a frequency peak must be to be counted as a peak, while the latter determines how many such peaks must be present at given 
instant to produce a boat detection.

### obi.json

The OBI (Octave Band Intensity) detector finds boats by looking for variations in the 
sound intensity within the 2nd, 3rd, and 4th octave band, centered at 125 Hz, 250 Hz, and 500Hz.
The performance of the OBI detector can be optimized by adjusting the parameters found in the [obi.json](detectors/obi.json) 
configuration file. The most relevant parameters are the `prominence` and `multiplicity` 
parameters (found in the `detect_config` section). The former determines how prominent the increase in sound intensity must be to be counted as signal, while the latter determines in how many octave bands such a signal must be detected to produce a boat detection.

Below, you see the spectrogram of a 10-second long audio recordering containing noise from a boat. 
Narrow peaks in the frequency spectrum are seen as sharp horizontal lines in the spectrogram, visible 
at about 20 Hz, 50 Hz, 95 Hz, and 145 Hz, along with an overall increase of sound intensity, especially 
in the third octave band centered at 250 Hz.

![](assets/figures/boat.png)


# Jupyter Notebook tutorial

If you would like to write your own boat detection program in Python, have a look at this [Jupyter Notebook tutorial](https://docs.meridian.cs.dal.ca/ketos/tutorials/boat_detector_tutorial/index.html). 
