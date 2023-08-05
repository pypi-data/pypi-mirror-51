# musicgen
musicgen is a module for pre-processing audio and to prepare the dataset for neural networks in genarating music. Built on top of Music21 and youtube_dl
### Features
  - Download the songs,videos from URL
  - Get the notes from music
  - Prepare the dataset for neural networks

### Installation



```sh
$ pip install musicgen
```
#### get_notes(path='*.mid')
Get all the notes and chords from the midi files  
##### Args:  
path : path for the song with midi extension. ‘*.mid’ by default which gets the note of all the songs in the current working directory.  
##### Returns:  
List of notes obtained from the midi file   
#### download_song_with_url(url,audio_type='mp3',quality='192')
Downloads the audio of a video present in the given video URL to current working directory.  
##### Args:   
url : (string)  URL of a video  
audio_type :(string)"aac", "flac", "mp3", "m4a", "opus", "vorbis", or "wav". ‘mp3’ by default  
#### create_midi(prediction_output,name='output')
convert the output from the prediction to notes and create a midi file from the notes in current working directory.  
##### Args:   
prediction_output : the output predictions of a trained model.  
name : (string) name of the generated file. output by default.  
#### prepare_sequences(notes, n_vocab,sequence_length = 100)
Prepare the sequences used by the Neural Network  
##### Args:  
notes : (list) notes of midi file   
n_vocab : (int) number of unique notes  
sequence_length : (int) number of time steps required. 100 by default.  
##### Returns:  
network_input, network_output   

#### download_video_with_url(url)
Downloads the video from the given URL into current working directory.  
##### Args:  
url : (string)  URL of a video  

#### download_videos(path)
Downloads the videos from the URL’s present in a text file into current working directory.  
##### Args:  
path : (string)  path of a text file containing URL’s  

#### download_songs(path)
Downloads the audio of videos from the URL’s present in a text file into current working directory.  
##### Args:  
path : (string)  path of a text file containing URL’s.  

#### song_notes_to_pickle(path,output)
saves the notes of a midi file as a pickle object.  
##### Args:  
path : (string) path  of the songs    
output : (string) name of the pickle file.  

#### generate_notes(model, network_input, pitchnames, n_vocab)
generates the notes from the trained keras model  
##### Args:  
model : Trained keras model for prediction  
network_input : input to the network  
pitchnames : set of items in the notes. It is found using pitchnames = sorted(set(item for item in notes))  
n_vocab : (int) number of unique notes  
##### Returns:  
predicted_output  





