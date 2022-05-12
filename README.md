# ad-470-group2

## Project 3

### Run with Docker

#### Pre-reqs
You must have Docker installed before you proceed

#### Steps
From the root of the repo:

```bash
cd src/project-3
```

```bash
docker build --tag ad470-g2-p3-test .
```

```bash
docker run -d -p 5001:5000 ad470-g2-p3-test
```

Visit [localhost:5001/form](localhost:5001/form)
