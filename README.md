# Prometheus metrics to Honeycomb

> Tool to pull metrics from a url or file, and dump to a honeycomb dataset

# Getting started

## With docker

Just run the built docker image like so:

```bash
docker run --rm hcaptcha/prometheus2honeycomb python3 prometheus2honeycomb.py --url http://my-metrics-server:8000/metrics --ship
```

## Without docker
First you'll need the prom2json go tool installed via the following:

```bash
# via GO
go get github.com/prometheus/prom2json/cmd/prom2json

# via HTTP / github releases (only for linux 386 at the moment)
# or install from https://github.com/prometheus/prom2json/releases
./bin/get_prom2json
```

Then configure the dataset name and honeycomb write key that you want to use to send your data to:

```bash
export DATASET_NAME=myDataset
export HONEYCOMB_WRITEKEY=myHoneycombWriteKey
```

Finally point the tool at a URL and it'll submit all the metrics it finds there.  You can also just print the results to screen without the `--ship` option:

```bash
pipenv run python3 prometheus2honeycomb.py --url http://my-metrics-server:8000/metrics --ship
```

You can also additional fields to the output of each event that gets sent to honeycomb by adding a `--extra-args key1=value1 key2=value2`

# Contributing

## Building

Currently this repo is manually built/deployed via the following steps:

```bash
docker build -t hcaptcha/prometheus2honeycomb:latest .
docker push hcaptcha/prometheus2honeycomb:latest
```

## Lint

To run the linter, run `./bin/lint`

## Stop

To stop the containers, run `./bin/stop`

## Testing

To test the whole workflow, run:
```
./bin/ci
```
