# COLA: COpilot for Landscape Architecture

## TLDR

COLA, short for COpilot for Landscape Architecture, is a human-in-the-loop agentic system for Landscape Architecture design.

## Demo

[![Demo](https://img.youtube.com/vi/0gFEBiUQDRk/0.jpg)](https://youtu.be/0gFEBiUQDRk)

<img src="images\spark.png" style="zoom:25%;" />

<img src="D:images\graph.png" style="zoom:25%;" />

<img src="images\screenshot-1.png" style="zoom:25%;" />

<img src="images\screenshot-2.png" alt="screenshot-2" style="zoom:25%;" />

<img src="images\screenshot-3.png" alt="screenshot-3" style="zoom:25%;" />

## Usage

**These instructions assume you are in the `COLA/` directory**

### Running the Agent

First, install the backend dependencies:

```sh
cd agent
poetry install
```

Then, create a `.env` file inside `./agent` with the following:

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...
```

Then, run:

```sh
poetry run dev
```

### Running the UI

First, install the frontend dependencies:

```sh
cd ui
pnpm i
```

Then, create a `.env` file inside `./ui` with the following:

```
OPENAI_API_KEY=...
```

Then, run the Next.js project:

```sh
pnpm run dev
```

### Usage

Navigate to [http://localhost:3000](http://localhost:3000).

### Running the LangGraph Studio

Run the LangGraph studio:
```sh
cd agent
langgraph dev
```
