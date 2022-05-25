# ad-470-group2

## Project 3

### Update styles with tailwindcss

If you make any changes to tailwindcss, run the following before running with Docker

```bash
tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify
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

```bash
gcloud config set project ad470-p3
```

```bash
gcloud builds submit --tag gcr.io/ad470-p3/server
```

```bash
gcloud run deploy --image gcr.io/ad470-p3/server
```
