set -e
cd NuRadioReco/test/tiny_reconstruction
python TinyReconstruction.py
python compareToReference.py MC_example_station_32.nur reference.json
