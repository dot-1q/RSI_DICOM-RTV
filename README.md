## DICOM Real time Video implementation using flask 

## How to install

1. Install the requirements:
```bash
pip3 install -r requirements.txt
```

## How to run

Run the server than continuously serves de image frames 

```bash
python3 server.py
```
Run the Web page

```bash
python3 dicom-rtv.py
```

Since the ID of the input device is hardcoded, sometimes it has to be changed by hand.
That is done on line 44.
```python
rate=RATE, input=True,input_device_index=<index>
```
