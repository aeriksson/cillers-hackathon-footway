# Footway Hackathon Cillers demo
This project serves as a starting point for the Cillers Footway Hackathon.

It's a simple demo app with building blocks in place for you to start building your own personal shopper app using the OpenAI or Anthropic and Footway APIs.

## Prerequisites
To get started, make sure you install Polytope:

### Docker or OrbStack
You'll need Docker or OrbStack to run the app. You can install Docker from [here](https://docs.docker.com/get-docker/) and OrbStack from [here](https://docs.orbstack.dev/install).

### Polytope CLI
On macOS:
```bash
brew install polytopelabs/tap/polytope-cli
```

Also make sure you're running at least Polytope 0.1.31:
```bash
pt --version
- The current CLI version is: 0.1.31-bae4935de-macos-arm64
```

If you're on an older version, you can update it with:
```bash
brew upgrade polytope-cli
```

For installation on Windows and Linux, see [the docs](https://polytope.com/docs/quick-start).

## Components
This app has two main components:
- [The API](./api) - A simple REST API written in Python that serves as a backend for the app.
- [The UI](./frontend) - A simple React UI written in TypeScript that serves as a frontend for the app.

## Running the app
To run the app, clone this repository and navigate to the project directory:

```bash
git clone https://github.com/aeriksson/cillers-hackathon-footway.git
cd cillers-hackathon-footway
```

Next, set the API keys you've been provided with as secrets:
```bash
pt secret set openai-api-key sk-proj-...
pt secret set anthropic-api-key sk-ant-...
pt secret set footway-api-key ...
```

Finally, run the following command to start the app:
```bash
pt run stack
```

Then open the UI at [http://localhost:3000](http://localhost:3000). This can take a little while to return something useful - especially on the first run, because it needs to set up all the dependencies.

API documentation is automatically generated and can be found at [http://localhost:3000/docs](http://localhost:3000/docs).

Some things you can try:
- `curl http://localhost:3000/api` - Responds with a hello world message. This means the API is working!
- `curl 'http://localhost:3000/api/test/footway?variant_ids=1216453'` - Run a query against the Footway API.
- `curl 'http://localhost:3000/api/test/vector?query=Soccer'` - Runs a query against the provided vector embeddings.
- `curl -X POST -H "Content-Type: application/json" -d '{"prompt":"wassup"}' http://localhost:3000/api/test/anthropic` - Run a query against the Anthropic API.
- `curl -X POST -H "Content-Type: application/json" -d '{"prompt":"wassup"}' http://localhost:3000/api/test/openai` - Run a query against the OpenAI API.

You'll have hot reload, so any changes you make to the code will be reflected in the UI immediately - however, if you add or remove packages you'll need to restart the app.
