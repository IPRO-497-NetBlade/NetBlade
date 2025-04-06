# NetBlade

An electron application that blocks IP addresses using the firewall and writes domains to the hosts file.

## How does it work ( simple representation )

```text
electron
--------> |------------|    python
          |            |-------------> |-------------------|
          |  electron  |  sub process  | python program    |
          |  --------  |               | --------------    |
          |   > html   |      std      |  takes requests   |
          |   > css    | <-----------> |  from js and      |
          |   > js     | communication |  responds it,     |
          |            |               |  in the terminal  |
          |------------|               |-------------------|
```

Essentially no network is being created only one terminal is used when electron is launched and than from
within javascript ( electron ) a python program is initiated as a subprocess.
These two programs than communicate via standard streams.

### Structure of example

```text
│
├── docs
│   ├── README.md
│   └── LICENSE
|
├── images
│   └── ...
|
├── index.html
├── style.css
├── app.js
├── main.js
│
├── blocker.py
|
├── config.json
└── package.json
```

## Prerequisites

Install Node.js and Python.

You will also need to install the win10toast python package.

```
pip install win10toast
```

> Note that installation may be different for different operating systems

## Execution Guide

1. Open a terminal window and cd to cloned project

   ```
   cd NetBlade
   ```

2. Initialize the electron application (first-time)

   ```
   npm i
   ```

3. Run the electron application

   ```
   npm start
   ```

### Interpretation Guide

Important functionality can be found in files `electron/app.js` where the core of electron is. Listeners are implemented there awaiting for click events to trigger initialization of program, communication and termination. The program `python/blocker.py` which is the external or 3rd party application that electron calls, is a simple for-loop awaiting commands. It responds to commands and terminates when sent an empty string, "terminate" or by pressing the terminate program button.


### Installing the App

On the repository page, go to releases and download the zip file. Uzip it and go to `make/squirrel.windows/x64` and open `NetBlade-0.1.0.Setup.exe`. It should take a couple of seconds and the app will open by itself. Close it and find the installation directory. Once there, go to `app-0.1.0` and place the `python` folder that was in the zip file.