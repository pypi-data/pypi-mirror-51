# blogger

`blogger` is a command line utility originally created for converting articles, text, or HTML into speech. This is especially helpful for bloggers who like to provide audio options for their users.

This is a wrapper around a couple of different text to speech tools and is designed to be a simple interface for any user of the `blogger` CLI.

`blogger` is an open-source project from Buster Technologies, the creators of [Buster ERP](https://bustererp.com). Our company published technical and business content on the [Simpler Software Blog](https://bustererp.com/blog) and needed a simple tool to convert articles to audio files.

## Installing

The package is available via pypi and can be install with `pip` or `pipenv`:

```shell
$ pip install -U blogger
```

---

## The simplest examples

The `blogger` CLI has default options for converting text to speech with very few inputs. Here is an example taking in a string of text and outputting the audio file:

```shell
$ blogger audio "This is an awesome article" -o article.mp3
```

The default `basic` text to speech converter gets the job done but is not the best automated speech in the world. Google has built out a much more advanced cloud API for text to speech which sounds closer to real speech. For this, you can use the `gtts` converter and pass in an [API token from Google which can be generated in the api console](https://cloud.google.com/docs/authentication/api-keys).

```shell
$ blogger audio \
  --converter=gtts \
  --token="$MYAPIKEY" \
  "This is another awesome article" \
  -o article.mp3
```

---

## Options

Outside of the default configurations though, you can feed `blogger` some different inputs depending on what is needed.

```shell
$ blogger

Usage: blogger [OPTIONS] COMMAND [ARGS]...

  Blogger CLI

Options:
  --help  Show this message and exit.

Commands:
  audio       Generates an audio file from text, files, or urls.
  converters  Details for text to speech converters.
  providers   Details for content providers.
  voices      Details for voice options.
```

```shell
$ blogger audio --help

Usage: blogger audio [OPTIONS] [INLINE_TEXT]

  Generates an audio file from text, files, or urls.

  All input is assumed to be in either plain text or HTML format. Any other
  formats could have potential issues during processing.

Options:
  --text TEXT                     The text to convert to speech.
  --file TEXT                     The file path to the file containing text to
                                  convert to speech.
  --url TEXT                      Parse an article from a URL.
  -p, --provider TEXT             When parsing from a URL, the provider
                                  defines the content provider (Ex. Medium,
                                  Ghost, etc.)
  --url-title-selector TEXT       For the manual provider, this specifies the
                                  tag and class or id in the DOM that contains
                                  the title.
  --url-content-selector TEXT     For the manual provider, this specifies the
                                  tag and class or id in the DOM that contains
                                  the content.
  -t, --token TEXT                Google API token used for the gtts provider.
  -vi, --voice TEXT               The voice option.
  -vp, --pitch TEXT               The pitch of the voice on a scale of -20.0
                                  to 20.0.
  -vr, --rate TEXT                The rate of speech on a scale of 0.0 to 4.0.
  -c, --converter TEXT            The type of text to speech converter to use.
                                  Defaults to basic.
  -o, --output TEXT               The output path for the audio file. If not
                                  specified, output will go to STDOUT.
  --full-preview / --short-preview
                                  Preview the entire article before
                                  converting.
  -v, --verbose / --no-verbose    Provides more debugging information.
  -y, --yes / --no                Assumes yes to prompts.
  --help                          Show this message and exit.
```

### Converters

There are two types of text to audio converters built into `blogger`.

```shell
$ blogger converters -l

basic A simple text to speech converter. (default)
gtts The Google cloud-based text to speech converter API.
```

#### Basic

The `basic` converter, which is used by default, converts text to speech using a simple google translate utility. As it says, it's a very basic option and outputs a decent audio file.

#### GTTS (Google Text To Speech)

Google provides a [cloud text to speech API](https://cloud.google.com/text-to-speech/) that works much better than their previous text to speech software. You must have an [API token](https://cloud.google.com/docs/authentication/api-keys) to use this converter.

```shell
$ blogger audio \
  --converter=gtts \
  --token="$MYAPIKEY" \
  --file=/tmp/input.txt \
  -o article.mp3
```

If utilizing the `gtts` converter, it comes with a few command line options too. The only required option is the API token:

```shell
-t, --token TEXT                Google API token used for the gtts provider.
-vi, --voice TEXT               The voice option.
-vp, --pitch TEXT               The pitch of the voice on a scale of -20.0
                                to 20.0.
-vr, --rate TEXT                The rate of speech on a scale of 0.0 to 4.0.
```

Read the instructions on [how to generate your API token here](https://cloud.google.com/docs/authentication/api-keys).

### Input

There are multiple ways that text can be passed into `blogger`. Only 1 of the following methods can be used in a single command at a time. Conflicts will result in a single input method being used and the other input being ignored.

#### Inline

As seen in the simple example above, you can pass text directly into the CLI:

```shell
$ blogger audio "Convert this text please" -o article.mp3

$ blogger audio --text="Convert this text please" -o article.mp3

$ blogger audio --text="Convert this text please" --output=/my_audio/article.mp3
```

#### Files

Another option is to read a file in:

```shell
$ blogger audio --file=./article.txt -o article.mp3
```

#### URL

And finally you can read articles posted online, strip out the relevant content, and produce an audio file. This is ideal for articles already written and published that need to be converted afterwards.

When reading a URL, `blogger` needs some help figuring out what content to be looking at. For this we use providers. A provider represents a content provider (think Medium, Ghost, Wordpress, etc.) Please see the [Providers](#Providers) section for more details about what blog formats are supported automatically.

```shell
$ blogger audio \
  --url=https://bustererp.com/blog/whats-in-python-3-8 \
  --provider=ghost \
  -o article.mp3
```

```shell
$ blogger audio \
  --url=https://medium.com/@reedrehg/10-ways-to-prevent-technical-debt-33dd17075fba \
  --provider=medium \
  -o article.mp3
```

If a relevant provider does not exist, then you can pass selectors in to show us what exactly to look for. Generally `blogger` is always looking for a title and then a content body.

```shell
$ blogger audio \
    --url=https://myblog.com/myarticle \
    --url-title-selector="h1.blog-title" \
    --url-content-selector="div#blog-content" \
    -o article.mp3
```

### Article previews

Each `audio` command will show you a preview of what was processed to ensure that you are pulling the right information. Use the `--full-preview` flag to preview the entire content, not just part of the content.

```shell
$ blogger audio --url=https://myblog.com/myarticle --provider=ghost -o article.mp3

Converting audio using the gtts converter:
  Text Preview:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
    turpis ante, egestas id diam sed, convallis ultrices erat.
    Praesent ut nibh non quam pellentesque finibus. Maecenas convallis,
    metus a sollicitudin porttitor, dolor leo facilisis erat,
    sed condimentum nisl quam in nunc. Quisque sed mattis ligula,
    sed finibus nunc. Proin et nisl ut leo tempor dignissim in sed
    mauris. Duis porta lacinia sapien sit amet consequat. Quisque
    eget lectus non lorem vehicula porta eu a lacus. Etiam fermentum,
    purus at malesuada tristique, lorem elit hendrerit libero,
    a molestie felis felis a nibh. Quisqu...

Processing...
Successfully outputted to /tmp/audio.mp3
```

### Providers

Check the providers list to see the currently available blog providers supported by the system. The `--provider` flag will only be relevant when combined with the `--url` option.

```shell
$ blogger providers -l

manual Uses user provided input to determine how to parse content (default)
ghost Handles parsing content for Ghost hosted blogs (https://ghost.io)
medium Handles parsing content written on Medium (https://medium.com)
```

### Voices

Check the voices list to see the currently available voice. This is only compatible with the `gtts` converter:

```shell
$ blogger voices -l

US-A United States english accent option A
US-B United States english accent option B
US-C United States english accent option C
US-D United States english accent option D
US-E United States english accent option E
US-F United States english accent option F
AU-A Australian english accent option A
AU-B Australian english accent option B
AU-C Australian english accent option C
AU-D Australian english accent option D
GB-A British english accent option A
GB-B British english accent option B
GB-C British english accent option C
GB-D British english accent option D
IN-A Indian english accent option A
IN-B Indian english accent option Bextremely
IN-C Indian english accent option C
```

```shell
$ blogger audio \
  --converter=gtts \
  --token="$MYAPIKEY" \
  --file=/tmp/input.txt \
  --voice="US-C" \
  --yes
```

## Contibuting to `blogger`

`blogger` is open-source software and freely distributable under the terms of the [MIT license](https://github.com/bustertechnologies/blogger/blob/master/LICENSE). The source code is hosted on [GitHub](https://github.com/bustertechnologies/blogger).

Please contribute in the form of pull requests, bug reports, or general comments in the [GitHub issue tracker](https://github.com/bustertechnologies/blogger/issues).

`blogger` was originally created by [Holden Rehg](https://github.com/holdenrehg), with development sponsored by [Buster Technologies](https://bustererp.com).

---

Buster Technologies, LLC.
