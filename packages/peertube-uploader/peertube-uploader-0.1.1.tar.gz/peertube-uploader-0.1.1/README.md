# PeerTube Uploader

A script to make uploading to peertube instances easier.

For documentation on the API used see 
https://docs.joinpeertube.org/api-rest-reference.html

## Installation
 
    pip install peertube-uploader
    
## Development

    pip install -r requirements.txt

## Usage

One installed you can run the `ptu` command.

````
$ ptu 
usage: main.py [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]
               [-u USERNAME] [-p PASSWORD] [-e ENDPOINT] [-c CLIENT_ID]
               [-s CLIENT_SECRET] [-t ACCESS_TOKEN]

A script to make uploading to peertube instances easier. For documentation on
the API used see https://docs.joinpeertube.org/api-rest-reference.html

optional arguments:
  --version             show program's version number and exit
  -v, --verbose         Increase verbosity of output. Can be repeated.
  -q, --quiet           Suppress output except warnings and errors.
  --log-file LOG_FILE   Specify a file to log output. Disabled by default.
  -h, --help            Show help message and exit.
  --debug               Show tracebacks on errors.
  -u USERNAME, --username USERNAME
                        Username
  -p PASSWORD, --password PASSWORD
                        Password
  -e ENDPOINT, --endpoint ENDPOINT
                        Host name
  -c CLIENT_ID, --client_id CLIENT_ID
                        Client ID to use
  -s CLIENT_SECRET, --client_secret CLIENT_SECRET
                        Client secret to use
  -t ACCESS_TOKEN, --access_token ACCESS_TOKEN
                        Access token to use

Commands:
  complete       print bash completion command (cliff)
  help           print detailed help for another command (cliff)
  import         Trigger an import of a URI (peertube-uploader)
  upload-video   Upload videos from the file-system (peertube-uploader)
````

## Thanks

Thanks to all the [contributors](https://gitlab.com/NamingThingsIsHard/media_tools/peertube-uploader/-/graphs/master).
