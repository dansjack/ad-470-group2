# ad-470-group2

## Project 3

### Update styles with tailwindcss

If you make any changes to tailwindcss, run the following before running with Docker

```bash
tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify
```

### Run locally

#### Pre-reqs
Change `main.py` to look like below:  
<img width="600" alt="image" src="https://user-images.githubusercontent.com/30481844/170155980-273a8df2-a09f-4831-ab92-3cb6aa50048a.png">

There's a [known issue](https://github.com/actions/runner/issues/805) with installing tokenizers for Huggingface on M1 macs. I tried different workarounds for a few hours, but couldn't get it running.

_Note: this may not be necessary on non-M1 macs._

#### Steps

Create virtual env
```bash
cd project-3/server
python3 -m venv venv
```

Active virtual env
```bash
source tutorial-env/bin/venv
```

Install packages
```bash
pip3 install -r requirements.txt
```

Start the app
```bash
FLASK_APP=main.py FLASK_ENV=development flask run
```

### Run with Docker

#### Pre-reqs

You must have Docker installed before you proceed

#### Steps

From the root of the repo:

```bash
cd project-3/server
```

```bash
docker build --tag ad470-g2-p3-test .
```

```bash
docker run -d -p 8080:8080 ad470-g2-p3-test
```

Visit [localhost:8080](localhost:8080)

### Run with Cloud Run

#### Pre-reqs

* The [gcloud cli](https://cloud.google.com/sdk/docs/install).
* You must have access to our google cloud project, ad470-p3. Submit an issue or email dan.jack@hey.com if you need access.

#### Steps

```bash
gcloud config set project ad470-p3
```

```bash
gcloud builds submit --tag gcr.io/ad470-p3/server
```

```bash
gcloud run deploy --image gcr.io/ad470-p3/server
```

Once deployed, you can view logs for the server on [Google Cloud Platform](https://console.cloud.google.com/run/detail/us-central1/server/logs?project=ad470-p3)
