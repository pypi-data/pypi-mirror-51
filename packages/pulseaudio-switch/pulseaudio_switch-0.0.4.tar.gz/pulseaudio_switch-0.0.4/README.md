# pulseaudio_switch

## Description
Change the default audio device and move all active streams to the new audio device in
pulseaudio.
Check in `pacmd list` the index number of the audio source device or find out the corresponding
index number of your soundcard by trying out index numbers, i€ℕ, starting from 0.

## Example
`pulseaudio_switch --output_sink 1`
